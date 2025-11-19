import os
import socket
import subprocess

#TARGET_IP = "20.171.26.154" ip de la maquina
TARGET_IP = "127.0.0.1" #ip personal


# 1. Listar usuarios del sistema

def listar_usuarios():
    print("\n===== USUARIOS DEL SISTEMA =====")
    try:
        if os.name == "nt":     
            os.system("net user")
        else:                   
            os.system("cut -d: -f1 /etc/passwd")
    except Exception as e:
        print("Error:", e)



#Escanear puertos abiertos de la IP

def escanear_puertos(ip):
    print(f"\n===== PUERTOS ABIERTOS EN {ip} =====")

    puertos_comunes = [
        21, 22, 23, 25, 53, 80, 110,
        135, 139, 443, 445, 3306, 3389
    ]

    abiertos = []

    for puerto in puertos_comunes:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)

        try:
            resultado = sock.connect_ex((ip, puerto))
            if resultado == 0:
                abiertos.append(puerto)
        except:
            pass
        finally:
            sock.close()

    if not abiertos:
        print("No se encontraron puertos abiertos.")
    else:
        for p in abiertos:
            print(f"• Puerto {p}")



#Listar servicios del sistema

def listar_servicios():
    print("\n===== SERVICIOS DEL SISTEMA =====")

    try:
        if os.name == "nt": 
            comando = ["sc", "query", "state=", "all"]
        else:  
            comando = ["systemctl", "list-units", "--type=service"]

        resultado = subprocess.run(comando, capture_output=True, text=True, encoding="latin-1")
        texto = resultado.stdout.splitlines()

        servicios = []

        if os.name == "nt":
            for linea in texto:

                if "NOMBRE_SERVICIO:" in linea:
                    nombre = linea.split("NOMBRE_SERVICIO:")[1].strip()
                    servicios.append(nombre)

 
                elif "SERVICE_NAME:" in linea:
                    nombre = linea.split("SERVICE_NAME:")[1].strip()
                    servicios.append(nombre)

        else:  
            for linea in texto:
                if ".service" in linea:
                    nombre = linea.split()[0]
                    servicios.append(nombre)


        if servicios:
            for i, srv in enumerate(servicios, 1):
                print(f"{i}. {srv}")
        else:
            print("No se encontraron servicios.")

    except Exception as e:
        print("Error listando servicios:", e)

# MAIN
if __name__ == "__main__":
    print("---------- Informacion del sistema ----------")

    listar_usuarios()
    escanear_puertos(TARGET_IP)
    listar_servicios()

    print("\nAuditoría completada.")