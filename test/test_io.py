from pyrocko import mseed, trace, util, io
from pyrocko.io import FileLoadError
import unittest
import numpy as num
import time
import tempfile
import random
from random import choice as rc
from os.path import join as pjoin
import os, sys
import shutil

import common

abc = 'abcdefghijklmnopqrstuvwxyz' 
    
def rn(n):
    return ''.join( [ random.choice(abc) for i in xrange(n) ] )

class IOTestCase( unittest.TestCase ):

    def testWriteRead(self):
        now = time.time()
        n = 10
        deltat = 0.1
        
        networks = [ rn(2) for i in range(5) ]
        
        traces1 = [ trace.Trace(rc(networks), rn(4), rn(2), rn(3), tmin=now+i*deltat*n*2, deltat=deltat, ydata=num.arange(n, dtype=num.int32), mtime=now)
            for i in range(3) ]
            
        tempdir = tempfile.mkdtemp()

        for format in ('mseed', 'sac', 'yaff'):
            fns = io.save(traces1, pjoin(tempdir, '%(network)s_%(station)s_%(location)s_%(channel)s'), format=format)

            for fn in fns:
                assert io.detect_format(fn) == format

            traces2 = []
            for fn in fns:
                traces2.extend(io.load(fn, format='detect'))
                
            for tr in traces1:
                assert tr in traces2, 'failed for format %s' % format
                
            for fn in fns:
                os.remove(fn)

        shutil.rmtree(tempdir)
        
    def testReadEmpty(self):
        tempfn = tempfile.mkstemp()[1]
        try:
            trs = list(mseed.iload(tempfn))
        except FileLoadError, e:
            pass
            
        assert str(e).find('No SEED data detected') != -1
        os.remove(tempfn)
    
    
    def testReadSac(self):
        fpath = common.test_data_file('test1.sac')
        tr = io.load(fpath, format='sac')[0]
        assert tr.meta['cmpaz'] == 0.0
        assert tr.meta['cmpinc'] == 0.0

    def testLongCode(self):
        c = '1234567'
        tr = trace.Trace(c,c,c,c, ydata=num.zeros(10))
        e = None
        try:
            io.save(tr, 'test.mseed')
        except mseed.CodeTooLong, e:
            pass

        assert isinstance(e, mseed.CodeTooLong)

    def testMSeedDetect(self):
        fpath = common.test_data_file('test2.mseed')
        io.load(fpath, format='detect')


if __name__ == "__main__":
    util.setup_logging('test_io', 'warning')
    unittest.main()

    
