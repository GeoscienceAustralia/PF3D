"""Test script for aim to extract wind profiles from NCEP1 data
"""

# Vent location in geographic coordinates (decimal degrees) of the Guntur crater
vent_easting = 814924
vent_northing = 9208168
vent_zone = 48
vent_hemisphere = 'S'

# Time to start extraction
start_year = 2009
start_month = 1
start_day = 1
start_hour = 0

# Time to end extraction
end_year = 2009
end_month = 2
end_day = 27
end_hour = 18

# Location of NCEP files
NCEP_dir = '/model_area/tephra/3D_wind/NCEP1/hazardmap'

# Location of generated windprofiles
windfield_directory = 'guntur_multiple_wind_test'

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
