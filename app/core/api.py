from requests import Session
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from app.core.pattern.singleton import Singleton


class ApiServiceSingleton(Singleton):

    def __init__(self, retries=3, timeout=10 * 60, api_base_url=None):
        self.api_base_url = api_base_url
        self._retries = retries
        self._timeout = timeout

    def __make_requests_with_retries(self):
        session = Session()
        retries = Retry(
            total=self._retries,
            backoff_factor=10,
            status_forcelist=[502, 503, 504]
        )
        session.mount('https://', HTTPAdapter(max_retries=retries))
        session.mount('http://', HTTPAdapter(max_retries=retries))
        return session

    def __requests(self, method, path, headers_request=None, **kwargs):
        headers = {
            'Content-Type': 'application/json'
        }

        if headers_request:
            headers.update(headers_request)

        response = method(
            self.api_base_url + path,
            timeout=self._timeout,
            headers=headers,
            **kwargs
        )
        return response

    def post(self, path, headers_request=None, **kwargs):
        requests = self.__make_requests_with_retries()
        response = self.__requests(requests.post, path, headers_request, **kwargs)
        return response
