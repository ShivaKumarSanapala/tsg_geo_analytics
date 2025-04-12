---

# 🗺️ TSG Geo Analytics

**TSG Geo Analytics** is a full-stack platform for geospatial data analytics and visualization. It combines a modern React frontend, a Flask-based Python backend, and a PostgreSQL/PostGIS database—fully containerized using Docker and orchestrated via Docker Compose.

---

## 🚀 Getting Started

### 🔹 1. Clone & Build the Frontend

Start by cloning the frontend repository and building its Docker image:

```bash
git clone https://github.com/ShivaKumarSanapala/geo_viz
cd geo_viz
docker build -t tsg_frontend .
```

This builds the Docker image for the React-based frontend.

---

### 🔹 2. Clone & Set Up the Backend

Navigate back and clone the backend repository:

```bash
cd ..
git clone https://github.com/ShivaKumarSanapala/tsg_geo_analytics
cd tsg_geo_analytics
```

#### 🧱 2.1 Build the Backend Docker Image

```bash
docker build --no-cache -t tsg_geo_analytics .
```

This builds the Docker image for the backend Flask service.

#### ▶️ 2.2 Start All Services Using Docker Compose

Use Docker Compose to launch the full stack—frontend, backend, and database:

```bash
docker-compose up -d
```

This spins up all services as defined in `docker-compose.yml`.

---

### 📥 3. Load Geospatial Data into the Database

Once the containers are up and running, load data into PostgreSQL/PostGIS:

```bash
docker-compose exec tsg_backend python -m app.scripts.load_data
```

This script populates the database with geospatial datasets needed for analytics and visualization.

---

## 📐 System Architecture

A high-level overview of the system components and their interactions is available here:

👉 [**View Architecture Overview**](https://github.com/ShivaKumarSanapala/tsg_geo_analytics/blob/dev/architecture.md)

---

## 🛠 Tech Stack

### ✅ Frontend – [`geo_viz`](https://github.com/ShivaKumarSanapala/geo_viz)

- **React** – For building dynamic and responsive UI.
- **Mapbox GL JS** – High-performance library for interactive maps.

### ✅ Backend – [`tsg_geo_analytics`](https://github.com/ShivaKumarSanapala/tsg_geo_analytics)

- **Flask** – Lightweight Python framework for RESTful APIs.
- **PostgreSQL + PostGIS** – Spatial database for geolocation and mapping data.
- **Docker** – Containerization of all services.
- **Docker Compose** – Service orchestration for multi-container setups.

---

## 📌 Notes

- Ensure **Docker** and **Docker Compose** are installed on your system.
- Frontend and backend containers communicate via service names defined in `docker-compose.yml`.
- For Mapbox access, set your access token in a `.env` file inside the frontend directory if required.

---
