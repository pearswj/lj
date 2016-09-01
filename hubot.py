import re

class Entry:
    def __init__(self, time, level, msg):
        self.time = time
        self.level = level
        self.msg = msg

    def __str__(self):
        return "[{}] {} {}".format(self.time, self.level, self.msg)

_pattern = '^\[(.*?)\] ([A-Z]+) (.*)$'
_re_hubot = re.compile(_pattern)

def parse(data):
    """Processes a log message and attempts to return a hubot log entry."""
    m = _re_hubot.match(data)
    if m:
        time, level, msg = m.groups()
        return Entry(time, level, msg)
    else:
        return None
