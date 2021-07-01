"""A video playlist class."""
from .video import Video
from pathlib import Path
import csv

class Playlist:
    """A class used to represent a Playlist."""
    def __init__(self, name):
        self._name = name
        self._video_list = []

    @property
    def video_list(self) -> list:
        """Returns the videos in playlist."""
        return self._video_list

    @property
    def name(self) -> str:
        """Returns the videos in playlist."""
        return self._name
