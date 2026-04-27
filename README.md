# Weather API with built with FastApi and Redis

This is a REST API that fetches the weather data for a iven lcoation using Visual Crossing Weather API, and caches data using Redis

## 🌟 Features
- **Real-time Weather Data**: Fetches current weather conditions from Visual Crossing Weather API
- **Redis Caching**: Caches weather data for 30 minutes
- **Fast Response Times**: Sub-millisecond responses for cached data
- **Error Handling**: Easy to read Fallback mechanism if Redis fails
- **RESTful Design**: Clean and intuitive API endpoints

## 🚀 Tech Stack

- **FastAPI**: for building the api 
- **Redis**: for caching
- **Pyth on 3.14**: main language
- **Visual Crossing Weather API**: weather data provider

## ⚙️ Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/weather-api.git
cd weather-api
```

2. **Create and activate virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install fastapi uvicorn redis python-dotenv requests
```

4. **Set up environment variables**

Create a `.env` file in the root directory:
```env
WEATHER_API_KEY=your_visual_crossing_api_key
REDIS_URL=redis://:your_password@localhost:6379
```

5. **Start Redis server**
```bash
redis-server
```

## 🔥 Running the Application

**Development mode:**
```bash
fastapi dev
```

**Production mode:**
```bash
uvicorn api:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://127.0.0.1:8000`

### Get Weather Data

```http
GET /weather/{location}
```

**Parameters:**
- `location` (path parameter): City name or location (e.g., "Mumbai", "New York", "London")

**Example Request:**
```bash
curl http://127.0.0.1:8000/weather/Mumbai
```

**Example Response:**
```json
{
  "location": "Mumbai, Maharashtra, India",
  "temperature": "31.6°C",
  "conditions": "Partially cloudy",
  "humidity": "69.6%",
  "wind_speed": "14.8 km/h",
  "feels_like": "39.0°C"
}
```

## 📊 Performance

- **Cache HIT**: ~3ms response time
- **Cache MISS**: ~500ms response time (includes external API call)
- **Cache Duration**: 30 minutes (1800 seconds)

### ⭐️ Project Reference URL
https://roadmap.sh/projects/weather-api-wrapper-service