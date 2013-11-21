import time

import monocle

monocle.init("twisted")
from monocle.stack import eventloop
from monocle import _o, Return
from monocle.experimental import Channel

@_o
def p0wn(url, c):
    from monocle.stack.network.http import HttpClient, HttpHeaders
    from urlparse import urlparse
    from base64 import encodestring

    o = urlparse(url)
    client = HttpClient()

    print o
    try:
        yield client.connect(o.hostname, getattr(o, 'port', 80), scheme=o.scheme)
    except Exception:
        print "error", url
        yield Return("Error")

    if hasattr(o, 'username'):
        headers = HttpHeaders({
            "Authorization": "Basic %s" % encodestring("%s:%s" % (o.username, o.password))
        })

    i = 0
    mean = 0
    total = 0
    while True:
        then = time.time()
        res = yield client.request(o.path, headers=headers or None)
        now = time.time()

        i += 1
        duration = now - then
        total += duration
        mean = total / i

        c.send({'url': url, 'duration': duration, 'count': i, 'mean': mean})

@_o
def pprint(c):
    import os

    _all = {}

    then = time.time()
    while True:
        d = yield c.recv()
        _all[d['url']] = d

        if time.time() - then > 2.0:
            os.system('clear')
            then = time.time()
            for k, v in _all.items():
                print " %s -- %s -- %s for %s calls" % (k, v['duration'], v['mean'], v['count'])


if __name__ == '__main__':
    with open('to_pawn.txt') as f:
        p = f.read()

    to_pawn = p.split(',')

    c = Channel(32)
    monocle.launch(pprint, c)

    for url in to_pawn:
        monocle.launch(p0wn, url.strip(), c)

    eventloop.run()
