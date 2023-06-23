# Use the official Python image as the base image
FROM python:3.7.16

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# RUN apt-get install libjpeg-dev zlib1g-dev
# RUN pip install --no-cache-dir --upgrade pip
# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask app files to the container
COPY . .

# Expose the Flask app port
EXPOSE 5000

# ENTRYPOINT ["python"]

CMD ["python", "main.py"]


# Set the entrypoint command to run the Flask app
# CMD ["python", "main.py"]
