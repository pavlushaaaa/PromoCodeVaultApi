# Use an official Python runtime as a parent image
FROM python:3.8

# Set the working directory in the container
# This should be one directory up since your Dockerfile is inside the `api` directory
WORKDIR /usr/src/app

# Copy the current directory contents (which is `api`) into the container at /usr/src/app/api
COPY . ./api

# Install any needed packages specified in requirements.txt
# Make sure your requirements.txt is in the `api` directory
RUN pip install --no-cache-dir -r api/requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV NAME World

# Run app.py when the container launches
# Since WORKDIR is `/usr/src/app`, you need to go into the `api` directory
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]