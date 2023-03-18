from flask import Flask, render_template
import requests
import pandas as pd
import plotly.express as px
import plotly.io as pio

app = Flask(__name__)

TOMTOM_API_KEY = "H90qT99QKgD0IzIadAPC7pIYsFkhY86L"
#OPENWEATHER_API_KEY = "your_openweather_api_key"
IPSWICH_COORDS = "52.056736,1.148220"
FIELDS = """{
  incidents
    {
      type,
      geometry{
        type,coordinates
      },
      properties{
        iconCategory
      }
    }
}"""


@app.route("/")
def index():
    traffic_data = get_traffic_data()
    #weather_data = get_weather_data(traffic_data)
    #plot = create_plot(traffic_data, weather_data)

    #return render_template("index.html", plot=plot)

def get_traffic_data():
    url = f"https://api.tomtom.com/traffic/services/5/incidentDetails?key={TOMTOM_API_KEY}&bbox=1.08,52.01,1.22,52.10&fields={FIELDS}"
    #url = 'https://api.tomtom.com/traffic/services/5/incidentDetails?key={Your_Api_Key}&bbox={bbox}&fields={fields}&language={language}&t={t}&categoryFilter={categoryFilter}&timeValidityFilter={timeValidityFilter}'
    #https://{baseURL}/traffic/services/{versionNumber}/incidentDetails?key={Your_Api_Key}&ids={ids}&fields={fields}&language={language}&t={t}&categoryFilter={categoryFilter}&timeValidityFilter={timeValidityFilter}
    response = requests.get(url)
    data = response.json()
    print(data)
    return render_template('index.html')
'''
def get_weather_data(traffic_data):
    weather_data = []
    for incident in traffic_data:
        time = incident["ts"]
        url = f"https://api.openweathermap.org/data/2.5/onecall/timemachine?lat={IPSWICH_COORDS[0]}&lon={IPSWICH_COORDS[1]}&dt={time}&appid={OPENWEATHER_API_KEY}"
        response = requests.get(url)
        data = response.json()
        weather_data.append(data["current"])

    return weather_data
'''
'''
def create_plot(traffic_data, weather_data):
    df = pd.DataFrame(traffic_data)
    df_weather = pd.DataFrame(weather_data)
    df["weather"] = df_weather["weather"].apply(lambda x: x[0]["description"])
    df["temp"] = df_weather["temp"]

    fig = px.scatter(df, x="temp", y="tmc", color="weather", title="Temperature vs. Traffic Incidents in Ipswich, UK")

    return pio.to_html(fig, full_html=False)
'''

if __name__ == "__main__":
    app.run(debug=True)
