# Affordable Mentions

## 🙏 Credits to deezspot

The whole download process was adapted from [deezspot](https://github.com/jakiepari/deezspot). A BIG Thank-You to this project!

## ⚠️ Disclaimer

Use this project at your own risk. I'm not responsible _(and the author from deezspot is even less responsible)_ for any problems caused with your account.

Developers please note that the download process is intentionally separated into two sections: Downloading and Decrypting. I advise you to not store any decrypted audio easily readable to the user.

# DeezerGW

DeezerGW is a library that implements the private API of [Deezer](https://deezer.com)

## Installation

```
pip install deezergw
```

## Features

- Get info of tracks, albums, artists and playlists by the ID
- Search for tracks, albums, artists and playlists
- Manage favorite tracks, albums, artists and playlists
- Download tracks (ID3 support currently missing) as a MP3 (128 or 320) or FLAC
- Fully type safe
- Python >= 3.8

## Basic use

```python
import deezergw

# Initialize the Client using a key for encryption (e.g. unix username)
client = deezergw.Client("choose_a_key_here", arl="put_your_browser_arl_here")

# Save session. Encrypted using the key
logindump = deezergw.generate_logindump()
with open("dump.dat", "wb") as f:
    f.write(logindump)

# Restore the session
with open("dump.dat", "rb") as f:
    dump = f.read()
new_client = deezergw.Client("choose_a_key_here", logindump=dump)

# Get a track
track = new_client.get_track("91066235")

# Metadata - See IntelliType for all options
print(track.title)
print(track.is_favorite)

print(track.album_name)

# Download the track
encrypted_data, info = track.download_encrypted()
decrypted_data = deezergw.decrypt_audio(encrypted_data, track.id) # or info["track_id"]
save_decrypted(decrypted_data, "filename." + info["file_format"])

# Search
results = new_client.search("C418 Alpha")
album = results.albums[0].get_full_album()
print(album.tracks[0].title)

# Favorite (basically) anything
track.favorite() # toggle
album.favorite(True) # force favorited
results.playlists[1].favorite(False) # force not favorited

# Get cover url
cover = track.cover_url(128)
```
