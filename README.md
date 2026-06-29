# Mineradio Local Player

A local music player fork of [Mineradio](https://github.com/XxHuberrr/Mineradio) adapted for Linux with an English UI, offline-only mode, and integrated track downloading via spotDL.

**Original project**: [XxHuberrr/Mineradio](https://github.com/XxHuberrr/Mineradio)  
**Base fork**: [oirge/Mineradio](https://github.com/oirge/Mineradio) (local player v1.1.5)  
**License**: GPL v3

---

## Changes from upstream

### Linux support
- Launcher script at `~/.local/bin/mineradio` — sets NVM PATH before starting Electron so Node.js resolves correctly
- `.desktop` file at `~/.local/share/applications/mineradio.desktop` for app menu integration
- Works on Wayland (Hyprland tested)

### UI
- Full English translation (was Simplified Chinese)
- Font changed to **Outfit** (was Noto Sans SC)
- Login popup disabled on startup
- `LOCAL_ONLY_MODE = true` — hides all online music features, no account required

### Download panel
- New **Download Track** button in the toolbar (⊙ icon)
- **YouTube Link** field → downloads via `yt-dlp` + searches lyrics with `syncedlyrics` (works for any YouTube video)
- **Song + Artist** field → downloads via `spotDL` (best for songs on Spotify — includes metadata + album art)
- Progress log shown in real time inside the app
- Library auto-refreshes after download completes

---

## Requirements

- Node.js (via [nvm](https://github.com/nvm-sh/nvm))
- Python 3 + pip (usually pre-installed on Linux)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) for YouTube downloads:
  ```bash
  pip install yt-dlp
  ```
- [syncedlyrics](https://github.com/moehmeni/syncedlyrics) for fetching LRC from YouTube downloads:
  ```bash
  pip install syncedlyrics
  ```
- [spotDL](https://github.com/spotDL/spotify-downloader) for Spotify-based downloads:

```bash
# Install spotDL
pip install spotdl

# First run — downloads ffmpeg automatically
spotdl --download-ffmpeg
```

> On some distros, use `pip3` instead of `pip`. If `spotdl` isn't found after install, add `~/.local/bin` to your PATH:
> ```bash
> echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc && source ~/.bashrc
> ```

---

## Running

```bash
npm install
npm start
```

### Linux launcher (recommended)

Create `~/.local/bin/mineradio`:
```bash
#!/bin/bash
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && source "$NVM_DIR/nvm.sh"
cd /path/to/Mineradio-local
npm start &>/dev/null &
```

Make it executable: `chmod +x ~/.local/bin/mineradio`

---

## Music library

The app scans a local folder recursively. Subfolders are treated as playlists.

**Recommended folder structure:**
```
~/Music/
  playlist-name/
    01 - Song Title.mp3
    01 - Song Title.lrc   ← synced lyrics (same filename stem)
```

LRC files with the same stem as an MP3 are auto-detected. Re-import the folder after adding new LRC files.

---

## Downloading music + lyrics

### One-shot (recommended)

Use the **Download Track** button in the app toolbar, or from terminal:

```bash
spotdl download "Song Title Artist Name" --output ~/Music --generate-lrc
```

This downloads MP3 with Spotify metadata (title, artist, album art) and generates a synced `.lrc` file in one step.

### Fetching lyrics only (for existing MP3s)

Install `syncedlyrics`:
```bash
pip install syncedlyrics
```

Run a search (searches Musixmatch, NetEase, Deezer, Lrclib):
```python
import syncedlyrics
lrc = syncedlyrics.search("Song Title Artist", providers=["Musixmatch", "NetEase", "Deezer", "Lrclib"])
```

> **Note**: Timing may be off if your MP3 is a YouTube MV version (longer intro) vs the Spotify version spotDL downloads.

---

## Building

Windows installer:
```bash
npm run build:win
```

Linux build:
```bash
npm run build:linux
```
