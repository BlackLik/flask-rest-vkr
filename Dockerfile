# Use an official Python runtime as a parent image
FROM python:3.10-alpine

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Set environment varibles
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV POSTGRESQL_HOST = localhost
ENV POSTGRESQL_PORT = 5432
ENV POSTGRESQL_DB = spo_db
ENV POSTGRESQL_USER = admin
ENV POSTGRESQL_PASSWORD = Admin_123
ENV DEBUG=0



# Run the command to start uWSGI
CMD ["gunicorn", "-w", "4", "app:app"]

