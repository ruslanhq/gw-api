import httpx
import requests

from uuid import uuid4


class MakeRequest:

    def __init__(
            self, uri, method='GET', data=None, params=None, auth=None, app=None
    ):
        self.uri = uri
        self.data = data
        self.params = params
        self.method = method
        self.application = app
        self.auth = auth
        self.headers = {
            'X-Application-ID': uuid4().hex,
            'Content-Type': 'application/json',
        }

    async def do_request(self):
        async with httpx.AsyncClient(
                app=self.application, http2=True, verify=False, max_redirects=3
        ) as client:  # type: httpx.AsyncClient
            response = await client.request(
                self.method, self.uri, json=self.data, params=self.params,
                auth=self.auth, headers=self.headers,
            )
            response.raise_for_status()

            return response.json()

    def do_sync_request(self):
        with requests.Session() as session:
            response = session.request(
                self.method, self.uri, json=self.data, params=self.params,
                auth=self.auth, headers=self.headers,
            )
            response.raise_for_status()

            return response.json()
