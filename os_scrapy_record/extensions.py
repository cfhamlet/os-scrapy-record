import logging
import time
from typing import Generator, Type

from scrapy import signals
from scrapy.crawler import Crawler
from scrapy.http.response import Request, Response
from scrapy.spiders import Spider
from twisted.python.failure import Failure

from .const import FETCH_TIME
from .items import FetchRecord, fetch_record


class OnResponse(object):
    def __init__(self, crawler: Type[Crawler]):
        crawler.signals.connect(self.regist, signal=signals.request_scheduled)
        self.logger = logging.getLogger(self.__class__.__name__)

    @classmethod
    def from_crawler(cls, crawler: Type[Crawler]):
        return cls(crawler)

    def regist(self, request: Type[Request], spider: Type[Spider]):
        pass


class ResponseCallback(OnResponse):
    def __init__(self, crawler: Type[Crawler]):
        super(ResponseCallback, self).__init__(crawler)
        crawler.signals.connect(
            self.response_downloaded, signal=signals.response_downloaded
        )

    def response_downloaded(
        self, response: Type[Response], request: Type[Request], spider: Type[Spider]
    ):
        request.meta[FETCH_TIME] = int(time.time())

    def regist(self, request: Type[Request], spider: Type[Spider]):
        if request.callback is None:
            request.callback = self.callback

    def callback(self, response: Type[Response]) -> Generator[FetchRecord, None, None]:
        record = fetch_record(response=response)
        yield record


class ResponseErrback(OnResponse):
    def regist(self, request: Type[Request], spider: Type[Spider]):
        if request.errback is None:
            request.errback = self.errback

    def errback(self, failure: Failure) -> Generator[FetchRecord, None, None]:
        request = failure.request
        if FETCH_TIME not in request.meta:
            request.meta[FETCH_TIME] = int(time.time())
        record = fetch_record(failure=failure)
        yield record
