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