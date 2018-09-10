
FROM continuumio/miniconda3
EXPOSE 3000

RUN apt-get update -y

COPY batchai/requirements.txt /
RUN pip install --upgrade pip
RUN python3 -m pip install -r requirements.txt

COPY batchai/predict.py /
COPY batchai/predict_config.json / 
