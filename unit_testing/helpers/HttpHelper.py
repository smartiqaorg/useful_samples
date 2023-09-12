import logging
import json
import simplejson
import urllib3

import requests
from requests import Timeout, HTTPError, TooManyRedirects, ConnectionError
from requests.auth import HTTPBasicAuth

from utilities import truncate_str_by_symbols, retry

log = logging.getLogger(__name__)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class HTTPHelper:
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'

    HTTP_PORT = 80
    HTTPS_PORT = 443

    HTTP = 'http'
    HTTPS = 'https'

    HEADERS = {'Accept': 'application/json;charset=UTF-8'}

    def __init__(self, host, port=HTTPS_PORT, protocol=HTTPS, headers=None, username=None, password=None, s_cert=False,
                 c_cert=None, c_key=None):
        self.host = host
        self.base_url = f"{protocol}://{host}:{port}"
        if not port:
            self.base_url = f"{protocol}://{host}"
        self.headers = headers or self.HEADERS
        if username and password:
            self.auth = HTTPBasicAuth(username, password)
        else:
            self.auth = None
        self.verify = s_cert
        if c_cert and c_key:
            self.cert = (c_cert, c_key)
        else:
            self.cert = None

    @retry(max_retries=2, timeout=300, period=60, exceptions=[HTTPError])
    def requester(self, method, rel_url, headers=None, data=None, params=None, json=None, files=None, expected_error=None):
        url = f"{self.base_url}{rel_url}"
        log.debug('-------------------- HTTP_REQUEST_BEGIN_SESSION --------------------')
        log.debug(f'URL: {url}')
        log.debug(f'HEADERS: {headers or self.headers}')
        log.debug(f'METHOD: {method}')
        if params:
            log.debug(f'PARAMS: {params}')
        if data:
            log.debug(f'DATA: {data}')
        if json:
            log.debug(f'JSON: {json}')
        response = requests.request(method, url, headers=headers or self.headers, data=data, json=json, params=params,
                                    cert=self.cert, verify=self.verify, auth=self.auth, files=files)
        log.debug(f'RESPONSE CODE: {response.status_code}')
        try:
            response.raise_for_status()
        except (Timeout, ConnectionError, TooManyRedirects, HTTPError) as e:
            if expected_error and expected_error in str(e):
                log.warning(f"Expected error: {e}")
                return
            else:
                raise e
        return self._parse(response)

    def get(self, url: str, headers: dict = None, params: dict = None, expected_error: str = None):
        return self.requester(self.GET, url, headers=headers, params=params, expected_error=expected_error)

    def post(self, url: str, headers: dict = None, data: dict = None, params: dict = None, json: dict = None,
             files: dict = None, expected_error: str = None):
        return self.requester(self.POST, url, headers=headers, data=data, params=params, json=json, files=files,
                              expected_error=expected_error)

    def put(self, url: str, headers: dict = None, data: dict = None, params: dict = None, json: dict = None,
            expected_error: str = None):
        return self.requester(self.PUT, url, headers=headers, data=data, params=params, json=json, expected_error=expected_error)

    def delete(self, url: str, headers: dict = None, expected_error: str = None):
        return self.requester(self.DELETE, url, headers=headers, expected_error=expected_error)

    @staticmethod
    def _parse(response):
        content = response.content
        if response.headers.get('Content-Type') in ['application/json', 'application/json;charset=UTF-8', 'text/plain; charset=utf-8'] \
                or 'application/json' in str(response.request.headers):
            try:
                content = response.json()
                log.debug(f'RESPONSE DATA: {truncate_str_by_symbols(data=content, max_length=20000)}')
            except (json.JSONDecodeError, simplejson.JSONDecodeError):
                # We don't log non-json response since it could be not readable and large (if it's a file content for example)
                pass
        log.debug('-------------------- HTTP_REQUEST_END_SESSION --------------------')
        return content
