"""Read wind data in Australian Bureau of Meteorology ACCESS-R format

Read wind data in netCDF4 format from the ACCESS-Regional model [ACCESS-R]
Extract altitudes, time, velocity at given point and create FALL3D wind profiles.

Example data is located at:
ftp://ftp.bom.gov.au/register/sample/access/netcdf4/ACCESS-R/pressure/

The formats are documented at:
http://www.bom.gov.au/nwp/doc/access/docs/ACCESS-R.all-flds.all-lvls.pressure.shtml
http://www.bom.gov.au/nwp/doc/access/docs/ACCESS-R.all-flds.all-lvls.pressure.pdf

Dependancies required to decompress and read in netCDF4 ACCESS-R data:
HDF5-1.8.14
netCDF4-4.3.2
python-netCDF4-1.1.1
"""

from aim.access_forecast_data import extract_access_windprofile
    
        
if __name__ == '__main__':
    
# Vent location (UTM)
    x_coordinate_of_vent = 439423
    y_coordinate_of_vent = 9167213
    zone=49
    hemisphere='S'

# Path to directory of ACCESS-R files (netCDF4)
	
    fn = extract_access_windprofile(access_dir='/home/drabc/pf3d/fall3d_v6/testing/ACCESS-R/all_flds_all_lvls',
                                    utm_vent_coordinates=(x_coordinate_of_vent, y_coordinate_of_vent, zone, hemisphere))
    print fn
    
