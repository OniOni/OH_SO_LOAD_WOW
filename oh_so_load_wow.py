import monocle

monocle.init("twisted")
from monocle.stack import eventloop

from monocle import _o, Return

@_o
def p0wn(url):
    from monocle.stack.network.http import HttpClient, HttpHeaders
    from urlparse import urlparse
    from base64 import encodestring

    o = urlparse(url)
    client = HttpClient()
    yield client.connect(o.hostname, o.port, scheme=o.scheme)

    if hasattr(o, 'username'):
        headers = HttpHeaders({
            "Authorization": "Basic %s" % encodestring("%s:%s" % (o.username, o.password))
        })

    i = 0
    while True:
        res = yield client.request(o.path, headers=headers or None)
        i += 1
        print "%s -- %s -- %s" % (url, res.body, i)

if __name__ == '__main__':
    to_pawn = [
        'http://admin:0e779f56-385a-41be-a562-6f6908bf5acf@mathieu.dev.saucelabs.net:8842/rest/v1/admin/tunnels',
        'http://mathieu.dev.saucelabs.net:8842/rest/v1/info/counter',
        'http://mathieu.dev.saucelabs.net:8842/rest/v1/hello'
    ]

    for url in to_pawn:
        monocle.launch(p0wn, url)

    eventloop.run()
