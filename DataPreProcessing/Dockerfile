FROM python:3.11-slim
WORKDIR /DataPreProcessing
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .
ENV FLASK_APP=datapreprocessing.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5001
EXPOSE 5001
CMD ["python", "-m", "flask", "run"]
