"""Read wind data in ACCESS-T format
Extract altitudes, time, velocity at given point.
"""

import numpy, os
from Scientific.IO import NetCDF
from coordinate_transforms import UTMtoLL, redfearn

def find_nearest_point(latitudes, longitudes, location):
    """Return nearest point to specified location
    
    It is assumed that latitudes are sorted from high to low, 
    while longitudes are sorted from low to high as per the ACCESS file format.
    
    Output:
        location: Selected point (lat, lon):
        location_indices: Indices of selected point ordered as (lat, lon)    
    """
    
    lat, lon = location

    # Very quick and dirty search. It'll get one of the four closest points     
    # We can narrow this down a little more if needed.
    
    for j, y in enumerate(latitudes):
         if y < lat:
            break
            
    for i, x in enumerate(longitudes):
        if x > lon:
            break            
    
    # Check
    assert numpy.allclose(latitudes[j], y)
    assert numpy.allclose(longitudes[i], x)
    
    return (y, x), (j, i) 

    
def read_access_file(filename, location=None):
    """Read ACCESS NetCDF file
    
    Input:
        filename: NetCDF file in ACCESS format
        location: (latitude, longitude) of location where wind profile is sought. Return values from point nearest specified location
        
    Output:
        time: Time of forecast in seconds after the time of analysis 
        data: altitude, u_velocity, v_velocity and temperature for each level
        point: Coordinates of selected point (lat, lon)
    """

    if location is None:
        msg = 'You must specify a location where wind profile is sought.'
        raise Exception(msg)
    
    fid = NetCDF.NetCDFFile(filename)
    
    #for var in fid.variables:
    #    print var

    # Get nearest point to vent    
    point, indices = find_nearest_point(latitudes=fid.variables['lat'][:],
                                        longitudes=fid.variables['lon'][:],
                                        location=location)
                               
    m, n = indices
    
    # Get time slices
    # FIXME: What does time mean here?
    time = fid.variables['time'][:]
    lvl = fid.variables['lvl'][:] # Pressure levels
    msg = 'Time vector in ACCESS-T files is assumed to contain one and only one element'
    assert len(time) == 1, msg
    
    # Extract wind data at that point (for each time step and each level)
    u = fid.variables['zonal_wnd'][:] # East/west wind velocity component
    v = fid.variables['merid_wnd'][:] # North/south wind velocity component    
    T = fid.variables['air_temp'][:]  # Temperature
    z = fid.variables['geop_ht'][:]   # Geopotential height
    
    fid.close()

    # Build dataset
    X = []
    for l, _ in enumerate(lvl):
        altitude = z[0, l, m, n]
        u_wind = u[0, l, m, n]
        v_wind = v[0, l, m, n]            
        temperature = T[0, l, m, n] - 273.15 # Konvert from Kelvin to Centigrade

        X.append([altitude, u_wind, v_wind, temperature])

    # Return time[s], wind data and selected location
    return int(time[0]*24*3600), X, point

    
def extract_access_windprofile(access_dir,
                               utm_vent_coordinates,
                               verbose=True):
    """Extract wind data from 
    
    Input:
       access_dir: Directory with ACCESS-T forecast files.
       utm_vent_coordinates: Coordinates of vent location in UTM: (easting, northing, zone, hemisphere)
       
    Output:
       Name of generated windprofile:
       
       
    Note - wind data is assumed to be from the same analysis date. If not an exception will be raised.   
    """
                               
    msg = 'utm_vent_coordinates must have the form (easting, northing, zone, hemispher)'
    assert len(utm_vent_coordinates) == 4, msg

    msg = 'hemisphere must be either N or S'
    assert utm_vent_coordinates[3].upper() in ['N', 'S'], msg
    

    vent_latitude, vent_longitude = UTMtoLL(utm_vent_coordinates[1],
                                            utm_vent_coordinates[0],
                                            utm_vent_coordinates[2],
                                            isSouthernHemisphere=True)
    

    files = []
    forecast_hours = []
    ref_analysis_time = ''
    max_hour = 0
    for filename in os.listdir(access_dir):
        
        if filename.endswith('.pressure.nc'):
            fields = filename.split('.')
            
            msg = 'ACCESS-T filename expected to have product id: IDY25100'
            assert fields[0] == 'IDY25100', msg
            
            analysis_time = fields[3]
            h = int(fields[4])
            if h > max_hour: max_hour = h
            forecast_hours.append(h)
            
            if ref_analysis_time == '':
                ref_analysis_time = analysis_time
            else:
                msg = 'Analysis time must be the same for all files in directory "%s". I got both %s and %s.' % (access_dir, analysis_time, ref_analysis_time)
                msg += ' You must make a decision and clean-up :-)'
                assert ref_analysis_time == analysis_time, msg
            
            files.append(filename)
            
    # Sort filenames by forecast hour (kind of Schwartzian transform)
    entries = zip(forecast_hours, files)
    entries.sort()
    
    # Extract and store wind data        
    time_offset = int(ref_analysis_time[-2:])*3600  # Keep track of start time (seconds)
    output_filename = 'IDY25100_%s_%ih.profile' % (analysis_time, max_hour)
    fid = open(output_filename, 'w')
    
    for i, (forecast_hour, filename) in enumerate(entries):
        if verbose:
            print 'Extracting wind from %s at location latitude=%.5f, longitude=%.5f' % (filename, 
                                                                                         vent_latitude, 
                                                                                         vent_longitude)            
        time, data, point = read_access_file(filename,
                                             location=(vent_latitude, vent_longitude))
                                             
                                             
        if i == 0:
            # Write header
            zone, easting, northing = redfearn(point[0], point[1])
            fid.write('%i %i\n' % (easting, northing))               # Location of wind data
            fid.write('%s\n' % ref_analysis_time[:-2]) # Date


        # Determine time interval from (sorted in entries) forecast_hours
        if i+1 < len(forecast_hours):
            interval = (entries[i+1][0] - entries[i][0]) * 3600
        else:    
            interval = 3*3600 # Assume 3 hours for the last (or the only) forecast
        
        msg = 'Something is wrong - forecast hour in filename %s does not match time: %i s' % (filename, time)
        assert numpy.allclose(forecast_hour*3600, time), msg

        start_time = time + time_offset
        end_time = start_time + interval
        
        # Generate FALL3D wind profile
        fid.write('%i %i\n' % (start_time, end_time)) # Write time window
        fid.write('%i\n' % len(data))                 # Write number of altitude levels

        for altitude, u_wind, v_wind, temperature in data:
            fid.write('%.1f %.2f %.2f %.2f\n' % (altitude, u_wind, v_wind, temperature))
    
    fid.close()
    return output_filename
    
        
if __name__ == '__main__':
    
    # Merapi location (UTM)
    x_coordinate_of_vent = 439423
    y_coordinate_of_vent = 9167213
    zone=49
    hemisphere='S'

    fn = extract_access_windprofile(access_dir='.',
                                    utm_vent_coordinates=(x_coordinate_of_vent, y_coordinate_of_vent, zone, hemisphere))
    print fn
    
