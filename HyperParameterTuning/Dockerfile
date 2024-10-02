FROM python:3.11-slim
WORKDIR /HyperParameterTuning
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .
ENV FLASK_APP=hyperParameterTuning.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5004
EXPOSE 5004
CMD ["python", "-m", "flask", "run"]
