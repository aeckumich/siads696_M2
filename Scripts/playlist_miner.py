"""
This script takes goes through a list of known spotify playlists, and creates a
CSV file with track id, playlist id, and playlist name
"""

from get_spotify_creds import get_spotify_creds
import requests


def search_for_playlist(q: str, number: int = 10) -> list:
    """
    This function uses a query string to search Spotify's APIs
    for playlists that match and returns a list of playlist information.
    :param q: The query string.
    :param number: The maximum number of results to return.
    :return playlists: A list of playlist information in a tuple (playlist id, playlist name,
    playlist description).
    """

    access_token = get_spotify_creds()
    headers = {"Authorization": "Bearer " + access_token}

    url = "https://api.spotify.com/v1/search/"
    params = {"q": q, "limit": number, "type": "playlist"}

    response = requests.get(url, params=params, headers=headers)

    if response.status_code != 200:
        raise ValueError(
            "Something went wrong with the API request. Status code: "
            + str(response.status_code)
        )

    response = response.json()
    playlists = []
    for playlist in response["playlists"]["items"]:
        description = playlist["description"]
        id = playlist["id"]
        name = playlist["name"]

        playlists.append((id, name, description,))

    return playlists


if "__main__" == __name__:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--query", "-q", help="The query string", type=str)
    parser.add_argument("--number", "-n", help="number of results to return", type=int)
    args = parser.parse_args()
    playlists = search_for_playlist(args.query, args.number)

    for playlist in playlists:
        print(playlist)
