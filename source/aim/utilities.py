"""Utilities used by AIM
  
"""  

import os, sys        
from math import sqrt, pi, sin, cos, acos
from subprocess import Popen, PIPE
from config import update_marker, tephra_output_dir, fall3d_distro

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

def pipe(cmd, verbose=False):
    """Simplification of the new style pipe command
    
    One object p is returned and it has
    p.stdout, p.stdin and p.stderr
    
    If p.stdout is None an exception will be raised.
    """
    
    if verbose:
        print cmd
        
    p = Popen(cmd, shell=True,
              stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True)
              
    if p.stdout is None:
        msg = 'Piping of command %s could be executed' % cmd
        raise Exception(msg)
        
    return p

        
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
        
    Fall3d_dir = os.path.join(FALL3DHOME, fall3d_distro)
    
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
    
    try:
        p = pipe('whoami')
    except:    
        username = 'unknown'    
    else:
        username = p.stdout.read().strip()
        
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

    p = pipe('echo $SHELL')
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
    p = pipe(s)
              
    result = []
    for line in p.stdout.readlines():
        s = line.strip()
        if s: 
            print space + s
        

def nc2asc(ncfilename,
           subdataset,
           ascii_header_file=None, # If ASCII header is known it can be supplied
           projection=None,
           verbose=False):
    """Extract given subdataset from ncfile name and create one ASCII file for each band.
    
    The underlying command is of the form
    gdal_translate -of AAIGrid -b 4 NETCDF:"merapi.res.nc":THICKNESS merapi.003h.depothick.asc
    
    """
       
    # First assert that this is a valid NetCDF file and that requested subdataset exists
    s = 'gdalinfo %s' % ncfilename
    
    try:
        p = pipe(s)
    except: 
        msg = 'Could not read NetCDF file %s' % ncfilename
        raise Exception(msg)
    else:
        lines = p.stdout.readlines()
        expected_header = 'Driver: netCDF/Network Common Data Format'
        header = lines[0].strip()
        if header != expected_header:
            msg = 'File %s does not look like a valid NetCDF file.\n' % ncfilename
            msg += 'Expected header: "%s"\n' % expected_header
            msg += 'but got instead: "%s"' % header
            raise Exception(msg)
    
        # Look for something like: SUBDATASET_3_NAME=NETCDF:"merapi.res.nc":THICKNESS
        found = False
        for line in lines:
            info = line.strip()
            if info.startswith('SUBDATASET') and info.find('NAME=NETCDF:') > 0 and info.endswith(':THICKNESS'):
                #print 'Found', info
                found = True
                
        msg = 'Did not find subdataset %s in %s' % (subdataset, ncfilename)        
        assert found, msg        
            
    # Then extract all bands for this subdataset        
    # Command is for example: gdalinfo NETCDF:"merapi.res.nc":THICKNESS
    #
    # FIXME (Ole): There is much more scope for using NetCDF info here if needed
    #              For now we just assume 'hours' but use the numbers given here
    s = 'gdalinfo NETCDF:"%s":%s' % (ncfilename, subdataset)
    
    try:
        p = pipe(s)
    except:               
        msg = 'Could not execute command: %s' % s
        raise Exception(msg)
    else:
        bands = {}
        lines = p.stdout.readlines()
        for line in lines:
            info = line.strip()
            #print info
            
            # Get new band
            if info.startswith('Band'):
                fields = info.split()
                band_number = int(fields[1])
                bands[band_number] = [] # Create new entry
                
                assert band_number == len(bands)
                              
            # Get associated time                  
            if info.startswith('NETCDF_DIMENSION_time'):
                fields = info.split('=')
                
                # Round to nearest integer!                 
                #FIXME: This is not totally general but handy for naming of files                
                time = int(float(fields[1]))
                bands[band_number].append(time)
                
                
            # Get associated units                  
            if info.startswith('NETCDF_time_units'):
                fields = info.split('=')
                
                unit = fields[1]
                bands[band_number].append(unit)                
                
    # Extract ASCII file for each band    
    for key in bands:
        time = bands[key][0]
        dim =  bands[key][1]
        
        # Name each output file
        basename = ncfilename.split('.')[0]
        bandname = str(time).zfill(3)
        output_filename = basename + '.' + bandname + dim + '.' + subdataset.lower() + '.asc'
        prjfilename = output_filename[:-4] + '.prj'
        #print key, bands[key], output_filename            
        

        # Convert NetCDF subdataset and band to ascii file
        s = 'gdal_translate -of AAIGrid -b %i NETCDF:"%s":%s %s' % (key, ncfilename, subdataset, output_filename)
        if verbose:
            run(s, verbose=verbose)
        else:
            run(s, stdout='/dev/null', stderr='/dev/null', verbose=verbose)
        
        # Now replace the header which GDAL gets wrong
        #s = 'ncdump %s' % ncfilename
        #p = Popen(s, shell=True,
        #          stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True)   
        #           
        #if p.stdout is None:
        #    msg = 'Could not execute command: %s' % s
        #    raise Exception(msg)    
        #else:
        #    lines = p.stdout.readlines()
        #    
        #    for line in lines:
        #        info = line.strip()        
        #        fields = info.split('=')
        #        if info.startswith('XMIN'):
        #            xllcorner = float(fields[1]) - cellsize/2
        
        
        # Now replace the header which GDAL gets wrong
        if ascii_header_file:
        
            # Read replacement
            f = open(ascii_header_file)
            new_header = f.readlines()[:6]
            f.close()
            
            # Read ASCII file
            f = open(output_filename)
            lines = f.readlines()
            f.close()
                        
            # Write replacement      
            f = open(output_filename, 'w')
            for i, line in enumerate(lines):
                if i < 6:
                    f.write(new_header[i])
                else:
                    f.write(line)
            f.close()        
        
        if projection:
            # Create associated projection file
            fid = open(prjfilename, 'w')
            fid.write(projection)
            fid.close()
        
                              
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
    msg = 'Cells are not square'
    assert abs(cellsize - (ymax-ymin)/(nrows-1)) < 1.0e-6, msg 

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


def asc2grd(ascfilename, 
            nodatavalue=1.70141e+38,
            projection=None):
    """Convert ESRI asc grid format to Surfer grd file 

    Input:
    ascfilename: Name of ESRI asc grid (extension .asc assumed) with format
    
        ncols <ncols>
        nrows <nrows>
        xllcorner <x coordinate of lower left corner>
        yllcorner <y coordinate of lower left corner>
        cellsize <cellsize>
        NODATA_value <nodata value, typically -9999 for elevation data or 
        otherwise 1.70141e+38>
    
    An output file with same basename and the extension .grd
    Golden Software Surfer grid file 
    will be generated following the format


        DSAA
        <ncols> <nrows>
        <xmin> <xmax>
        <ymin> <ymax>
        <zmin> <zmax>
        z11 z21 z31 ....  (rows of z values)


        Note: Surfer grids use 1.70141e+38 for no data.


    # FIXME: Not done yet    
    If optional argument projection is specified, a projection file with same basename and the 
        extension .prj will be generated.
        It is assumed that the projection follows the WKT projection format.
    """
    
    basename, extension = os.path.splitext(ascfilename)
    msg = 'ASCII file %s must have extension asc' % ascfilename
    assert extension == '.asc', msg

    grdfilename = basename + '.grd'
    prjfilename = basename + '.prj'


    fid = open(ascfilename)
    lines = fid.readlines()
    fid.close()

    fid = open(grdfilename, 'w')
    # Write header
    fid.write('DSAA\n')
    
    # Check header and get number of columns
    line = lines[0].strip()
    fields = line.split()
        
    msg = 'Input file %s does not look like an ASCII grd file. It must start with ncols' % ascfilename
    assert fields[0] == 'ncols', msg
    assert len(fields) == 2
    ncols = int(fields[1])

    # Get number of rows and write
    line = lines[1]
    fields = line.split() 
    nrows = int(fields[1])       
    
    fid.write('%i %i\n' % (ncols, nrows))
    
    # Get data and compute zmin and zmax
    data = lines[6:]    
    zmin = sys.maxint
    zmax = -zmin
    for line in data:
        for z in [float(x) for x in line.split()]:
            if z > zmax: zmax = z
            if z < zmin: zmin = z            

    # Get cellsize
    msg = 'ASCII file does not look right. Check Traceback and source code %s.' % __file__
    line = lines[4]
    assert line.startswith('cellsize'), msg
    fields = line.split()
    cellsize = float(fields[1])        
        
    # Get origin
    line = lines[2]
    assert line.startswith('xllcorner'), msg
    fields = line.split()
    xmin = float(fields[1]) + cellsize/2
    
    line = lines[3]
    assert line.startswith('yllcorner'), msg
    fields = line.split()
    ymin = float(fields[1]) + cellsize/2    
    
    # Calculate upper bounds and write
    xmax = cellsize * (ncols-1) + xmin
    ymax = cellsize * (nrows-1) + ymin
    
    assert abs(cellsize - (xmax-xmin)/(ncols-1)) < 1.0e-6
    assert abs(cellsize - (ymax-ymin)/(nrows-1)) < 1.0e-6    
    
    fid.write('%f %f\n' % (xmin, xmax))
    fid.write('%f %f\n' % (ymin, ymax))    
    fid.write('%e %e\n' % (zmin, zmax))


    # Write ASCII data reversed into GRD file

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
