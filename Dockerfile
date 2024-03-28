# Use an official Python 3.10 slim image as the base image
FROM python:3.10-slim

# Install missing library
RUN apt-get update && apt-get install -y git libgomp1 libsndfile1 ffmpeg

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed dependencies specified in requirements.txt
RUN pip install -r requirements.txt

# Make port 5001 available to the world outside this container
EXPOSE 5001

# Define environment variable
ENV FLASK_APP=app.py

# Run app.py when the container launches
CMD ["python", "app.py"]