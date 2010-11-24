"""Extract wind profiles from NCEP1 data for use with scenario modelling or hazard mapping.

This script is a template for extracting wind profiles from NCEP1 re-analysis meteorological data at/or close to the vent location. The user must download NCEP data for the region and time period needed (see instructions in Appendix 2 - AIM User Manual). The user must point to the location of the NCEP files. The user must also designate a name and location for the directory where extracted wind profile(s) will be stored. 

There are two extration options: 'merged' and 'multiple'. 

Option #1 'merged' 

This option will extract a single profile (or a series of profiles if longer than 6 hours which will be merged into a single profile). The merged profile will contain time interval information (i.e 0 to 21600, 21600 to 43200) to be used for scenario modelling. 

Option #2 'multiple'

This option will generate multiple profiles with no time interval information (i.e. 0 to 99999) that will be used for hazard mapping. 

To run:

python extract_windfields.py

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
