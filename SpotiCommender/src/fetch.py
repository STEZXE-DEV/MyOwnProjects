from auth import get_spotify_client

sp = get_spotify_client()

def get_top_artists(limit=10):
    results = sp.current_user_top_artists(limit=limit, time_range="medium_term")
    return results["items"]

def get_user_top_genres(limit=5):
    """Zwraca najczęściej słuchane gatunki użytkownika."""
    top_artists = sp.current_user_top_artists(limit=limit, time_range="medium_term")["items"]
    genres_count = {}
    for artist in top_artists:
        for genre in artist.get("genres", []):
            genres_count[genre] = genres_count.get(genre, 0) + 1
    sorted_genres = sorted(genres_count.items(), key=lambda x: x[1], reverse=True)
    return [g[0] for g in sorted_genres]

def search_artists_by_genre(genre, limit=5):
    results = sp.search(q=f'genre:"{genre}"', type="artist", limit=limit)
    return results["artists"]["items"]

def get_top_tracks(artist_id, limit=3):
    try:
        results = sp.artist_top_tracks(artist_id, country=None)
        return results["tracks"][:limit]
    except:
        return []
    
def search_tracks_by_genres(genres, limit_per_genre=10):
    """Szukaj utworów w Spotify po podanych gatunkach."""
    tracks = []
    for genre in genres:
        genre = genre.strip()
        if not genre:
            continue
        # wyszukaj utwory dla gatunku
        results = sp.search(q=f'genre:"{genre}"', type="track", limit=limit_per_genre)
        tracks.extend(results["tracks"]["items"])
    return tracks

