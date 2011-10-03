#!/usr/bin/env python

import ex.exceptions
import lib.utils
import sys
import lib.dumper

from optparse import OptionParser

def main():
    parser = OptionParser()
    parser.add_option("-t", "--target", dest="target",
                      help="the target to convert")
    parser.add_option("-s", "--src", dest="src",
                      help="target source")
    parser.add_option("-d", "--dest", dest="dest",
                      help="target dest")
    parser.add_option("-l", "--list", dest="list",
                      default = False,
                      help="list out the valid conversions")

    (options, args) = parser.parse_args()

    valid_conversions = lib.utils.get_valid_num_conversions()

    if (options.list is not False):
        print "valid number conversions are:"
        print(dumper.dump(valid_conversions))
        return(0)

    if (options.target is None):
        raise ex.exceptions.NoArgError("no target provided")

    target = options.target

    if (options.src is None):
        raise ex.exceptions.NoArgError("no src provided")
    if options.src not in valid_conversions:
        raise ex.exceptions.BadArgError("invalid source " +\
                                          options.src)

    src = options.src

    if (options.dest is None):
        raise ex.exceptions.NoArgError("no dest provided")

    valid_dests = valid_conversions[src].keys()

    if not options.dest in valid_dests:
        raise ex.exceptions.NoArgError("invalid dest " +\
                                         options.dest)

    dest = options.dest
    callback = valid_conversions[src][dest]['converter']
    try:
        converted_src = callback(target)
        if 'formatter' in valid_conversions[src][dest]:
            formatter = valid_conversions[src][dest]['formatter']
            converted_src = formatter(converted_src)
        print converted_src
    except ex.exceptions.ValidationError as e:
        print e
        return(2)

if __name__ == "__main__":
    sys.exit(main())
