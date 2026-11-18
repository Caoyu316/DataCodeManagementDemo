FROM python:3.14-slim
WORKDIR /app
COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY *.py .
COPY data/ data/
CMD ["python", "report.py", "pipeline.py"]
