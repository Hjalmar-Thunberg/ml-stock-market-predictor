docker build --tag backend .
docker run --name backend -itd --publish 8000:8000 backend
