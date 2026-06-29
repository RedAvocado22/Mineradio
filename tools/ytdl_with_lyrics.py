#!/usr/bin/env python3
"""
Download a song from YouTube + fetch synced LRC lyrics.
Usage: python tools/ytdl_with_lyrics.py "URL" [output_dir]
"""

import sys
import os
import subprocess
import re
import syncedlyrics

url = sys.argv[1] if len(sys.argv) > 1 else None
out_dir = os.path.expanduser(sys.argv[2] if len(sys.argv) > 2 else "~/Music")

if not url:
    print("Usage: python ytdl_with_lyrics.py <youtube_url> [output_dir]")
    sys.exit(1)

# Step 1: get title before downloading
print(f"Fetching title from YouTube...")
result = subprocess.run(
    ["yt-dlp", "--print", "%(artist)s - %(title)s", "--no-playlist", url],
    capture_output=True, text=True
)
song_title = result.stdout.strip() or None

# Fallback to plain title if no artist tag
if not song_title or song_title.startswith(" - "):
    result2 = subprocess.run(
        ["yt-dlp", "--print", "%(title)s", "--no-playlist", url],
        capture_output=True, text=True
    )
    song_title = result2.stdout.strip()

print(f"Title: {song_title}")

# Step 2: download MP3
print(f"Downloading MP3 to {out_dir}...")
dl = subprocess.run([
    "yt-dlp", "-x", "--audio-format", "mp3",
    "--embed-thumbnail", "--no-playlist",
    "-o", os.path.join(out_dir, "%(title)s.%(ext)s"),
    url
])
if dl.returncode != 0:
    print("yt-dlp failed")
    sys.exit(1)

# Step 3: find MP3 filename
mp3_title = subprocess.run(
    ["yt-dlp", "--print", "%(title)s", "--no-playlist", url],
    capture_output=True, text=True
).stdout.strip()
mp3_path = os.path.join(out_dir, mp3_title + ".mp3")
lrc_path = os.path.join(out_dir, mp3_title + ".lrc")

# Step 4: fetch lyrics
print(f"Searching lyrics for: {song_title!r}")
lrc = None
try:
    lrc = syncedlyrics.search(song_title, providers=["Musixmatch", "NetEase", "Deezer", "Lrclib"])
except Exception as e:
    print(f"Lyrics error: {e}")

if lrc:
    with open(lrc_path, "w", encoding="utf-8") as f:
        f.write(lrc)
    print(f"✓ Saved LRC → {lrc_path}")
else:
    print("✗ No lyrics found (instrumental or too obscure)")

print(f"✓ Done — {mp3_path}")
