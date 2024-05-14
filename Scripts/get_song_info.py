"""
The first function of this file takes the playlist ID as an argument, and returns the song ID.

The second function takes the song ID and gets the song features
"""

from get_spotify_creds import get_spotify_creds
import requests

test_id = '37i9dQZF1EIdChYeHNDfK5' #delete this later.
def get_song_ids(playlist_id:str, limit:int = 10) -> list:
    """
    Returns a list of song IDs in a given playlist
    :param playlist_id (str): The playlist ID to query.
    :return: song_ids (list): list of song IDs.
    """

    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks/"
    access_token = get_spotify_creds()
    headers = {"Authorization": "Bearer " + access_token}
    params = {"limit" : limit}
    response = requests.get(url, headers=headers, params=params).json()

    song_ids = [item["track"]["id"] for item in response["items"]]

    return song_ids

def get_track_info(song_id:str):
    url = f"https://api.spotify.com/v1/tracks/{song_id}"
    access_token = get_spotify_creds()
    headers = {"Authorization": "Bearer " + access_token}
    response = requests.get(url, headers=headers).json()

    print(response)
    track_name = response["name"]
    artist_name = response["artists"][0]["name"]
    album_name = response["album"]["name"]
    track_popularity = response["popularity"]

    """
    I'll finish this up tomorrow, but this looks like the info we can get from the track end point. 
    There's more relevant information in audio features endpoint. 
    """"# print(track_name, artist_name, album_name)






if __name__ == '__main__':
    song_ids = get_song_ids(test_id, limit=50)
    get_track_info(song_ids[6])





