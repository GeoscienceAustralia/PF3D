"""Utilities used by AIM
  
"""  

import os, sys        
from math import sqrt, pi, sin, cos, acos
from subprocess import Popen, PIPE
from config import update_marker, tephra_output_dir, fall3d_distro
import numpy
import logging
import time
from Scientific.IO.NetCDF import NetCDFFile


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
        if stdout and stderr: msg += 'See logfiles %s and %s for details' % (stdout, stderr)
        raise Exception(msg)

    return err

    
def run_with_errorcheck(cmd, name, verbose=False):
    """Run general command with logging and errorchecking
    """
        
    stdout = '%s.stdout' % name    
    stderr = '%s.stderr' % name    
    err = run(cmd,
              stdout=stdout,
              stderr=stderr,
              verbose=verbose)        
    if err:
        msg = 'Command "%s" ended abnormally. Log files are:\n' % cmd
        msg += '  %s\n' % stdout            
        msg += '  %s\n' % stderr                        
        raise Exception(msg)
            
                            
    
    
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
        
        # Skip comments and blank lines
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

            
def get_layers_from_windfield(windfield):
    """Get meteorological wind altitudes from Fall3d wind field
    
    Extension .profile assumed
    Format is 
    
    
    814924 9208168
    20090101
    0 9999999
    17
    64.0    3.50    0.20   26.65    3.51  266.73
    751.0    7.00    1.70   22.05    7.20  256.35
    1481.0   10.50    1.90   17.65   10.67  259.74
    3119.0    8.90   -2.20   10.25    9.17  283.88
    4383.0   10.50   -2.40    2.35   10.77  282.87
    5837.0    7.00   -3.80   -5.15    7.96  298.50
    7564.0    4.20    3.70  -14.75    5.60  228.62
    9689.0    1.40    2.40  -27.65    2.78  210.26
    10967.0   -4.10   -1.00  -39.65    4.22   76.29
    12446.0   -5.90   -1.30  -54.35    6.04   77.57
    14223.0  -13.20    1.40  -70.75   13.27   96.05
    16566.0  -17.80   -5.40  -76.15   18.60   73.12
    18575.0   -2.50    2.80  -78.35    3.75  138.24
    20565.0    1.90    0.40  -65.25    1.94  258.11
    23751.0    9.80   -0.10  -59.75    9.80  270.58
    26306.0  -11.90    5.50  -55.75   13.11  114.81
    30814.0  -28.10    2.20  -47.05   28.19   94.48

    
    """
    
    if not windfield.endswith('.profile'):
        return
        
        
    fid = open(windfield)
    lines = fid.readlines()
    fid.close()

    altitudes = []
    
    for line in lines:
        fields = line.split()
        if len(fields) < 4:
            continue
        else:
            altitudes.append(float(fields[0]))
    
    return altitudes

            
            
def get_eruptiontime_from_windfield(windfield):
    """Get eruption year, month and date from Fall3d wind field
    
    Extension .profile assumed
    Format is 
    
    814924 9208168
    20090101
    0 9999999
    17
    71.0    1.50   -0.30   26.35    1.53  281.31
    ....
    
    """
    
    if not windfield.endswith('.profile'):
        return
        
        
    fid = open(windfield)
    lines = fid.readlines()
    fid.close()

    timestamp = lines[1]
    
    year = int(timestamp[:4])
    month = int(timestamp[4:6])
    date = int(timestamp[6:])
    
    return year, month, date
    
        
        
        
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
    
    #return time.strftime('%Y-%m-%dT%H:%M:%S') # ISO 8601
    return time.strftime('%Y-%m-%dT%H%M%S') # Something Windows can read

    
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
        
    
    
def list_to_string(L):
    """Convert list of numerical values suitable for Fall3d
    If L is a single number it will be used as such.
    """
    
    try: 
        s = float(L)
    except:    
        s = ''
        for x in L:
            s += '%f ' % x
        
    return s
    
        
def calculate_extrema(filename, verbose=False):
    """Calculate minimum and maximum value of ASCII file.
    
    Format is ESRI ASCII grid.
    """

    import sys 
    
    # Read ASCII file
    fid = open(filename)
    lines = fid.readlines()  
    fid.close()  
    
    # Check header and get number of columns
    line = lines[0].strip()
    fields = line.split()
        
    msg = 'Input file %s does not look like an ASCII grd file. It must start with ncols' % filename
    assert fields[0] == 'ncols', msg
    assert len(fields) == 2
    
    # Compute extrema and return
    min_val = sys.maxint
    max_val = -min_val
    
    for line in lines[6:]:
        A = numpy.array([float(x) for x in line.split()])
        min_val = min(min_val, A.min()) 
        max_val = max(max_val, A.max())         
        

    return min_val, max_val    
        
        
def nc2asc(ncfilename,
           subdataset,
           projection=None,
           verbose=False):
    """Extract given subdataset from ncfile name and create one ASCII file for each band.
    
    This function is reading the NetCDF file using the Python Library Scientific.IO.NetCDF
    
    Time is assumed to be in whole hours.
    """

    
    basename, _ = os.path.splitext(ncfilename) # Get rid of .nc
    basename, _ = os.path.splitext(basename)   # Get rid of .res
        
    if verbose:
        print 'Converting layer %s in file %s to ASCII files' % (subdataset, 
                                                                 ncfilename)
          
    
    infile = NetCDFFile(ncfilename)

    layers = infile.variables.keys()

    
    
    
    msg = 'Subdataset %s was not found in file %s. Options are %s.' % (subdataset, ncfilename, layers)
    assert subdataset in layers, msg
    
    
    
    units = infile.variables['time'].units
    msg = 'Time units must be "h". I got %s' % units
    assert units == 'h', msg

    A = infile.variables[subdataset].getValue()            
    msg = 'Data must have 3 dimensions: Time, X and Y. I got shape: %s' % str(A.shape)
    assert len(A.shape) == 3, msg 

    times = infile.variables['time'].getValue()
    assert A.shape[0] == len(times)
    
    cols = infile.dimensions['x']
    rows = infile.dimensions['y']    
    
    assert A.shape[1] == rows
    assert A.shape[2] == cols
    
    # Header information
    xmin = float(infile.XMIN)
    xmax = float(infile.XMAX)
    ymin = float(infile.YMIN)
    ymax = float(infile.YMAX)  
    
    #print xmin, xmax
    #print ymin, ymax
    cellsize = (xmax-xmin)/cols  
    #print cellsize
    #print (ymax-ymin)/rows      
    assert numpy.allclose(cellsize, (ymax-ymin)/rows)
        
    header = 'ncols %i\n' % cols
    header += 'nrows %i\n' % rows 
    header += 'xllcorner %.1f\n' % xmin      
    header += 'yllcorner %.1f\n' % ymin          
    header += 'cellsize %.1f\n' % cellsize
    header += 'NODATA_value -9999\n'
    
    # Loop through time slices and name files by hour.
    for k, t in enumerate(times):
        hour = str(int(t)).zfill(2) + 'h'

        asciifilename = basename + '.' + hour + '.' + subdataset.lower() + '.asc'
        prjfilename = asciifilename[:-4] + '.prj'
        
        outfile = open(asciifilename, 'w')
        outfile.write(header)
        
        for j in range(rows)[::-1]: # Rows are upside down
            for i in range(cols):
                outfile.write('%f ' % A[k, j, i])
            outfile.write('\n')    
            
        outfile.close()    
        
        if projection:
            # Create associated projection file
            fid = open(prjfilename, 'w')
            fid.write(projection)
            fid.close()
        
        
    
    infile.close()
    
    
    
    
    
        
def OBSOLETE_nc2asc(ncfilename,
           subdataset,
           ascii_header_file=None, # If ASCII header is known it can be supplied
           projection=None,
           verbose=False):
    """Extract given subdataset from ncfile name and create one ASCII file for each band.
    
    The underlying command is of the form
    gdal_translate -of AAIGrid -b 4 NETCDF:"merapi.res.nc":THICKNESS merapi.003h.depothick.asc
    
    """
       
       
    print 'NC', ncfilename
    
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
        print lines
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
        #f = NetCDFFile(ncfilename)
        #print f.variables.keys
        
        
        
        if ascii_header_file:
        #if False:
        
            # Read replacement
            f = open(ascii_header_file)
            new_header = f.readlines()[:6]
            f.close()
            
            print 'Supplied newheader:', new_header
            
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
   
    # Get cellsize
    cellsize = (xmax-xmin)/(ncols-1)
    
    # Put out warning if cells are not square
    msg = 'Cells are not square: %i, %i' % (cellsize, (ymax-ymin)/(nrows-1))
    if abs(cellsize - (ymax-ymin)/(nrows-1)) > 1.0e-1: print 'WARNING (grd2asc): %s' % msg
    #assert abs(cellsize - (ymax-ymin)/(nrows-1)) < 1.0e-6, msg 

    # Write origin using pixel registration used by ESRI instead of grid line registration used by Surfer.
    fid.write('xllcorner %f\n' % (xmin - cellsize/2.))   # FIXME: CHECK THIS 
    fid.write('yllcorner %f\n' % (ymin - cellsize/2.))
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


        
    
# FIXME: I think this is obsolete as the labeling happens in the contouring now        
def label_kml_contours(kmlfile, contours, units):
    """Label contours in KML file as generated by ogr2ogr with specified interval, number of contours and units
    
    kmlfile: Name of kml contour file that is to be patched with labels
    interval: Contour interval if fixed, if not interval will be -1
    number_of_contours: Number of contours specified. If -1 it means that a fixed interval was used.
    contours: The original input. Can be False, True, List or number.
    units:
    
    """

    return 
    
    level_name = 'Level [%s]' % units
    #print kmlfile, interval
        
    fid = open(kmlfile)
    lines = fid.readlines()
    fid.close()
    
     
    #if interval > 0:
    #    # This means a fixed interval was used. Create list of levels
        
        
        
        
        
    level = number_of_contours*interval
    fid = open(kmlfile, 'w')
    for line in lines:
        
        # Write existing data back
        fid.write(line)

        # Add new attribute 'Level' to Schema
        if line.strip().startswith('<Schema name='):
            fid.write('\t<SimpleField name="%s" type="string"></SimpleField>\n' % level_name)
            
        # Add contours to 'Level' at each contour
        if line.strip().startswith('<ExtendedData><SchemaData'):
            fid.write('\t\t<SimpleData name="%s">%f</SimpleData>\n' % (level_name, level))
            level -= interval
            

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

    
    
    
def generate_contours(filename, contours, units, attribute_name, 
                      output_dir='.', meteorological_model=None, WKT_projection=None, 
                      verbose=True):
    """Contour ASCII grid into shp and kml files
    
    The function uses model parameters Load_contours, Thickness_contours and Thickness_units.
    """
       
        

    if verbose: print 'Processing %s:\t' % filename
    
    
    pathname = os.path.join(output_dir, filename)
    basename, ext = os.path.splitext(pathname)
    
    tiffile = basename + '.tif'
    shpfile = basename + '.shp'
    kmlfile = basename + '.kml'
    prjfile = basename + '.prj'
    
    # Get range of data
    min, max = calculate_extrema(pathname)
    
    # Establish if interval is constant
    if contours is False:
        if verbose: print '  No contouring requested'
        return
    elif contours is True:
        interval = (max-min)/8 # Calculate interval automatically
    else:
        # The variable 'contours' is either a list or a number
        try: 
            interval = float(contours) # Constant interval specified
        except:
            # The variable 'contours' must be a list
            if type(contours) != type([]):
                msg = 'Expected list of contours. Must be either True, False, a number or a list of numbers.'
                raise Exception(msg)
            
            interval = -1 # Indicate interval is not fixed

            
    # Check for degenerate interval values        
    if 0 < interval < 1.0e-6: 
        msg = '  WARNING (generate_contours): Range in file %s is too small to contour: %f' % (pathname, interval)
        print msg
        return
            
    if min + interval >= max:
        msg = '  WARNING (generate_contours): No contours generated for range=[%f, %f], interval=%f' % (min, max, interval) 
        print msg
        return

    
    # Generate list of contours from input
    contour_list = []                
    if interval < 0:
        # A list was specified
        for c in contours:
            msg = 'Value in contour list %s was not a number. I got %s' % (contours, c)
            
            if c is True or c is False:
                # Just catching situation where someone puts boolean values in list.
                # The problem is that float(c) below will convert it to 1 or 0
                raise Exception(msg)
                
            try:
                val = float(c)
            except:
                raise Exception(msg)
            else:
                contour_list.append(val)
    else:
        # A constant interval was given. Build list (exclude both min and max themselves)
        level = min + interval    
        while level < max:
            contour_list.append(level)
            level += interval                         
           


            
    # Generate GeoTIFF raster
    s = 'gdal_translate -of GTiff %s %s' % (pathname, tiffile)
    run_with_errorcheck(s, tiffile, 
                             verbose=False)                                


    # Clear the way for contours.
    s = '/bin/rm -rf %s' % shpfile # 
    run(s, verbose=False)
    
    
    # Convert contours into GDAL argument
    u = units.lower()                     
    fixed_levels = ''
    
    for c in contour_list:
        fixed_levels += ' %.6f' % c                                                 
        #if u == 'mm':
        #    fixed_levels += ' %.0f' % c
        #elif u == 'cm':     
        #    fixed_levels += ' %.2f' % c                            
        #elif u == 'm':     
        #    fixed_levels += ' %.6f' % c                                 
        #else:
        #    # E.g. kg/m^2 for ash load
        #    fixed_levels += ' %.4f' % c                                                     

            
    if verbose: 
        print '  Units: %s' % units
        print '  Range in data: [%f, %f]' % (min, max) 
        print '  Contour levels: %s' % fixed_levels
            
    
    # Check that all contour levels are within range
    for c in contour_list:
        if not min < c < max:
            print '  WARNING: Requested contour %f is outside range and will not be shown.' % c
    
    
    # Run contouring algorithm 
    s = 'gdal_contour -a %s -fl %s %s %s' % (attribute_name, fixed_levels, tiffile, shpfile)
    run_with_errorcheck(s, shpfile, 
                        verbose=False)                               
    
    
    # Generate KML
    if meteorological_model == 'ncep1':
        # FIXME: Test should be about coordinate system rather than meteo model
        # Such as params['Coordinates'] == 'UTM' or 'LON-LAT'
        s = 'ogr2ogr -f KML -t_srs EPSG:4623 %s %s' % (kmlfile, shpfile)      
    else:                              
        if WKT_projection:
            s = 'ogr2ogr -f KML -t_srs EPSG:4623 -s_srs %s %s %s' % (prjfile, kmlfile, shpfile)
        else: 
            print 'WARNING (generate_contours): Model did not have a projection file'
            s = 'ogr2ogr -f KML -t_srs EPSG:4623 %s %s' % (kmlfile, shpfile)                
    
    run_with_errorcheck(s, kmlfile, 
                        verbose=False)
        
    # Label KML file with contour intervals
    #label_kml_contours(kmlfile, contours, units)
                                                
    
