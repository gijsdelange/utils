# Prints information about a data file, especially on blocks
# args: Data

import qt
from qt import Data
data, = args

print 'Name:',data.get_time_name()
print 'Timestamp:',data._timemark
print 'npoints:',data.get_npoints()
print 'npoints max block:', data.get_npoints_max_block()
print 'npoints last block:',data.get_npoints_last_block()
print 'nblocks:',data.get_nblocks()
print 'block sizes:',data._block_sizes
print 'nblocks*block sizes:',(data.get_nblocks() *data.get_npoints_last_block())
print ''