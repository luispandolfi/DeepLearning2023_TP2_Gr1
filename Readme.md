# Instalación de dependencias
```bash
conda create -n TP2 python=3.9
conda activate TP2
pip install -r requirements.txt
```

# Docker

## Docker de OpenSearch

Descargar la imagen:
```bash
docker pull opensearchproject/opensearch
```

Ejecutar el docker:
```bash
docker run -p 9200:9200 -p 9600:9600 -e "discovery.type=single-node" -d -v .\databases\opensearch\data:/usr/share/opensearch/data opensearchproject/opensearch:latest
```

## Docker de Postgres

Descargar la imagen:
```bash
docker pull postgres
```

Ejecutar el docker:
```bash
docker run -d --name sistemarecomendacion-postgres -e POSTGRES_USER=admin -e POSTGRES_PASSWORD=Password01 -e PGDATA=/var/lib/postgresql/data/pgdata -v <repo_path>\databases\postgres:/var/lib/postgresql/data -p 5432:5432 postgres
```

Reemplazar <repo_path> con el path en donde esta clonado este repositorio git.
Ejemplo: "C:\private\deep_learning\DeepLearning2023_TP2_Gr1"

Tambien puede ejecutarse estando en el path <repo_path> y reemplazando <repo_path> por .

Nótese que se crea el usuario "admin" con password "Password01" en la base de datos.

Se hacen dos mapeos importantes entre el docker y tu computadora:
- los archivos de datos de la base Postgres los almacena en "<repo_path>\databases\postgres". Esta ubicación se va ignorar en el .gitignore
- mapea el puerto 5432 usado por Postgres con el mismo puerto en tu computadora para poder accederlo

### Herramienta visual para Postgres (opcional)

Pgadmin4 es una herramienta para gestionar PostgreSql.

Sitio de descarga:
https://www.pgadmin.org/download/

### Crear BD

Mediante pgAdmin4 cree una base de datos de nombre "sisrec" - por ahora esta hecho asi, esto podemos evitarlo, parece hay una base de datos ya creada por defecto en el docker.

## Comandos útiles de Docker

Listar los contenedores en ejecución:
```
docker ps
```

Matar a un contenedor:
```
docker kill <container_id>
```

# ORM: SQLAlchemy

Sitio oficial:
https://www.sqlalchemy.org/

Para comenzar:
https://docs.sqlalchemy.org/en/20/orm/quickstart.html

# FastAPI

https://fastapi.tiangolo.com/

## ¿Cómo ejecutar los servicios?

En la consola ejecutar el comando:
```
uvicorn main:app --reload
```

En un browser abir la url:
http://127.0.0.1:8000/docs
