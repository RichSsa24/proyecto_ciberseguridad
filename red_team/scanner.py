import subprocess
import json
import argparse
from datetime import datetime
from pathlib import Path

class NetworkScanner:
    def __init__(self, output_dir="scan_results"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
    def run_scan(self, target, scan_type="stealth", ports=None):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_filename = f"{target.replace('/', '_').replace(':', '_')}_{timestamp}"
        
        scan_profiles = {
            "stealth": ["-sS", "-T4"],
            "version": ["-sV", "-T4"],
            "aggressive": ["-sS", "-sV", "-O", "-A", "-T4"],
            "quick": ["-sS", "-F", "-T5"],
            "comprehensive": ["-sS", "-sV", "-sC", "-O", "-T4"]
        }
        
        flags = scan_profiles.get(scan_type, ["-sS"])
        flags.append("-Pn")
        
        if ports:
            flags.extend(["-p", ports])
        
        cmd = ["nmap"] + flags + [target]
        
        xml_output = self.output_dir / f"{base_filename}.xml"
        txt_output = self.output_dir / f"{base_filename}.txt"
        
        cmd.extend(["-oX", str(xml_output), "-oN", str(txt_output)])
        
        print(f"[*] Ejecutando: {' '.join(cmd)}")
        print(f"[*] Target: {target}")
        print(f"[*] Tipo de scan: {scan_type}")
        print(f"[*] Guardando resultados en: {self.output_dir}")
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            
            scan_info = {
                "timestamp": timestamp,
                "target": target,
                "scan_type": scan_type,
                "command": " ".join(cmd),
                "exit_code": result.returncode,
                "xml_file": str(xml_output),
                "txt_file": str(txt_output)
            }
            
            json_output = self.output_dir / f"{base_filename}.json"
            with open(json_output, 'w') as f:
                json.dump(scan_info, f, indent=2)
            
            if result.returncode == 0:
                print(f"[+] Scan completado exitosamente")
                print(f"[+] Resultados guardados:")
                print(f"    - XML: {xml_output}")
                print(f"    - TXT: {txt_output}")
                print(f"    - JSON: {json_output}")
            else:
                print(f"[-] Error en el scan. Exit code: {result.returncode}")
                print(f"[-] Error: {result.stderr}")
                
            return scan_info
            
        except subprocess.TimeoutExpired:
            print("[-] Timeout: El scan tardo demasiado")
            return None
        except FileNotFoundError:
            print("[-] Error: Nmap no esta instalado o no esta en el PATH")
            return None
        except Exception as e:
            print(f"[-] Error inesperado: {str(e)}")
            return None
    
    def batch_scan(self, targets, scan_type="stealth", ports=None):
        results = []
        for target in targets:
            print(f"\n{'='*60}")
            result = self.run_scan(target, scan_type, ports)
            if result:
                results.append(result)
        
        batch_summary = self.output_dir / f"batch_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(batch_summary, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n[+] Resumen de batch guardado en: {batch_summary}")
        return results

def main():
    parser = argparse.ArgumentParser(
        description="Network Scanner - Wrapper interactivo de Nmap",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python scanner.py -t 192.168.1.1
  python scanner.py -t 192.168.1.1 -s version -p 22,80,443
  python scanner.py -t 192.168.1.1 -s aggressive -o mis_scans
  python scanner.py -T targets.txt -s quick
  python scanner.py -t scanme.nmap.org -s comprehensive
        """
    )
    
    target_group = parser.add_mutually_exclusive_group(required=True)
    target_group.add_argument(
        "-t", "--target",
        help="IP o hostname objetivo (ej: 192.168.1.1, scanme.nmap.org)"
    )
    target_group.add_argument(
        "-T", "--target-file",
        help="Archivo con lista de targets (uno por linea)"
    )
    
    parser.add_argument(
        "-s", "--scan-type",
        choices=["stealth", "version", "aggressive", "quick", "comprehensive"],
        default="stealth",
        help="Tipo de scan (default: stealth)"
    )
    
    parser.add_argument(
        "-p", "--ports",
        help="Puertos a escanear (ej: 22,80,443 o 1-1000)"
    )
    
    parser.add_argument(
        "-o", "--output-dir",
        default="scan_results",
        help="Directorio de salida (default: scan_results)"
    )
    
    args = parser.parse_args()
    
    scanner = NetworkScanner(output_dir=args.output_dir)
    
    if args.target:
        scanner.run_scan(args.target, args.scan_type, args.ports)
    elif args.target_file:
        try:
            with open(args.target_file, 'r') as f:
                targets = [line.strip() for line in f if line.strip()]
            scanner.batch_scan(targets, args.scan_type, args.ports)
        except FileNotFoundError:
            print(f"[-] Error: No se encontro el archivo {args.target_file}")
        except Exception as e:
            print(f"[-] Error leyendo archivo: {str(e)}")

if __name__ == "__main__":
    main()