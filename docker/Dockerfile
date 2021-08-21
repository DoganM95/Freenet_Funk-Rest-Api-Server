FROM python:3

# Create app directory
WORKDIR /usr/src/app

# Bundle app source
COPY . .

# Install required python modules
RUN python -m pip install funkapi
RUN python -m pip install flask

# Add permissions
RUN chmod --recursive +rwx ./*

# Define communication port
EXPOSE 5000

# Start the server
CMD [ "python","./server.py" ]