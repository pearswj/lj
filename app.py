from flask import Flask
from flask import request
from flask import make_response
# import json
import redis
import re

import logplex, hubot

app = Flask(__name__)

r = redis.StrictRedis(host='localhost', port=6379, db=0)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/logs", methods=['GET', 'POST'])
def logs():
    # TODO: check Content-Type header ('application/logplex-1')
    for line in request.data.strip().split('\n'):
        # TODO: check Logplex-Msg-Count header (`msgs.length`?)
        for entry in logplex.parse(line):
            # app.logger.debug("{}: {}".format(entry.time, entry.msg))
            # app.logger.debug(entry)
            # app.logger.debug(entry.is_hubot)
            # if entry.is_hubot:
            h = hubot.parse(entry.msg)
            if h:
                key = "log:{}:{}".format(h.level.lower(), entry.timestamp)
                # app.logger.debug(key)
                r.incr(key)
                r.expire(key, 604800)
            # if entry.name == "app" and re.match("Error", entry.msg):
            if re.match(".*Error", entry.msg):
                app.logger.info(entry)
                i = r.incr("log:count:error")
                r.set("log:detail:error:" + str(i), entry)
            # TODO: do something

    res = make_response()
    res.headers['Content-Length'] = '0'
    return res

@app.route('/get')
def get():
    keys = r.keys("log:*")
    a = []
    for k in keys:
        m = re.match('^log:error:([0-9]+)$', k)
        if m:
            a.append("{},{}".format(m.group(1), r.get(k)))
    return '\n'.join(a), 200

if __name__ == "__main__":
    app.debug = True
    app.run()
