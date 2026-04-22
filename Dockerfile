# Use official Python images
FROM python:3.10

# Create a working directory in the container
WORKDIR /app

# Copy the entire source code into the container
COPY . /app

# Install libraries from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Command to run the application when the container starts
CMD ["python", "main.py"]
