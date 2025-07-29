FROM python:3.11-slim-alpine

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY . .

# Expose port (if FastAPI)
EXPOSE 8000

# Command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
