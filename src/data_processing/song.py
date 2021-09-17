from dataclasses import dataclass


@dataclass
class Song:
    """
    This is a class that will act as a container for a song object
    """
    index: int
    title: str
    artist: str
    genre: str
    year: int
    length: int

    def __gt__(self, other):
        return self.index > other.index

    def __str__(self):
        return f"Title: {self.title}\nArtist: {self.artist}"
