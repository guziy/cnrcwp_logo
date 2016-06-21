from mpl_toolkits.basemap import Basemap, maskoceans, interp
import numpy as np
import matplotlib.pyplot as plt
lon_0=-100
lat_0=65
resDpi=72


colorLine='k'
lWidth=4
h = 3000.

mlogo = Basemap(projection='nsper',lon_0=lon_0,lat_0=lat_0,satellite_height=h*1000.,resolution='c')
#mlogo = Basemap(height=16700000,width=12000000,resolution='l',area_thresh=1000.,projection='omerc', lon_0=-100,lat_0=15,lon_2=-120,lat_2=65,lon_1=-50,lat_1=-55)


mlogo.fillcontinents(color='black',lake_color='white')
#mlogo.drawcoastlines(color=colorLine,linewidth=lWidth )
#mlogo.drawparallels(np.linspace(-80,80,20), color=colorLine,linewidth=lWidth, dashes=[1,0])
#mlogo.drawmeridians(np.linspace(-180,180,10), color=colorLine,linewidth=lWidth)

# make up some data on a regular lat/lon grid.
#nlats = 73; nlons = 145; delta = 2.*np.pi/(nlons-1)
#lats = (0.5*np.pi-delta*np.indices((nlats,nlons))[0,:,:])
#lons = (delta*np.indices((nlats,nlons))[1,:,:])
#wave = 0.75*(np.sin(2.*lats)**8*np.cos(4.*lons))
#mean = 0.5*np.cos(2.*lats)*((np.sin(2.*lats))**2 + 2.)
# compute native map projection coordinates of lat/lon grid.
#x, y = mlogo(lons*180./np.pi, lats*180./np.pi)
# contour data over the map.
#cs = mlogo.contour(x,y,wave+mean,15,linewidths=lWidth)

plt.savefig('cnrcwpLogo.png', dpi=50)
