"""
The first function of this file takes the playlist ID as an argument, and returns the song ID.

The second function takes the song ID and gets the song features
"""

from get_spotify_creds import get_spotify_creds
import requests

test_id = "37i9dQZF1EIdChYeHNDfK5"  # delete this later.


def get_song_ids(playlist_id: str, limit: int = 10, access_token:str = None) -> list:
    """
    Returns a list of song IDs in a given playlist
    :param playlist_id (str): The playlist ID to query.
    :return: song_ids (list): list of song IDs.
    """

    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks/"
    if access_token == None:
        access_token = get_spotify_creds()
    headers = {"Authorization": "Bearer " + access_token}
    params = {"limit": limit}
    response = requests.get(url, headers=headers, params=params).json()

    song_ids = [item["track"]["id"] for item in response["items"]]

    return song_ids


def get_track_info(song_id: str, access_token:str = None):
    song_url = f"https://api.spotify.com/v1/tracks/{song_id}"
    if access_token == None:
        access_token = get_spotify_creds()
    headers = {"Authorization": "Bearer " + access_token}
    response = requests.get(song_url, headers=headers).json()

    if "name" in response:
        # sometimes spotify sends an incomplete json file causing issues when info doesnt exist
        track_name = response["name"]
        artist_name = response["artists"][0]["name"]
        album_name = response["album"]["name"]
        track_popularity = response["popularity"]

        song_feat_url = f"https://api.spotify.com/v1/audio-features/{song_id}"
        response = requests.get(song_feat_url, headers=headers).json()
        danceability = response["danceability"]
        energy = response["energy"]
        key = response["key"]
        loudness = response["loudness"]
        mode = response["mode"]
        speechiness = response["speechiness"]
        acousticness = response["acousticness"]
        instrumentalness = response["instrumentalness"]
        liveness = response["liveness"]
        valence = response["valence"]
        tempo = response["tempo"]
        duration = response["duration_ms"]
        time_signature = response["time_signature"]
        return [
            track_name,
            artist_name,
            album_name,
            track_popularity,
            danceability,
            energy,
            key,
            loudness,
            mode,
            speechiness,
            acousticness,
            instrumentalness,
            liveness,
            valence,
            duration,
            tempo,
            time_signature,
        ]
    else:
        return None


if __name__ == "__main__":
    song_ids = get_song_ids(test_id, limit=50)
    for id in song_ids:
        print(get_track_info(id)[0])
