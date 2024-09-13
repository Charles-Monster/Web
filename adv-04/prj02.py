import json
import requests

json_str = json.dumps(data)

json_data = json.loads(json_str)
########################定義函數########################
API_KEY = "XXX"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
UNITS = "metric"
LANG = "zh_tw"
