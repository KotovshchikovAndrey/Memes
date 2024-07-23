# Memes

## Запуск

0. Создать .env файлы с необходимыми параметрами в папках ApiMicroservice и FileMicroservice (необходимые параметры указаны в /src/config/settings.py)

1. docker-compose --env-file <.env docker file> up -d

2. docker exec -it minio bash

3. mc alias set memes http://localhost:9000 <access_key> <secret_key>

4. mc mb memes/memes

5. exit

6. docker exec -it kafka kafka-topics --create --topic <topic_name> --partitions 1 --replication-factor 1 --bootstrap-server kafka:9092

7. docker-compose --env-file <.env docker file> restart file_service
