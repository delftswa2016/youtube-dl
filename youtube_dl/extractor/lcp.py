# coding: utf-8
from __future__ import unicode_literals

import re
import logging

from .common import InfoExtractor
from ..utils import (
    determine_ext,
    parse_duration,
    int_or_none,
)

class lcpIE(InfoExtractor):
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
        display_id = self._match_id(url)
        webpage = self._download_webpage(url, display_id)
        self.report_extraction(display_id)

        # Get the initial page
        embed_url = self._search_regex(r'<iframe[^>]+src=(["\'])(?P<url>.+?)\1', webpage, 'embed url', group='url')

        # Download the contents of the iframe
        arkena_extract_regex = r'https?:\/\/(?:[a-zA-Z0-9]+.)?lcp.fr\/embed\/(?P<clip_id>[0-9]+)\/(?P<player_id>[0-9]+)\/(?P<name>[^\/]+)'
        clip_id = self._search_regex(arkena_extract_regex, embed_url, 'clip_id from embed url', group='clip_id')
        player_id = self._search_regex(arkena_extract_regex, embed_url, 'player_id form embed url', group='player_id')
        # TODO: Is this necessary?
        name = self._search_regex(arkena_extract_regex, embed_url, 'name form embed url', group='name')

        arkena_url = 'http://play.arkena.com/config/avp/v1/player/media/{0}/{1}/{2}/?callbackMethod=?'.format(clip_id, name, player_id)
        # Download arkena info
        arkena_info = self._download_webpage(arkena_url, clip_id)

        bitrate = 1499152
        # TODO: This requires a fixed formatting of the JSON response, is this the case?
        arkena_info_regex = r'"Url":"(?P<url>[^"]*)","Bitrate":"{0}"'.format(bitrate)
        video_url = self._search_regex(arkena_info_regex, arkena_info, 'video url extracted from arkena info',group='url')

        # return self.url_result(embed_url)
        return {
            'id' : display_id,
            'url' : video_url,
            'ext' : 'mp4',
            'title' : self._og_search_title(webpage)
        }