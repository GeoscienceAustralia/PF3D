"""Convert Surfer grd file to ESRI asc grid format 

Usage:
   python grd2asc.py <grdfile>

   where <grdfile> is a Golden Software Surfer grid file with format

DSAA
<ncols> <nrows>
<xmin> <xmax>
<ymin> <ymax>
<zmin> <zmax>
z11 z21 z31 ....  (rows of z values)


Note: Surfer grids use 1.70141e+38 for no data.


An output file with same basename and the extension .asc will be generated following the format

ncols <ncols>
nrows <nrows>
xllcorner <x coordinate of lower left corner>
yllcorner <y coordinate of lower left corner>
cellsize <cellsize>
NODATA_value <nodata value, typically -9999 for elevation data or otherwise 1.70141e+38>

Additionally a projection file with same basename and the extension .prj will be generated.


This can be used for projected data (e.g. UTM) or geodetic data.

"""

import os, sys
from utilities import grd2asc

def usage():
    print 'Usage:'
    print 'python grd2asc.py <grdfile>'


if __name__ == '__main__':
    
    if len(sys.argv) < 2:
        usage()
        sys.exit()

    grdfilename = sys.argv[1]

    grd2asc(grdfilename)
