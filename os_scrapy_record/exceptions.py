from .fetch_status import FetchStatus


class FetchStatusException(Exception):
    def __init__(self, fetch_status: FetchStatus):
        self._fetch_status = fetch_status

    @property
    def fetch_status(self):
        return self._fetch_status

    def __str__(self):
        return str(self._fetch_status)
