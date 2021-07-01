"""A video player class."""

import random

from .video_library import VideoLibrary
from .video import Video
from .video_playlist import Playlist

class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()
        self._currently_playing = None
        self._video_is_paused = True
        self._playlist_list = []
    def contains(self, list, filter):
        if callable(filter):
            for x in list:
                if filter(x):
                    return x
            return False
        else:
            for x in list:
                if(filter == x):
                    return (filter)
            return False

    def flagged_video_count(self):
        counter = 0
        for video in self._video_library.get_all_videos():
            if video.flagged == True:
                counter += 1
        return counter

    def format_video_info(self, video):
        video_info = ""
        for property, value in vars(video).items():
            if(property == "_title"):
                video_info += value + " "
            if (property == "_video_id"):
                video_info += "(" + value + ") "
            if (property == "_tags"):
                video_info += str(value).replace(',', '').replace('(', '[').replace(')', ']').replace("'", "")
            if (property == "_flagged"):
                if value == True:
                    video_info += " - FLAGGED (reason: " + video.flagged_reason + ")"
        return video_info

    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        """Returns all videos."""
        print("Here's a list of all available videos:")
        temp_list_sorted = sorted(self._video_library.get_all_videos(), key=lambda video: video.title)
        for video in temp_list_sorted:
            print(self.format_video_info(video))

    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """
        search_result = self._video_library.get_video(video_id)
        #search_result = self.contains(self._video_library.get_all_videos(), lambda video: video.video_id == video_id)
        if search_result:
            if search_result.flagged == True:
                print("Cannot play video: Video is currently flagged (reason: " + search_result.flagged_reason + ")")
            else:
                if self._currently_playing:
                    print("Stopping video: " + self._currently_playing.title)
                print("Playing video: " + search_result.title)
                self._currently_playing = search_result
                self._video_is_paused = False
                return
        else:
            print("Cannot play video: Video does not exist")

    def stop_video(self):
        if self._currently_playing:
            print("Stopping video: " + self._currently_playing.title)
            self._currently_playing = None
        else:
            print("Cannot stop video: No video is currently playing")


    def play_random_video(self):
        if self.flagged_video_count() == len(self._video_library.get_all_videos()):
            print("No videos available")
            return
        temp_library = self._video_library.get_all_videos()
        rand = random.randrange(len(temp_library))
        while True:
            random_video = temp_library[rand]
            if random_video.flagged == False:
                break
        if self._currently_playing:
            print("Stopping video: " + self._currently_playing.title)
            print("Playing video: " + random_video.title)
        else:
            print("Playing video: " + random_video.title)
        self._currently_playing = random_video
        self._video_is_paused = False
        """Plays a random video from the video library."""


    def pause_video(self):
        """Pauses the current video."""
        if not self._video_is_paused:
            print("Pausing video: " + self._currently_playing.title)
            self._video_is_paused = True
        else:
            if not self._currently_playing:
                print("Cannot pause video: No video is currently playing")
            else:
                print("Video already paused: " + self._currently_playing.title)

    def continue_video(self):
        """Resumes playing the current video."""
        if self._currently_playing:
            if self._video_is_paused:
                print("Continuing video: " + self._currently_playing.title)
                self._video_is_paused = False
            else:
                print("Cannot continue video: Video is not paused")
        else:
            print("Cannot continue video: No video is currently playing")

    def show_playing(self):
        """Displays video currently playing."""
        if self._currently_playing:
            if self._video_is_paused:
                print("Currently playing: " + self.format_video_info(self._currently_playing) + " - PAUSED")
            else:
                print("Currently playing: " + self.format_video_info(self._currently_playing))
        else:
            print("No video is currently playing")

    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        search_result = self.contains(self._playlist_list, lambda playlist: playlist._name.upper() == playlist_name.upper())
        if search_result:
            print("Cannot create playlist: A playlist with the same name already exists")
        else:
            self._playlist_list.append(Playlist(playlist_name))
            print("Successfully created new playlist: " + playlist_name)

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """
        if self._video_library.get_video(video_id) and self._video_library.get_video(video_id).flagged:
            print("Cannot add video to " + playlist_name + ": Video is currently flagged (reason: " + self._video_library.get_video(video_id)._flagged_reason + ")")
        else:
            playlist_search_result = self.contains(self._playlist_list, lambda playlist: playlist.name.upper() == playlist_name.upper())
            video_search_result = self.contains(self._video_library.get_all_videos(), lambda video: video.video_id == video_id)
            if playlist_search_result:
                if not (video_id) in playlist_search_result.video_list:
                    if video_search_result:
                        print("Added video to " + playlist_name + ": " + video_search_result.title)
                        playlist_search_result.video_list.append(video_id)
                    else:
                        print("Cannot add video to " + playlist_name + ": Video does not exist")
                else:
                        print("Cannot add video to " + playlist_name + ": Video already added")
            else:
                print("Cannot add video to " + playlist_name + ": Playlist does not exist")

    def show_all_playlists(self):
        """Display all playlists."""

        if len(self._playlist_list) == 0:
            print("No playlists exist yet")
        else:
            temp_playlist_sorted = sorted(self._playlist_list, key=lambda playlist: playlist.name)
            print("Showing all playlists:")
            for playlist in temp_playlist_sorted:
                print("\t" + playlist.name)

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        search_result = self.contains(self._playlist_list, lambda playlist: playlist._name.upper() == playlist_name.upper())
        if(search_result):
            vid_list = search_result.video_list
            if not len(search_result.video_list) == 0:
                print("Showing playlist: " + playlist_name)
                for vids in vid_list:
                    print("\t" + self.format_video_info(self.contains(self._video_library.get_all_videos(), lambda video: video.video_id == vids)))
            elif len(vid_list) == 0:
                print("Showing playlist: " + playlist_name)
                print("\tNo videos here yet")
        else:
            print("Cannot show playlist " + playlist_name + ": Playlist does not exist")

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        playlist_search_result = self.contains(self._playlist_list, lambda playlist: playlist.name.upper() == playlist_name.upper())
        if not playlist_search_result:
            print("Cannot remove video from " + playlist_name + ": Playlist does not exist")
        else:
            vid_object = self.contains(self._video_library.get_all_videos(), lambda video: video.video_id == video_id)
            if not vid_object:
                print("Cannot remove video from " + playlist_name + ": Video does not exist")
            elif not (video_id) in playlist_search_result.video_list:
                print("Cannot remove video from " + playlist_name + ": Video is not in playlist")
            else:
                vid_name = vid_object.title
                playlist_search_result.video_list.remove(video_id)
                print("Removed video from " + playlist_name + ": " + vid_name)

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        playlist_search_result = self.contains(self._playlist_list, lambda playlist: playlist.name.upper() == playlist_name.upper())
        if (playlist_search_result):
            playlist_search_result.video_list.clear()
            print("Successfully removed all videos from " + playlist_name)
        else:
            print("Cannot clear playlist " + playlist_name + ": Playlist does not exist")

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        playlist_search_result = self.contains(self._playlist_list, lambda playlist: playlist.name.upper() == playlist_name.upper())
        if not (playlist_search_result):
            print("Cannot delete playlist " + playlist_name + ": Playlist does not exist")
        else:
            self._playlist_list.remove(playlist_search_result)
            print("Deleted playlist: " + playlist_name)

    def search_videos(self, search_term):
        temp_search_list = []
        for i in range(len(self._video_library.get_all_videos())):
            if search_term.lower() in self._video_library.get_all_videos()[i].title.lower() and not self._video_library.get_all_videos()[i].flagged:
                temp_search_list.append(self._video_library.get_all_videos()[i])
        if temp_search_list != []:
            i = 1
            print("Here are the results for " + search_term + ":")
            temp_search_list_sorted = sorted(temp_search_list, key=lambda video: video.title)
            for video in temp_search_list_sorted:
                print("\t" + str(i) + ") " + self.format_video_info(video))
                i += 1
            print("Would you like to play any of the above? If yes, specify the number of the video.")
            print("If your answer is not a valid number, we will assume it's a no.")
            vid_choice = input()
            if vid_choice.isdecimal():
                if int(vid_choice) > 0 and int(vid_choice) <= len(temp_search_list_sorted):
                    self.play_video(temp_search_list_sorted[int(vid_choice) - 1].video_id)
        else:
            print("No search results for " + search_term)

    def search_videos_tag(self, video_tag):
        temp_search_list = []
        for i in range(len(self._video_library.get_all_videos())):
            if video_tag.lower() in str(self._video_library.get_all_videos()[i].tags).lower() and not self._video_library.get_all_videos()[i].flagged:
                temp_search_list.append(self._video_library.get_all_videos()[i])
        if temp_search_list != []:
            i = 1
            print("Here are the results for " + video_tag + ":")
            temp_search_list_sorted = sorted(temp_search_list, key=lambda video: video.title)
            for video in temp_search_list_sorted:
                print("\t" + str(i) + ") " + self.format_video_info(video))
                i += 1
            print("Would you like to play any of the above? If yes, specify the number of the video.")
            print("If your answer is not a valid number, we will assume it's a no.")
            vid_choice = input()
            if vid_choice.isdecimal():
                if int(vid_choice) > 0 and int(vid_choice) <= len(temp_search_list_sorted):
                    self.play_video(temp_search_list_sorted[int(vid_choice) - 1].video_id)
        else:
            print("No search results for " + video_tag)

    def flag_video(self, video_id, flag_reason=""):
        if flag_reason == "":
            flag_reason = "Not supplied"
        chosen_vid = self._video_library.get_video(video_id)
        if not chosen_vid:
            print("Cannot flag video: Video does not exist")
        else:
            if chosen_vid.flagged == False:
                if self._currently_playing and self._currently_playing.title == chosen_vid.title:
                    self.stop_video()
                print("Successfully flagged video: " + chosen_vid.title + " (reason: " + flag_reason + ")")
                chosen_vid.set_flag(True)
                chosen_vid.set_flagged_reason(flag_reason)
                if chosen_vid.title == self._currently_playing:
                    self.stop_video()
            else:
                print("Cannot flag video: Video is already flagged")

    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        chosen_vid = self._video_library.get_video(video_id)
        if not chosen_vid:
            print("Cannot remove flag from video: Video does not exist")
        else:
            if chosen_vid.flagged:
                chosen_vid.set_flag(False)
                chosen_vid.set_flagged_reason("")
                print("Successfully removed flag from video: " + chosen_vid.title)
            elif not chosen_vid.flagged:
                print("Cannot remove flag from video: Video is not flagged")

        #print("allow_video needs implementation")
