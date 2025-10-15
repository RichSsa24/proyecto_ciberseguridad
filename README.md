# 🛡️ Proyecto Final — Red Team vs Blue Team en Azure
**Curso:** CY-302 Programación Avanzada  
**Docente:** Andrés Vargas  
**Fecha:**  Octubre de 2025

---

## 👥 Integrantes del equipo
- Hector Díaz Urbina  
- Emily Navarro Guevara  
- José Ricardo Solís Arias  
- Marijesus Herrera Nuñez  
- Kamila Chavarria Genardi  
- Yeremy Corrales Madrigal

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



