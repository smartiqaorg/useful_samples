from helpers.HttpHelper import HTTPHelper
from requests import Response, PreparedRequest
from unittest.mock import MagicMock, patch
import pytest
from json import JSONDecodeError
from simplejson import JSONDecodeError as SimpleJsonJSONDecodeError


@pytest.fixture(scope='module')
@patch('test_http_helper.Response', autospec=True)
def m_response(MockedResponse):
    m_response = MockedResponse()
    return m_response


content_types = ['application/json', 'application/json;charset=UTF-8', 'text/plain; charset=utf-8', None]


@pytest.mark.parametrize("content_type", content_types)
def test_parse_method(m_response, content_type):
    if content_type:
        m_response.headers = {'Content-Type': content_type}
    else:
        m_response.headers = {}
        m_response.request = MagicMock(target=PreparedRequest, attribute='headers')
        m_response.request.headers = 'application/json'
    m_response.json.return_value = {'RequestId': 'E126ABAD-A242-46D0-BEEC-C67F2454BD33', 'Error': ''}
    HTTPHelper._parse(response=m_response)
    m_response.json.assert_called()


@pytest.mark.parametrize("error", [JSONDecodeError, SimpleJsonJSONDecodeError])
def test_parse_method_catch_exception(m_response, error):
    m_response.headers = {'Content-Type': 'application/json'}
    m_response.json.side_effect = error('JSON error was suppressed', 'doc', 0)
    HTTPHelper._parse(response=m_response)
    m_response.json.assert_called()
