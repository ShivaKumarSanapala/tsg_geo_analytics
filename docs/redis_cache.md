We can identify the caching implementation is centered around **Redis** and is initialized and used primarily in `app/services/cache.py`. Here's a detailed analysis of all aspects:

---

### ✅ **1. Redis Initialization**

#### 📄 `app/services/cache.py`
```python
redis_client = None

def init_redis(app):
    global redis_client
    redis_client = redis.Redis(
        host=app.config.get("REDIS_HOST", "localhost"),
        port=app.config.get("REDIS_PORT", 6379),
        db=0,
        decode_responses=True
    )
    redis_client.ping()
```
- **What it does**: Initializes a global Redis client using Flask `app.config`.
- `decode_responses=True`: Ensures that Redis responses are strings (not bytes).
- `ping()`: Validates the connection.

🧠 **Note**: If `init_redis` is not called during Flask app startup, Redis won’t work properly.

---

### ✅ **2. Geo-based Caching – Cities**

#### 📄 `cache.load_cities_to_redis_from_db()`
```python
pipe.geoadd("cities:geo", (lon, lat, city.geoidfq))
```
- **Purpose**: Load all cities into a Redis **GEO index** named `cities:geo`.
- **Usage**: Enables fast spatial queries using `geosearch`.

---

### ✅ **3. Key Naming Conventions**

The following **Redis keys** are used:

| Redis Key | Purpose |
|----------|--------|
| `cities:geo` | Redis GEO index to search nearby cities |
| `city:data:<geoidfq>` | Stores city details like name, lat/lng, and GeoJSON |
| `geojson:state:<geoidfq>` | Caches GeoJSON of a state geometry |
| `geojson:county:<geoidfq>` | Caches GeoJSON of a county geometry |
| `search:states:<query>` / `search:counties:<query>` | Caches search results for state or county by name or geoid |

All keys are cached using:
```python
redis_client.set(...) or redis_client.setex(...)
```

---

### ✅ **4. Cache Usage in `geospatial.py`**

#### 🔍 `search_boundaries_service`
```python
cache_key = f"search:{boundary_type}:{query}"
cached_results = redis_client.get(cache_key)
redis_client.setex(cache_key, 3600, json.dumps(data))
```
- **Checks cache** before querying DB.
- **Sets cache** after DB lookup (TTL = 60 mins).

#### 📍 `get_nearby_cities_from_redis`
- Uses:
  - `redis_client.geosearch(...)` to find nearby cities.
  - For each city ID found:
    - Try to get from cache: `redis_client.get(city_data_key(cid))`
    - If not present, fetch from DB and **set** in Redis:
      ```python
      redis_client.set(f"city:data:{city.geoidfq}", json.dumps(city_data))
      ```

#### 📊 `fetch_demographics`
```python
state_geo_key = f"geojson:state:{state_obj.geoidfq}`
state_geojson = redis_client.get(state_geo_key)
redis_client.set(state_geo_key, json.dumps(state_geojson))
```
- **Cache geometry** of state and county if not already cached.

---

### ✅ **5. Redis-Backed Geo Queries**

Redis’ **GEO commands** are used with:
```python
redis_client.geosearch(
    cities_geo_index(),
    longitude=lng,
    latitude=lat,
    radius=radius,
    unit='m',
    withdist=True,
    sort='ASC'
)
```
- Fast spatial querying by lat/lng.
- This only gives `geoidfq`, rest of the city details are fetched from:
  - Redis: if already cached
  - DB: otherwise, then added to Redis

---

### ✅ **6. No Cache Invalidation Logic Found**

As of now:
- No usage of `redis_client.delete(...)`
- No TTL on most `set(...)` operations except:
  - `search_boundaries_service` → TTL = 3600
- This may cause **stale data** over time if DB updates and Redis doesn’t.

---

### ✅ **7. Utility Functions for Key Management**
In `cache.py`:
```python
def city_data_key(geoidfq): return f"city:data:{geoidfq}"
def geojson_state_key(geoidfq): return f"geojson:state:{geoidfq}"
def geojson_county_key(geoidfq): return f"geojson:county:{geoidfq}"
```
- Promotes consistent key naming.
- Easier to change Redis schema later.

---
