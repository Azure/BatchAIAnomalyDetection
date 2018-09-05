
FROM continuumio/miniconda3
EXPOSE 3000

RUN apt-get update -y
COPY requirements.txt /
RUN pip install --upgrade pip
RUN python3 -m pip install -r requirements.txt

COPY submit_jobs.py /
COPY bai_pred_config.json /
COPY pred.sh /
RUN ["chmod", "+x", "pred.sh"]
CMD /pred.sh
