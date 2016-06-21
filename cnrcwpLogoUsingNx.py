from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.font_manager import FontProperties
from mpl_toolkits.basemap import Basemap
import cnrcwpLogo
import matplotlib.pyplot as plt
import matplotlib.patheffects as peff

import networkx as nx

def main():

    lon_0 = -100
    lat_0 = 65
    resDpi = 72

    colorLine = 'k'
    lWidth = 4
    h = 3000.

    fig = plt.figure(figsize=(8.533, 3.333))
    assert isinstance(fig, Figure)
    print(fig.get_size_inches())

    mlogo = Basemap(projection='nsper', lon_0=lon_0, lat_0=lat_0, satellite_height=h * 600., resolution='l')
    #mlogo = Basemap(height=16700000,width=12000000,resolution='l',area_thresh=1000.,projection='omerc', lon_0=-100,lat_0=15,lon_2=-120,lat_2=65,lon_1=-50,lat_1=-55)


    mlogo.fillcontinents(color='black', lake_color='white')
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



    cities = cnrcwpLogo.create_cities(mlogo)


    ax = plt.gca()
    assert isinstance(ax, Axes)

    ax.set_anchor("NW")
    #write the text over
    txt = ax.annotate("CNRCWP", xy=(0.345, 0.48), xycoords="figure fraction",
                      font_properties=FontProperties(size=75, family="serif", weight="bold"), color="#21759b")

    #set stroke
    txt.set_path_effects([peff.withStroke(linewidth=3, foreground="#000000")])

    G = nx.Graph()
    for city in cities:
        G.add_node(city.name, )



    plt.tight_layout(pad=0.5)
    #plt.show()
    plt.savefig('cnrcwpLogo_nx.png', dpi=200, transparent=True)


if __name__ == "__main__":
    main()
