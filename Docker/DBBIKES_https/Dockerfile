FROM tiangolo/uwsgi-nginx-flask:python3.7
COPY ./requirement.txt .
RUN pip install -r requirement.txt
COPY ./app /app
