import httpx


class MakeRequest:

    def __init__(self, uri, method, params, data):
        self.uri = uri
        self.data = data
        self.params = params
        self.method = method

    async def do_request(self, app):
        async with httpx.AsyncClient(
                app=app, http2=True, verify=False, max_redirects=3
        ) as client:  # type: httpx.AsyncClient
            response = await client.request(
                self.method, self.uri, json=self.data, params=self.params
            )
            response.raise_for_status()

            return response.json()
