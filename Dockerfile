FROM python:3.8-buster

LABEL writer="zerrozhao@gmail.com"

WORKDIR /src/block7stats

COPY . /src/block7stats/

RUN pip install -r requirements.env.txt
RUN pip install -r requirements.txt

CMD ["python","main.py"]