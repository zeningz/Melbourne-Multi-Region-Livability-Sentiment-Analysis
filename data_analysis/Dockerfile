FROM python:3.7.4

WORKDIR /usr/src/app

COPY . .

RUN pip install -r analysis_dependencies.txt

CMD ["python", "main.py"]