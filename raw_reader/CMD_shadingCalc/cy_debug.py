#!/usr/bin/env python

DEBUG_OFF           = 0
DEBUG_ERROR         = 1
DEBUG_WARNING       = 2
DEBUG_INFO          = 3

#--------------------------------------
# Class: DebugPrint
#--------------------------------------
class DebugPrint():
    """
    """
    def __init__(self, name='DP'):
        """
        """
        self.prefix = name
        self.level  = DEBUG_ERROR
        self.trace_en  = False

    def set_level(self, level):
        self.level = level

    def enable_trace(self, en):
        self.trace_en = en


    def error(self, *args):
        if self.level >= DEBUG_ERROR:
            s = 'Error@' + self.prefix + ': ' + (''.join(map(str, args)))
            print(s)

    def warning(self, *args):
        if self.level >= DEBUG_WARNING:
            s = 'Warning@' + self.prefix + ': ' + (''.join(map(str, args)))
            print(s)

    def info(self, *args):
        if self.level >= DEBUG_INFO:
            s = 'Info@' + self.prefix + ': ' + (''.join(map(str, args)))
            print(s)

    def trace(self, *args):
        if self.trace_en:
            s = 'Trace@' + self.prefix + ': ' + (''.join(map(str, args)))
            print(s)

#---------------------------------------------------------------
# Module Test
#---------------------------------------------------------------

def main():
    print('I am in!')
    dprint = DebugPrint('main')
    print('Setting debug level: DEBUG_WARNING')
    dprint.set_level(DEBUG_WARNING)

    dprint.info('You won\'t see this!!')
    dprint.error('a error')
    dprint.warning('a warning')



if __name__ == "__main__":
    main()
