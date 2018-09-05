
FROM continuumio/miniconda3
EXPOSE 3000

RUN apt-get update -y
RUN apt-get install -y g++ unixodbc-dev

COPY requirements.txt /
RUN pip install --upgrade pip
RUN python3 -m pip install -r requirements.txt

COPY msodbcsql_13.1.9.2-1_amd64.deb /
COPY msodbcsql17_17.2.0.1-1_amd64.deb /
RUN ACCEPT_EULA=Y apt install -y /msodbcsql17_17.2.0.1-1_amd64.deb
RUN ACCEPT_EULA=Y apt install -y /msodbcsql_13.1.9.2-1_amd64.deb

RUN apt-get install -y locales
RUN echo "nb_NO.UTF-8 UTF-8" > /etc/locale.gen
RUN echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen
RUN locale-gen

COPY train.py /
COPY predict.py /
COPY train_config.json /
COPY predict_config.json / 
