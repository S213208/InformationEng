import requests
import json
import mysql.connector
from datetime import datetime, timedelta

#Call Open-Meteo Archive API
def fetch_weather_data():
    url = "https://archive-api.open-meteo.com/v1/archive?latitude=52.1872&longitude=0.9708&start_date=2011-01-01&end_date=2021-12-31&daily=temperature_2m_mean,precipitation_sum,rain_sum,snowfall_sum&timezone=Europe%2FLondon"
    response = requests.get(url)
    weather_data = response.json()
    return weather_data

#Process JSON data
def process_weather_data(weather_data):
    daily_data = weather_data['daily']
    daily_keys = ['temperature_2m_mean', 'precipitation_sum', 'rain_sum', 'snowfall_sum']
    date_list = daily_data['time']
    
    monthly_data = {}
    
    for i, date_str in enumerate(date_list):
        date = datetime.strptime(date_str, "%Y-%m-%d")
        year_month = (date.year, date.month)
        
        if year_month not in monthly_data:
            monthly_data[year_month] = {
                'temperature_sum': 0,
                'temperature_count': 0,
                'precipitation_sum': 0,
                'rain_sum': 0,
                'snowfall_sum': 0
            }
        
        for key in daily_keys:
            value = daily_data[key][i]
            
            if key == 'temperature_2m_mean':
                monthly_data[year_month]['temperature_sum'] += value
                monthly_data[year_month]['temperature_count'] += 1
            else:
                monthly_data[year_month][key] += value
    
    for year_month, data in monthly_data.items():
        data['temperature_avg'] = data['temperature_sum'] / data['temperature_count']
        del data['temperature_sum']
        del data['temperature_count']
    
    return monthly_data
def insert_weather_data_to_database(monthly_data):
    connection = mysql.connector.connect(
        user='root',
        password='Beenandgone1$',
        host='127.0.0.1',
        database='planningautomation',
        auth_plugin='mysql_native_password')

    cursor = connection.cursor()
    
    # Check if the table exists
    check_table_query = """
    SELECT COUNT(*)
    FROM INFORMATION_SCHEMA.TABLES
    WHERE TABLE_SCHEMA = 'traffic' AND TABLE_NAME = 'weather';
    """
    cursor.execute(check_table_query)
    table_exists = cursor.fetchone()[0] > 0

    # Drop the table if it exists
    if table_exists:
        drop_table_query = """DROP TABLE traffic.weather;"""
        cursor.execute(drop_table_query)

    # Create the table
    create_table_query = """
    CREATE TABLE traffic.weather (
        id INT AUTO_INCREMENT PRIMARY KEY,
        year INT,
        month INT,
        temperature_avg DECIMAL(5, 2),
        precipitation_sum DECIMAL(5, 2),
        rain_sum DECIMAL(5, 2),
        snowfall_sum DECIMAL(5, 2)
    );
    """
    cursor.execute(create_table_query)

    # Insert data into the table
    insert_query = """INSERT INTO traffic.weather (year, month, temperature_avg, precipitation_sum, rain_sum, snowfall_sum)
                      VALUES (%s, %s, %s, %s, %s, %s)"""

    for year_month, data in monthly_data.items():
        year, month = year_month
        values = (year, month, data['temperature_avg'], data['precipitation_sum'], data['rain_sum'], data['snowfall_sum'])
        cursor.execute(insert_query, values)

    connection.commit()
    cursor.close()
    connection.close()

weather_data = fetch_weather_data()
monthly_data = process_weather_data(weather_data)
insert_weather_data_to_database(monthly_data)