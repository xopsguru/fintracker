# Base image
FROM python:3.13.5

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files into container
COPY . .

# Expose port
EXPOSE 5001

# Command to run the application
CMD ["python3", "app.py"]
