# use python as base image
FROM python:3.7-slim

# working directory
WORKDIR /app

# add documents to working directory
ADD . /app

# install requirements
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# open port 3300
EXPOSE 3300

# set environment name
ENV NAME OpentoAll

# run app
CMD ["python", "server.py"]