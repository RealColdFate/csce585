from dataclasses import dataclass
import json


def load_song_form_json(json_str: str):
    return json.loads(json_str, object_hook=lambda d: Song(**d))


@dataclass
class Song:
    """
    This is a class that will act as a container for a song object
    """

    INDEX_KEY = "index"
    TITLE_KEY = "title"
    ARTIST_KEY = "artist"
    GENRE_KEY = "genre"
    YEAR_KEY = "year"
    LENGTH_KEY = "LENGTH"

    index: int
    title: str
    artist: str
    genre: str
    year: int
    length: int

    def to_json(self) -> str:
        return json.dumps(self.__dict__)

    def __gt__(self, other):
        return self.index > other.index

    def __str__(self):
        return f"Title: {self.title}\nArtist: {self.artist}"
