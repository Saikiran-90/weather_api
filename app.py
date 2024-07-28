from flask import *
import requests
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')


@app.route('/coord',methods=('GET','POST'))
def get_coordinates():
    city = request.form.get('city')
    state = request.form.get('state')
    api_url = f'https://api.api-ninjas.com/v1/geocoding?city={city}'.format(city)
    response = requests.get(api_url,city, headers={'X-Api-Key': 'z3lgTXsvQ7831J0LoPF8cA==L5qf0thbjctcd6qU'})

   
    if response.status_code == requests.codes.ok:
        # print(response.json())
        data = json.loads(response.text)
        lat_long = []
        print(data)
        for key in data:
            if key['state'] == state:
                lat_long.append(key['latitude'])
                lat_long.append(key['longitude'])

        print(lat_long)
        cond = get_weather(lat_long[0],lat_long[1])
        print(cond)
        print(cond['location']['name'])
        print(cond['current']['condition']['text'])
        
        print(cond['current']['temp_c'])
        
        weather_loc = cond['location']['name']
        region = cond['location']['region']
        weather_cond = cond['current']['condition']['text']
        if weather_cond == "Overcast":
            weather_cond = "Cloudy"
        temp = cond['current']['temp_c']
        return render_template('home.html',weather_loc=weather_loc,weather_cond=weather_cond,temp=temp,region=region)
    else:
       return "Error:", response.status_code, response.text  


def get_weather(latitude,longitude):
    url = "https://weatherapi-com.p.rapidapi.com/current.json"
    querystring = {"q":f'{latitude},{longitude}'}
    headers = {
	"x-rapidapi-key": "26249fb5d7msh57789b9215eeee8p13b633jsn08b8d4bedb29",
	"x-rapidapi-host": "weatherapi-com.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    # print(response.json())
    # print(response.json()['current']['temp_c'])
    # print(response.json()['location']['name']) 
    return response.json()



if __name__ == '__main__':
    app.run(debug=True)