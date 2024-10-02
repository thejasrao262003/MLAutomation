FROM python:3.11-slim
WORKDIR /FrontEnd
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "frontend.py", "--server.address=0.0.0.0"]