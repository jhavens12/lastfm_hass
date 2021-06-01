import credentials
import requests
import pprint
import json


last_fm_key = credentials.key
last_fm_secret = credentials.secret
last_fm_user = credentials.user


dates = ["7day"]


def post_sensor(sensor,data):
    headers = {"Authorization": "Bearer "+credentials.api_token,
               'content-type': 'application/json'}

    url = credentials.api_url+"/api/states/"+sensor
    #data = '{"state": "1", "attributes": {"unit_of_measurement": "Miles"}}'
    response = requests.post(url, headers=headers, data=data)
    print("Posting Sensor: ",sensor)
    #print(response.text)

def get_lastfm_tracks(input_period):

    url = "http://ws.audioscrobbler.com/2.0/?method=user.gettoptracks&user="+last_fm_user+"&api_key="+last_fm_key+"&limit=3&period="+input_period+"&format=json"
    dataset = requests.get(url).json()
    sensor = {}
    sensor['attributes'] = {}
    for n,i in enumerate(dataset['toptracks']['track']):
        s = n+1
        if s == 1:
            sensor['state'] = i['artist']['name']+" - "+i['name']
        sensor['attributes'][s] = i['artist']['name']+" - "+i['name']+" - Plays: "+i['playcount']
    post_sensor("sensor.lastfm_top_tracks",json.dumps(sensor))

def get_lastfm_artists(input_period):

    url = "http://ws.audioscrobbler.com/2.0/?method=user.gettopartists&user="+last_fm_user+"&api_key="+last_fm_key+"&limit=3&period="+input_period+"&format=json"
    dataset = requests.get(url).json()
    sensor = {}
    sensor['attributes'] = {}
    for n,i in enumerate(dataset['topartists']['artist']):
        s = n+1
        if s == 1:
            sensor['state'] = i['name']
        sensor['attributes'][s] = i['name']+" - Plays: "+i['playcount']
    post_sensor("sensor.lastfm_top_artists",json.dumps(sensor))

def get_lastfm_playcount():

    url = "http://ws.audioscrobbler.com/2.0/?method=user.getinfo&user="+last_fm_user+"&api_key="+last_fm_key+"&format=json"
    dataset = requests.get(url).json()

    sensor = {}
    sensor['state'] = dataset['user']['playcount']

    post_sensor("sensor.lastfm_playcount",json.dumps(sensor))

get_lastfm_playcount()
get_lastfm_artists('7day')
get_lastfm_tracks('7day')
