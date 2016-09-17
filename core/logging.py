from datetime import datetime


class LoggingMixIn:

    def write_log(self, s):

        with open('logs.txt', 'a') as f:
            s = '{0} -- {1}'.format(datetime.now(), s)
            f.write(s+'\n')

