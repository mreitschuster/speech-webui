# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONBUFFERED=1

# Set working directory in the container
WORKDIR /app

# Copy requirements.txt to the container at /app/
COPY requirements.txt .

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the content of your current folder into the container at /app/
COPY . .


EXPOSE 7860
ENV GRADIO_SERVER_NAME="0.0.0.0"


# Run Gradio app on container start
CMD ["python", "app.py"]