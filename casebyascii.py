CWB_Station_ID_Array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10
                        , 11, 12, 13, 14, 15, 16, 17, 18, 19, 20
                        , 21]
CWB_Station_Name = ["LongDong", "FuguiCape", "HsinChu", "TaiChung", "MiTuo"
                    , "XiaoLiuQiu", "ELuanBi", "TaiTung", "LanYu", "HuaLien"
                    , "SuAo", "GuiShanDao", "CiMei", "PengHu", "MaTsu"
                    , "KinMen", "Pratas", "TaiChungPort", "QiGu", "ChengGong"
                    , "DongJiDao"]
Model_node = [125015, 118616, 103666, 96926, 76803
              , 86070, 92210, 113387, 109545, 131214
              , 131958, 122212, 81343, 94166, 142585
              , 94479, 81229, 96918, 79827, 121599
              , 74658]
import os
import numpy as np
import pandas as pd
from netCDF4 import Dataset
import cftime as cftime
import codecs
import datetime
def wind_dir(U, V):
    WDIR= (270-np.rad2deg(np.arctan2(V, U)))%360
    return WDIR
def wind_spd(U, V):
    WSPD = np.sqrt(np.square(U)+np.square(V))
    return WSPD

# 手動設定區
path = "D:/Work/Wave_schedule/mdc24msc25/"
path2 = "D:/Work/Wave_schedule/mdc24msc25"
# make directory
if not os.path.exists(path2 + "/newascii"):
    os.makedirs(path2 + "/newascii")

# for stanum in CWB_Station_ID_Array:
for stanum in range(1,2):
    staname = CWB_Station_Name[stanum - 1]
    modeli = Model_node[stanum - 1]  # 模式點位
    nc1 = Dataset(path + "schout_4.nc", 'r')
    u1 = nc1['wind_speed'][:, modeli - 1, 0]
    v1 = nc1['wind_speed'][:, modeli - 1, 1]
    wind1 = wind_spd(u1, v1)
    wdir1 = wind_dir(u1, v1)
    h1 = nc1['WWM_1'][:, modeli - 1]
    l1 = nc1['WWM_6'][:, modeli - 1]
    t1 = nc1['WWM_2'][:, modeli - 1]
    d1 = nc1['WWM_9'][:, modeli - 1]
    sp1 = nc1['WWM_10'][:, modeli - 1]
    fp1 = 1/(nc1['WWM_11'][:, modeli - 1])
    nc2 = Dataset(path + "schout_5.nc", 'r')
    u2 = nc2['wind_speed'][:, modeli - 1, 0]
    v2 = nc2['wind_speed'][:, modeli - 1, 1]
    wind2 = wind_spd(u2, v2)
    wdir2 = wind_dir(u2, v2)
    u2 = nc2['wind_speed'][:, modeli - 1]
    h2 = nc2['WWM_1'][:, modeli - 1]
    l2 = nc2['WWM_6'][:, modeli - 1]
    t2 = nc2['WWM_2'][:, modeli - 1]
    d2 = nc2['WWM_9'][:, modeli - 1]
    sp2 = nc2['WWM_10'][:, modeli - 1]
    fp2 = 1 / (nc2['WWM_11'][:, modeli - 1])
    #append data
    newwind = np.append(wind1, wind2)
    newwdir = np.append(wdir1, wdir2)
    newh = np.append(h1, h2)
    newl = np.append(l1, l2)
    newt = np.append(t1, t2)
    newd = np.append(d1, d2)
    newsp = np.append(sp1, sp2)
    newfp = np.append(fp1, fp2)
    ##時間範圍
    time1 = nc1['time'][:]
    timeunit1 = nc1['time'].units
    time2 = nc2['time'][:]
    timeunit2 = nc2['time'].units
    try:
        t_cal = nc1['time'].calendar
    except AttributeError:  # Attribute doesn't exist
        t_cal = u"gregorian"  # or standard
    datevar = np.array([])
    for i in range(0, 24):
        datevar = np.append(datevar, pd.to_datetime(str(cftime.num2date(time1[i], units=timeunit1, calendar=t_cal)),
                                                    format="%Y-%m-%d %H:%M:%S"))
    for i in range(0, 24):
        datevar = np.append(datevar, pd.to_datetime(
            str(cftime.num2date(time2[i], units=timeunit2, calendar=t_cal)),
            format="%Y-%m-%d %H:%M:%S"))
    #
    asc = codecs.open(path + 'newascii/' + staname + '.txt', 'w', 'utf-8')
    asc.write("    Date     Time     U10    Dir.     Hs     L      Tr    Dir.  Spr.     fp \n"
              "            h  m  s  (m/s)  (d.N)    (m)    (m)    (s)   (d.N)  (deg)   (Hz)\n"
              "-----------------------------------------------------------------------------\n")

    data ={"yyyymmdd hh mi se": datevar, "wind_speed": newwind, "wind_dir": newwdir,
           "Hs": newh, "L": newl, "Tr": newt, "Dir": newd, "Spr": newsp, "fp": newfp}
    data1 = pd.DataFrame(data=data)
    data2= data1.round({'wind_speed': 2, 'wind_dir': 1, 'Hs': 3, 'L': 1,
                        'Tr': 2, 'Dir': 1, 'Spr': 2, 'fp': 4})
    asc.write(data2.to_string(index=False, header=False))