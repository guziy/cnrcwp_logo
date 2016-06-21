from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.font_manager import FontProperties
from mpl_toolkits.basemap import Basemap, maskoceans, interp
import numpy as np

import matplotlib.patheffects as peff
import matplotlib.pyplot as plt


# The points are named after the cities, although they do not really coincide geographically
cityname_to_lon_lat = {
    "Montreal": (-73.5550, 45.5081),
   #  "Toronto": (-79.4042, 43.6481),
    "Victoria": (-123.3347, 48.4328),
    "Waterloo": (-80.5361, 43.4706),
    "Saskatoon": (-106.6353, 52.1311),
    "Calgary": (-115.0669, 55.0544),
    "UNBC": (-112.7502, 60.9136)
}

name_to_city = {}

connector_color = "w"
mark_color = "w"


class City:
    def __init__(self, name, lon, lat):
        self.name = name
        self.lon = lon
        self.lat = lat
        self.basemap = None
        self.x = None
        self.y = None


    def set_basemap(self, basemap=None):
        self.x, self.y = basemap(self.lon, self.lat)
        self.basemap = basemap


def create_cities(theBasemap):
    cities = []
    global name_to_city
    for name, point in cityname_to_lon_lat.items():
        city = City(name, *point)
        cities.append(city)
        name_to_city[name] = city
        city.set_basemap(theBasemap)
    return cities


def _connect_cities(cityA, cityB, theBasemap, flat=True, zorder=1):
    if flat:
        x, y = [], []
        for city in [cityA, cityB]:
            x.append(city.x)
            y.append(city.y)

        theBasemap.plot(x, y, connector_color, lw=2, alpha=0.8)
    else:
        theBasemap.drawgreatcircle(cityA.lon, cityA.lat, cityB.lon, cityB.lat, lw=1, color=connector_color,
                                   zorder=zorder)


def main():
    lon_0 = -100
    lat_0 = 65

    colorLine = 'k'
    lWidth = 4
    h = 3000.

    roundText = False

    fig = plt.figure(figsize=(8.533, 3.333))
    assert isinstance(fig, Figure)
    print(fig.get_size_inches())

    mlogo = Basemap(projection='nsper', lon_0=lon_0, lat_0=lat_0, satellite_height=h * 1000., resolution='c')
    #mlogo = Basemap(projection='nsper', lon_0=lon_0, lat_0=lat_0, satellite_height=h * 100000000., resolution='c')
    #mlogo = Basemap(projection='npstere', lon_0=lon_0, lat_0=lat_0, boundinglat=40, resolution='c', round=True)
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

    cities = create_cities(mlogo)

    montreal = name_to_city["Montreal"]
    unbc = name_to_city["UNBC"]
    victoria = name_to_city["Victoria"]
    saskatoon = name_to_city["Saskatoon"]
    calgary = name_to_city["Calgary"]
    waterloo = name_to_city["Waterloo"]

    x, y = [], []

    for city in cities:

        xi, yi = mlogo(city.lon, city.lat)
        x.append(xi)
        y.append(yi)

    mlogo.scatter(x, y, s=200, marker="o", c=mark_color, zorder=3, linewidths=0.1)

    ax = plt.gca()
    assert isinstance(ax, Axes)



    ## Output logo text
    textStr = "CNRCWP"
    if not roundText:
        ax.set_anchor("NW")
        #write the text over
        txt = ax.annotate("CNRCWP", xy=(0.345, 0.48), xycoords="figure fraction",
                          font_properties=FontProperties(size=75, family="ABADI MT CONDENSED", weight="extra bold"),
                          color="k")

        #set stroke
        txt.set_path_effects([peff.withStroke(linewidth=3, foreground="w")])
    else:
        x0, y0 = 0.4, 0.5
        r0 = 0.73

        phi0_deg = -147
        dphi_deg = 21

        dphi = np.radians(dphi_deg)
        phi0 = np.radians(phi0_deg)
        for i in range(len(textStr)):

            if textStr[i] == "W":
                r = 0.92 * r0
            else:
                r = r0

            xi, yi = x0 + r * np.cos(phi0 + dphi * i), y0 + r * np.sin(phi0 + dphi * i)
            txt = ax.annotate(textStr[i], xy=(xi, yi),
                              xycoords="axes fraction",
                              font_properties=FontProperties(size=35, family="serif", weight="bold"),
                              color="#21759b", rotation=90 + phi0_deg + i * dphi_deg)
            # set stroke
            txt.set_path_effects([peff.withStroke(linewidth=3, foreground="w")])

        ax.annotate("x", xy=(0.5, 0.5), xycoords="axes fraction")

    _connect_cities(saskatoon, unbc, mlogo)
    _connect_cities(victoria, calgary, mlogo)
    #    _connect_cities(calgary, saskatoon, mlogo)
    _connect_cities(montreal, saskatoon, mlogo)
    _connect_cities(saskatoon, waterloo, mlogo)
    #    _connect_cities(unbc, victoria, mlogo)
    _connect_cities(calgary, unbc, mlogo)
    _connect_cities(victoria, saskatoon, mlogo)
    _connect_cities(waterloo, montreal, mlogo)

    # plt.tight_layout(pad=2)
    # plt.show()
    plt.savefig('cnrcwpLogo_official.png', dpi=250, transparent=True)


if __name__ == "__main__":
    main()
