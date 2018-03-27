#!/usr/bin/env python
# -*- noplot -*-

"""

This example shows how to use matplotlib to provide a data cursor.  It
uses matplotlib to draw the cursor and may be a slow since this
requires redrawing the figure with every mouse move.

Faster cursoring is possible using native GUI drawing, as in
wxcursor_demo.py
"""
from __future__ import print_function
from pylab import *
ax,data = args
import numpy as np

class Cursor:
    def __init__(self, ax,data):
        self.ax = ax
        xlim = plt.xlim()
        ylim=plt.ylim()
        if len(data)==2:
            self.coords = data[0]
            self.vals = data[1]
        else:
            self.coords=data[0],data[1]
            self.vals=data[2]
        self.lx = ax.axhline(color='k')  # the horiz line
        self.ly = ax.axvline(color='k')  # the vert line
        self.xvalst =(self.coords[0][0,1:]+self.coords[0][0,:-1])/2.
        self.yvalst =(self.coords[1][1:,0]+self.coords[1][:-1,0])/2.
        self.x = []#[-0.512,-0.498]
        self.y =[]#[13.15,12.05]
        self.z = []
        self.mx = []
        self.my = []
        # self.cx = self.x[-1]
        # self.cy = self.y[-1]
        # text location in axes coords
        self.txt = ax.text( 0.7, 0.9, '', transform=ax.transAxes)
        self.txt.set_color('0.5')
        self.ranxy = [1,1]
        print (xlim,ylim)
        self.line = plt.plot([],[],'w-o')[0]
        self.mline = plt.plot([],[],'r-o')[0]
        plt.xlim(xlim)
        plt.ylim(ylim)
        self.deactivated = False
        self.name = 'Cursor1'
    def key_press(self, event):
        if (not event.inaxes) or self.deactivated: 
            print ('cursor %s deactivated'%self.name)
            return
        
        if event.key =='a':
            xi = self.get_coord_position(self.cx,self.xvalst)
            yi = self.get_coord_position(self.cy,self.yvalst)
            self.cx = self.xvalst[xi]
            self.cy = self.yvalst[yi]
            self.cz = self.vals.transpose()[xi,yi]
            #print (self.cx,self.cy)
            self.x += [self.cx]
            self.y += [self.cy]
            self.z += [self.cz]
            self.txt.set_text( 'x=%1.5f, y=%1.5f, z = %1.5f'%(self.cx,self.cy, self.cz))
            self.txt.set_color('k')
            #self.sortxy()
            self.line.set_xdata(self.x)
            self.line.set_ydata(self.y)
            
        elif event.key == 'm':
            xi,yi = self.x[-1],self.y[-1]
            #self.test = [xi,yi]
            xi=self.get_coord_position(xi,self.xvalst)
            yi=self.get_coord_position(yi,self.yvalst)
            self.test0 = [xi,yi]
            x,y, maxval = self.find_local_maximum(xi,yi,self.vals.transpose(),self.ranxy)
            self.test1 = [x,y]
            self.test2 = (self.xvalst[x],self.yvalst[y])
            self.mx += [self.xvalst[x]]
            self.my += [self.yvalst[y]] 
            self.mline.set_xdata(self.mx)
            self.mline.set_ydata(self.my)
            
        elif event.key=='d':
            if len(self.x) ==1:
                self.x=[]
                self.y=[]
            else:
                self.x = self.x[:-1]
                self.y = self.y[:-1]
                self.z = self.z[:-1]
                self.cx = self.x[-1]
                self.cy = self.y[-1]
                self.txt.set_text( 'x=%1.4f, y=%1.4f'%(self.cx,self.cy))
                self.txt.set_color('k')
            self.line.set_xdata(self.x)
            self.line.set_ydata(self.y)
        elif event.key=='u':
            self.line.set_xdata(self.x)
            self.line.set_ydata(self.y)
        elif event.key=='x':
            dist = np.abs((self.x[0] - self.cx)**2+(self.y[0] - self.cy)**2)
            xloc = 0
            #print (len(self.x),dist)
            for kk in range(1,len(self.x)):
                disti = np.sqrt((self.x[kk] - self.cx)**2+(self.y[kk] - self.cy)**2)
                if disti<dist:
                    dist = disti
                    xloc = kk
                    #print ('min at',kk)
            xind = xloc
            #print (xind)
            self.x[xind]=self.cx
            self.y[xind]=self.cy
            self.line.set_xdata(self.x)
            self.line.set_ydata(self.y)
            #print 'replacing %s with %s'%(x,self.cx)
            #self.txt.set_text( 'x=%1.4f, y=%1.4f'%(self.cx,self.cy))
        
        elif event.key =='u':
            self.line.set_xdata(self.x)
            self.line.set_ydata(self.y)
        
        
        draw()    
    def get_diff(self):
        dx = np.gradient(self.x)
        dy = np.gradient(self.y)
        return dy/dx
    
    def find_local_maximum(self,xi,yi,z,ranxy):
        [rx,ry]=ranxy
        miny, minx = np.clip([yi-ry,xi-rx],0,np.inf)
        if rx == 0:
            #print ('rx =0')
            maxval = np.max(z[xi,miny:yi+ry])
            y = np.where(z[xi,miny:yi+ry] == maxval)[0][0]
            
            x = 0
        elif ry ==0:
            maxval = np.max(z[minx:xi+rx,yi])
            x = np.where(z[minx:xi+rx,yi]== maxval)[0][0]
            
            y = 0
        else:
            maxval = np.max(z[minx:xi+rx,miny:yi+ry])
            [x],[y] = np.where(z[minx:xi+rx,miny:yi+ry] == maxval)
            
        #print ('maxpos: ',x,y)
        return minx+x, miny+y, maxval
    def get_coord_position(self,value,drange):
        dd = (drange[1]-drange[0])/2.
        try:
            corval = np.abs(np.diff(drange+dd>value)).tolist().index(1)+1
        except:
            if np.sum(drange>value)==0:
                corval = drange.tolist().index(np.max(drange))
            else:
                corval = drange.tolist().index(np.min(drange))
        return corval
        
    def get_linecut(self):
        xcors = [self.x[0],self.x[-1]]
        ycors = [self.y[0],self.y[-1]]
        xvalst =(self.coords[0][0,1:]+self.coords[0][0,:-1])/2.
        yvalst =(self.coords[1][1:,0]+self.coords[1][:-1,0])/2. 
        z = self.vals
        self.xvalst = xvalst
        self.yvalst = yvalst
        xrange = np.arange(len(xvalst),dtype='int')
        yrange = np.arange(len(yvalst),dtype='int')
        mixc,maxc = np.min(xcors),np.max(xcors)
        if xcors[0]<xcors[1]:
            xorder=1
            mixc,maxc = np.min(xcors),np.max(xcors)
        else:
            xorder=-1
            mixc,maxc = np.max(xcors), np.min(xcors)
        if ycors[0]<ycors[1]:
            yorder=1
            miyc,mayc = np.min(ycors),np.max(ycors)
        else:
            yorder=-1
            miyc,mayc = np.max(ycors),np.min(ycors)
        
        
        xsta = self.get_coord_position(mixc,xvalst)#np.abs(np.diff(xvalst>mixc)).tolist().index(1)
        xsto = self.get_coord_position(maxc,xvalst)#np.abs(np.diff(xvalst>maxc)).tolist().index(1)
        #print (xsta,xsto)
        
        xvalsi = np.array(np.linspace(xsta,xsto,np.abs(xsta-xsto)+1),dtype=int)
        #print (np.diff(yvalst>miyc))
        
        ysta = self.get_coord_position(miyc,yvalst)#np.abs(np.diff(yvalst>miyc)).tolist().index(1)
            
        ysto = self.get_coord_position(mayc,yvalst)#np.abs(np.diff(yvalst>mayc)).tolist().index(1)
        yvalsi = np.array(np.linspace(ysta,ysto,np.abs(ysta-ysto)+1),dtype=int)
        #print (ysta,ysto)
        self.xvalsi =xvalsi
        self.yvalsi=yvalsi
        
        #print (xvalst[0],xcors[1])
        nx = len(xvalsi)
        ny = len(yvalsi)
        print ('nx,ny',nx==0,nx)
        if nx==1:
            print ('cut along x, ny = ',ny)
            #xvalsi = [np.abs(np.diff(xvalst>mixc))] # xindices
        elif ny==1:
            print ('cut along y, nx = ',nx)
            #yvalsi = [np.abs(np.diff(yvalst>miyc))]# yindices
        else:
            print ('nx, ny: ',nx,ny)
        
        if nx>ny:
            xinds = np.array(xvalsi)
            yinds = np.array(yvalsi)
            transp=False
            z=z.transpose()
        elif ny>nx:
            transp = True
            xinds = np.array(yvalsi)
            yinds = np.array(xvalsi)
            
        npoints = len(xinds)
        #print ('2',yinds[[0,-1]],xinds[[0,-1]],transp)
        [yistart,yistop] = yinds[[0,-1]]
        if len(yinds)>1:
            
            zvals = []
            yindsf = np.linspace(yistart,yistop,npoints)
            
            for kk in range(npoints):
                yif = yindsf[kk]
                yind1,yind2 = np.int(np.ceil(yif)),np.int(np.floor(yif))
                if yind1==yind2:
                    w1=0.5
                    w2=0.5
                else:
                    w1,w2 = np.abs(yif-yind1),np.abs(yif-yind2)
                #print (yind1,yind2,yif,kk,w1,w2)
                zval = w1*z[xinds[kk],yind1]+w2*z[xinds[kk],yind2]
                zvals+=[zval]
            
        else:
            #print ('yinds: ',len(yinds[0]),'len: ',len(yvalst))
            zvals = z[xinds,yinds[0]]
            yvalsr = yvalst[yinds[0]]
        if transp:
            
            xvalsr = np.linspace(xvalst[yistart],xvalst[yistop],npoints)
            yvalsr = yvalst[xinds]
            
            
        else:
            yvalsr = np.linspace(yvalst[yistart],yvalst[yistop],npoints)
            xvalsr = xvalst[xinds]
        cf = plt.gcf().get_label()
        
        plt.figure('linecut')
        plt.clf()
        plt.subplot(211)
        plt.plot(xvalsr,zvals)
        plt.title('x-cut')
        plt.subplot(212)
        plt.plot(yvalsr,zvals)
        plt.title('y-cut')
        plt.figure(cf)
        return xvalsr,yvalsr,zvals
        
    
        
    def button_press(self, event):
        if not event.inaxes: return

        x, y = event.xdata, event.ydata
        # update the line positions
        self.lx.set_ydata(y )
        self.ly.set_xdata(x )
        self.cx = x
        self.cy = y
        self.txt.set_text( 'x=%1.4f, y=%1.4f'%(x,y))
        self.txt.set_color('0.5')
        draw()
    def sortxy(self):
        sxs = np.sort(self.x)
        ind = []
        for sx in sxs:
            ind+=[self.x.index(sx)]
        self.x= np.array(self.x)[ind].tolist()
        self.y= np.array(self.y)[ind].tolist()
        self.line.set_xdata(self.x)
        self.line.set_ydata(self.y)
        draw()
class SnaptoCursor:
    """
    Like Cursor but the crosshair snaps to the nearest x,y point
    For simplicity, I'm assuming x is sorted
    """
    def __init__(self, ax, x, y):
        self.ax = ax
        self.lx = ax.axhline(color='k')  # the horiz line
        self.ly = ax.axvline(color='k')  # the vert line
        self.x = []
        self.y = []
        # text location in axes coords
        self.txt = ax.text( 0.7, 0.9, '', transform=ax.transAxes)

    def mouse_move(self, event):

        if not event.inaxes: return

        x, y = event.xdata, event.ydata

        indx = searchsorted(self.x, [x])[0]
        x = self.x[indx]
        y = self.y[indx]
        # update the line positions
        self.lx.set_ydata(y )
        self.ly.set_xdata(x )

        self.txt.set_text( 'x=%1.2f, y=%1.2f'%(x,y) )
        print ('x=%1.2f, y=%1.2f'%(x,y))
        self.xy = x,y
        draw()



cursor = Cursor(ax,data)
#cursor = SnaptoCursor(ax, t, s)
connect('key_press_event', cursor.key_press)
connect('button_release_event', cursor.button_press)
set_return(cursor)
