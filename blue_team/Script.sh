#!/bin/bash

echo "[+] Iniciando configuración básica."

# Verificar si ufw está instalado
command -v ufw &> /dev/null || (echo "[!] UFW no está instalado. Instalando..." && sudo apt-get update -y && sudo apt-get install ufw -y)


# Resetear configuración previa
sudo ufw --force reset

# Establecer políticas por defecto
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Permitir servicios esenciales
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS

# Activar firewall
sudo ufw --force enable

# Mostrar estado final
echo
echo "Configuración final del firewall:"
sudo ufw status verbose

echo "Firewall configurado correctamente."

