"""Public interface to Ash Impact Modelling (AIM)

This module publishes one function, run_scenario() which will execute Fall3d based
on volcanological parameters specified in a scenario script (e.g. merapi.py), a
topographic data file and a wind profile dataset. The format of these files is 
described in (FIXME: Add reference to manual here!).

AIM works with scenario modules containing all required volcanological parameters.


The function run_scenario() can be used in several ways: 

------------------------    
As a stand alone script:
------------------------

Create a new script run_scenario.py with the following contents:
    
import sys
from aim import run_scenario
run_scenario(sys.argv[1])


Models are run py executing run_scenario.py with the 
scenario module as a command line argument, e.g.
python run_scenario.py merapi.py    



---------------------------
Within the scenario script:
---------------------------

There are two options:

1) Run single scenario

Add the following code at the very end of the scenario module:

# Run model using specified parameters
if __name__ == '__main__':
    from aim import run_scenario
    run_scenario(__file__)

2) Run scenario based on dictionary of parameters
if __name__ == '__main__':
    from aim import run_scenario, get_scenario_parameters
    
    # Get parameters specified in scenario_file
    params = get_scenario_parameters(__file__)    
    
    # Run scenario
    run_scenario(params)

In the latter case, it is then possible to run multiple scenarios with one or more parameters changing. E.g.

for x in [1,11,3,7]:
    params['x'] = x
    run_scenario(params)    
    
Models are run py executing the scenario modules directly, e.g.
python merapi.py    
        

        
The optional parameter, dircomment, provides a mechanism for tagging 
the output directory with an arbitrary comment in addition to username and 
date. This can for example be used to highlight a parameter that is looped,
e.g.

for x in [1,11,3,7]:
    params['x'] = x
    run_scenario(params, dircomment='x=%d' % x) 
  
"""

import os, time

from utilities import get_scenario_parameters, header, run, makedir, get_eruptiontime_from_windfield, get_layers_from_windfield
from wrapper import AIM

        
def run_scenario(scenario, dircomment=None,
                 store_locally=False, 
                 timestamp_output=True,
                 verbose=True):
    """Run volcanic ash impact scenario
    
    The argument scenario can be either
    * A Python script
    or
    * A Dictionary 
   
    In any case scenario must specify all required 
    volcanological parameters as stated in the file required_parameters.txt.
    
    If any parameters are missing or if additional parameters are
    specified an exception will be raised.
    
    Optional parameters:
      dircomment: will be added to output dir for easy identification.
      store_locally: if True, don't use TEPHRAHOME for outputs
      timestamp_output: If True, add timestamp to output dir
                        If False overwrite previous output with same name 
      
    
    
    """

    t_start = time.time()
    
    # Determine if scenario is a Python script or 
    # a parameter dictionary
    try:
        # Get parameters specified in scenario_file
        params = get_scenario_parameters(scenario)
    except:
        # This is not a valid Python script. 
        # See if it behaves like a dictionary
        try:
             scenario.keys()
        except:
             # Not a dictionary either. Raise exception
             msg = 'Argument scenario must be either the name of a '
             msg += 'Python script or a dictionary'
             raise Exception(msg)
        else:
             # The scenario argument is the parameters dictionary
             params = scenario
             

    # Determine if any of the parameters provide are a tuple
    # in which case each combination is run separately
    for name in params:
        p = params[name]
        if type(p) is tuple:
            # Unpack tuple and run scenario for each parameter value
            # This recursion will continue until no parameters 
            # have tuples as values
            params_unpacked = params.copy()
            for value in p:
                params_unpacked[name] = value
                aim = run_scenario(params_unpacked, dircomment=dircomment + '_%s_%s' % (name, value),
                                   store_locally=store_locally, 
                                   timestamp_output=timestamp_output,
                                   verbose=verbose)
            
            return 
                          
    # Instantiate model object  
    aim = AIM(params, 
              dircomment=dircomment,
              store_locally=store_locally,
              timestamp_output=timestamp_output,
              verbose=verbose)    

    if not aim.postprocessing:
        # Store scenario script, input data files and 
        # actual parameters to provide a complete audit trail
        aim.store_inputdata(verbose=verbose)
            
        # Generate input file for Fall3d-6
        aim.write_input_file(verbose=verbose)

        # Generate input data files in Fall3D format
        aim.generate_windprofile(verbose=verbose)    
        aim.generate_topography(verbose=verbose)
    
        # Run scripts for Fall3d
        aim.set_granum(verbose=verbose)
        aim.set_database(verbose=verbose)
        aim.set_source(verbose=verbose)
        aim.run_fall3d(verbose=verbose)

    # Fall3d postprocessing nc2grd
    aim.nc2grd()
    
    # AIM post processing
    #aim.convert_ncgrids_to_asciigrids(verbose=verbose)
    aim.convert_surfergrids_to_asciigrids()
    aim.generate_contours(verbose=True)

    aim.organise_output()
    
    # Done
    if verbose:
        header('Simulation finished in %.2f seconds, output data are in %s'
                   % (time.time() - t_start,
                      aim.output_dir))
 
        try:
            target = os.readlink(aim.symlink)                      
        except e:
            header('WARNING: Shortcut %s does not appear to be working. Use real directory %s instead.' % (symlink, target))
            print 'Error message was', e
        else:    
            
            if target == aim.output_dir:              
                header('Shortcut to output data is: %s -> %s' % (aim.symlink, target))
            else:
                header('WARNING: Shortcut %s has been changed by more recent run to: %s' % (aim.symlink, target))
                        
        print
    
    # Return object in case user wants access to it 
    # (e.g. for further postprocessing)
    return aim

    
def run_multiple_windfields(scenario, 
                            windfield_directory=None,
                            dircomment=None,
                            verbose=True):
    """Run volcanic ash impact model for multiple wind fields.
    
    The wind fields are assumed to be in subfolder specified by windfield_directory, 
    have the extension *.txt or *.profile and follow the format use with scenarios.
    
    """
    
    header('Hazard modelling usingc multiple wind fields from %s' % windfield_directory)    
    
    basename, _ = os.path.splitext(scenario)
    aim_windfile = basename + '_wind.txt'    
    fall3d_windfile = basename + '.profile'
    
    for file in os.listdir(windfield_directory):
        
        
        
        # Clean
        s = '/bin/rm %s %s' % (aim_windfile, fall3d_windfile)
        
        # Determine format of windfile
        if file.endswith('.txt'):
            # Use AIM wind field
            local_windfile = aim_windfile
        elif file.endswith('.profile'):
            # link Fall3d wind field to local file
            local_windfile = fall3d_windfile
        else:
            # Do nothing
            continue
            
        # Copy actual wind field to local file
        windfield = '%s/%s' % (windfield_directory, file)
        windname, _ = os.path.splitext(file)
        header('Computing event using wind field: %s' % windfield)
        s = 'cp %s %s' % (windfield, local_windfile)
        run(s, verbose=False)             
        print 
        
            
        # Get params from model script
        params = get_scenario_parameters(scenario)    
        
        # Override or create parameters derived from native Fall3d wind field
        params['wind_altitudes'] = get_layers_from_windfield(windfield)
        params['Eruption_Year'], params['Eruption_Month'], params['Eruption_Day'] = get_eruptiontime_from_windfield(windfield)        
        params['Meteorological_model'] = 'profile'

        # Run scenario                        
        aim = run_scenario(params,  
                           timestamp_output=False,    
                           dircomment=dircomment)

        # Copy result file to output folder
        hazard_output_folder = basename + '_hazard_outputs'
        makedir(hazard_output_folder)
        
        result_file = aim.scenario_name + '.res.nc'    
        newname = aim.scenario_name + '.%s.res.nc' % windname # Name after wind file    
        s = 'cp %s/%s %s/%s' % (aim.output_dir, result_file, hazard_output_folder, newname) 
        run(s)
