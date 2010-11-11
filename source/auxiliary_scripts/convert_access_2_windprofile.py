"""Read wind data in ACCESS-T format
Extract altitudes, time, velocity at given point.
"""

from aim.access_forecast_data import extract_access_windprofile
    
        
if __name__ == '__main__':
    
    # Merapi location (UTM)
    x_coordinate_of_vent = 439423
    y_coordinate_of_vent = 9167213
    zone=49
    hemisphere='S'

    fn = extract_access_windprofile(access_dir='/model_area/tephra/3D_wind/ACCESS/',
                                    utm_vent_coordinates=(x_coordinate_of_vent, y_coordinate_of_vent, zone, hemisphere))
    print fn
    
