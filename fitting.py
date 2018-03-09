import os
import numpy as np
import pandas as pd
from astropy.io import fits
from astropy.coordinates import SkyCoord
from astropy import units as u

def load_quasar_catalog():

    # loading the quasar catalog
    # columns=[ra,dec,mag_auto_r,region,redshift,flag]

    quasar_catalog = "ALL&SN_Xmatch.fits"
    quasars = fits.open(quasar_catalog)[1].data
    quasars = sorted(quasars,key=lambda x:x[0])
    return quasars

def degtohexname(ra,dec):

    rah=int(ra)
    ram=int(60*(ra-rah))
    ras=3600.*(ra-rah-(ram/60.))

    if (dec >= 0.0):
        decd=int(dec)
        decm=int(60.*(dec-decd))
        decs=3600.*(dec-decd-(decm/60.))
        return "J%02d%02d%05.2f+%02d%02d%05.2f" % (rah,ram,ras,decd,decm,decs)
    else:
        decd=-int(dec)
        dec=-dec
        decm=int(60.*(dec-decd))
        decs=3600.*(dec-decd-(decm/60.))
        dec=-dec
        return "J%02d%02d%05.2f-%02d%02d%05.2f" % (rah,ram,ras,decd,decm,decs)

 

def find_the_quasars(name,ra,dec,band,all_objects):

    # Finding the target quasars in the single-epoch objects

    print "- Fitting ",name,band
    all_objects=all_objects[all_objects["BAND"]==band]
    all_objects=all_objects[all_objects["RA"]>ra-0.01]
    all_objects=all_objects[all_objects["RA"]<ra+0.01]
    all_objects=all_objects[all_objects["DEC"]>dec-0.01]
    all_objects=all_objects[all_objects["DEC"]<dec+0.01]
    
    if len(all_objects)== 0:
        return None
    coor_quasar = SkyCoord(ra=ra*u.degree,
                           dec=dec*u.degree)
    coor_all_objects = SkyCoord(ra=all_objects["RA"]*u.degree,
                                dec=all_objects["DEC"]*u.degree)
    dist = coor_quasar.separation(coor_all_objects)
    matched_quasars = all_objects.loc[dist<1.0*u.arcsec ]
    matched_quasars = matched_quasars.sort_index(by='MJD_OBS') 
    return matched_quasars 

def read_single_epoch_catalog():

    catalog = {}
    fieldname = ["E1","E2","S1","S2","C1","C2","C3","X1","X2","X3"]
    fieldname = ["E1"]
    for field in fieldname:
        print "--- Loading the single epoch catalog at "+field+" ---"
#        data = pd.read_csv(field+".csv",sep=" ",names=["RA","DEC","MJD_OBS","FLUX_PSF","FLUX_ERR_PSF","FLUX_AUTO","FLUX_ERR_AUTO","BAND"],dtype={"RA":float,"DEC":float,"MJD_OBS":float,"FLUX_PSF":float,"FLUX_ERR_PSF":float,"FLUX_AUTO":float,"FLUX_ERR_AUTO":float,"BAND":str})
        data = pd.read_csv(field+".csv",header=None,na_values=-99,sep=" ",comment="#",names=["RA","DEC","MJD_OBS","FLUX_PSF","FLUX_ERR_PSF","FLUX_AUTO","FLUX_ERR_AUTO","BAND"],dtype={"RA":float,"DEC":float,"MJD_OBS":float,"FLUX_PSF":float,"FLUX_ERR_PSF":float,"FLUX_AUTO":float,"FLUX_ERR_AUTO":float,"BAND":str})
        catalog.update({field:data})
    print "--- Finished ---"
    return catalog

def create_dir(directory):

    if not os.path.exists(directory):
        os.makedirs(directory)

if __name__ == '__main__':

    catalog = read_single_epoch_catalog()
    quasar_catalog = load_quasar_catalog()
    f = open("quasar_catalog.csv","w")
    f.write("# name ra dec mag_r field redshift N_g N_r N_i N_z\n")
    band_list = ["g","r","i","z"]
    for quasar in quasar_catalog[0:2]:
        ra = quasar[0]
        dec = quasar[1]
        region = quasar[3]
        name = degtohexname(ra,dec)
        f.write(name+" ")
        f.write(" ".join(np.array(quasar).astype(str)))
        create_dir("lightcurve/"+name)
        for band in band_list:
            matched_quasars = find_the_quasars(name,ra,dec,band,catalog[region])
            if matched_quasars is None:
                print "No data found !"
                f.write(" 0")
            else:
                f.write(" "+str(len(matched_quasars)))
                matched_quasars.to_csv("lightcurve/"+name+"/"+band+".csv",index=False,columns=["MJD_OBS","FLUX_PSF","FLUX_ERR_PSF","FLUX_AUTO","FLUX_ERR_AUTO"])
        f.write("\n")
    f.close()
    os.system("zip -r lightcurve.zip lightcurve")
#    print find_the_quasars(test[0],test[1],"r",catalog[test[3]])


