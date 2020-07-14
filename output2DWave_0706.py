#要改colorbar、IO、title
import os
os.environ['PROJ_LIB'] = "D:/Software/anaconda/anaconda/share/proj"
import numpy as np
import pandas as pd
from netCDF4 import Dataset
import matplotlib.pyplot as plt
import matplotlib.colors
import cftime
from mpl_toolkits.basemap import Basemap

pwd = "D:/Work/Wave_schedule/wave/mdc24msc25"
hgridpwd = 'D:/Work/Wave_schedule/'
path = "D:/Work/Wave_schedule/post"
# make directory
if not os.path.exists(path+"/2Dwave"):
    os.makedirs(path+"/2Dwave")
#color setting
colors = ["#0041ff", "#0082ff", "#00c3ff", "#00ff7f", "#7fff00", "#ffff00", "#ffc800", "#ff9600"
          , "#ff6e00", "#ff3200", "#ff0000", "#ff0035", "#ff006b", "#ff0096", "#ff00c8"
          , "#ff00ff", "#ff35ff"]
cmap= matplotlib.colors.ListedColormap(colors)
norm= matplotlib.colors.Normalize(vmin=0, vmax=17)
#
wave = np.zeros((24, 448286))
for num in range(4, 6):
    data1 = Dataset(pwd+"/schout_"+str(num)+".nc", 'r')
    time = data1['time'][:]
    timeunit = data1['time'].units
    try:
        t_cal = data1['time'].calendar
    except AttributeError:  # Attribute doesn't exist
        t_cal = u"gregorian"  # or standard
    datevar = np.array([])
    datevar = np.append(datevar, cftime.num2date(time, units=timeunit, calendar=t_cal))
    wave = data1['WWM_1'][:, :]
    grid = pd.read_csv(hgridpwd + "newhgrid.ll", header=None, skiprows=[0])
    print(grid[0][0])
    ne, nd = grid[0][0].split()
    ne = int(ne)
    nd = int(nd)
    lon = []
    lat = []
    dep = []
    for i in range(nd):
        a, x, y, z = grid[0][i+1].split()
        lon.append(float(x))
        lat.append(float(y))
        dep.append(float(z))
    ele = []
    maxlon = max(lon)+1
    minlon = min(lon)-2
    maxlat = max(lat)
    minlat = min(lat)-1

    m = Basemap(projection='merc', llcrnrlat=minlat, urcrnrlat=maxlat,
            llcrnrlon=minlon, urcrnrlon=maxlon, resolution='h')  # resolution='h'

    lon = np.array(lon)
    lat = np.array(lat)
    xx, yy = m(lon, lat)

    for i in range(0, 24):            #時間範圍
        fig = plt.figure()
        fig.set_size_inches(12, 12, forward=True)
        cs = m.contourf(xx, yy, wave[i, :], np.linspace(0, 12, 13, endpoint=True), tri=True, extend='both'
                        , cmap=cmap, norm=norm)
        # color bar  pad is distance in colobar to pic
        cbar = m.colorbar(cs, location='bottom', pad="5%", format='%d')
        # set fontsize in color bar
        cbar.ax.tick_params(labelsize=20)
        m.drawcoastlines()
        m.fillcontinents(color='#AAAAAA', lake_color='aqua')
        # make ylabel
        m.drawparallels(np.arange(5, 45, 5), labels=[
            1, 0, 0, 0], fontsize=20, linewidth=0.5)
        # make xlabel
        m.drawmeridians(np.arange(110, 150, 10), labels=[
            0, 0, 0, 1], fontsize=20, linewidth=0.5)
        # title
        timeStr = (pd.to_datetime(str(datevar[i]),format="%Y-%m-%d %H:%M:%S")).strftime(" %Y/%m/%d %H:%M")
        plt.title('Sig. Wave Height      ' +
                  timeStr, fontsize=18, weight='bold')
        plt.xlabel('Longitude', fontsize=20, labelpad=85)
        plt.ylabel('Latitude', fontsize=20, labelpad=60)
        fig.savefig(path + "/2Dwave/" + '{0:04d}'.format((i+1)+(num-4)*24) + '.png')
