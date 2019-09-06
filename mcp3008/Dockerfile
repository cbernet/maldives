# Use an official Python runtime as a base image
# FROM python:3.6.9-slim-stretch
FROM woahbase/alpine-rpigpio:armv7l

# Set the working directory to /app
WORKDIR /app

# install gcc, needed to install spidev for python
RUN apk add --no-cache gcc python3-dev musl-dev linux-headers

# Install any needed python packages specified in requirements.txt
COPY requirements.txt /app/
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the script
COPY *.py /app/

# Run app.py when the container launches
# The -u flag specifies to use the unbuffered ouput.
# in this way, what's printed by the app is visible on the host
# while the container is running
CMD ["python", "-u", "read_adc.py"]
