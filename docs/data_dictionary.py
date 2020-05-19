album = {
    "id": "32HZWKCeUbJudLgwGFLd2p",
    "name": "Silver (feat. Eddie Henderson, Juini Booth & Kenny Wollesen)",
    "artists": [
        {
            "id": "5aweKNLI0ZyI48q5TmoCxT",
            "name": "Ilhan Ersahin"
        }
    ],
    "total_tracks": 11,
    "tracks": [
        {
            "id": "1dChLNfqO43MmCpkW3iegQ",
            "name": "Silver Overture (feat. Eddie Henderson, Juini Booth & Kenny Wollesen)",
            "artists": [
                {
                    "id": "5aweKNLI0ZyI48q5TmoCxT",
                    "name": "Ilhan Ersahin"
                },
                {
                    "id": "4LMsUGCTzMsLYcL90zb8sF",
                    "name": "Eddie Henderson"
                },
                {
                    "id": "1tXPpeeujLI04jJNir7Zke",
                    "name": "Juini Booth"
                },
                {
                    "id": "6Zn84vmI9vs51dH9UK52bV",
                    "name": "Kenny Wollesen"
                }
            ],
            "duration_ms": 167557,
            "track_number": 1
        },
    ]
}

audio_features = {
    "id": "5KvOWvM8d5gLYYoHrO3hKP",
    "danceability": 0.773,
    "energy": 0.645,
    "key": 1,
    "loudness": -10.348,
    "mode": 1,
    "speechiness": 0.0427,
    "acousticness": 0.0831,
    "instrumentalness": 0.785,
    "liveness": 0.0823,
    "valence": 0.699,
    "tempo": 133.927,
    "duration_ms": 266680,
    "time_signature": 4
}

track = {
    "id": "5KvOWvM8d5gLYYoHrO3hKP",
    "name": "Mellow Mood",
    "artists": [
        {
            "id": "0HED7cXMsNbjeqjYNyskFU",
            "name": "Soul Sugar"
        }
    ],
    "duration_ms": 266680,
    "track_number": 6,
    "danceability": 0.773,
    "energy": 0.645,
    "key": 1,
    "loudness": -10.348,
    "mode": 1,
    "speechiness": 0.0427,
    "acousticness": 0.0831,
    "instrumentalness": 0.785,
    "liveness": 0.0823,
    "valence": 0.699,
    "tempo": 133.927,
    "time_signature": 4
}

playlist = {
    "id": "1RCkV13SZppDGX6DjtL4JD",
    "name": "Acid Jazz Funk",
    "description": "acid jazz us3 funk prince maceo parker james brown ronny jordan guru jazzmatazz, blackwave, jazz meets funk and hip hop.",
    "tracks": [
        {
            "id": "79ykdWd22NalUbAITqxd1A",
            "name": "Roots (Back To A Way Of Life)",
            "artists": [
                {
                    "id": "5moJNCJeiNwuQAhDLJXULs",
                    "name": "Incognito"
                }
            ],
            "duration_ms": 342000,
            "track_number": 1
        }
    ]
}

json_library = {
    "tracks": [
        {
            "id": "String",
            "name": "String",
            "artists": [
                {
                    "id": "string",
                    "name": "string"
                }
            ],
            "duration_ms": "float",
        }
    ],
    "albums": [
        {
            "id": "String",
            "name": "String",
            "genre": "String",
            "tags": ["String", "String"],
            "year": "String",
            "artists": [
                {
                    "id": "string",
                    "name": "string"
                }
            ],
            "tracks": [
                {
                    "id": "string",
                    "name": "string",
                    "duration_ms": "float",
                    "track_number": "int"
                },
                {
                    "id": "string",
                    "name": "string",
                    "duration_ms": "float",
                    "track_number": "int"
                }
            ],
            "total_tracks": "int"
        },
    ],
    "playlists": [
        {
            "id": "string",
            "name": "string",
            "description": "string",
            "tracks": [
                "track_id",
                "track_id",
                "track_id",
            ]
        }
    ],
    "artists": [
        {
            "id": "string",
            "name": "string",
        }
    ],
    "track_details": [
        {
            "id": {
                "name": "String",
                "artists": [
                    {
                        "id": "string",
                        "name": "string"
                    }
                ],
                "duration_ms": "float",
                "genres": ["String", "String"],  # or single?
                "tags": ["String", "String"],
                "audio_features": {
                    "tempo": "float",
                    "danceability": "float",
                },
            }
        },
        {
            "id": {
                "name": "String",
                "artists": [
                    {
                        "id": "string",
                        "name": "string"
                    }
                ],
                "duration_ms": "float",
                "genres": ["String", "String"],  # or single?
                "tags": ["String", "String"],
                "audio_features": {
                    "tempo": "float",
                    "danceability": "float",
                },
            }
        },
    ]
}
