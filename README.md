# Y4A1_Quasar_lightcurve


Now, I only put 5 qusars for test. Will update the directory for the whole catalog later.


## File description:

1. quasar_catalog.csv: the master quasar catalog contain main information(ra,dec,redshift,N_<band>)
   (N_<band>: the number of measurment in each band)
        
2. lightcurve: The directory which contain the light curve for each quasar in each band.

3. lightcurve/<tragetname>/<band>.csv: The lightcurve data including MJD_OBS,FLUX_PSF,FLUX_ERR_PSF,FLUX_AUTO,FLUX_ERR_AUTO.

4. lightcurve.zip: the zip file of lightcurve.

5. fitting.py: The light curve generation script.

6. query.py: The script query DES database to get single_epoch objects.

## Comment:

The flux is already the calibrated flux "nanomaggies".
The conversion to to magnitudes is:
```
 Mag = 22.5 - 2.5 log10(Flux)
```

