# interfejs CLI

from fetch import get_top_artists, get_user_top_genres, search_artists_by_genre, get_top_tracks

def recommend_tracks_by_genre(limit_artists_per_genre=3, limit_tracks_per_artist=3):
    recommendations = []
    genres = get_user_top_genres(limit=5)

    for genre in genres:
        artists = search_artists_by_genre(genre, limit=limit_artists_per_genre)
        for artist in artists:
            tracks = get_top_tracks(artist["id"], limit=limit_tracks_per_artist)
            if tracks:
                recommendations.extend(tracks)
    return recommendations

from fetch import search_artists_by_genre, get_top_tracks

def recommend_tracks_by_genres(genres, limit_artists_per_genre=3, limit_tracks_per_artist=3):
    recommendations = []

    for genre in genres:
        genre = genre.strip()
        if not genre:
            continue
        artists = search_artists_by_genre(genre, limit=limit_artists_per_genre)
        for artist in artists:
            tracks = get_top_tracks(artist["id"], limit=limit_tracks_per_artist)
            if tracks:
                recommendations.extend(tracks)
    return recommendations
