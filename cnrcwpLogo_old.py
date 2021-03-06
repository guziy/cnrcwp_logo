
import pyparsing
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.font_manager import FontProperties
from mpl_toolkits.basemap import Basemap, maskoceans, interp
import matplotlib.patheffects as peff
import matplotlib.pyplot as plt




cityname_to_lon_lat = {
    "Montreal": (-73.5550, 45.5081),
    "Toronto": (-79.4042, 43.6481),
    "Victoria": (-123.3347, 48.4328),
    "Waterloo": (-80.5361, 43.4706),
    "Saskatoon": (-106.6353, 52.1311),
    "Calgary": (-114.0669, 51.0544),
    "UNBC": (-122.7502, 53.9136)
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


    def set_basemap(self, basemap = None):
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


def _connect_cities(cityA, cityB, theBasemap, flat=False, zorder=1):

    if flat:
        x, y = [], []
        for city in [cityA, cityB]:
            x.append(city.x)
            y.append(city.y)

        theBasemap.plot(x, y, connector_color, lw=2, alpha=0.8)
    else:
        theBasemap.drawgreatcircle(cityA.lon, cityA.lat, cityB.lon, cityB.lat, lw=1, color=connector_color, zorder=zorder)


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

    mlogo = Basemap(projection='nsper', lon_0=lon_0, lat_0=lat_0, satellite_height=h * 600., resolution='c')
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
    toronto = name_to_city["Toronto"]
    unbc = name_to_city["UNBC"]
    victoria = name_to_city["Victoria"]
    saskatoon = name_to_city["Saskatoon"]
    calgary = name_to_city["Calgary"]
    waterloo = name_to_city["Waterloo"]

    x, y = [], []

    for city in cities:

        if city in [toronto, waterloo]:
            pass

        xi, yi = mlogo(city.lon, city.lat)
        x.append(xi)
        y.append(yi)

    mlogo.scatter(x, y, s=300, marker="o", c=mark_color, zorder=3, linewidths=0.1)

    ax = plt.gca()
    assert isinstance(ax, Axes)

    ax.set_anchor("NW")
    #write the text over
    txt = ax.annotate("CNRCWP", xy=(0.345, 0.48), xycoords="figure fraction",
                      font_properties=FontProperties(size=75, family="serif", weight="bold"), color="#21759b")

    #set stroke
    txt.set_path_effects([peff.withStroke(linewidth=3, foreground="#000000")])

    _connect_cities(saskatoon, unbc, mlogo)

    _connect_cities(montreal, toronto, mlogo)
    _connect_cities(victoria, calgary, mlogo)
    _connect_cities(calgary, saskatoon, mlogo)
    _connect_cities(montreal, saskatoon, mlogo)
    #_connect_cities(montreal, unbc, mlogo)
    _connect_cities(saskatoon, waterloo, mlogo)
    _connect_cities(unbc, victoria, mlogo)
    _connect_cities(calgary, unbc, mlogo)
    #_connect_cities(waterloo, calgary, mlogo)
    #_connect_cities(waterloo, victoria, mlogo)


    plt.tight_layout(pad=0.5)
    #plt.show()
    plt.savefig('cnrcwpLogo.png', dpi=100, transparent=True)


if __name__ == "__main__":
    main()
