'''
Created on 17.08.2013

:author: Sebastian Illing
:contact: sebastian.illing@met.fu-berlin.de

Copyright (C) 2014  Sebastian Illing
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>
'''

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as N
from mpl_toolkits.basemap import Basemap, cm

from filehandler import FileHandler


class Plotter(object):
    
    
    colorDict =  {'red':   ((0., 0, 0),  (0.35, 0, 0),  (0.45, 1,1),(0.5, 1,1),(0.55, 1,1),(0.60, 0.1, 0.1), (0.65, 1.0, 1.0), (0.89,1, 1),(1, 0.5, 0.5)),
                  'green': ((0., 0, 0), (0.125,0, 0), (0.375,1, 1),(0.45, 1,1), (0.5, 1,1), (0.55, 1,1),(0.60,1, 1),(0.65,1,1),(0.91,0,0), (1, 0, 0)),
                  'blue':  ((0., 0.5, 0.5), (0.11, 1, 1), (0.34, 1, 1), (0.45, 1,1),(0.5, 1,1),(0.55, 1,1),(0.56,0, 0),(1, 0, 0))}
    
#    colorDict2 =  {'red':   ((0., 1, 1), (1, 1, 1)),
#                  'green': ((0., 1, 1), (1, 0.1, 0.1)),
#                  'blue':  ((0., 1, 1), (1, 0.1, 0.1))}
    
    colorDict2 = {'blue': ((0.0, 0.96862745285034180, 0.96862745285034180),
                           (0.2, 0.78039216995239258, 0.78039216995239258),
                           (0.4, 0.50980395078659058, 0.50980395078659058), 
                           (0.6, 0.30196079611778259, 0.30196079611778259), 
                           (0.8, 0.16862745583057404, 0.16862745583057404),
                           (1.0, 0.12156862765550613, 0.12156862765550613),),
                            
                  'green': ((0, 0.9686274528503418, 0.9686274528503418),
                            (0.2,0.85882353782653809, 0.85882353782653809),
                            (0.4,0.64705884456634521, 0.64705884456634521), 
                            (0.6,0.37647059559822083, 0.37647059559822083), 
                            (0.8,0.094117648899555206, 0.094117648899555206), 
                            (1.0, 0.0, 0.0)),
                            
                  'red': ((0, 0.9686274528503418, 0.9686274528503418),
                          (0.2, 0.99215686321258545, 0.99215686321258545),
                          (0.4, 0.95686274766921997, 0.95686274766921997),
                          (0.6, 0.83921569585800171, 0.83921569585800171),
                          (0.8, 0.69803923368453979, 0.69803923368453979),
                          (1.0, 0.40392157435417175, 0.40392157435417175))
                  }
    
    @staticmethod
    def plotField(fileName, vmin, vmax, colormap='goddard', output_folder='/', lonlatbox='-180,180,-90,90'):
        '''
        Plot any field variable
        
        :param fileName: filepath
        :param vmin: min value for colorbar
        :param vmax: max value for colorbar
        ''' 
        fig1 = plt.figure(figsize=(12,7),dpi=500)
        
        if(colormap == 'goddard'): 
            my_cmap = mpl.colors.LinearSegmentedColormap('my_colormap',Plotter.colorDict2,256)
        else:
            my_cmap = plt.cm.RdBu_r
        
        file_values = FileHandler.openNetCDFFile(fileName)
        mVar = file_values['variable']
        lon = file_values['lon']
        lat = file_values['lat']

        if lonlatbox is None:
            if lon[0] < 0:
                lonlatbox = '-180,180,-90,90'
            else:
                lonlatbox = '0,360,-90,90'
        lonlatbox = map(int,lonlatbox.split(','))
        m = Basemap(llcrnrlon=lonlatbox[0],llcrnrlat=lonlatbox[2],urcrnrlon=lonlatbox[1],urcrnrlat=lonlatbox[3])

        def divi(x):
            return float(x)/10
        
        colorSteps = map(divi,range(int(vmin*10),int((vmax*10)+1),1))#(vmax-vmin)/2))
        
        if vmax == 0.5:
            colorSteps = [-0.5, -0.45, -0.4, -0.35, -0.3, -0.25, -0.2, -0.15, -0.1, -0.05, 0, 
                          0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5]
            
        if vmax == 0. and vmin == -0.5:
            colorSteps = [-0.5, -0.475, -0.45, -0.425, -0.4, -0.375, -0.35, -0.325, -0.3, -0.275, -0.25, -0.225, 
                          -0.2, -0.175, -0.15, -0.125, -0.1, -0.075, -0.05, -0.025, 0]
            
        if vmax == 2. and vmin == 0:
            colorSteps = [0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9,0.95, 
                          1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0]
        colorTicks = colorSteps[0::2]
        my_cmap.set_bad("grey")                         #set missing value color
        #maskedArray = N.ma.masked_greater(mVar, 0.8e20) #mask missing Values
        maskedArray = N.ma.masked_outside(mVar, -0.8e20, 0.8e20)
        #discrete colormap
        norm = mpl.colors.BoundaryNorm(colorSteps, my_cmap.N)
        cs = m.imshow(maskedArray, interpolation="nearest", cmap=my_cmap, norm=norm)
        cb = m.colorbar(cs,"right", size="5%", pad='5%' , ticks=colorTicks)
        m.drawcoastlines()  
        m.drawparallels(N.arange(-90.,120.,30.),labels=[1,0,0,0]) # draw parallels
        m.drawmeridians(N.arange(0.,420.,60.),labels=[0,0,0,1]) # draw meridians
        
        plt.title(Plotter.__getTitle(fileName))
        plt.text(lonlatbox[0]+(lon[1]-lon[0])/2, lonlatbox[2]+(lat[1]-lat[0])/2, 'MurCSS')
        #print lonlatbox[0]+lon[1]-lon[0]
        return m
        #Plotter.saveFig(output_folder, fn)
     
    @staticmethod    
    def saveFig(output_folder, fn):
        
        plt.savefig(output_folder+fn+'.eps', format='eps')
        
    @staticmethod
    def addCrosses(map, sig_mask_x, sig_mask_y, marker='x', color='k', size=9):
        
        map.scatter(sig_mask_x, sig_mask_y, size, marker=marker,color=color)
    
    @staticmethod    
    def __getTitle(fn):    
        
        fn = fn.split('/')[-1]
        fn = fn.split('_')        
        title = ''
        length = 0
        for part in fn:
            title += part+'_'
            length += len(part)
            if length >= 60 or part == 'vs':
                title += '\n'
                length = 0
        return title
        
        
        
        
        
        
        
        