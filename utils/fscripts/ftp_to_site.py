import ftplib
filepath,filename = args
ftp = ftplib.FTP('dicarlolab.tudelft.nl','ftp@dicarlolab.tudelft.nl','LLC#687')
pic = open(filepath,'rb') 
ftploc = "dicarlolab.tudelft.nl//html//wp-content//uploads//"
ftp.cwd(ftploc)
ftp.storbinary('STOR %s'%filename, pic) 