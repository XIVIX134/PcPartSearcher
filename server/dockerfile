FROM python:3.9-slim

WORKDIR /app

# Copy server requirements first
COPY server/requirements.txt .
RUN pip install -r requirements.txt

# Copy server code and scrapers
COPY server/ .
COPY scrapers/ ./scrapers/

# Set Python path
ENV PYTHONPATH=/app

EXPOSE 5000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5000"]