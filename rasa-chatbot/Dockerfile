# Use the official Rasa base image
FROM rasa/rasa:3.5.6-full

# Copy the Rasa chatbot files to the container
WORKDIR  /app

COPY . .

USER root

# RUN  rasa train

# Expose the Rasa server ports
EXPOSE 5005

# Set the entrypoint command to run the Rasa server
CMD [ "run","-m","/app/models","--enable-api","--cors","*" ,"--endpoints", "endpoints.yml", "--log-file", "out.log"]

