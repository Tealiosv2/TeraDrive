# TeraDrive

docker setup:
docker run --name TeraDrive -e POSTGRES_PASSWORD=mysecretpassword -d -p 5432:5432 postgres
docker exec -it TeraDrive psql -U postgres
CREATE DATABASE teradrive;




