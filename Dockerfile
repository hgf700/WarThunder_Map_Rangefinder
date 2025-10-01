FROM ultralytics/ultralytics:latest

WORKDIR /app
COPY . /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python", "train.py"]
