# coding: utf-8
from __future__ import unicode_literals

import re

from .common import InfoExtractor
from ..utils import (
    determine_ext,
    parse_duration,
    int_or_none,
)

class lcpIE(InfoExtractor):
    _VALID_URL = r'http?://(?:www\.)?lcp\.fr/(?:[^/]+/)*(?P<id>[^/]+)'

    _TESTS = [{

    }]

    def _real_extract(self, url):
        display_id = self._match_id(url)

        webpage = self._download_webpage(url, display_id)

        digiteka_url = self._proto_relative_url(self._search_regex(
            r'url\s*:\s*(["\'])(?P<url>(?:https?://)?//(?:www\.)?(?:digiteka\.net|ultimedia\.com)/deliver/.+?)\1',
            webpage, 'digiteka url', group='url'))
        return self.url_result(digiteka_url, 'Digiteka')
