FROM alpine/git AS cloner
WORKDIR /src
ARG CACHEBUST=1
RUN git clone https://github.com/ShivaKumarSanapala/tsg_geo_analytics.git .

FROM python:3.11
WORKDIR /app
COPY --from=cloner /src /app
RUN pip install -r requirements.txt
CMD ["python", "-m", "app.main"]
