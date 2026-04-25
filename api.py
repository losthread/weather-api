from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import requests
import os

# Load env varibles
load_dotenv()
API_KEY = os.getenv("WEATHER_API_KEY")
BASE_URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"

print(f"API_KEY loaded: {API_KEY}")
print(f"API_KEY is None: {API_KEY is None}")
print(f"API_KEY length: {len(API_KEY) if API_KEY else 0}")

# fastapi instance
app = FastAPI()

# fetch data from visual crossing weather api
async def getWeather(location: str): #type hints
  try:
    # final url
    url = f"{BASE_URL}/{location}"

    # parameters for the API request
    params = {
      "key": API_KEY,
      "unitGroup": "metric",
      "include": "current"
    }

    # request
    response = requests.get(url, params=params)
    response.raise_for_status()

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
  
  except requests.exceptions.RequestException as e:
    raise HTTPException(status_code=500, detail=f"Error fetching weather: {str(e)}")

# http methods
# POST: create data
# GET: read data
# PUT: update data
# DELETE: delete data

# Routes
@app.get("/")
async def root():
  return {"message": "Weather API is running"}

@app.get("/weather/{location}")
async def weather_endpoint(location: str):
  return await getWeather(location)