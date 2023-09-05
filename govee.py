import requests
import json

def control_govee_lights(command):

    device_control_url = "https://developer-api.govee.com/v1/devices/control"

    with open("secrets.json", "r") as secrets_file:
        secrets = json.load(secrets_file)
        api_key = secrets["govee_api_key"]
        model = secrets["Model"]
        address = secrets["Address"]

    headers = {
        "Govee-API-Key": api_key,
        "Content-Type": "application/json"
}

    control_data = {
        "device": address,
        "model": model,
        "cmd": {
            "name": command["name"],
            "value": command["value"]
        }
    }

    response = requests.put(device_control_url, headers=headers,json=control_data)


    if response.status_code == 200:
        data = response.json()
        print(f"worked: {data}")
    else:
        print("didnt work")


#get status of lights
#do it based on webcam skin colour 
#do it based on whether or not someone is stranger or not (turn red if stranger, green if me) w reference photo