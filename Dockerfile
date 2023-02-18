FROM public.ecr.aws/bitnami/python:3.9
EXPOSE 8080
WORKDIR /app
COPY main.py main.py
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
CMD [ "python3", "main.py" ]
