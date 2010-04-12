"""Run all AIM executables

This script replaces the scripts provided by Fall3D
and adds AIM specific methods.

"""

def check_parameter_ranges(params):    
    """Catch unphysical situations and raise appropriate error messages
       Input:
           params: Dictionary of modelling parameters                
    """

    # Get scenario name    
    scenario_name = params['scenario_name']
        
    # Create local variables from dictionary
    for key in params:
        s = '%s = params["%s"]' % (key, key)
        exec(s)

    # Check parameters    
    if params['Mass_eruption_rate'] < 0:
         msg = 'Mass eruption rate must be greater than zero.\n'
         msg += 'A value of %e was specified' % params['Mass_eruption_rate']
         raise Exception(msg)


    #log_estimated_mass_eruption_rate = 4 + 1.7*math.log(Eruption_column_height)
    #if abs(log_estimated_mass_eruption_rate - math.log(Mass_eruption_rate)) > 1:
    #    msg = 'Mass eruption rate and eruption column height do not correlate \n'
    #    msg += 'for mass eruption rate = %e and for eruption column height = %i.\n' % (Mass_eruption_rate, Eruption_column_height)
    #    raise Exception(msg)


    # Assert that column height is compatible with mass eruption rate
    Eruption_column_height = Z_layers[-1]
    if Eruption_column_height < 2000:
        msg = 'Eruption column height must be greater than or equal to 2000.\n'
        msg += 'A height of %i was specified' % Eruption_column_height
        raise Exception(msg)    

    if 2000 <= Eruption_column_height < 10000:
        msg = 'Mass eruption rate inconsistent with column height: '
        msg += 'Eruption_column_height = %.0f m, ' % Eruption_column_height
        msg += 'Mass_eruption_rate = %.0e kg/s' % Mass_eruption_rate
        assert 1.0e4 <= Mass_eruption_rate <= 1.0e6, msg
      
    if 10000 <= Eruption_column_height < 15000:
        msg = 'Mass eruption rate inconsistent with column height: '
        msg += 'Eruption_column_height = %.0f m, ' % Eruption_column_height
        msg += 'Mass_eruption_rate = %.0e kg/s' % Mass_eruption_rate
        assert 1.0e4 <= Mass_eruption_rate < 1.0e8, msg    
      
    if 15000 <= Eruption_column_height < 30000:
        msg = 'Mass eruption rate inconsistent with column height: '
        msg += 'Eruption_column_height = %.0f m, ' % Eruption_column_height
        msg += 'Mass_eruption_rate = %.0e kg/s' % Mass_eruption_rate
        assert 1.0e5 <= Mass_eruption_rate < 1.0e8, msg        
      
    if 30000 <= Eruption_column_height < 80000:
        msg = 'Mass eruption rate inconsistent with column height: '
        msg += 'Eruption_column_height = %.0f m, ' % Eruption_column_height
        msg += 'Mass_eruption_rate = %.0e kg/s' % Mass_eruption_rate
        assert 1.0e8 <= Mass_eruption_rate < 1.0e12, msg            

    if Eruption_column_height >= 80000:
        msg = 'Eruption column height cannot equal or exceed 80000.\n'
        msg += 'A height of %i was specified' % Eruption_column_height
        raise Exception(msg)

      
    # Check that vent location is within model domain
    lo = X_coordinate_lower_left_corner
    hi = lo + Cell_size*1000*Number_cells_X_direction
    msg = 'Vent location not within easting range [%i, %i]' % (lo, hi)
    assert lo <= Vent_location_X_coordinate <= hi, msg

    lo = Y_coordinate_lower_left_corner
    hi = lo + Cell_size*1000*Number_cells_Y_direction
    msg = 'Vent location not within northing range [%i, %i]' % (lo, hi)
    assert lo <= Vent_location_Y_coordinate <= hi, msg
      

#    if Number_cells_X_direction > 150 or Number_cells_Y_direction > 150:
#        msg = 'WARNING: DEM dimensions cannot exceed 150. '
#        msg += ' I got %i, %i' % (Number_cells_X_direction, 
#                                  Number_cells_Y_direction)
#        raise Exception(msg)



        
def derive_implied_parameters(topography_grid, params):
    """Compute parameters that can be derived from topography grid and scenario parameters.
       Input:
           topography_grid: filename
           params: dictionary with model parameters
    """
    
    derive_spatial_parameters(topography_grid, params)
    derive_modelling_parameters(params)
   
            
        
def derive_spatial_parameters(topography_grid, params):
    """Derive spatial parameters from topography grid
       Input:
           topography_grid: filename
           params: dictionary with model parameters
    """
    
    scenario_name = params['scenario_name']
    
    try:    
        fid = open(topography_grid)
    except IOError:
     
        # Assume existence of native Fall3d topogrid named
        # <scenario_name>.regionaltopo.grd
        #
        #DSAA
        #171  171
        #430000.0  600000.0
        #4100000.0 4270000.0
        #0.0    3129.5
        
        native_grid = '%s.regionaltopo.grd' % scenario_name
        print('AIM topography grid %s could not be found.' % topography_grid)
        print('Assuming existence of Fall3d grid named %s'% native_grid)
        
        fid = open(native_grid)
        lines = fid.readlines()        
        fid.close()
        
        for i, line in enumerate(lines[:4]):
            fields = line.strip().split()
    
            if i == 0: assert line.strip() == 'DSAA'
    
            if i == 1:
                nx = params['Number_cells_X_direction'] = int(fields[0])
                ny = params['Number_cells_Y_direction'] = int(fields[1])
            
            if i == 2:
                xmin = round(float(fields[0]), 1)
                xmax = round(float(fields[1]), 1)
                params['X_coordinate_lower_left_corner'] = xmin
                    
            if i == 3:
                ymin = round(float(fields[0]), 1)
                ymax = round(float(fields[1]), 1)            
                params['Y_coordinate_lower_left_corner'] = ymin

        params['Cell_size'] = (xmax-xmin)/nx/1000 # Convert to km
        return

                
    # Get data from AIM topofile    
    lines = fid.readlines()
    for i, line in enumerate(lines[:5]):
        fields = line.strip().split()
        val = float(fields[1])
    
        if i == 0:
            assert fields[0] == 'ncols'
            params['Number_cells_X_direction'] = int(val)
            
        if i == 1:
            assert fields[0] == 'nrows'
            params['Number_cells_Y_direction'] = int(val)        
            
        if i == 2:
            assert fields[0] == 'xllcorner'
            params['X_coordinate_lower_left_corner'] = round(val, 1)        
            
        if i == 3:
            assert fields[0] == 'yllcorner'
            params['Y_coordinate_lower_left_corner'] = round(val, 1)
            
        if i == 4:
            assert fields[0] == 'cellsize'
            params['Cell_size'] = float(val)/1000  # Convert to km

            
            
def derive_modelling_parameters(params):
    """Compute modelling parameters that can be derived from scenario parameters
    """
    
    # Assume the lowest atmospheric layer starts at zero
    params['Z_layer_minimum'] = 0
    
    
    Zmax = params['Z_layers'][-1] 
    if Zmax >= 20000:
        params['Z_layer_increment'] = 10000
    elif 10000 <= Zmax < 20000:
        params['Z_layer_increment'] = 1000        
    else:
        params['Z_layer_increment'] = 500


    params['meteo_time_step'] = params['Hours_between_meteo_data_blocks'] * 60
    #params['source_type'] = 'plume'                       # only relevant source type
    params['load_units'] = 'kg/m2'                        # only relevant unit 
    params['class_load_units'] = 'kg/m2'                  # only relevant unit
    params['total_concentration_units'] = 'kg/m3'         # only relevant unit
    params['z_cummulative_concentration_units'] = 'kg/m2' # only relevant unit
    params['z_maximum_concentration_units'] = 'kg/m3'     # only relevant unit


