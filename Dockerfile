FROM python:3.11

RUN apt-get update && apt-get install -y git

WORKDIR /app

RUN git clone https://github.com/ShivaKumarSanapala/tsg_geo_analytics.git .

RUN pip install -r requirements.txt

CMD ["python", "-m", "app.main"]
