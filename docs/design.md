# Memo's Music Library

## Requirements
- A database of albums and tracks
- Tools to update this database:
  - Imports (e.g. album list, artist list, ...)
  - Edit album details
  - Edit track details
  - Lookups to Musicbrains/LastFM
    - track listings
    - tags
    - album details
  - Lookups to Spotify
    - album/track/artist ids
    - track audio features
    - cover pics? (maybe just display)
- A playlist creating engine
  - selection mechanism (regex?)
  - display selected tracks (live update)
  - save to spotify

## Architecture
- library as SQLite db
- GUI with Bootstrap
- python 3.8

## GUI design
- Main window:
  - Tab: Library
    - top part (3 listboxes)
      - genre filter
      - artist filter
      - album filter
    - bottom part
      - track list with album info (table with scrollbars)
  - Tab: Playlists
    - left: existing playlists
    - right:
      - top: selection formula
      - bottom: selected tracks
      
