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

class dagbladetIE(InfoExtractor):
    _VALID_URL = r'http?://(?:www\.)?dagbladet\.no/(?:[^/]+/)*(?P<id>[^/]+)'

    _TESTS = [{

    }]

    def _real_extract(self, url):
        logging.basicConfig(filename='temp.log',level=logging.DEBUG)
        display_id = self._match_id(url)
        webpage = self._download_webpage(url, display_id)
        logging.debug(webpage)

        lcp_url = self._search_regex(r'src="([^"]+)" type="video/mp4"></video>', webpage, 'video URLs', default=None)





        logging.warning(lcp_url)
        return self.url_result(lcp_url, 'lcp')
