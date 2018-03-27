import PIL
import PIL.Image as Image
import os
import gc
import PythonMagick
try:
    fdir, pformat = args
except:
    fdir = fdir
    pformat = pformat
flist = os.listdir(fdir)
for fil in flist:
    fpath = os.path.join(fdir,fil)
    try:
        if fpath[-3:] == 'pdf' or fpath[-3:] == 'PDF':
            print 'opening %s'%fpath[-3:]
            f = PythonMagick.Image(fpath)
            f.write(os.path.join(fdir,fil[:-3]+pformat))
            
        else:
            f = Image.open(fpath)
            f.save(os.path.join(fdir,fil[:-3]+pformat))
        del f
        gc.collect()
    except:
        print 'unknown format: %s, did not save %s'%(fil,os.path.join(fdir,fil[:-3]+pformat))
