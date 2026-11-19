"""Restrict test browser requests to one local origin, including redirect chains."""
from urllib.parse import urljoin, urlsplit


def is_local_origin(url, allowed_origin):
    parsed = urlsplit(url)
    return (
        parsed.scheme == 'http'
        and parsed.hostname in {'localhost', '127.0.0.1'}
        and not parsed.username
        and not parsed.password
        and (parsed.scheme, parsed.hostname, parsed.port)
        == (urlsplit(allowed_origin).scheme, urlsplit(allowed_origin).hostname,
            urlsplit(allowed_origin).port)
    )


def local_only_route(route, allowed_origin, blocked):
    """Fetch each redirect separately so an allowed URL cannot redirect off-site.

    Playwright route.fetch follows redirects by default. Disable that behavior,
    inspect each Location, and fulfill only the final local response.
    """
    url = route.request.url
    for _ in range(8):
        if not is_local_origin(url, allowed_origin):
            blocked.append(url)
            route.abort('blockedbyclient')
            return
        response = route.fetch(url=url, max_redirects=0)
        location = response.headers.get('location')
        if 300 <= response.status < 400 and location:
            url = urljoin(url, location)
            continue
        route.fulfill(response=response)
        return
    blocked.append('redirect-limit: ' + url)
    route.abort('blockedbyclient')
