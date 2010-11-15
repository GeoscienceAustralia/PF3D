"""Test script for aim to extract wind profiles from NCEP1 data
"""

# Vent location in geographic coordinates (decimal degrees) of the Guntur crater
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

# Location of NCEP files
NCEP_dir = '/model_area/tephra/3D_wind/NCEP1/indonesia/2003'

# Location of generated windprofiles
windfield_directory = '/model_area/tephra/3D_wind/NCEP1/merapi_single_scenario_2003'

# Determine if generated wind profile should be used for hazard modelling 
# Options are 
#    'multiple' (hazard modelling)
#    'merged'   (scenario modelling)
wind_field_type = 'merged'
#wind_field_type = 'multiple'

#--------------------------------------
if __name__ == '__main__':
    from aim import generate_wind_profiles_from_ncep
    
    if wind_field_type == 'multiple':
        generate_wind_profiles_from_ncep(__file__)
    elif wind_field_type == 'merged':
        from aim import join_wind_profiles
        generate_wind_profiles_from_ncep(__file__, update_timeblocks=True)
        join_wind_profiles(windfield_directory)
    else:
        print 'wind_field_type must be either \'multiple\' or \'merged\'' 
