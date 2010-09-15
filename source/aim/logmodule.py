import logging, sys, time

class StreamLogger(object):

    def __init__(self, stream, log, echo=True):
        self.stream = stream
        self.data = ''
        self.log = log
        self.echo = echo

    def write(self, data):
        if self.echo:
            self.stream.write(data)
            self.stream.flush()

        timestamp = time.strftime('%b%d-%H:%M')
        
        self.data += data
        tmp = str(self.data)
        if '\x0a' in tmp or '\x0d' in tmp:
            tmp = tmp.rstrip('\x0a\x0d')
            self.log.info('[%s] %s' % (timestamp, tmp))
            self.data = ''

        
        
def start_logging(filename, echo=True):
    """ Duplicate print statements to file.
    Slightly modified from last example in 
    http://stackoverflow.com/questions/616645/how-do-i-duplicate-sys-stdout-to-a-log-file-in-python
    
    
    Inputs:
        filename: Log filename to which output is always written
        echo: Determine if out should also be written to stdout. Default True.
    """

    print 'Logging to AIM logfile: %s\n' % filename
                            
    
    log = logging.getLogger('AIM')


    logging.basicConfig(level=logging.INFO,
                        filename=filename,
                        filemode='a')

    # Redirect stdout. 
    # Argument must be __stdout__ (the immutable version) in case redirection had taken place before                        
    sys.stdout = StreamLogger(sys.__stdout__, log, echo=echo)


    
