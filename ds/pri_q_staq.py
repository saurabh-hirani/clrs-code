#!/usr/bin/env python

DEBUG = 0

import sys

import ex.exceptions
from ds.pri_q import Max_Pri_Queue

elem_key_map = {}
DEBUG = 0

def inc_numgen(limit):
    for num in xrange(1, limit + 1):
        yield num

def dec_numgen(limit):
    for num in xrange(1, limit + 1):
        yield num * -1

def get_elem_id(elem):
    try:
        id = elem.id()
    except AttributeError:            
        id = elem
    return id

def get_elem_key(elem_id):
    global elem_key_map
    key = elem_key_map[get_elem_id(elem_id)]
    return key

def gen_key(elem_id, key_generator):
    global elem_key_map
    key = key_generator.next()
    elem_key_map[elem_id] = key
    return key

def extractor(runq, elemclass):
    q_iter = runq.get_iter()
    elemlist = []
    while (1):
        try:
            id = q_iter.next()
            try:
                elem = elemclass.cache(id)
            except AttributeError:
                elem = id
            elemlist.append(str(elem))
        except StopIteration:
            break
    return ' '.join(elemlist)

def inserter(runq, elemlist, entity): 
    if entity == 'stack':
        key_generator = inc_numgen(len(elemlist))
    else:
        key_generator = dec_numgen(len(elemlist))
    for elem in elemlist:
        elem_id = get_elem_id(elem)
        print "inserting " + str(elem)
        gen_key(elem_id, key_generator)
        runq.insert(elem_id)
    return len(elemlist)

def get_parser():
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-l", "--list", dest="list",
                      help="List of elements to insert")
    parser.add_option("-d", "--debug", dest="debug",
                       default=DEBUG, help="Turn debugging on/off")
    parser.add_option("-e", "--entity", dest="entity",
                      help="stack|queue")
    return parser

def parse_cmdline_args(parser):
    (options, args) = parser.parse_args()
    try:
        if (options.list is None):
            raise ex.exceptions.NoArgError('No list provided') 
        if (options.entity is None):
            raise ex.exceptions.NoArgError('No entity provided') 
        if (options.entity != 'stack' and options.entity != 'queue'):
            raise ex.exceptions.BadArgError(
                'entity - Invalid val - ' + str(options.entity) +\
                ' provided'
            ) 
    except ex.exceptions.ValidationError as e:
        print e
        parser.print_help()
        raise
    return dict(
        list = options.list,
        entity = options.entity,
        debug = options.debug
    )

def parse_call_args(argv):
    global DEBUG
    try:
        mand_args = ['list', 'entity']
        for arg in mand_args:
            if arg not in argv:
                raise ex.exceptions.NoArgError('No ' + arg +\
                                               ' provided') 
        if 'debug' not in argv:
            argv['debug'] = DEBUG
        if (argv['entity'] != 'stack' and argv['entity'] != 'queue'):
            raise ex.exceptions.BadArgError(
                'entity - Invalid val - ' + argv['entity'] +\
                ' provided'
            ) 
    except ex.exceptions.ValidationError as e:
        print e
        raise
    return dict(
        list = argv['list'],
        entity = argv['entity'],
        debug = argv['debug']
    )

def main(argv=None):
    input = {}
    if argv is None:
        parser = get_parser()
        try:
            input = parse_cmdline_args(parser)
        except ex.exceptions.ValidationError:
            return(2)
        import re
        elemlist = re.split(r'\s+', input['list'].strip()) 
        del re
    else:
         try:
             input = parse_call_args(argv)
         except ex.exceptions.ValidationError:
            return(2)
         elemlist = input['list']

    cmprator = lambda x,y: get_elem_key(x) - get_elem_key(y)
    runq = Max_Pri_Queue(
        elem_key_handler = get_elem_key,
        cmprator = cmprator,
        debug = input['debug']
    )
    inserter(runq, elemlist, input['entity'])
    print "extracted [" + str(extractor(runq, elemlist[0].__class__)) + "]"
        
if __name__ == "__main__":
    sys.exit(main())
