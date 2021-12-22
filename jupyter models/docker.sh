export STOCKMODELS_PATH=pwd
docker run --name stockModels -itd -p 8888:8888 -v ${STOCKMODELS_PATH}:/home/jovyan/ jupyter/scipy-notebook
