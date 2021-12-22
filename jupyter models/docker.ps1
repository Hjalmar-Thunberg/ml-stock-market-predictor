$directorypath = (Get-Item .).FullName
docker run --name stockModels -p 8888:8888 -v $directorypath:/home/jovyan/ jupyter/scipy-notebook