import os
import json
import base64
import requests
from ytmusicapi import YTMusic

from urllib import parse
from dotenv import load_dotenv
load_dotenv()


# ~
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")


try:
  ytmusic = YTMusic()
except:
  print("Check your internet connection...")
  pass

class Yutify:

  def __init__(self) -> None:
    
    self.all_spotify = {}


  # Put everything together to get Spotify music URL
  def get_music_url(self, yt_url: str):

    if not yt_url.startswith('http'):
      return {'error': 'Please enter a valid YouTube™ music video URL.'}

    else:
      music_info = self.get_music_info(yt_url)
      try:
        artist_name = music_info["artist"]
        song_name = music_info["song_name"]
      except KeyError:
        return music_info #error

      token = self.get_spotify_token()
      result = self.search_music(token, artist_name, song_name)

      return result

  # Get artist & song name from YouTube URL
  def get_music_info(self, yt_url):

    # Check for two possible youtube urls:
    # one with query at the end,
    # second that 'youtu.be/' one 😑
    # Grab da youtube video ID
    try:
      yt_url_parsed = parse.urlparse(yt_url)
      yt_id = parse.parse_qs(yt_url_parsed.query)['v'][0]
    except KeyError:
      yt_url_parsed = parse.urlparse(yt_url)
      yt_id = (yt_url_parsed.path).replace('/', '')

    try:
      video = ytmusic.get_song(yt_id)
      artist = video['videoDetails']['author']
      song_name = video['videoDetails']['title']
    
    except Exception:
      return {'error': "Couldn't get any music information. Is it really music?"}

    if song_name is not None and artist is not None:
      all_music_info = {
        'artist': artist,
        'song_name': song_name
      }

      return all_music_info
    
    else:
      return {'error': "Couldn't get any music information. Is it really music?"}


  # Request Spotify access token
  def get_spotify_token(self):
    # Basically combine clientid:clientsecret
    # and convert it into base64 string
    # Check Spotify documentaion
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = 'https://accounts.spotify.com/api/token'
    headers = {
      'Authorization': 'Basic ' + auth_base64,
      'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {'grant_type': 'client_credentials'}
    result = requests.post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result['access_token']

    return token


  # Header for sending request using access token.
  # Will be used in every future requests made to api.
  def get_auth_header(self, token):
    return {'Authorization': 'Bearer ' + token}


  # Search for music with artist name
  def search_music(self, token, artist_name, song_name, type = 'track'): # Default search type/filter 'track'. Can be 'album'...

    try:

      url = f"https://api.spotify.com/v1/search"
      headers = self.get_auth_header(token)
      # NOTE: search limit is set to 1. We are getting only 1 result
      query = f"?q={artist_name}%20-%20{song_name}&type={type}&limit=1"
      query_url = url + query

      response = requests.get(query_url, headers=headers)
      if not response.status_code == 200:
        return {'error': 'Unable to fetch data from Spotify.'}
      response_json = json.loads((response.content))['tracks']['items'][0]

      # Since the search limit is 1, 
      # if the song title/name doesn't match with
      # the one we got from youtube music, return error
      if not response_json['name'] == song_name:
        return {'error': "Couldn't find exact matches for it. Please try Official Audio link."}

      else:
        title = response_json['name']
        artists_json = response_json['artists']
        artists = []
        # There can be more than one artist in a song
        # Go through every artist and add their name into 'Artists'
        for artist in artists_json:
          artist = artist['name']
          artists.append(artist)
        artists = ', '.join(artists)
        album_art = response_json['album']['images'][0]['url']
        spotify_url = response_json['external_urls']['spotify']
        embed = self.get_spotify_embed(spotify_url)

        # Save useful information, so that we can use it when needed
        self.all_spotify = {
          'title': title,
          'artists': artists,
          'album_art': album_art,
          'url': spotify_url,
          'embed': embed
        }

        return self.all_spotify

    except Exception:
      return {'error': "Looks like this song isn't available on Spotify... :( \nMaybe try again?"}


  # Get Spotify Embed using oEmbed API
  def get_spotify_embed(self, spotify_url):

    url = f"https://open.spotify.com/oembed"
    query = f"?url={spotify_url}"
    query_url = url + query

    response = requests.get(query_url)
    if not response.status_code == 200:
      return {'error': 'Unable to fetch data from Spotify.'}

    response_json = json.loads((response.content))
    # Just replacing the `height` value of `iframe` here
    # Yes 🙂
    embed = response_json['html'].replace('height="152"', 'height="352"')
    
    return embed


if __name__ == '__main__':

  pass
