Sure! Here's a clean and professional `README.md` snippet for your project:

---

# TSG Geo Analytics

This project provides tools for analyzing geospatial data using a PostgreSQL backend with PostGIS support. Below are the steps to build and run the application.

---

## 🚀 Getting Started

### 1. Build Docker Image

To build the Docker image for the application, run the following command in the root directory:

```bash
docker build --no-cache -t tsg_geo_analytics .
```

This will create a fresh image of the `tsg_geo_analytics` container without using cached layers.

---

### 2. Load Data into PostgreSQL

After the containers are up and running via `docker-compose`, you can load the required data into the PostgreSQL database by executing:

```bash
docker-compose exec tsg_backend python -m app.scripts.load_data
```

This command runs the data loading script inside the backend container.

---
