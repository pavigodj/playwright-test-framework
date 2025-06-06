# Use an official playwright image
FROM mcr.microsoft.com/playwright:v1.52.0-jammy

# Set the working directory in the container
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Copy the requirements.txt file from your local machine to the container
COPY requirements.txt .

# Install Python and pip
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=America/Los_Angeles
RUN apt-get update && \
    apt-get install -y --no-install-recommends tzdata && \
    apt-get clean

# Install all test framework dependencies
RUN apt-get install -y --no-install-recommends python3-pip && \
    pip3 install --no-cache-dir -r requirements.txt && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install gunicorn
RUN pip install pipenv

CMD exec gunicorn --bind :8080 --workers 1 --worker-class uvicorn.workers.UvicornWorker --threads 8 main:app
