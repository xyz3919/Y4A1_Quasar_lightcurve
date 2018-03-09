import despydb.desdbi
import numpy as np
import os,sys
import pandas as pd

def setup_dbh(section = "db-dessci"):
    # Setup desar queries here for later
    try:
        desdmfile = os.environ["des_services"]
    except KeyError:
        desdmfile = None
    dbh = despydb.desdbi.DesDbi(desdmfile,section)
    cur = dbh.cursor()
    return dbh,cur

def get_single_epoch_object(field):

    dbh,cur = setup_dbh()
    get_list = "with SNVAR_TEMP_1 as (select CATALOGNAME, MAG_ZERO, SIGMA_MAG_ZERO, MAG_ONE, SIGMA_MAG_ONE, MJD_OBS from  Y4A1_EXPOSURE join Y4A1_ZEROPOINT on Y4A1_EXPOSURE.expnum = Y4A1_ZEROPOINT.expnum where field like 'SN-"+str(field)+"' and Y4A1_ZEROPOINT.flag < 16 and Y4A1_ZEROPOINT.source = 'FGCM' and Y4A1_ZEROPOINT.version = 'y4a1_v1.5' and EXPTIME > 30 order by CATALOGNAME ) select RA, DEC, MJD_OBS, Y4A1_FINALCUT_OBJECT.FLUX_PSF*POWER(10,-0.4*MAG_ZERO+9) as FLUX_PSF, SQRT(POWER(SIGMA_MAG_ZERO*Y4A1_FINALCUT_OBJECT.FLUX_PSF, 2) + POWER(Y4A1_FINALCUT_OBJECT.FLUXERR_PSF, 2))*POWER(10,-0.4*MAG_ZERO+9) as FLUXERR_PSF, Y4A1_FINALCUT_OBJECT.FLUX_AUTO*POWER(10,-0.4*MAG_ZERO+9) as FLUX_AUTO, SQRT(POWER(SIGMA_MAG_ZERO*Y4A1_FINALCUT_OBJECT.FLUX_AUTO, 2) + POWER(Y4A1_FINALCUT_OBJECT.FLUXERR_AUTO, 2))*POWER(10,-0.4*MAG_ZERO+9) as FLUXERR_AUTO, BAND from  Y4A1_FINALCUT_OBJECT, SNVAR_TEMP_1 where CATALOGNAME = FILENAME and Flags = 0 and imaflags_iso = 0  order by DEC, RA"
    cur.execute(get_list)
    info_list =  map(list,cur.fetchall())
    dbh.close()
    return info_list

def build_single_epoch_catalog():

    fields = ["E1","E2","S1","S2","C1","C2","C3","X1","X2","X3"]
#    fields = ["S1"]
    for field in fields:
        data = get_single_epoch_object(field)
        np.savetxt(field+".csv", data, fmt="%s %s %s %s %s %s %s %s", delimiter=",",header="RA,DEC,MJD_OBS,FLUX_PSF,FLUX_ERR_PSF,FLUX_AUTO,FLUX_ERR_AUTO,BAND")
    
if __name__ == '__main__':

    build_single_epoch_catalog()

