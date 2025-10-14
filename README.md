# 🛡️ Proyecto Final — Red Team vs Blue Team en Azure
**Curso:** CY-302 Programación Avanzada  
**Docente:** Andrés Vargas  
**Fecha:** 9 de octubre de 2025

---

## 👥 Integrantes del equipo
- Hector Díaz Urbina  
- Emily Navarro Guevara  
- José Ricardo Solís Arias  
- Marijesus Herrera Nuñez  
- Kamila Chavarria Genardi  
- Jeremy Corrales

---

## 📌 Descripción general
Este proyecto práctico consiste en simular un escenario controlado de **ataque y defensa en entornos Azure**, dividiendo al equipo en dos roles principales:

- **Red Team:** Ejecuta ataques controlados contra una máquina objetivo.  
- **Blue Team:** Defiende la máquina, detecta actividad maliciosa y responde de forma básica.

El propósito es **entender el ciclo completo de ciberseguridad ofensiva y defensiva**:  
> Ataque → Detección → Acción.

---

## 📂 Estructura del repositorio
```
proyecto_ciberseguridad/
│
├── blue_team/
│   ├── firewall_basic.sh        # Script básico de firewall
│   ├── os_audit.py              # Auditoría básica del sistema
│   ├── sniffer_defense.py       # Detección de tráfico sospechoso
│   └── log_events.txt           # Registro de eventos detectados
│
├── red_team/
│   ├── scanner.py               # Escáner con Nmap (flags básicos)
│   └── packet_attack.py         # Simulación de ataque SYN simple
│
├── docs/
│   ├── E1.pdf                   # Entrega 1 — Base del proyecto
│   ├── E2.pdf                   # Entrega 2 — Herramientas base
│   ├── E3.pdf                   # Entrega 3 — Detección y respuesta
│   └── E4.pdf                   # Entrega 4 — Integración final
│
└── README.md
```

---

## 🧠 Requerimientos técnicos
- **Lenguaje:** Python 3  
- **Herramientas:** Nmap, Scapy, Paramiko  
- **Firewall:** UFW / iptables  
- **Infraestructura:** Microsoft Azure VM

---

## 🚀 Instrucciones de uso

### 1. **Configuración inicial (Entrega 1)**  
- Crear la VM en Azure con IP pública y puertos abiertos (22, 80, 443).  
- Configurar NSG y aplicar reglas básicas de firewall.  
- Ejecutar:
```bash
cd blue_team
sudo bash firewall_basic.sh
```

---

### 2. **Escaneo y auditoría (Entrega 2)**  
**Red Team:**  
```bash
cd red_team
python3 scanner.py
```
> Guarda los resultados del escaneo en un archivo de salida.

**Blue Team:**  
```bash
cd blue_team
python3 os_audit.py
```
> Lista usuarios, puertos abiertos y servicios activos.

---

### 3. **Detección y respuesta (Entrega 3)**  
- El Blue Team ejecuta `sniffer_defense.py` para escuchar paquetes SYN sospechosos.  
- El Red Team lanza `packet_attack.py`.  
- Los eventos detectados se registran automáticamente en `log_events.txt`.

```bash
# Blue Team
python3 sniffer_defense.py

# Red Team
python3 packet_attack.py
```

---

### 4. **Integración final (Entrega 4)**  
- Ejecutar los scripts en secuencia:  
  `scanner.py` o `packet_attack.py` → detección por `sniffer_defense.py` → acción sugerida.  
- Consultar el diagrama, resultados y recomendaciones en `docs/E4.pdf`.

---

## 🛡️ Buenas prácticas
- Realizar pruebas únicamente dentro de la infraestructura del curso.  
- No utilizar IPs externas ni datos personales.  
- Apagar las VMs cuando no estén en uso para evitar costos innecesarios.  
- Documentar cualquier error encontrado y cómo se solucionaría.

---

## 📝 Entregables y rúbricas

| Entrega | Descripción                          | Peso | Evidencia requerida                                |
|---------|---------------------------------------|------|----------------------------------------------------|
| E1      | Base del proyecto & entorno           | 20%  | README, estructura, firewall, PDF con evidencias   |
| E2      | Herramientas base                     | 25%  | scanner.py, os_audit.py, PDF con capturas          |
| E3      | Detección y respuesta                 | 25%  | sniffer_defense.py, packet_attack.py, PDF          |
| E4      | Integración final                     | 30%  | Flujo ataque→detección→acción, diagrama, PDF, video|

---

## 📎 Recursos útiles
- Documentación oficial de Nmap: https://nmap.org/book/man.html  
- Scapy Docs: https://scapy.readthedocs.io/en/latest/  
- Paramiko Docs: http://www.paramiko.org/  
- Azure Portal: https://portal.azure.com

---

## 📜 Licencia
Este proyecto es para fines académicos dentro del curso CY-302 y no debe ser utilizado en entornos externos.

---
