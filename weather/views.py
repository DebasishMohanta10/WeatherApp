from django.shortcuts import render
import requests
import json
import datetime 

def get_ip_geolocation_data(ip_address):
    response = requests.get("https://ipgeolocation.abstractapi.com/v1/?api_key=c0d666385dc942f9b47b9e7c15037db7")
    response = json.loads(response.content)
    return response["city"]

def get_temp(city):
    units = 'metric'
    api_key = "7cb0ac52bc6ad17736c2e67cbe8e9178"
    response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units={units}")
    content = json.loads(response.text)
    return content

def home(request):
    if request.method == 'GET':
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        
        city = get_ip_geolocation_data(ip)
        temp_data = get_temp(city)
        description = temp_data['weather'][0]['description']
        icon = temp_data['weather'][0]['icon']
        temp = temp_data['main']['temp']
        humidity = temp_data['main']['humidity']
        wind = temp_data['wind']['speed']
        country =temp_data['sys']['country']
        sunrise =datetime.datetime.fromtimestamp(temp_data['sys']['sunrise'])
        context = {
            'city': city,
            'temp': temp,
            'humidity': humidity,
            'icon': icon,
            'wind': wind,
            'description': description,
            'country': country,
            'sunrise': sunrise
        }
        return render(request,'home.html',context)
    if request.method == 'POST':
        city = request.POST['location']
        temp_data = get_temp(city)
        if temp_data['cod'] == '404':
            return render(request,'home.html',{ "message": temp_data['message']})
        else:
            description = temp_data['weather'][0]['description']
            icon = temp_data['weather'][0]['icon']
            temp = temp_data['main']['temp']
            humidity = temp_data['main']['humidity']
            wind = temp_data['wind']['speed']
            country =temp_data['sys']['country']
            sunrise =datetime.datetime.fromtimestamp(temp_data['sys']['sunrise'])
            context = {
                'city': city,
                'temp': temp,
                'humidity': humidity,
                'icon': icon,
                'wind': wind,
                'description': description,
                'country': country,
                'sunrise': sunrise
            }
            return render(request,'home.html',context)
