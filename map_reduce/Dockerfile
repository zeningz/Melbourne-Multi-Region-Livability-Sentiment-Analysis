FROM python:3.7.4

WORKDIR /usr/src/app

COPY . .

RUN pip install -r map_reduce_dependencies.txt

CMD ["python", "map_reduce.py"]