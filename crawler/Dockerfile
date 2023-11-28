FROM python:3.7.4

WORKDIR /usr/src/app

COPY . .

RUN pip install -r crawler_dependencies.txt

CMD ["python", "crawl_data.py"]