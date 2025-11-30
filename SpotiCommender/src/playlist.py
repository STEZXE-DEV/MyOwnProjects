from auth import get_spotify_client
from recommender import recommend_tracks_by_genre

sp = get_spotify_client()

def create_playlist(name="Rekomendacje wg gatunku"):
    user_id = sp.current_user()["id"]
    playlist = sp.user_playlist_create(user=user_id, name=name, public=True)
    return playlist["id"]

def add_tracks_to_playlist(playlist_id, tracks):
    # Spotify akceptuje URI
    track_uris = [track["uri"] for track in tracks]
    # Dodawanie po 100 (limit API)
    for i in range(0, len(track_uris), 100):
        sp.playlist_add_items(playlist_id, track_uris[i:i+100])

if __name__ == "__main__":
    tracks = recommend_tracks_by_genre()
    playlist_id = create_playlist("Moje rekomendacje Spotify")
    add_tracks_to_playlist(playlist_id, tracks)
    print(f"Stworzono playlistę z {len(tracks)} utworami!")
