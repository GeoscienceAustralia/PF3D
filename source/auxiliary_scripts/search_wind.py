"""Search wind profiles for some of the strongest from a particular direction
"""

import os, numpy
from aim.utilities import convert_windfield_to_meteorological_winddirection, get_wind_direction


def get_windfield_data(filename):
    """Get wind speed and direction for each altitude from Fall3d wind field
    
    Extension .profile assumed
    Format is 
    
    
    814924 9208168
    20090101
    0 9999999
    17
    64.0    3.50    0.20   26.65    3.51  266.73
    751.0    7.00    1.70   22.05    7.20  256.35
    1481.0   10.50    1.90   17.65   10.67  259.74
    3119.0    8.90   -2.20   10.25    9.17  283.88
    4383.0   10.50   -2.40    2.35   10.77  282.87
    5837.0    7.00   -3.80   -5.15    7.96  298.50
    7564.0    4.20    3.70  -14.75    5.60  228.62
    9689.0    1.40    2.40  -27.65    2.78  210.26
    10967.0   -4.10   -1.00  -39.65    4.22   76.29
    12446.0   -5.90   -1.30  -54.35    6.04   77.57
    14223.0  -13.20    1.40  -70.75   13.27   96.05
    16566.0  -17.80   -5.40  -76.15   18.60   73.12
    18575.0   -2.50    2.80  -78.35    3.75  138.24
    20565.0    1.90    0.40  -65.25    1.94  258.11
    23751.0    9.80   -0.10  -59.75    9.80  270.58
    26306.0  -11.90    5.50  -55.75   13.11  114.81
    30814.0  -28.10    2.20  -47.05   28.19   94.48

    
    """
    
    if not filename.endswith('.profile'):
        return
        
        
    fid = open(filename)
    lines = fid.readlines()
    fid.close()

    wind_data = [] # altitude, speed, meteorological direction
    
    for line in lines:
        fields = line.split()
        if len(fields) != 6:
            continue
        else:
            
            z = float(fields[0])
            u = float(fields[1])
            v = float(fields[2])
            s = float(fields[4])
            phi = float(fields[5])
            
            #if numpy.allclose(phi, 360): phi = 0.0
            #speed, direction = convert_windfield_to_meteorological_winddirection(u, v)
            #
            #msg = '%f, %f' % (speed, s)
            #assert numpy.allclose(speed, s, rtol=4.0e-2), msg
            #
            #if numpy.allclose(speed, 0):
            #    # Direction is meaningless for speed == 0
            #    pass
            #else:    
            #    msg = '%f, %f' % (phi, direction)            
            #    assert numpy.allclose(phi, direction, rtol=1.0e-2), msg
            
            #wind_data.append([z, speed, direction])
            wind_data.append([z, s, phi])
            
    return wind_data

def search_windfields(directory, direction, tolerance=10, height_limit=None, count=10):
    """Search wind profiles for some of the strongest from given meteorological direction (i.e. where it is coming from)   
    
    directory: pathname i.e. '.'
    direction: Meteorological direction e.g. 'N' (0 or 360 degrees)
    tolerance: Accepted window on each side of direction [decimal degrees]
    height_limit: Upper limit of wind altitude to be considered [m]
    count: How many entries to return
    """
    

    phi = get_wind_direction(direction) # Make sure this is numerical degrees

    files = [file for file in os.listdir('.') if file.endswith('.profile')]
    
    
    print 'Selecting candidates from %i files with wind direction' % len(files),
    print 'from %s with tolerance %i degrees on either side' % (str(direction), 
                                                                tolerance),
    if height_limit:
        print 'and altitudes lower than %i m' % height_limit
    else:
        print
            
    candidates = [] # Keep track of filename, layer, direction and speed   
    for filename in files:

        wind_data = get_windfield_data(filename)
            
        # Filter direction - keep file if one layer has specified direction
        for z, speed, direction in wind_data:
            if abs(phi - direction) < tolerance or abs(phi+360 - direction) < tolerance:
                if height_limit and z < height_limit:
                    candidates.append([filename, z, speed, direction])
                    

    print 'Found %i matching wind fields - sorting by speed' % len(candidates)
    
    # Sort entries according to speed (Schwartzian transform)
    entries = [(a[2],a[0],a[1],a[3]) for a in candidates] # speed, filename, z, direction 
    entries.sort()
    candidates = [(a[1],a[2],a[0],a[3]) for a in entries] # filename, z, speed, direction
        
    print 'Returning top %i wind fields' % count
    return candidates[-count:]

    
if __name__ == '__main__':

    direction = 'N' # Meteorological wind direciton 
    res = search_windfields(directory='.',
                            direction=direction,
                            tolerance=10,
                            height_limit=10000,                           
                            count=30)
    
    print
    print 'Filename:                  altitude [m]  speed [m/s]  direction [degrees]'
    print '-------------------------------------------------------------------------'
    for entry in res[::-1]:
        filename = entry[0].strip() + ':'
        print '%s %i         %.1f         %.1f' % (filename.ljust(26), entry[1], entry[2], entry[3])
