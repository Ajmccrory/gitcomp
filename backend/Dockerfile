FROM python:3.9-slim

WORKDIR /gitcomp-backend

COPY . /gitcomp-backend

RUN pip3 install --no-cache-dir --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENV FLASK_APP = app.py

CMD ["flask", "run", "--host=0.0.0.0"]
