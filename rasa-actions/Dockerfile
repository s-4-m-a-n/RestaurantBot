# Use the official Rasa SDK base image
FROM rasa/rasa-sdk:3.5.1

WORKDIR  /app

COPY requirements.txt .

USER root
# COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

# USER 1001

COPY . .
# Expose the Rasa Action Server port
EXPOSE 5055

# Set the entrypoint command to run the Rasa Action Server
CMD ["start", "--actions", "actions"]
# CMD ["start"]

# CMD ["rasa", "run", "actions", "--actions", "actions"]
# CMD ["rasa", "run", "actions"]

