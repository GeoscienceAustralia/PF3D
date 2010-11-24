"""Extract wind profiles from NCEP1 data for use with scenario modelling or hazard mapping.

"""

# Location in UTM coordinates of the vent
vent_easting = 439423
vent_northing = 9167213
vent_zone = 49
vent_hemisphere = 'S'

# Time to start extraction
start_year = 2003
start_month = 10
start_day = 29
start_hour = 18

# Time to end extraction
end_year = 2003
end_month = 10
end_day = 30
end_hour = 12

# Path to directory of NCEP files
NCEP_dir = '/model_area/tephra/3D_wind/NCEP1/indonesia/2003'

# Path to directory of generated wind profiles
windfield_directory = '/model_area/tephra/3D_wind/NCEP1/merapi_single_scenario_2003'

# Wind field type options are 'multiple' (hazard modelling) or 'merged' (scenario modelling)
wind_field_type = 'merged' 


#--------------------------------------
if __name__ == '__main__':
    from aim import generate_wind_profiles_from_ncep
    
    
    # FIXME: Roll into one call 
    
    if wind_field_type == 'multiple':
        generate_wind_profiles_from_ncep(__file__)
    elif wind_field_type == 'merged':
        from aim import join_wind_profiles
        generate_wind_profiles_from_ncep(__file__, update_timeblocks=True)
        join_wind_profiles(windfield_directory)
    else:
        print 'wind_field_type must be either \'multiple\' or \'merged\'' 
