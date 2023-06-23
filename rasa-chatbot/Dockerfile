# Use the official Rasa base image
FROM rasa/rasa:3.5.6-full

# Copy the Rasa chatbot files to the container
WORKDIR  /app

COPY . /app

USER root

# RUN mkdir ./models_1
# ENV RASA_MODEL_DIR=/app/models_1
# RUN ["rasa", "train"]

# Expose the Rasa server ports
EXPOSE 5005

# Set the entrypoint command to run the Rasa server
CMD [ "run","-m","/app/models","--enable-api","--cors","*" ,"--endpoints", "endpoints.yml", "--log-file", "out.log"]

