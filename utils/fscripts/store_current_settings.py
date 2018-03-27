# store_settings
import os
import qt
filepath, = args
_dir,_fname = os.path.split(filepath)
tempdat = qt.Data()
tempdat._filename = _fname
tempdat._dir = _dir
print '5',tempdat.get_settings_filepath()

tempdat._write_settings_file()
