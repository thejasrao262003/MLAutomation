FROM python:3.11-slim
WORKDIR /Visualisation
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .
ENV FLASK_APP=visualisation.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5002
EXPOSE 5002
CMD ["python", "-m", "flask", "run"]
