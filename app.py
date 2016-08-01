from flask import Flask
from flask import request
from flask import make_response
# import json
import re
import redis
# import dateutil.parser

from logplex import LogEntry

app = Flask(__name__)

r = redis.StrictRedis(host='localhost', port=6379, db=0)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/logs", methods=['GET', 'POST'])
def logs():
    # app.logger.debug(request.data)
    # app.logger.debug("\033[1m{}\033[0m".format(request.data.strip().split('\n')))
    for line in request.data.strip().split('\n'):

        for entry in LogEntry.parse(line):
            app.logger.debug(entry.time)    

        # l = LogEntry(line)
        # app.logger.debug(l.time)
        # app.logger.debug(l.msg)

        pattern = '<\d+>\d+ \d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\d(.\d+)?[+-]\d\d:\d\d'
        s = [m.start() for m in re.finditer(pattern, line)]

        pattern2 = '<\d+>'
        s2 = [m.start() for m in re.finditer(pattern2, line)]

        if s != s2:
            r.incr('re_mismatch')
            app.logger.debug("expected: {}, actual: {}, string: '{}'".format(s2, s, line))
            app.logger.debug("\033[1mmismatches: {}\033[0m".format(count))

        # for i in s:
        #     for x in partition(line, s)[1:]:
        #         l = LogEntry(x.strip())
        #         app.logger.debug("{}: {}".format(l.time, l.msg))
        #         app.logger.debug(dateutil.parser.parse(l.time))

    # app.logger.debug(request.form)

    res = make_response()
    res.headers['Content-Length'] = '0'
    return res

# def partition(alist, indices):
#     return [alist[i:j] for i, j in zip([0]+indices, indices+[None])]

@app.route('/mismatches')
def get():
    m = r.get('re_mismatch')
    return "{}".format(m), 200

if __name__ == "__main__":
    app.debug = True
    app.run()
