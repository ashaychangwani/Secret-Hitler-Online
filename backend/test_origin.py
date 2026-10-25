"""Integration regression: run against an isolated backend with PUBLIC_ORIGIN set.
Usage: python backend/test_origin.py http://127.0.0.1:4040
"""
import base64
import os
import socket
import sys
import urllib.request
import urllib.error
from urllib.parse import urlsplit

base = sys.argv[1]
origin = 'https://secret-hitler.ashayc.com'

def request(path, supplied_origin, method='GET'):
    headers = {'Origin': supplied_origin}
    if method == 'OPTIONS':
        headers['Access-Control-Request-Method'] = 'GET'
    try:
        return urllib.request.urlopen(urllib.request.Request(base + path, headers=headers, method=method))
    except urllib.error.HTTPError as error:
        return error

for method in ['GET', 'OPTIONS']:
    response = request('/ping', origin, method)
    assert response.status < 300, (method, response.status)
    assert response.headers.get('Access-Control-Allow-Origin') == origin, dict(response.headers)
    for evil in [origin + '.evil.test', 'http://secret-hitler.ashayc.com', 'https://evil.test']:
        response = request('/ping', evil, method)
        assert response.status == 403, (evil, response.status)

# Real HTTP websocket upgrade; origin rejection must occur before upgrade.
url = urlsplit(base)
for supplied_origin, expected in [(origin, 101), (origin + '.evil.test', 403)]:
    with socket.create_connection((url.hostname, url.port or 80), timeout=5) as sock:
        key = base64.b64encode(os.urandom(16)).decode()
        sock.sendall((f'GET /game HTTP/1.1\r\nHost: {url.netloc}\r\nOrigin: {supplied_origin}\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n').encode())
        status = int(sock.recv(4096).split(b'\r\n')[0].split()[1])
        assert status == expected, (supplied_origin, status)

response = request('/new-lobby', origin)
assert response.status == 200, response.status
print('PASS: HTTP + preflight allow exact origin, reject suffix/http/foreign origin; websocket 101/403; new lobby with isolated Postgres')
