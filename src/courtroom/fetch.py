"""Bounded, SSRF-protected fetching of user-submitted URLs.

Limitations: DNS is validated before connecting but the HTTP client resolves again, so a DNS-rebinding
attacker is only partially mitigated. Run the app without access to sensitive internal networks.
"""
from __future__ import annotations
from html.parser import HTMLParser
from urllib.parse import urljoin, urlsplit
import ipaddress
import re
import socket
import requests

MAX_BYTES = 1_000_000
MAX_REDIRECTS = 3
ALLOWED_PORTS = {None, 80, 443}
ALLOWED_TYPES = ('text/html', 'text/plain', 'application/xhtml+xml')
BLOCKED_HOSTS = {'localhost', 'localhost.localdomain', 'metadata.google.internal'}


class FetchError(Exception):
    def __init__(self, reason: str, blocked: bool = False):
        super().__init__(reason)
        self.reason, self.blocked = reason, blocked  # blocked=True: URL itself is unsafe (never forward it anywhere)


def _check_ip(ip: str) -> None:
    addr = ipaddress.ip_address(ip.split('%')[0])
    if getattr(addr, 'ipv4_mapped', None):
        addr = addr.ipv4_mapped
    if not addr.is_global or addr.is_multicast:
        raise FetchError(f'Address {addr} is not a public internet address', blocked=True)


def check_url(url: str, resolver=socket.getaddrinfo) -> str:
    """Raise FetchError(blocked=True) unless the URL is http(s) to a public host. Returns the URL."""
    parts = urlsplit(url.strip())
    if parts.scheme not in ('http', 'https'):
        raise FetchError('Only http(s) URLs are allowed', blocked=True)
    if parts.username or parts.password:
        raise FetchError('URLs with credentials are not allowed', blocked=True)
    try:
        port = parts.port
    except ValueError:
        raise FetchError('Invalid port', blocked=True)
    if port not in ALLOWED_PORTS:
        raise FetchError(f'Port {port} is not allowed', blocked=True)
    host = (parts.hostname or '').lower().rstrip('.')
    if not host or host in BLOCKED_HOSTS or host.endswith(('.local', '.internal', '.localhost')):
        raise FetchError('Host is not allowed', blocked=True)
    try:
        ipaddress.ip_address(host)
        _check_ip(host)
        return url
    except ValueError:
        pass  # not an IP literal; resolve the name
    try:
        infos = resolver(host, port or (443 if parts.scheme == 'https' else 80), type=socket.SOCK_STREAM)
    except OSError as exc:
        raise FetchError(f'Could not resolve host: {exc}')
    if not infos:
        raise FetchError('Could not resolve host')
    for info in infos:
        _check_ip(info[4][0])  # every resolved address must be public
    return url


class _Text(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.title = ''
        self._skip = 0
        self._in_title = False

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style', 'noscript', 'template'):
            self._skip += 1
        elif tag == 'title':
            self._in_title = True

    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'noscript', 'template') and self._skip:
            self._skip -= 1
        elif tag == 'title':
            self._in_title = False

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        elif not self._skip:
            self.parts.append(data)


def extract_text(body: str, content_type: str) -> tuple[str, str]:
    if 'html' not in content_type:
        return '', re.sub(r'\s+', ' ', body).strip()
    p = _Text()
    p.feed(body)
    return re.sub(r'\s+', ' ', p.title).strip(), re.sub(r'\s+', ' ', ' '.join(p.parts)).strip()


def _default_get(url: str):
    return requests.get(url, stream=True, allow_redirects=False, timeout=(5, 10),
                        headers={'User-Agent': 'ResearchCourtroom/2 (+evidence-fetch)'})


class SafeFetcher:
    def __init__(self, http_get=_default_get, resolver=socket.getaddrinfo,
                 max_bytes: int = MAX_BYTES, max_redirects: int = MAX_REDIRECTS):
        self.http_get, self.resolver = http_get, resolver
        self.max_bytes, self.max_redirects = max_bytes, max_redirects

    def fetch(self, url: str) -> dict:
        current = url.strip()
        for _ in range(self.max_redirects + 1):
            check_url(current, self.resolver)  # re-validated on every redirect hop
            try:
                resp = self.http_get(current)
            except requests.RequestException as exc:
                raise FetchError(f'Network error: {exc}')
            try:
                if resp.status_code in (301, 302, 303, 307, 308):
                    location = resp.headers.get('Location')
                    if not location:
                        raise FetchError('Redirect without Location')
                    current = urljoin(current, location)
                    continue
                if resp.status_code != 200:
                    raise FetchError(f'HTTP {resp.status_code}')
                ctype = resp.headers.get('Content-Type', '').split(';')[0].strip().lower()
                if ctype not in ALLOWED_TYPES:
                    raise FetchError(f'Unsupported content type: {ctype or "unknown"}')
                chunks, size = [], 0
                for chunk in resp.iter_content(chunk_size=16384):
                    size += len(chunk)
                    if size > self.max_bytes:
                        raise FetchError(f'Response larger than {self.max_bytes} bytes')
                    chunks.append(chunk)
                body = b''.join(chunks).decode('utf-8', errors='replace')
            except requests.RequestException as exc:
                raise FetchError(f'Network error: {exc}')
            finally:
                close = getattr(resp, 'close', None)
                if close:
                    close()
            title, text = extract_text(body, ctype)
            if not text:
                raise FetchError('Page contained no readable text')
            return {'url': current, 'title': title or current, 'text': text, 'content_type': ctype, 'status': 200}
        raise FetchError('Too many redirects')
