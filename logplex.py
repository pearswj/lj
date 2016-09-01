import re
import dateutil.parser
import calendar

class Entry:
    def __init__(self, data):
        sep = data.split(' ')

        self.prival_version = sep[0]
        self.time = dateutil.parser.parse(sep[1])
        self.hostname = sep[2]
        self.name = sep[3]
        self.procid = sep[4]
        self.msgid = sep[5]
        self.msg = ' '.join(sep[6:])

        self.timestamp = calendar.timegm(self.time.utctimetuple())

    # @property
    # def is_hubot(self):
    #     return bool(re.search('^\[.*?\] [A-Z]+', self.msg))

    def __str__(self):
        return "{} {}[{}]: {}".format(self.time, self.name, self.procid, self.msg)

def parse(data):
    """Processes logplex data and returns a list of log entries."""
    return [Entry(x.strip()) for x in _split_msgs(data)[1:]]

def _partition(alist, indices):
    return [alist[i:j] for i, j in zip([0]+indices, indices+[None])]

_pattern = '<\d+>\d+ \d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\d(.\d+)?[+-]\d\d:\d\d'
_re_logplex = re.compile(_pattern)

def _split_msgs(string):
    s = [m.start() for m in _re_logplex.finditer(string)]

    return _partition(string, s)
