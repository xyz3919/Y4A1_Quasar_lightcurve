import numpy as np
from matplotlib import pyplot as plt
import pandas as pd

def load_lightcurve(target):

    lightcurve_list = {}
    band_list = ["g","r","i","z"]
#    band_list = ["g"]
    for band in band_list:
        lightcurve = pd.read_csv("lightcurve/"+target+"/"+band+".csv")
        add_mag_into_lightcurve(lightcurve)
        lightcurve_list.update({band:lightcurve})
    return lightcurve_list

def plot_lightcurve(target,lightcurve_list):

    colors = {"g":"blue","r":"green","i":"red","z":"black"}
    ploty = {"MAG_AUTO":"MAG_ERR_AUTO","MAG_PSF":"MAG_ERR_PSF"}
    for ylabel in ploty.keys():
        ax = plt.subplot()
        for band in lightcurve_list.keys():
            data = lightcurve_list[band] 
            ax.errorbar(data["MJD_OBS"], data[ylabel], 
                        yerr=data[ploty[ylabel]],color=colors[band],
                        label=band,fmt='o')
        ax.set_xlabel("MJD_OBS")
        ax.set_ylabel(ylabel)
        ax.set_title(target)
        ax.legend()
        plt.savefig("lightcurve/"+target+"/"+ylabel+".png")
        plt.close()
              

def add_mag_into_lightcurve(data):

    change_list = ["FLUX_AUTO","FLUX_ERR_AUTO","FLUX_PSF","FLUX_ERR_PSF"]
    for change in change_list:
        after = str.replace(change,"FLUX","MAG")
        if "ERR" in change:
            data[after] = 2.5*0.434*data[change]/data[str.replace(change,"_ERR","")]
        else:
            data[after] = 22.5 - 2.5*np.log10(data[change])

    return data

if __name__  == '__main__':

    plot_lightcurve("J063957.89-432307.77",load_lightcurve("J063957.89-432307.77"))
