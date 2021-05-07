import requests
import requests_mock 


requests_mock.Mocker.TEST_PREFIX = 'foo'

@requests_mock.Mocker()
class BinanceMocker:
    
    def foo_one(self, m):
        m.register_uri('GET', 'http://test.com', text='resp')
        return requests.get('http://test.com').text

    def foo_two(self, m):
        m.register_uri('GET', 'http://test.com', text='resp')
        return requests.get('http://test.com').text
