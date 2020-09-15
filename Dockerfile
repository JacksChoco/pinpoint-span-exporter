FROM python:3.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /opsnow-daily-analysis
WORKDIR /opsnow-daily-analysis
RUN mkdir -p ~/.pip
RUN pip3 install prometheus_client requests
ADD . /opsnow-daily-analysis/

CMD ["python3","prometheus.py"]
