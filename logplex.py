import re
import dateutil.parser

class LogEntry:
    def __init__(self, line):
        # print line
        sep = line.split(' ')

        # print "\033[1m{}: {}\033[0m".format(len(sep), line)

        self.prival_version = sep[0]
        # print sep[1]
        self.time = dateutil.parser.parse(sep[1])
        # self.time = sep[1]
        self.hostname = sep[2]
        self.name = sep[3]
        self.procid = sep[4]
        self.msgid = sep[5]
        self.msg = ' '.join(sep[6:])

    @staticmethod
    def parse(data):
        pattern = '<\d+>\d+ \d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\d(.\d+)?[+-]\d\d:\d\d'
        s = [m.start() for m in re.finditer(pattern, data)]

        # s = re.search('<\d+>', line)
        # print "\033[1m{}\033[0m".format(s)

        r = []

        for i in s:
            for x in partition(data, s)[1:]:
                r.append(LogEntry(x.strip()))
                # app.logger.debug("{}: {}".format(l.time, l.msg))
        return r

def partition(alist, indices):
    return [alist[i:j] for i, j in zip([0]+indices, indices+[None])]
