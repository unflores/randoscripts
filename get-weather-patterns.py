import requests
import json

# from types import SimpleNamespace
import csv


appid = "5796abbde9106b7da4febfae8c44c232"


def load_cities():
    with open("./cities", "r") as file:
        lines = file.readlines()
        cities = [line.strip() for line in lines]

    return cities


def fetch_weather_data(cities):
    weather_data = []
    for city in cities:
        response = requests.get(
            f"https://api.openweathermap.org/data/2.5/find?q={city}&appid={appid}&units=metric",
            headers={"Content-Type": "application/json"},
        )

        if response.status_code != 200:
            print("failure:")
            print(f"Could not find resuts for: {city}")
            print(response.text)

        raw_data = json.loads(response.text)
        open_weather = raw_data["list"][0]

        weather = {
            "open_weather_id": open_weather["id"],
            "name": city,
            "timestamp": open_weather["dt"],
            "descriptions": open_weather["weather"],
            "lat": open_weather["coord"]["lat"],
            "lon": open_weather["coord"]["lon"],
            "accuracy": raw_data["message"],
        }

        weather_data.append(weather)
    return weather_data


def create_weather_csv(weather_data):
    columns = [["Id", "Name", "Description", "Lat", "Lon"]]
    with open("output.csv", "w", newline="") as file:
        writer = csv.writer(file)
        rows = [
            [
                weather["open_weather_id"],
                weather["name"],
                weather["descriptions"][0]["description"],
                weather["lat"],
                weather["lon"],
            ]
            for weather in weather_data
        ]
        writer.writerows(columns)
        writer.writerows(rows)


if __name__ == "__main__":
    cities = load_cities()
    weather_data = fetch_weather_data(cities)
    create_weather_csv(weather_data)

    print("definitely all done.")
