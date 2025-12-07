# sniffer_defense.py - Blue Team Network Defense

Sniffer de red para detectar actividad sospechosa y generar respuestas automáticas.

---

## Descripción

Herramienta de defensa que utiliza Scapy para monitorear tráfico TCP y detectar:
- Escaneos SYN (posibles port scans)
- Conexiones a puertos inusuales
- Patrones de ataque por volumen

---

## Requisitos

```bash
# Python 3.8+
pip3 install scapy

# Permisos root/sudo
```

---

## Uso

### Básico
```bash
sudo python3 sniffer_defense.py
```

### Con Opciones
```bash
# Especificar interfaz
sudo python3 sniffer_defense.py -i eth0

# Capturar cantidad específica de paquetes
sudo python3 sniffer_defense.py -c 100

# Combinar opciones
sudo python3 sniffer_defense.py -i wlan0 -c 500
```

---

## Argumentos

| Argumento | Descripción | Default |
|-----------|-------------|---------|
| `-i, --interface` | Interfaz de red a monitorear | Todas |
| `-c, --count` | Número de paquetes a capturar (0 = infinito) | 0 |

---

## Archivos Generados

- **log_events.txt**: Registro de eventos con timestamp
- **blocked_ips.txt**: Lista de IPs que superaron el umbral de intentos

---

## Detección

### SYN Scans
- Detecta paquetes con flag SYN (0x02)
- Cuenta intentos por IP origen
- Umbral: 5 intentos antes de bloqueo sugerido

### Puertos Inusuales
Puertos comunes permitidos: 22, 80, 443, 53, 25, 110, 143

Cualquier otro puerto genera alerta.

---

## Ejemplo de Salida

```
============================================================
Blue Team - Sniffer de Defensa
============================================================
Log: log_events.txt
Blocklist: blocked_ips.txt
Umbral de bloqueo: 5 intentos
============================================================

[2025-12-07 10:30:15] Iniciando sniffer de defensa en interfaz: eth0
[2025-12-07 10:30:22] ALERTA: SYN scan detectado desde 192.168.1.50 al puerto 22
[2025-12-07 10:30:23] ALERTA: SYN scan detectado desde 192.168.1.50 al puerto 80
[2025-12-07 10:30:25] ALERTA: Conexión a puerto inusual 8080 desde 192.168.1.50
[2025-12-07 10:30:30] CRITICO: IP 192.168.1.50 ha realizado 5 intentos
[2025-12-07 10:30:30] IP 192.168.1.50 agregada a blocklist. Comando sugerido: sudo iptables -A INPUT -s 192.168.1.50 -j DROP
```

---

## Configuración Interna

Variables modificables en el código:

```python
LOG_FILE = "log_events.txt"              # Archivo de log
BLOCKED_IPS_FILE = "blocked_ips.txt"     # Lista de bloqueo
COMMON_PORTS = {22, 80, 443, 53, 25, 110, 143}  # Puertos permitidos
THRESHOLD_ATTACKS = 5                     # Intentos antes de bloqueo
```

---

## Troubleshooting

### Error: Permission denied
```bash
# Solución: Ejecutar con sudo
sudo python3 sniffer_defense.py
```

### Error: Module 'scapy' not found
```bash
# Solución: Instalar Scapy
pip3 install scapy
```

### No detecta tráfico
```bash
# Verificar interfaces disponibles
ip link show

# Usar interfaz correcta
sudo python3 sniffer_defense.py -i <interfaz>
```

---

## Bloqueo Manual de IPs

El script sugiere comandos de bloqueo. Para ejecutarlos manualmente:

```bash
# Bloquear IP con iptables
sudo iptables -A INPUT -s <IP_SOSPECHOSA> -j DROP

# Ver reglas activas
sudo iptables -L -n -v

# Desbloquear IP
sudo iptables -D INPUT -s <IP_SOSPECHOSA> -j DROP
```

---

## Nota de Seguridad

**Solo usar en infraestructura autorizada**. Monitorear tráfico de red requiere permisos y debe realizarse con consentimiento explícito.
