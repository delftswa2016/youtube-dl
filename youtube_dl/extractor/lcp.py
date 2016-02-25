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
    _VALID_URL = r'http?://(?:www\.)?lcp\.fr/(?:[^/]+/)*(?P<id>[^/]+)'

    _TESTS = [{

    }]

    def _real_extract(self, url):
        logging.basicConfig(filename='temp.log',level=logging.DEBUG)
        mobj = re.match(self._VALID_URL, url)
        display_id = mobj.group('id')

        webpage = self._download_webpage(url, display_id)

        logging.debug(webpage)
        lcp_url = self._search_regex(
            r'src="([^"]+)"></video>"', webpage, 'video URL')


        logging.warning(lcp_url)
        return self.url_result(lcp_url, 'lcp')
