from get_song_info import get_song_ids, get_track_info
from playlist_miner import search_for_playlist
from get_spotify_creds import get_spotify_creds
import csv
from time import sleep
class API_Counter:
    def __init__(self, limit:int = 70):
        self.count = 0
        self.limit = limit

    def increment(self):
        self.count += 1
        if self.count == self.limit:
            print("API limit reached. Pausing...")
            sleep(30)
            self.count = 0



def build_data_playlist(q: list, playlist_limit: int, access_token:str, fname:str = "test.csv"):
    """
    This file runs all necessary functions to build the dataset
    :param q:
    :param playlist_limit:
    :return:
    """

    manager = API_Counter()

    header = ["track_name", "artist_name", "album_name", "track_popularity", "danceability", "energy", "key", "loudness",
            "mode", "speechiness", "acousticness", "instrumentalness", "liveness", "valence", "duration", "tempo", "time_signature",
              "playlist_id", "playlist_name", "playlist_description"]

    with open(fname, "w") as f:
        writer = csv.writer(f, delimiter=",", quoting=csv.QUOTE_MINIMAL)
        writer.writerow(header)

        for playlist_search in q:
            print(f"Searching for playlists. Query term: {playlist_search}")
            manager.increment()
            playlists = search_for_playlist(playlist_search, number=playlist_limit, access_token=access_token)

            for playlist in playlists:
                playlist_id = playlist[0]
                playlist_name = playlist[1]
                playlist_description = playlist[2]
                print(f"\tGetting songs for playist {playlist_name}")

                ### limit to the API cannot exceed 50. If playlist longer than 50 currently tosses error
                ### will implement better fix in the future.
                if playlist[-1] > 50:
                    limit = 50
                else:
                    limit = playlist[-1]
                song_ids = get_song_ids(playlist_id, limit=limit, access_token=access_token)
                manager.increment()
                for song_id in song_ids:
                    manager.increment()
                    track_info = get_track_info(song_id, access_token=access_token)
                    if track_info == None:
                        continue
                    track_info.append(playlist_id)
                    track_info.append(playlist_name)
                    track_info.append(playlist_description)
                    writer.writerow(track_info)
                    print(f"\t\tSuccessfully retrieved track info for {track_info[0]} by {track_info[1]}")



if __name__ == "__main__":
    build_data_playlist(["sad", "happy", "hungry"],20, fname="../Data/sample_data.csv")
