import dearpygui.dearpygui as dpg
import os, sys
from auth import get_spotify_client
from recommender import recommend_tracks_by_genres
from fetch import get_user_top_genres

sp = get_spotify_client()
current_tracks = []

dpg.create_context()

# --- Funkcje ---
def open_in_spotify(sender, app_data, user_data):
    uri = user_data
    if sys.platform.startswith('win'):
        os.startfile(uri)
    elif sys.platform.startswith('darwin'):
        os.system(f"open '{uri}'")
    else:
        os.system(f"xdg-open '{uri}'")

def create_playlist_callback():
    selected_tracks = [track['uri'] for track in current_tracks if dpg.get_value(track['checkbox'])]
    if not selected_tracks:
        dpg.set_value("msg_text", "Nie wybrano żadnych utworów!")
        dpg.show_item("msg_popup")
        return

    playlist_name = dpg.get_value("playlist_name")
    if not playlist_name:
        dpg.set_value("msg_text", "Nie podano nazwy playlisty!")
        dpg.show_item("msg_popup")
        return

    user_id = sp.current_user()["id"]
    playlist = sp.user_playlist_create(user_id, name=playlist_name, public=True)

    for i in range(0, len(selected_tracks), 100):
        sp.playlist_add_items(playlist["id"], selected_tracks[i:i+100])

    dpg.set_value("msg_text", f"Playlistę '{playlist_name}' utworzono z {len(selected_tracks)} utworami!")
    dpg.show_item("msg_popup")

def fetch_tracks_callback():
    global current_tracks
    for track in current_tracks:
        dpg.delete_item(track['row'])
    current_tracks.clear()

    genres_input = dpg.get_value("genres_input")
    genres = [g.strip() for g in genres_input.split(",") if g.strip()]

    tracks = recommend_tracks_by_genres(genres)  # nowa funkcja
    if not tracks:
        dpg.add_text("Nie znaleziono utworów dla podanych gatunków.", parent="tracks_group")
        return

    for track in tracks:
        row = dpg.add_group(horizontal=True, parent="tracks_group")
        checkbox = dpg.add_checkbox(label="", parent=row)
        dpg.add_text(f"{track['name']} — {track['artists'][0]['name']}", parent=row)
        dpg.add_button(label="▶", callback=open_in_spotify, user_data=track['uri'], parent=row)
        current_tracks.append({'uri': track['uri'], 'checkbox': checkbox, 'row': row})


# --- GUI ---
top_genres = get_user_top_genres(limit=5)
placeholder = ", ".join(top_genres)

with dpg.window(label="Spotify Recommender", width=700, height=500):
    dpg.add_text("Gatunki (oddziel przecinkami):")
    dpg.add_input_text(tag="genres_input", default_value=placeholder, width=400)
    dpg.add_separator()

    with dpg.group(horizontal=False, tag="tracks_group"):
        pass

    dpg.add_input_text(label="Nazwa playlisty", tag="playlist_name", width=400)
    dpg.add_button(label="Szukaj utworów", callback=fetch_tracks_callback)
    dpg.add_button(label="Stwórz playlistę", callback=create_playlist_callback)

    with dpg.popup(dpg.last_item(), modal=True, tag="msg_popup"):
        dpg.add_text("", tag="msg_text")
        dpg.add_button(label="OK", width=75, callback=lambda: dpg.hide_item("msg_popup"))

dpg.create_viewport(title='Spotify Recommender', width=700, height=500)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
