# Memo's  Music Library (mmlib)

## Description
A library of albums, where each track is connected to Spotify, and has several 
tags and audio features. These tags are used to make rule based playlists 
that can be saved to Spotify. 

## MVP
- read / write a local copy of the Spotify library
    - SQLite db for storing Spotify saved tracks, saved albums, 
    playlists (those will be overwritten with each import)
    - separate table for all tracks for saving local extras, e.g. genres, tags, audio 
      features? -> this will need atomic read/write
- manage tags, genres, etc. for grouping (into playlists)
- create & "sync" playlists with Spotify

----

More documentation [here](./docs).
