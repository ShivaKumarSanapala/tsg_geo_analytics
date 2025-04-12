FROM python:3.11

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y \
    curl \
    unzip \
    vim \
    build-essential \
    libpq-dev \
    gdal-bin \
    postgresql-client \
    # Install Node.js 18.x (LTS version)
    && curl -sL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

RUN npm install -g mapshaper

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip && pip install -r requirements.txt

CMD ["python", "-m", "app.main"]
