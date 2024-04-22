# Use an official Python 3.11 runtime as a parent image
FROM python:3.11

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents (which is `app`) into the container at /usr/src/app/app
COPY app/ ./app

# Copy the requirements.txt file into the working directory
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
# Make sure your requirements.txt is in the root of your project directory and includes alembic and sqlalchemy
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV NAME World

# Ensure Alembic is configured properly and runs migrations before starting the app
CMD ["sh", "-c", "alembic -c app/alembic.ini upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]