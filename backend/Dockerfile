FROM python:3.11

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
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
