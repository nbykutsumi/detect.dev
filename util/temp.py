from numpy import *
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
#******************************************
BBox = [[30,130],[60,150]]
[lllat,lllon],[urlat,urlon] = BBox

a1lat= array([-60,0,60])
a1lon= arange(0,350+10,60)

a1LAT = r_[ array([-90.0]), (a1lat[1:] + a1lat[:-1])*0.5, array([90.0 ])]
a1LON = r_[ array([0.0]),   (a1lon[1:] + a1lon[:-1])*0.5, array([360.0])]

X, Y = meshgrid(a1LON, a1LAT)
Z    = Y

fig  = plt.figure()
ax   = fig.add_axes([0.1,0.1,0.8,0.8])

M    = Basemap( resolution="l", llcrnrlat = lllat, llcrnrlon=lllon, urcrnrlat=urlat, urcrnrlon=urlon, ax=ax)
im   = M.pcolormesh(X,Y,Z)
M.drawcoastlines()
plt.colorbar(im)
#ax.pcolor(X,Y,Z)
show()


