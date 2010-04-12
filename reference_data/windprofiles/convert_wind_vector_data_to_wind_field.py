"""Convert files of the form

hgt.indo.ltm.csv
uwnd.indo.ltm.csv
vwnd.indo.ltm.csv
wspd.indo.ltm.csv

to csv file 

indonesian_windfields.csv

of the form

Pressure, Height, Speed, Direction  


Email from Craig Arthur 22 Jan 2010:

'uwnd' is the east-west component of wind speed (eastwards [i.e. a 'westerly' wind] positive) and 'vwnd' is the north-south component (northwards flow [i.e. a 'southerly' wind] positive). Hence the jetstream over this region is generally an easterly wind at about 150 hPa (roughly 15 km at those latitudes).
"""

import numpy, math
from aim.utilities import convert_windfield_to_meteorological_winddirection

def read_csv_with_header(filename):


    data = {}
    fid = open(filename)
    
    lines = fid.readlines()
    
    fields = lines[0].strip().split(',')
    assert len(fields) == 13   
    variable = fields[0]
    months = fields[1:]
    
    for month in months:    
        data[month] = {}
    
    pressures = []
    for line in lines[1:]:
        fields = line.split(',')
        
        pressure = float(fields[0])
        pressures.append(pressure)
        for i, value in enumerate(fields[1:]):
            month = months[i]
            data[month][pressure] = float(value) 
                
        
    return months, pressures, data


    
if __name__ == '__main__':

    # Read original wind data
    months, pressures, uwnd = read_csv_with_header('uwnd.indo.ltm.csv')
    months, pressures, vwnd = read_csv_with_header('vwnd.indo.ltm.csv')
    months, pressures, hgt = read_csv_with_header('hgt.indo.ltm.csv')  
    months, pressures, wspd = read_csv_with_header('wspd.indo.ltm.csv')      
    
    # Store vector fields per month    
    for month in months:
        fid = open('wind_vector_field.indo.%s.csv' % month.lower(), 'w')
        
        fid.write('Pressure [hPa], Height above sea level [m], Eastward wind speed: u [m/s], Northward wind speed: v [m/s]\n')
        
        for pressure in pressures:
            fid.write('%i, %f, %f, %f\n' % (pressure, 
                                            hgt[month][pressure], 
                                            uwnd[month][pressure],
                                            vwnd[month][pressure]))
                                          

        fid.close()

    # Calculate and store associated wind speed and direction. 
    # Direction is meteorological, i.e. a Westerly wind is blowing towards the east.
    for month in months:
        fid = open('wind_speed_and_direction.indo.%s.csv' % month.lower(), 'w')
        
        fid.write('Pressure [hPa], Height above sea level [m], Absolute wind speed [m/s], Wind direction [deg from azimuth]\n')        

        for pressure in pressures:
        
            u = uwnd[month][pressure]
            v = vwnd[month][pressure]
            
            speed, direction = convert_windfield_to_meteorological_winddirection(u, v)
            assert numpy.allclose(speed, wspd[month][pressure]) # Sanity check
        
            fid.write('%i, %f, %f, %f\n' % (pressure, 
                                            hgt[month][pressure],
                                            speed,
                                            direction))
                

        
        
    fid.close()
