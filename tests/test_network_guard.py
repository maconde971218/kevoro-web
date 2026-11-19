"""Verify redirect blocking without sending any external network request."""
from types import SimpleNamespace
import unittest

from browser_support import local_only_route


ORIGIN = 'http://127.0.0.1:8765'


class FakeRoute:
    def __init__(self, url, responses=()):
        self.request = SimpleNamespace(url=url)
        self.responses = iter(responses)
        self.fetches = []
        self.fulfilled = None
        self.abort_reason = None

    def fetch(self, **kwargs):
        self.fetches.append(kwargs)
        return next(self.responses)

    def abort(self, reason):
        self.abort_reason = reason

    def fulfill(self, response):
        self.fulfilled = response


class NetworkGuardTests(unittest.TestCase):
    def test_external_request_is_never_fetched(self):
        blocked = []
        route = FakeRoute('https://example.invalid/resource')
        local_only_route(route, ORIGIN, blocked)
        self.assertEqual(route.fetches, [])
        self.assertEqual(route.abort_reason, 'blockedbyclient')
        self.assertEqual(blocked, ['https://example.invalid/resource'])

    def test_local_redirect_chain_cannot_escape_to_external_origin(self):
        blocked = []
        route = FakeRoute(ORIGIN + '/first', [
            SimpleNamespace(status=302, headers={'location': '/second'}),
            SimpleNamespace(status=302, headers={'location': '//example.invalid/third'}),
        ])
        local_only_route(route, ORIGIN, blocked)
        self.assertEqual([entry['url'] for entry in route.fetches],
                         [ORIGIN + '/first', ORIGIN + '/second'])
        self.assertTrue(all(entry['max_redirects'] == 0 for entry in route.fetches))
        self.assertEqual(route.abort_reason, 'blockedbyclient')
        self.assertIsNone(route.fulfilled)
        self.assertEqual(blocked, ['http://example.invalid/third'])

    def test_local_response_is_delivered(self):
        response = SimpleNamespace(status=200, headers={})
        route = FakeRoute(ORIGIN + '/assets/app.js', [response])
        blocked = []
        local_only_route(route, ORIGIN, blocked)
        self.assertIs(route.fulfilled, response)
        self.assertEqual(blocked, [])

    def test_redirect_loop_is_bounded(self):
        route = FakeRoute(ORIGIN, [
            SimpleNamespace(status=302, headers={'location': '/'}) for _ in range(8)
        ])
        blocked = []
        local_only_route(route, ORIGIN, blocked)
        self.assertEqual(len(route.fetches), 8)
        self.assertEqual(route.abort_reason, 'blockedbyclient')
        self.assertTrue(blocked[0].startswith('redirect-limit:'))


if __name__ == '__main__':
    unittest.main()
