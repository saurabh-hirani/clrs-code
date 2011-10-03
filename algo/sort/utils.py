#!/usr/bin/env python

import lib.utils
import ex.exceptions

DEBUG = 0 # debug switch for all sort prog. overridden by cmdline
REC_INDENT = 0

def get_cmdline_parser():
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-l", "--list", dest="list",
                      help="List of elements to sort")
    parser.add_option("-d", "--debug", dest="debug",
                      default=DEBUG, help="Turn debugging on/off")
    return parser

def validate_call_args(argv):
    """ validate user supplied args when direct function call """
    if type(argv) is not type({}):
        raise ex.exceptions.BadArgError('Invalid call args ' +\
                                          'supplied')
    if not 'list' in argv:
        raise ex.exceptions.BadArgError("Call args don't have " +\
                                          "'list' key")
    global DEBUG
    global REC_INDENT

    if not 'debug' in argv:
        argv['debug'] = DEBUG

def parse_cmdline_args(parser):
    (options, args) = parser.parse_args()
    if (options.list is None):
        raise ex.exceptions.NoArgError('No list provided')
    return dict(list = options.list, 
                debug = options.debug)

def build_args(argv=None):
    from_cmdline = False
    parser = None

    if argv is None:
        from_cmdline = True

    if from_cmdline:
        try:
            parser = get_cmdline_parser()
            input = parse_cmdline_args(parser)
        except ex.exceptions.ValidationError as e :
            print e
            parser.print_help()
            raise
    else:
        try:
            validate_call_args(argv)
        except ex.exceptions.ValidationError as e:
            print e
            raise
        print input

    import re
    elemlist = re.split(r'\s+', input['list'].strip())
    del re

    try:
        lib.utils.xform_list(elemlist)
    except ex.exceptions.ValidationError as e:
        print e
        if from_cmdline: parser.print_help()
        raise

    return dict(list = elemlist, 
                debug = input['debug'])
