import lib.utils
import ex.exceptions
modname = 'ds.pri_q_staq'
mod = lib.utils.fqdn_import(modname)
from ds.process import Process
p1 = Process(name = 'p1', pid = 1)
p2 = Process(name = 'p2', pid = 2)
p3 = Process(name = 'p3', pid = 3)
p4 = Process(name = 'p4', pid = 4)
mod.main(argv = dict(list = [p1, p2, p3, p4], entity = 'stack'))
mod.main(argv = dict(list = [p1, p2, p3, p4], entity = 'queue'))
