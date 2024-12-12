# Proyecto de Scraping con Docker y ChromeDriver

Este proyecto realiza scraping automatizado para interactuar con YouTube, dejando comentarios recomendando productos. A continuación se explican los pasos para configurar y ejecutar el proyecto en cualquier máquina.

---

## Requisitos

1. **Instalación de Docker**:

   - Asegúrate de tener Docker y Docker Compose instalados en la máquina.
     - [Instrucciones para instalar Docker](https://docs.docker.com/get-docker/)
     - [Instrucciones para instalar Docker Compose](https://docs.docker.com/compose/install/)

2. **ChromeDriver**:

   - El archivo `chromedriver.exe` ya está incluido en la carpeta principal del proyecto.
   - Asegúrate de que la versión de ChromeDriver sea compatible con la versión de Google Chrome instalada en la máquina.

3. **Base de datos**:

   - El archivo `Afiliados.db` está en la carpeta `database/` y contiene los registros de los videos visitados y comentarios realizados.

---

## Estructura del Proyecto

```
AFILIADOS2/
|
├── database/
|   ├── Afiliados.db          # Base de datos SQLite
|   ├── consultas.py          # Código para manejar consultas a la base de datos
|   └── db_config.py          # Configuración de conexión a la base de datos
|
├── scraping/
|   ├── amazon.py             # Código para scraping en Amazon
|   └── youtube.py            # Código para scraping en YouTube
|
├── utils/
|   ├── ai_recommendations.py # Funciones de recomendación con IA
|   ├── categories.py         # Funciones de manejo de categorías
|   └── chromedriver.exe      # Ejecutable de ChromeDriver
|
├── Dockerfile                # Definición de la imagen Docker
├── docker-compose.yml        # Configuración para Docker Compose
├── main.py                   # Script principal del proyecto
└── requirements.txt          # Dependencias de Python
```

---

## Configuración y Ejecución

### 1. Clonar el proyecto o mover la carpeta a la nueva máquina

Asegúrate de que todos los archivos (incluyendo `chromedriver.exe` y `Afiliados.db`) estén presentes.

### 2. Construir la imagen Docker

Desde la carpeta raíz del proyecto, ejecuta:

```bash
docker-compose build
```

### 3. Iniciar ChromeDriver

Desde la carpeta raíz del proyecto, ejecuta:

```bash
chromedriver --port=4444 --allowed-origins=* --whitelisted-ips=""
```

Este comando inicia ChromeDriver en el puerto `4444`. Si el puerto ya está ocupado, puedes cambiarlo, por ejemplo, a `5555`:

```bash
chromedriver --port=5555 --allowed-origins=* --whitelisted-ips=""
```

Asegúrate de que el puerto coincide con el configurado en el código (por defecto es `4444`).

### 4. Ejecutar el contenedor

Ejecuta el siguiente comando:

```bash
docker-compose run --rm app
```

Este comando iniciará la aplicación y ejecutará el scraping.

---

## Notas importantes

1. **Base de datos externa**:

   - La base de datos `Afiliados.db` está mapeada como volumen externo, por lo que los datos persisten aunque el contenedor sea eliminado.
   - Puedes verificar que los cambios se reflejan directamente en el archivo `database/Afiliados.db`.

2. **Cambios en el código**:

   - Si haces cambios en el código, estos se reflejarán automáticamente gracias al volumen configurado en `docker-compose.yml`:
     ```yaml
     volumes:
       - ./database/Afiliados.db:/app/database/Afiliados.db
       - .:/app
     ```
   - No necesitas reconstruir la imagen para ver los cambios en el código.

3. **Detener el contenedor**:

   - El contenedor se elimina automáticamente después de la ejecución debido a la opción `--rm`. No es necesario usar `docker-compose down`.

4. **Problemas comunes**:

   - Si el contenedor no puede conectarse a ChromeDriver, verifica que este esté ejecutándose y en el puerto correcto.
   - Asegúrate de que la versión de ChromeDriver sea compatible con tu versión de Google Chrome.

---

## Comandos clave

- **Construir la imagen:**

  ```bash
  docker-compose build
  ```

- **Iniciar ChromeDriver:**

  ```bash
  chromedriver --port=4444 --allowed-origins=* --whitelisted-ips=""
  ```

- **Ejecutar el contenedor:**

  ```bash
  docker-compose run --rm app
  ```

