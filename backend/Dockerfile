FROM python:3.10-slim

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

ENV PYTHONPATH=/app:$PYTHONPATH

# Run app.py when the container launches
CMD ["uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000"]
