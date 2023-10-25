## Base de datos Postgres

### Descargar la imagen de postgres en docker

En consola, ejecutar el comando:
```
docker pull postgres
```

### Ejecutar el docker de Postgres

En consola, ejecutar el comando:
```
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


## ORM: SQLAlchemy

Sitio oficial:
https://www.sqlalchemy.org/

Para comenzar:
https://docs.sqlalchemy.org/en/20/orm/quickstart.html


## Crear environment con Conda

Pare ver los environments existentes:
conda env list

Vamos a crear el environment de nombre "tp2" y usar el archivo de requirements:

conda create --name tp2 python=3.9
conda activate tp2
conda install --yes --file requirements.txt

Para ver los packages instalados:
conda list

Además ejecute:
pip install psycopg2-binary
pip install pandas

## Otros

Mediante pgAdmin4 cree la base de datos sisrec

## FastAPI

https://fastapi.tiangolo.com/#installation

pip install fastapi
pip install "uvicorn[standard]"