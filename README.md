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

## App web para Render

El directorio `web/` contiene una app HTTP minima para poder usar Render Web
Service. Es independiente del Dockerfile de la raiz, que continua siendo la
imagen SSH usada por los cinco servidores Ansible. La app escucha en el puerto
indicado por la variable `PORT` que Render configura automaticamente.

Para probar la app localmente:

```bash
docker build -t practica-8-web -f web/Dockerfile web
docker run --rm -p 8080:8080 -e PORT=8080 practica-8-web
```

Abre `http://localhost:8080` en el navegador. El endpoint de comprobacion es
`http://localhost:8080/healthz`.

## Publicar la app y desplegar en Render

El workflow `.github/workflows/deploy.yml` se ejecuta al hacer `push` a `main`.
Construye **`web/Dockerfile`** para `linux/amd64`, publica la imagen en Docker
Hub con las etiquetas `web-latest`, `web-<SHA>` y `web-<fecha-UTC>`, y solicita
a Render desplegar la imagen etiquetada con el SHA.

Antes de usarlo:

1. Crea el repositorio `practica-8-ansible-electiva2` en Docker Hub si aun no
   existe.
2. Publica una primera imagen web para que Render pueda conectarla:

   ```bash
   docker login --username TU_USUARIO_DOCKERHUB
   docker build -t TU_USUARIO_DOCKERHUB/practica-8-ansible-electiva2:web-latest -f web/Dockerfile web
   docker push TU_USUARIO_DOCKERHUB/practica-8-ansible-electiva2:web-latest
   Isael es el mejor
   ```

   Al iniciar sesion en Docker Hub, usa un access token como contrasena.
3. En la configuracion del repositorio de GitHub, ve a **Settings > Secrets and
   variables > Actions** y crea estos repository secrets:
   - `DOCKERHUB_USERNAME`: usuario de Docker Hub.
   - `DOCKERHUB_TOKEN`: access token de Docker Hub con permiso para publicar.
   - `RENDER_API_KEY`: API key de Render.
   - `RENDER_SERVICE_ID`: ID del **nuevo Web Service** de Render.
4. En Render, crea un **Web Service** basado en una imagen Docker existente con esta
   imagen de Docker Hub como fuente:
   `docker.io/<usuario-dockerhub>/practica-8-ansible-electiva2:web-latest`.
   Selecciona el plan **Free**. Si la imagen es privada, configura tambien en
   Render las credenciales para descargarla. El servicio debe usar el mismo
   host, usuario y nombre de imagen; el workflow cambia el tag a `web-` mas el
   SHA del commit al solicitar el deploy.
5. Haz `push` a la rama `main`.

Las etiquetas de la app empiezan con `web-` para no reemplazar por accidente
las etiquetas de la imagen SSH del laboratorio Ansible en el mismo repositorio
de Docker Hub.

Si ya creaste un Private Service de pago para la imagen SSH, elimínalo para
detener futuros cargos. Crea un Web Service nuevo con la imagen `web/` y
actualiza `RENDER_SERVICE_ID` con el ID de ese nuevo servicio.

## Detener los contenedores

```bash
docker compose down
```

## Nota de seguridad

Las contraseñas `ansible` y la desactivacion de la verificacion de claves SSH
son unicamente para esta practica local. No reutilices estas credenciales ni
esta configuracion en servidores o redes de produccion.
