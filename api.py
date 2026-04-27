from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import os
import redis
import json
import requests

# fastAPI instance
app = FastAPI()

# Load env variables
load_dotenv()
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
REDIS_URL = os.getenv("REDIS_URL")
BASE_URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"

# cache
redis_client = redis.from_url(REDIS_URL, decode_responses=True)

# base route
# Fetch data from the visual weather api
async def getWeather(city: str):
  # create cache key
  cache_key = f'weather:{city.lower()}'

  try:
    # check the cached data
    cached = redis_client.get(cache_key)
    if cached:
      print(f"✓ Cache HIT for {city}")
      return json.loads(cached)
    
    print(f"✗ Cache MISS for {city} - Fetching from API")

    # if not in cache then call the visual weather api
    url = f'{BASE_URL}/{city}'

    params = {
      "key": WEATHER_API_KEY,
      "unitGroup": "metric",
      "include": "current"
    }

    # request 
    response = requests.get(url, params=params)
    # check the http response port
    response.raise_for_status()

    data = response.json()
    current = data['currentConditions']

    result = {
      "location": data["resolvedAddress"],
      "temperature": f"{current['temp']}°C",
      "conditions": current["conditions"],
      "humidity": f"{current['humidity']}%",
      "wind_speed": f"{current['windspeed']} km/h",
      "feels_like": f"{current['feelslike']}°C"
    }

    # Store the response in redis cache for 30 mins
    redis_client.setex(
      cache_key,
      1800,
      json.dumps(result)
    )

    return result
  
  # api call error handling
  except requests.exceptions.RequestException as e:
    raise HTTPException(status_code=500, detail=f"Error fetching weather: {str(e)}")
  
  # redis cache error handling
  except redis.RedisError as e:
    # still try to fetch from visual weather api
    print(f"Redis error: {e}")

    url = f"{BASE_URL}/{city}"

    params = {
      "key": WEATHER_API_KEY,
      "unitGroup": "metric",
      "include": "current"
    }

    response = requests.get(url, params=params)
    data = response.json()

    current = data['currentConditions']

    return {
      "location": data["resolvedAddress"],
      "temperature": f"{current['temp']}°C",
      "conditions": current["conditions"],
      "humidity": f"{current['humidity']}%",
      "wind_speed": f"{current['windspeed']} km/h",
      "feels_like": f"{current['feelslike']}°C"
    }
  
# Routes 
@app.get("/")
async def root():
  return {"message": "Weather api with redis is running"}

@app.get("/weather/{city}")
async def weather_endpoint(city: str):
  return await getWeather(city)