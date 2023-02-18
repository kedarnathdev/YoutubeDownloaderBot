FROM public.ecr.aws/docker/library/python:3.8-slim-buster
RUN docker purge system
EXPOSE 8080
WORKDIR /app
COPY main.py main.py
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
CMD [ "python3", "main.py" ]
