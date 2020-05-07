library = {
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
