FROM python:3

# Create app directory
WORKDIR /usr/src/app

# Bundle app source
COPY . .

RUN python -m pip install funkapi
RUN python -m pip install flask

RUN chmod +x ./*

# rename credential file
RUN mv ./configuration/credentials_template.py ./configuration/credentials.py

# communication port
EXPOSE 5000

# Start the server
CMD [ "./docker/entrypoint.sh" ]