"""Utilities used by AIM
  
"""  

import os        
from math import sqrt, pi, sin, cos, acos
from subprocess import Popen, PIPE
from config import update_marker, tephra_output_dir

def run(cmd, 
        stdout=None,
        stderr=None, 
        verbose=True):
        
    s = cmd    
    if stdout:
        s += ' > %s' % stdout
        
    if stderr:
        s += ' 2> %s' % stderr        
        
    if verbose:
        print s
    err = os.system(s)
    
    if err != 0:
        msg = 'Command "%s" failed with errorcode %i. ' % (cmd, err)
        if stderr: msg += 'See logfile %s for details' % stderr
        raise Exception(msg)

    return err
    
def header(s):
    dashes = '-'*len(s)
    print
    print dashes
    print s
    print dashes
    
def write_line(fid, text, indent=0):
    fid.write(' '*indent + text + '\n')

def makedir(newdir):
    """works the way a good mkdir should :)
        - already exists, silently complete
        - regular file in the way, raise an exception
        - parent directory(ies) does not exist, make them as well

    Based on            
    http://code.activestate.com/recipes/82465/
    
    Note os.makedirs does not silently pass if directory exists.
    """
    
    if os.path.isdir(newdir):
        pass
    elif os.path.isfile(newdir):
        msg = 'a file with the same name as the desired ' \
            'dir, "%s", already exists.' % newdir
        raise OSError(msg)
    else:
        head, tail = os.path.split(newdir)
        if head and not os.path.isdir(head):
            makedir(head)
        #print "_mkdir %s" % repr(newdir)
        if tail:
            os.mkdir(newdir)


    
def get_scenario_parameters(scenario_file):
    """Extract dictionary of parameters from scenario file
    """
    
    # Get all variables from scenario name space
    # Get copy so that the original __dict__ isn't modified
    scenario_name = scenario_file.split('.')[0]
    
    exec('import %s as scenario_module' % scenario_name)
    params = scenario_module.__dict__.copy() 
    
    # Remove built-in entries
    for key in params.keys():
        if key.startswith('__'):
            params.pop(key)

    # Add scenario name to dictionary
    params['scenario_name'] = scenario_name
    
    # Return parameter dictionary        
    return params     
        

        
        
def check_presence_of_required_parameters(params):
    """Check that scenario scripts provides the correct parameters
    as specified in required_parameters.txt
    
    Input:
        scenario: Name of scenario
        params: Dictionary of parameters provided in scenario  
    """
    
    # Get path 
    path = os.path.split(__file__)[0]

    # Get scenario name
    scenario_name = params['scenario_name']
        
    
    # Get required parameters
    filename = os.path.join(path, 
                            'required_parameters.txt')
    
    required_parameters = {}
    fid = open(filename, 'r')
    for line in fid.readlines():
    
        entry = line.strip()
        
        # Skip commens and blank lines
        if entry == '': continue                
        if entry.startswith('#'): continue
       
        # Check that each line specifies only one parameter
        if len(entry.split()) > 1:
            msg = 'Only one parameter must be specified per line '
            msg += 'in required_parameters.txt. I got %s ' % entry
            raise Exception(msg)

        # Register parameter name - value on RHS is irrelevant
        required_parameters[entry] = None
    
    # Add scenario_name to required parameters
    required_parameters['scenario_name'] = None                
    
    # Check that all required parameters were provided
    for parameter in required_parameters:
        if parameter not in params:
            # Bad - required parameter was missing
            msg = 'Required parameter "%s" was not specified in scenario "%s"'\
                % (parameter, scenario_name)
            raise Exception(msg)
            
    # Check that all provide parameters were also required
    # i.e. alert the user if a new parameter has been introduced
    for parameter in params:
        if parameter not in required_parameters:        
            # Bad - a new parameter has been introduced
            msg = 'Scenario "%s" provided a new parameter: "%s".\n'\
                % (scenario_name, parameter)
            msg += 'Consider updating "required_parameters.txt" or '
            msg += 'remove "%s" from scenario.' % parameter    
            raise Exception(msg)            
        
        
def get_fall3d_home(verbose=True):
    """Determine location of Fall3d package
    """
    
    #---------------------
    # Determine FALL3DHOME
    #---------------------
    if 'FALL3DHOME' in os.environ:
        FALL3DHOME = os.environ['FALL3DHOME']
    else:
        FALL3DHOME = os.getcwd()
        
    Fall3d_dir = os.path.join(FALL3DHOME, 'Fall3d-5.1.1')
    
    return Fall3d_dir

    
def get_tephradata(verbose=True):
    """Determine location of TEPHRADATA environment variable
    """
    
    #---------------------
    # Determine TEPHRADATA
    #---------------------
    if 'TEPHRADATA' in os.environ:
        TEPHRADATA = os.environ['TEPHRADATA']
    else:
        TEPHRADATA = os.path.join(os.getcwd(), tephra_output_dir)
        
    return TEPHRADATA

    
def get_username():
    """Get username
    """
    p = Popen('whoami', shell=True,
              stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True)
              
    if p.stdout is not None:
        username = p.stdout.read().strip()
    else:
        username = 'unknown'
        
        
    #print 'Got username', username
    return username
    
def get_timestamp():
    """Get timestamp in the ISO 8601 format
    
    http://www.iso.org/iso/date_and_time_format
    
    Format YYYY-MM-DDThh:mm:ss
    where the capital letter T is used to separate the date and time 
    components. 
    
    Example: 2009-04-01T13:01:02 represents one minute and two seconds 
    after one o'clock in the afternoon on the first of April 2009. 
    """
    
    from time import strftime
    #return strftime('%Y-%m-%dT%H:%M:%S') # ISO 8601
    return strftime('%Y-%m-%dT%H%M%S') # Something Windows can read

    
def get_shell():
    """Get shell if UNIX platform
    Otherwise return None
    """
    
    p = Popen('echo $SHELL', shell=True,
              stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True)
              
    shell = None
    if p.stdout is not None:
        shell = p.stdout.read().strip()
        shell = os.path.split(shell)[-1] # Only last part of path
        
    return shell

    
def set_bash_variable(envvar, envvalue):
    """Modify ~/.bashrc with specified environment variable
    If already exist, append using :
    
    """
    
    fid = open(os.path.expanduser('~/.bashrc'))
    lines = fid.readlines()
    fid.close()
    
    fid = open(os.path.expanduser('~/.bashrc'), 'w')
    found = False
    for line in lines:
        patchedline = line
        
        if envvar in line:
            if line.startswith('export %s=' % envvar):
                # Found - now append
                found = True
                path = line.split('=')[1].strip()
                path += ':' + envvalue
                patchedline = 'export %s=%s  %s\n' % (envvar, path, update_marker)                

        fid.write(patchedline)
        
    fid.write('\n') # In case last line did not have a newline            
                
    if not found:
        # Not found - just add it
        patchedline = 'export %s=%s  %s\n' % (envvar, envvalue, update_marker)
        fid.write(patchedline)
                

    fid.close()

    
def tail(filename, 
         count=5, 
         indent=2,
         noblanks=True):
    """Run UNIX tail command but optionally remove blank lines
    """

    space = ' '*indent
    s = 'tail -%i %s' % (count, filename)
    p = Popen(s, shell=True,
              stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True)
              
    result = []
    if p.stdout is not None:
        for line in p.stdout.readlines():
            s = line.strip()
            if s: 
                print space + s
        
    
    


def grd2asc(grdfilename, 
            nodatavalue=-9999, 
            projection=None): #1.70141e+38):
    """Convert Surfer grd file to ESRI asc grid format 

    Input:
    grdfilename: Name of Golden Software Surfer grid file 
                 (extension .grd assumed) with format

        DSAA
        <ncols> <nrows>
        <xmin> <xmax>
        <ymin> <ymax>
        <zmin> <zmax>
        z11 z21 z31 ....  (rows of z values)


        Note: Surfer grids use 1.70141e+38 for no data.


        An output file with same basename and the extension .asc 
        will be generated following the format

        ncols <ncols>
        nrows <nrows>
        xllcorner <x coordinate of lower left corner>
        yllcorner <y coordinate of lower left corner>
        cellsize <cellsize>
        NODATA_value <nodata value, typically -9999 for elevation data or 
        otherwise 1.70141e+38>

        If optional argument projection is specified, a projection file with same basename and the 
        extension .prj will be generated.
        It is assumed that the projection follows the WKT projection format.
    """
    
    basename, extension = os.path.splitext(grdfilename)
    msg = 'Grid file %s must have extension grd' % grdfilename
    assert extension == '.grd', msg

    ascfilename = basename + '.asc'
    prjfilename = basename + '.prj'


    fid = open(grdfilename)
    lines = fid.readlines()
    fid.close()

    fid = open(ascfilename, 'w')
    
    # Do header first
    line = lines[0]
    msg = 'input file %s does not look like a Surfer grd file. It must start with DSAA' % grdfilename
    assert line.strip() == 'DSAA', msg

    # Get dimensions
    line = lines[1]
    ncols, nrows = [int(x) for x in line.split()]
    fid.write('ncols %i\n' % ncols)
    fid.write('nrows %i\n' % nrows)

    # Get origin
    line = lines[2]
    xmin, xmax = [float(x) for x in line.split()]

    line = lines[3]
    ymin, ymax = [float(x) for x in line.split()]
   
    # Get cellsize and check that cells are square
    cellsize = (xmax-xmin)/(ncols-1)
    #msg = 'Cells are not square'
    #assert abs(cellsize - (ymax-ymin)/(nrows-1)) > 1.0e-6, msg 

    # Write origin using pixel registration used by ESRI instead of grid line registration used by Surfer.
    fid.write('xllcorner %f\n' % (xmin - cellsize/2))   # FIXME: CHECK THIS 
    fid.write('yllcorner %f\n' % (ymin - cellsize/2))
    fid.write('cellsize %f\n' % cellsize)
    
    # Write value for no data
    fid.write('NODATA_value %d\n' % nodatavalue)

    # Write data reversed
    data = lines[5:]
    data.reverse()

    for line in data:
        fid.write(line)

    fid.close()

    if projection:
        # Create associated projection file
        fid = open(prjfilename, 'w')
        fid.write(projection)
        fid.close()

        
def convert_meteorological_winddirection_to_windfield(s, d):
    """Convert windspeed and meteorological direction to windfield (u, v)
    
    Inputs:
      s: Absolute windspeed [m/s]
      d: Wind direction [degrees from azimuth (north)]. 
         A direction of 90 degrees means that the wind is 'easterly' i.e. it blows towards the west.
      
    Outputs:
      u: Velocity of the east component [m/s]
      v: Velocity of the north component [m/s]
    """
                
    # Convert degrees from north to radians
    r = pi*(450-d)/180
    
    # Map from meterological wind direction to wind field    
    r = r+pi 

    # Create ouput fields
    u = s*cos(r)
    v = s*sin(r)        
     
    return u, v            
                
def convert_windfield_to_meteorological_winddirection(u, v):
    """Compute wind direction from u and v velocities.
    Direction is 'meteorological, i.e. a Northerly wind blows towards the south.
    """
    
    u = float(u)
    v = float(v)    
    
    speed = sqrt(u*u + v*v)
    
    if speed > 0:
        theta = acos(u/speed)
    else:
        theta = 0 # Set wind direction to arbitrarily in case speed is zero
    
    # Correct for quadrant 3 and 4
    if v < 0:
        theta = 2*pi - theta

    # Reverse direction to meteorological interpretation
    angle = theta + pi 
    
    # Convert radians to degrees
    degrees = angle*180/pi  
    
    # Convert to degrees from azimuth (from North) 
    direction = 450 - degrees

    # Normalise direction
    if direction < 0:
        direction += 360
    
    return speed, direction

def get_wind_direction(x, filename=None):
    """Get wind direction (degrees from azimuth)
    
    Inputs
        x: text field that can either be 'N', 'NNE', 'NE', ...
           or degrees
        filename (optional) for error message
    Output
        Wind direction in decimal degrees from the North.
    """

    # Map from direction to azimuth degrees 
    direction_table={'N': 0,
                     'NNE': 22.5,
                     'NE': 45,
                     'ENE': 67.5,
                     'E': 90,
                     'ESE': 112.5,
                     'SE': 135,
                     'SSE': 157.5,
                     'S': 180,
                     'SSW': 202.5,
                     'SW': 225,
                     'WSW': 247.5,
                     'W': 270,
                     'WNW': 292.5,
                     'NW': 315,
                     'NNW': 337.5} 
        
    
    try:
        d = float(x)
    except:
        # Direction was not a numeric value
        d = float(direction_table[x])

    # Check input ranges
    if not 0 <= d <= 360:
        msg = 'Wind direction must be between 0 and 360 degrees.\n'
        msg += 'I got %.0f degrees.\n' % d
        if filename:
            msg += 'Input file: %s' % filename
        raise Exception(msg)
                

    return d
