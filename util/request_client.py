import requests


class RequestClient:
    def __init__(self, base_url, headers=None):
        self.base_url = base_url.rstrip('/')  # Remove trailing slash if any
        self.headers = headers or {}

    def get(self, endpoint, **kwargs):
        return self._request("GET", endpoint, **kwargs)

    def post(self, endpoint, data=None, **kwargs):
        return self._request("POST", endpoint, data=data, **kwargs)

    def put(self, endpoint, data=None, **kwargs):
        return self._request("PUT", endpoint, data=data, **kwargs)

    def delete(self, endpoint, **kwargs):
        return self._request("DELETE", endpoint, **kwargs)

    def _request(self, method, endpoint, data, **kwargs):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"  # Construct full URL
        headers = {**self.headers, **kwargs.pop("headers", {})}  # Merge default headers with headers from kwargs
        print(headers)
        print(**kwargs)
        response = requests.request(method, url, headers=headers, json=data)

        # Here, you can handle the response, raise for errors, etc.
        response.raise_for_status()

        return response.json()

# Usage:

# headers = {
#     'Authorization': 'Bearer YOUR_TOKEN',
#     'Content-Type': 'application/json',
# }
#
# client = RequestClient('https://api.example.com', headers=headers)
#
# response_data = client.get('/data_utility')
# print(response_data)
#
# post_data = {'key': 'value'}
# response_data = client.post('/data_utility', data_utility=post_data)
# print(response_data)
