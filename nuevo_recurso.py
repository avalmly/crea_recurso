#------------------------------------------------------------------------------------------
# Autor: Alberto Valero Mlynaricova
# Fecha: 16/12/2023
#
# Descripción:  Creará el recurso recurso1 solo permitirá conectarse a los usuarios del grupo   
#               alumnos que están disponible en directorio activo, en el caso de no existir el 
#               grupo será necesario crearlo usando powershell remoto al servidor de dominio
#------------------------------------------------------------------------------------------

import os
import sys
import subprocess    

def crea_recurso(recurso, ruta, grupo):
    try:
        with open("/sbin/plantilla_recurso", 'r') as plantilla_recurso:
            lineas = plantilla_recurso.read()

        # Realizar las sustituciones
        lineas_modificadas = (
            lineas
            .replace('recurso', recurso)
            .replace('ruta', ruta)
            .replace('grupo', grupo)
        )

        smb_conf_path = "/etc/samba/smb.conf"

        # Verificar si el recurso ya existe en smb.conf
        with open(smb_conf_path, 'r') as smb_conf:
            if f"[{recurso}]" not in smb_conf.read():
                # Añadir las líneas modificadas al archivo smb.conf
                with open(smb_conf_path, "a") as samba_file:
                    samba_file.write(f'\n{lineas_modificadas}\n')
                    
                # Verificar si el directorio ya existe antes de intentar crearlo
                if not os.path.exists(f"/recursos/{recurso}"):
                    # Crear el directorio del recurso
                    os.makedirs(f"/recursos/{recurso}")

                    # Configurar permisos del directorio
                    os.chmod(f"/recursos/{recurso}", 0o770)
                    os.system(f"chown :{grupo} /recursos/{recurso}")

                    print(f"Recurso '{recurso}' y directorio creado con éxito.")
                else:
                    print(f"El directorio '/recursos/{recurso}' ya existe.")
            else:
                print(f"El recurso '{recurso}' ya existe en smb.conf.")

    except FileNotFoundError:
        print("Error: No se encontró el archivo de plantilla 'plantilla_recurso'.")
    except Exception as e:
        print(f"Error durante la creación del recurso: {e}")

usuario = subprocess.run(["whoami"], capture_output=True, text=True)
usuario = usuario.stdout.strip()
ruta = f"/recursos/{usuario}"
host = "serverad"
usuario = "administrador"
password = "Departamento1!"

crea_recurso(usuario, ruta, usuario)