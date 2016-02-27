# coding: utf-8
from __future__ import unicode_literals
from .common import InfoExtractor
from ..utils import (
    int_or_none
)

class lcpIE(InfoExtractor):
    IE_NAME = 'LCP'

    _VALID_URL = r'https?:\/\/(?:www\.)?lcp\.fr\/(?:[^\/]+/)*(?P<id>[^/]+)'

    _TESTS = [{
        'url': 'http://www.lcp.fr/emissions/politique-matin/271085-politique-matin',
        'md5': '6cea4f7d13810464ef8485a924fc3333',
        'info_dict': {
            'id': '327336',
            'url': 'http://httpod.scdn.arkena.com/11970/327336_4.mp4',
            'ext': 'mp4',
            'title': 'Politique Matin - Politique matin | LCP Assemblée nationale'
        }
    }]

    def _real_extract(self, url):
        """Extracts the information for a given url and returns it in a dictionary"""
        display_id = self._match_id(url)

        # Extract the web page
        self.report_download_webpage(display_id)
        webpage = self._download_webpage(url, display_id)

        # Extract the required info of the media files
        media_files_info = self.__extract_from_webpage(display_id, webpage)
        # Extract the video formats from the media info
        video_formats = self.__get_video_formats(display_id, media_files_info)
        # Extract the thumbnails from the media info
        video_thumbnails = self.__get_thumbnails(media_files_info)

        # Return the dictionary with the information about the video to download
        return {
            'id' : display_id,
            'title' : self._og_search_title(webpage),
            'formats': video_formats,
            'thumbnails': video_thumbnails
        }

    def __extract_from_webpage(self, display_id, webpage):
        """Extracts the media info for the video for the provided web page."""
        embed_url = self.__extract_embed_url(webpage)
        embed_regex = r'(?:[a-zA-Z0-9]+\.)?lcp\.fr\/embed\/(?P<clip_id>[0-9]+)\/(?P<player_id>[0-9]+)\/(?P<skin_name>[^\/]+)'

        # Extract the identifying attributes from the embed url of the web page
        clip_id = self._search_regex(embed_regex, embed_url, 'clip id', group='clip_id')
        player_id = self._search_regex(embed_regex, embed_url, 'player id', group='player_id')
        skin_name = self._search_regex(embed_regex, embed_url, 'skin name', group='skin_name')

        # Extract the video url from the embedded player
        return self.__extract_from_player(display_id, clip_id, player_id, skin_name)

    def __extract_embed_url(self, webpage):
        """Extracts the embedded player url for the video."""
        self.report_extraction('embedded url')

        return self._search_regex(
            r'<iframe[^>]+src=(["\'])(?P<url>.+?)\1',
            webpage, 'embed url', group='url')

    def __extract_from_player(self, display_id, clip_id, player_id, skin_name):
        """Extracts the json object containing the required media info from the embedded arkena player"""
        arkena_url = 'http://play.arkena.com/config/avp/v1/player/media/{0}/{1}/{2}/?callbackMethod=?'.format(clip_id, skin_name, player_id)
        arkena_info = self._download_webpage(arkena_url, clip_id)

        #Extract the json containing information about the video files
        arkena_info_regex = r'\?\((?P<json>.*)\);'
        info_json = self._parse_json(self._search_regex(arkena_info_regex, arkena_info, 'json', group='json'), display_id)

        media_files_info = info_json['Playlist'][0]  # All videos are part of a playlist, a single video is in a playlist of size 1
        return media_files_info

    def __get_thumbnails(self, media_files_info):
        """Retrieves the thumbnails contained in the media info"""
        thumbnails = []
        for thumbnail in media_files_info['MediaInfo']['Poster']:
            thumbnails.append({
                'url': thumbnail['Url'],
                'width': int_or_none(thumbnail['Size'])
            })
        return thumbnails

    def __get_video_formats(self, display_id, media_files_info):
        """Retrieves the video formats contained in the media file info"""
        formats = []

        formats.extend(self.__get_mp4_video_formats(media_files_info['MediaFiles']))
        self._sort_formats(formats)

        return formats

    def __get_mp4_video_formats(self, media_files_json):
        """Retrieves all mp4 video formats contained in the media file info"""
        formats = []
        mp4_files_json = media_files_json['Mp4']

        for video_info in mp4_files_json:
            bitrate = int_or_none(video_info['Bitrate'])
            if bitrate is not None:
                bitrate = bitrate / 1000     # Set bitrate to KBit/s
            formats.append({
                'url': video_info['Url'],
                'ext': 'mp4',
                'tbr': bitrate
            })
        return formats