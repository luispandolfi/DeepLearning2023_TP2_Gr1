# Instalación de dependencias
```bash
conda create -n TP2 python=3.9
conda activate TP2

pip install -r requirements.txt
```

## Docker
docker pull opensearchproject/opensearch

cd vector_db
docker run -p 9200:9200 -p 9600:9600 -e "discovery.type=single-node" -d -v C:\Users\josez\OneDrive\Documentos\ITBA-DeepLearning\TP2\DeepLearning2023_TP2_Gr1\vector_db\db_data:/usr/share/opensearch/data opensearchproject/opensearch:latest

### Comandos útiles

Listar los contenedores en ejecución:
```
docker ps
```

Matar a un contenedor:
```
docker kill <container_id>
```