from datetime import datetime, timedelta

import backoff
import requests
import singer
from singer import metrics
from ratelimit import limits, sleep_and_retry, RateLimitException
from requests.exceptions import ConnectionError, Timeout

LOGGER = singer.get_logger()

class Server5xxError(Exception):
    pass

class InSidedClient(object):
    BASE_URL = 'https://api2-us-west-2.insided.com'

    def __init__(self, config):
        self.__user_agent = config.get('user_agent')
        self.__session = requests.Session()
        self.__client_id = config.get('client_id')
        self.__client_secret = config.get('client_secret')
        self.__refresh_token = config.get('refresh_token')

        self.__access_token = None
        self.__expires_at = None

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.__session.close()

    def refresh_access_token(self):
        data = self.request(
            'POST',
            url='https://api2-us-west-2.insided.com/oauth2/token',
            data={
                'client_id': self.__client_id,
                'client_secret': self.__client_secret,
                'grant_type': 'client_credentials',
                'scope': 'read'
            })

        self.__access_token = data['access_token']

        self.__expires_at = datetime.utcnow() + \
            timedelta(seconds=data['expires_in'] - 10) # pad by 10 seconds for clock drift

    @backoff.on_exception(backoff.expo,
                          (Server5xxError,
                           RateLimitException,
                           ConnectionError,
                           Timeout),
                          max_tries=5,
                          factor=3)
    @sleep_and_retry
    @limits(calls=300, period=60)
    def request(self,
                method,
                path=None,
                url=None,
                http_statuses_to_ignore=[],
                **kwargs):
        if 'headers' not in kwargs:
            kwargs['headers'] = {}

        ## non v2 endpints 500 if this header is missing
        kwargs['headers']['Accept'] = '*/*'

        if not url:
            if self.__access_token is None or \
               self.__expires_at <= datetime.utcnow():
                    self.refresh_access_token()
        
            kwargs['headers']['Authorization'] = 'Bearer {}'.format(self.__access_token)

            url = '{}{}'.format(self.BASE_URL, path)

        if 'endpoint' in kwargs:
            endpoint = kwargs.pop('endpoint')
        else:
            endpoint = None

        if self.__user_agent:
            kwargs['headers']['User-Agent'] = self.__user_agent

        with metrics.http_request_timer(endpoint) as timer:
            response = self.__session.request(method, url, **kwargs)
            timer.tags[metrics.Tag.http_status_code] = response.status_code

        if response.status_code in http_statuses_to_ignore:
            return None

        if response.status_code >= 500:
            raise Server5xxError()

        response.raise_for_status() 

        return response.json()
