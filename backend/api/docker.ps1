docker build --tag backend .
docker run --name backend --publish 8000:8000 backend