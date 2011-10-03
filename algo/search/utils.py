#!/usr/bin/env python

import lib.utils
import ex.exceptions

DEBUG = 0 # debug switch for all search prog. overridden by cmdline

def get_cmdline_parser():
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-l", "--list", dest="list",
                      help="List of elements to search from")
    parser.add_option("-t", "--target", dest="target",
                      help="Target element to search")
    parser.add_option("-s", "--strategy", dest="strategy",
                      default=None,
                      help="left|right - search leftmost," +\
                           " search rightmost, not provided - "+\
                           " search first found")
    parser.add_option("-d", "--debug", dest="debug",
                      default=DEBUG, help="Turn debugging on/off")
    return parser

def validate_call_args(argv):
    if type(argv) is not type({}):
        raise ex.exceptions.BadArgError('Invalid call args ' +\
                                          'supplied')
    for mand_key in ['list', 'target']:
        if not mand_key in argv:
            errmsg = "Call args don't have '" + mand_key + "' key"
            raise ex.exceptions.BadArgError(errmsg)
    def_vals = {
        'debug' : 0,
        'strategy' : None,
    }        
    argv.update(def_vals);
    if 'strategy' in argv:
        val = argv['strategy']
        if not (val == 'left' or val == 'right'):
            errmsg = "Invalid value specified for 'strategy'"
            raise ex.exceptions.BadArgError(errmsg)


def parse_cmdline_args(parser):
    (options, args) = parser.parse_args()

    if (options.list is None):
        raise ex.exceptions.NoArgError('No list provided')
    if (options.target is None):
        raise ex.exceptions.NoArgError('No target elem provided')
    if (options.strategy is not None):
        if not (options.strategy == 'left' or\
                options.strategy == 'right'):
            errmsg = "Invalid value specified for 'strategy'"
            raise ex.exceptions.BadArgError(errmsg)

    return dict(list = options.list, 
                target = options.target,
                strategy = options.strategy,
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
        lib.utils.xform_list(elemlist, xformer=int)
    except ex.exceptions.ValidationError as e:
        print e
        if from_cmdline: parser.print_help()
        raise

    target = input['target']

    try:
        target = lib.utils.xform_elem(target)
    except ex.exceptions.ValidationError as e:
        print e
        if from_cmdline: parser.print_help()
        raise

    return dict(list = elemlist, 
                target = target,
                strategy = input['strategy'],
                debug = input['debug'])
