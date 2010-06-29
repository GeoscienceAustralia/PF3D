"""Stand alone script to convert standard NCEP files to Fall3d-NCEP

The script equips the files with global attributes of the form below - 
mostly by deriving them from the data itself.


// global attributes:
		:LONMIN = -180.f ;
		:LONMAX = 177.5f ;
		:LATMIN = -90.f ;
		:LATMAX = 90.f ;
		:NX = 144 ;
		:NY = 73 ;
		:NP = 0 ;
		:NT = 21 ;
		:YEAR = 1992 ;
		:MONTH = 9 ;
		:DAY = 15 ;
		:HOUR = 0 ;
		:TIME_INCR = 21600 ;
		:CEN_LON = 0.f ;
		:CEN_LAT = 0.f ;
		:missing_value = 9.999e+20f ;

"""

import os, sys
from Scientific.IO.NetCDF import NetCDFFile

def usage():
    return 'Usage:\n  python %s <NCEP file>' % sys.argv[0]
    
    
def ncep2fall3d(ncep_filename, fall3d_ncep_filename, verbose=True):
    """Convert standard NCEP file to fall3d NCEP format
    """
    
    # Copy standard NCEP file to fall3d NCEP file
    s = 'cp %s %s' % (ncep_filename, fall3d_ncep_filename)
    os.system(s)
    
    # Open files
    infile = NetCDFFile(ncep_filename)
    outfile = NetCDFFile(ncep_filename, 'a')
    
    # Establish special global attributes for fall3 NCEP format     
    
    print 'Found dimensions:', infile.dimensions.keys()    
    print 'Found variables:', infile.variables.keys()
    
    lon = infile.variables['lon'][:]
    lonmin = min(lon)
    lonmax = max(lon)    
    
    lat = infile.variables['lat'][:]
    latmin = min(lat)
    latmax = max(lat)    
    
    nx = infile.dimensions['lon']
    ny = infile.dimensions['lat']        
    np = infile.dimensions['pres']                
    nt = infile.dimensions['time']            
    print nx, ny, np, nt
    

    infile.close()
    outfile.close()
    
    
if __name__ == '__main__':

    if len(sys.argv) < 2:
        print usage()
        import sys; sys.exit() 
        
    ncep_filename = sys.argv[1]
    
    # Create Fall3d NCEP filename with extension ncep1.nc
    
    basename, extension = os.path.splitext(ncep_filename)
    
    fall3d_ncep_filename = basename + '.ncep1' + extension   
    print ncep_filename 
    print fall3d_ncep_filename     

    ncep2fall3d(ncep_filename, fall3d_ncep_filename, verbose=True)
