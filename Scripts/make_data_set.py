from get_song_info import get_song_ids, get_track_info
from playlist_miner import search_for_playlist

def build_data_set(q:str, playlist_limit:int):
    """
    This file runs all necessary functions to build the dataset
    :param q:
    :param playlist_limit:
    :return:
    """

    playlists = search_for_playlist(q, number=playlist_limit)

    for playlist in playlists:
        playlist_id = playlist[0]
        song_ids = get_song_ids(playlist_id)
        for song_id in song_ids:
            track_info = get_track_info(song_id)
            print(track_info)
            break


if __name__ == '__main__':
    build_data_set('sad', 50)