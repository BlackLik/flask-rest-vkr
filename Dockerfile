# Use an official Python runtime as a parent image
FROM python:3.10-slim 

# Set the working directory in the container to /backend
WORKDIR /backend

# Add the current directory contents into the container at /backend
ADD . /backend

# Install any needed packages specified in requirements.txt
RUN chmod +x /backend/start.sh
RUN python -m pip install --upgrade pip
RUN pip install psycopg2-binary
RUN pip install requests
RUN pip install gunicorn
RUN pip install catboost
RUN pip install Flask
RUN pip install scikit-learn
RUN pip install Flask-SQLAlchemy
RUN pip install Flask-Cors
RUN pip install python-dotenv
RUN pip install numpy

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Set environment varibles
ENV FLASK_RUN_HOST=0.0.0.0
ENV POSTGRESQL_HOST=localhost
ENV POSTGRESQL_PORT=5432
ENV POSTGRESQL_DB=spo_db
ENV POSTGRESQL_USER=admin
ENV POSTGRESQL_PASSWORD=Admin_123
ENV DEBUG=0



# Run the command to start uWSGI
CMD ["gunicorn", "-w", "4", "application:app", "-b", "0.0.0.0:5000"]
