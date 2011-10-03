#!/usr/bin/env python
import random
import timeit
import sys

import lib.utils

def_numrange = 100
def_ntimes = 100
def_vals = dict(
    numrange = def_numrange,
    ntimes = def_ntimes,
)

class ValidationError(Exception): pass

class Timewrapper:
    def __init__(self, sortfunc, ntimes=def_vals['ntimes'], numrange=def_vals['numrange']):
        self.sortfunc = sortfunc
        self.ntimes = ntimes
        self.numrange = numrange
        self.dataset_idx = -1
        l = range(self.numrange)
        random.shuffle(l)
        self.list = l

    def gen_dataset(self):
        self.dataset = []

        import time;
        count = 0
        time_last_print = time_now = time.time()
        l = range(self.numrange)
        while count < self.ntimes:
            random.shuffle(l)
            self.dataset.append(l)
            time_now = time.time()
            if (time_now - time_last_print > 1):
                sys.stdout.write("\r")
                sys.stdout.write("Generated "+str(count)+ "/" + \
                                 str(self.ntimes))
                sys.stdout.flush()
                time_last_print = time.time()
            count += 1
        sys.stdout.write("\r")
        sys.stdout.write("Generated "+str(count)+ "/" + str(self.ntimes))
        sys.stdout.write("\n")

    def do_sort(self):
        self.dataset_idx += 1
        if (self.dataset_idx == self.ntimes):
            self.dataset_idx = 0 
        return self.sortfunc(self.dataset[self.dataset_idx])

def bench_my_sorts(sortfunc, **kwargs):
    curr_vals = dict(def_vals)
    curr_vals.update(kwargs)

    timewrapper_obj = Timewrapper(sortfunc, curr_vals['ntimes'], curr_vals['numrange'])
    print "Generating dataset..."
    timewrapper_obj.gen_dataset()
    print "Generated dataset..."
    t1 = timeit.Timer(timewrapper_obj.do_sort)
    info = "\nnumrange  - " + str(curr_vals['numrange']) + \
           "\nntimes - " + str(curr_vals['ntimes'])
    print "benchmarking "+ info
    print t1.timeit(curr_vals['ntimes'])

def bench_py_sort(numrange):
    l = range(numrange)
    random.shuffle(l)
    l.sort()

def get_cmdline_args():
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-m", "--module", 
                      dest="module", 
                      help="module whose do_sort method is to be called");
    parser.add_option("-R", "--numrange", 
                      dest="numrange", 
                      default=def_numrange,
                      help="range upto which nos. are to be sorted");
    parser.add_option("-n", "--ntimes", 
                      dest="ntimes", 
                      default=def_ntimes,
                      help="call the module.do_sort function ntimes");

    (options, args) = parser.parse_args()

    if options.module is None:
        sys.stderr.write("Provide module whose sort routine " +\
                         "is to be checked\n")
        parser.print_help()
        raise ValidationError

    for opt,optval in dict(numrange = options.numrange, ntimes = options.ntimes).items():
        if not lib.utils.is_number(optval):
            sys.stderr.write("Invalid value provided for " +\
                             opt + " - " + str(optval) + "\n")
            parser.print_help()
            raise ValidationError

    try: 
        mod = lib.utils.fqdn_import(options.module)
    except ImportError:
        sys.stderr.write("Failed to import module " + options.module +"\n")
        parser.print_help()
        raise ValidationError

    return dict(numrange = int(options.numrange), 
                ntimes = int(options.ntimes),
                module = mod)

def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        params = get_cmdline_args()
    except ValidationError:
        return(2)

    bench_my_sorts(params['module'].do_sort,
                   ntimes = params['ntimes'],
                   numrange = params['numrange'])


if __name__ == "__main__":
    sys.exit(main())
