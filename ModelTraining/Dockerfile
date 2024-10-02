FROM python:3.11-slim
WORKDIR /ModelTraining
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .
ENV FLASK_APP=modelTraining.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5003
EXPOSE 5003
CMD ["python", "-m", "flask", "run"]
