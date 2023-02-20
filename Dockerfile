FROM public.ecr.aws/docker/library/python:3.8-slim-buster
WORKDIR /app
COPY main.py main.py
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
CMD [ "python3", "main.py" ]
