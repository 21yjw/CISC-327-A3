# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set environment variables

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project
COPY . /app/

# Expose port 5000 to the outside of the container
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]