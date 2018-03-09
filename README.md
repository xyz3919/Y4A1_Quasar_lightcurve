#Y4A1_Quasar_lightcurve

File description:

1. quasar_catalog.csv: the master quasar catalog contain main information(ra,dec,redshift,N_<band>)
   (N_<band>: the number of measurment in each band)
        
2. lightcurve: The directory which contain the light curve for each quasar in each band.

3. lightcurve/<tragetname>/<band>.csv: The lightcurve data including MJD_OBS,FLUX_PSF,FLUX_ERR_PSF,FLUX_AUTO,FLUX_ERR_AUTO.

4. lightcurve.zip: the zip file of lightcurve.

5. fitting.py: The light curve generation script.

6. query.py: The script query DES database to get single_epoch objects.

