# TeraDrive

docker setup:<br>
docker run --name TeraDrive -e POSTGRES_PASSWORD=mysecretpassword -d -p 5432:5432 postgres<br>
docker exec -it TeraDrive psql -U postgres<br>
CREATE DATABASE teradrive;<br>

database setup:<br>
RUN:<br>
<b>initialize_database.py<b><br>
in package database_stuff



