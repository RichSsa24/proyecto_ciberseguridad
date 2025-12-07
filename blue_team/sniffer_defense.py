#!/usr/bin/env python3
    

from scapy.all import sniff, IP, TCP
from datetime import datetime
import argparse
import sys

# Configuración
LOG_FILE = "log_events.txt"
BLOCKED_IPS_FILE = "blocked_ips.txt"
COMMON_PORTS = {22, 80, 443, 53, 25, 110, 143}
THRESHOLD_ATTACKS = 5  # Número de intentos antes de sugerir bloqueo

# Contador de intentos por IP
attack_counter = {}


def log_event(message):
    """Registra un evento en el archivo de log con timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}\n"
    
    with open(LOG_FILE, "a") as log:
        log.write(log_entry)
    
    print(log_entry.strip())


def add_to_blocklist(ip_address):
    """Agrega una IP a la lista de bloqueo y sugiere comando."""
    with open(BLOCKED_IPS_FILE, "a") as blocklist:
        blocklist.write(f"{ip_address}\n")
    
    block_command = f"sudo iptables -A INPUT -s {ip_address} -j DROP"
    log_event(f"IP {ip_address} agregada a blocklist. Comando sugerido: {block_command}")


def packet_callback(packet):
    """Analiza cada paquete capturado en busca de actividad sospechosa."""
    if not packet.haslayer(IP) or not packet.haslayer(TCP):
        return
    
    ip_src = packet[IP].src
    ip_dst = packet[IP].dst
    tcp_dport = packet[TCP].dport
    tcp_flags = packet[TCP].flags
    
    # Detección de SYN scan (SYN sin ACK)
    if tcp_flags == 0x02:  # Flag SYN
        log_event(f"ALERTA: SYN scan detectado desde {ip_src} al puerto {tcp_dport}")
        
        # Incrementar contador de ataques
        attack_counter[ip_src] = attack_counter.get(ip_src, 0) + 1
        
        # Si supera el umbral, agregar a blocklist
        if attack_counter[ip_src] >= THRESHOLD_ATTACKS:
            log_event(f"CRITICO: IP {ip_src} ha realizado {attack_counter[ip_src]} intentos")
            add_to_blocklist(ip_src)
            attack_counter[ip_src] = 0  # Reset counter
    
    # Detección de puertos inusuales
    if tcp_dport not in COMMON_PORTS:
        log_event(f"ALERTA: Conexión a puerto inusual {tcp_dport} desde {ip_src}")


def start_sniffer(interface=None, packet_count=0):
    """Inicia el sniffer de red."""
    log_event(f"Iniciando sniffer de defensa en interfaz: {interface or 'todas'}")
    
    try:
        sniff(
            iface=interface,
            filter="tcp",
            prn=packet_callback,
            store=False,
            count=packet_count
        )
    except PermissionError:
        print("ERROR: Se requieren permisos de root. Ejecutar con sudo.")
        sys.exit(1)
    except KeyboardInterrupt:
        log_event("Sniffer detenido por el usuario")
        sys.exit(0)


def main():
    """Función principal con argumentos de línea de comandos."""
    parser = argparse.ArgumentParser(
        description="Sniffer de defensa para detectar actividad sospechosa"
    )
    parser.add_argument(
        "-i", "--interface",
        help="Interfaz de red a monitorear (ej: eth0, wlan0)",
        default=None
    )
    parser.add_argument(
        "-c", "--count",
        help="Número de paquetes a capturar (0 = infinito)",
        type=int,
        default=0
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("Blue Team - Sniffer de Defensa")
    print("=" * 60)
    print(f"Log: {LOG_FILE}")
    print(f"Blocklist: {BLOCKED_IPS_FILE}")
    print(f"Umbral de bloqueo: {THRESHOLD_ATTACKS} intentos")
    print("=" * 60)
    print("Presiona Ctrl+C para detener\n")
    
    start_sniffer(args.interface, args.count)


if __name__ == "__main__":
    main()