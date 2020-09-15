FROM python:3.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /pinpoint-span-exporter
WORKDIR /pinpoint-span-exporter
RUN mkdir -p ~/.pip
RUN pip3 install prometheus_client requests
ADD . /pinpoint-span-exporter/

CMD ["python3","prometheus.py"]
