FROM python:2.7
COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

ADD . /code
WORKDIR /code/

EXPOSE 5002
ENTRYPOINT ["python", "server.py"]