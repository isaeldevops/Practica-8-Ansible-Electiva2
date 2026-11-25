# Practica 8 - Ansible y Docker

Esta practica levanta cinco contenedores Ubuntu con SSH y usa Ansible para
configurarlos. Las conexiones se hacen a `127.0.0.1` mediante los puertos
`2221` a `2225`, publicados por Docker Compose; los nombres `servidor1` a
`servidor5` identifican los hosts en el inventario.

## Requisitos

- Docker con Docker Compose.
- Ansible instalado en el entorno que ejecutara los comandos (WSL Ubuntu si
  usas Windows).
- `sshpass` en el entorno de Ansible para autenticar por contraseña:

  ```bash
  sudo apt update
  sudo apt install -y ansible sshpass
  ```

En Windows puedes instalar WSL desde PowerShell con `wsl --install` y luego
ejecutar los comandos siguientes dentro de la distribucion Ubuntu. Activa
tambien la integracion de Docker Desktop con esa distribucion WSL.

Si el proyecto esta guardado en el disco de Windows, copia la carpeta al
sistema de archivos de Ubuntu antes de ejecutar Ansible. Ansible ignora
`ansible.cfg` cuando se ejecuta desde directorios montados como `/mnt/c` por
ser potencialmente escribibles por todos los usuarios:

```bash
cp -a /mnt/c/Users/<usuario>/Codex/ITLA/electiva-2/Practica-8-Ansible-Electiva2 \
  ~/Practica-8-Ansible-Electiva2
cd ~/Practica-8-Ansible-Electiva2
```

Reemplaza `<usuario>` con el usuario de Windows y ajusta la ruta si guardaste
el proyecto en otro lugar. Ejecuta los comandos de Docker y Ansible desde esa
copia dentro de Ubuntu.

## Levantar los servidores

Desde la carpeta del proyecto:

```bash
docker compose up -d --build
docker compose ps
```

La imagen instala OpenSSH Server, Python 3 y sudo. En cada contenedor se crea
el usuario `ansible` con la contraseña `ansible` y sudo sin contraseña.

## Probar la conexion y ejecutar el playbook

```bash
ansible servidores -m ping
ansible-playbook playbook.yml
```

El playbook actualiza la cache de APT, crea `itla`, crea
`/home/itla/app/hola.txt` e instala `cowsay` y `htop` en los cinco servidores.
Puedes comprobar el resultado con:

```bash
ansible servidores -a "cat /home/itla/app/hola.txt"
```

## Detener los contenedores

```bash
docker compose down
```

## Nota de seguridad

Las contraseñas `ansible` y la desactivacion de la verificacion de claves SSH
son unicamente para esta practica local. No reutilices estas credenciales ni
esta configuracion en servidores o redes de produccion.
