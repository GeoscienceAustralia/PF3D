import logging, sys, time

class StreamLogger(object):

    def __init__(self, stream, log):
        self.stream = stream
        self.data = ''
        self.log = log

    def write(self, data):
        self.stream.write(data)
        self.stream.flush()

        timestamp = time.strftime('%b%d-%H:%M')
        
        self.data += data
        tmp = str(self.data)
        if '\x0a' in tmp or '\x0d' in tmp:
            tmp = tmp.rstrip('\x0a\x0d')
            self.log.info('[%s] %s' % (timestamp, tmp))
            self.data = ''

        
        
def start_logging(filename):
    """ Duplicate print statements to file.
    Slightly modified from last example in 
    http://stackoverflow.com/questions/616645/how-do-i-duplicate-sys-stdout-to-a-log-file-in-python
    """

    log = logging.getLogger('AIM')


    logging.basicConfig(level=logging.INFO,
                        filename=filename,
                        filemode='a')

    sys.stdout = StreamLogger(sys.__stdout__, log) # Redirect stdout. Input must be __stdout__ in case redirection had taken place before

    print 'Logging to AIM logfile: %s\n' % filename
    
