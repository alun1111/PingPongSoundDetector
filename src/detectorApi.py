from threading import Thread
from flask import Flask

import datetime

from nocache import nocache
from tapsensor import TapTester

TIMEGROUPING = 5

app = Flask(__name__)
tt = TapTester()


@app.after_request
def add_header(r):
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


@app.route('/')
@nocache
def getLastNoise():
    delta = datetime.datetime.now() - tt.lastTap
    if delta.seconds > TIMEGROUPING:
        return app.send_static_file('soundTrueLookTrue.html')
    else:
        return app.send_static_file('soundFalseLookTrue.html')


def webApi():
    app.run(host='0.0.0.0')


# --------------------------------- END

# --------------------------------- RUNTHATSHIT

if __name__ == "__main__":
    t = Thread(target=webApi, args=[])
    t.start()
    while 1 == 1:
        tt.listen()
    t.end
