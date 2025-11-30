# logika rekomendacji
import gui
from recommender import recommend_tracks_by_genre
from gui import root
root.mainloop()


if __name__ == "__main__":
    recs = recommend_tracks_by_genre()
    print("\n🎧 Rekomendowane utwory:\n")
    for idx, track in enumerate(recs):
        print(f"{idx+1}. {track['name']} — {track['artists'][0]['name']}")
