"""Install Fall3d-5.1.1 on Linux platform

An environment variable, FALL3DHOME, may be specified to determine
the location of the Fall3d installation.
If it is not specified, Fall3d will be installed within the AIM source tree.
"""

#----------------------------------------
# User defined parameters
#----------------------------------------

compiler = 'fcompiler_gfortran'
#compiler = 'fcompiler_ifort'


#----------------------------------------
# Auxiliary modules and functions
#----------------------------------------
import os
from utilities import makedir, run, header, get_shell, set_bash_variable
from config import update_marker

def replace_string_in_file(filename, s1, s2, verbose=False):
    """Replace string s1 with string s2 in filename 
    """

    # Read data from filename
    infile = open(filename)
    lines = infile.readlines()
    infile.close()

    # Replace and store updated versions
    outfile = open(filename, 'w')
    for s in lines:
        new_string = s.replace(s1, s2).rstrip()

        if new_string.strip() != s.strip() and verbose:
            print 'Replaced %s with %s' % (s, new_string)
        
        outfile.write(new_string + '\n')
    outfile.close()

def set_compiler(filename):
    replace_string_in_file(filename, 'FC= ifort',  '#FC= ifort')
    replace_string_in_file(filename, 'LINKER= ifort',  '#LINKER= ifort')
    replace_string_in_file(filename, 'FFLAGS= -132',  '#FFLAGS= -132')
    replace_string_in_file(filename, 'LINKFLAGS= -132',  '#LINKFLAGS= -132')

    replace_string_in_file(filename, '#FC= gfortran',  'FC= gfortran')
    replace_string_in_file(filename, '#LINKER= gfortran',  'LINKER= gfortran')
    replace_string_in_file(filename, '#FFLAGS= -ffixed',  'FFLAGS= -ffixed')
    replace_string_in_file(filename, '#LINKFLAGS= -ffixed',  'LINKFLAGS= -ffixed')


if __name__ == '__main__':

    #----------------------------------------
    # Check that gfortran compiler is present
    #----------------------------------------
    err = os.system('gfortran -v 2> /dev/null')
    if err != 0:
        msg = 'Compiler gfortran must be present\n'
        msg += 'On Ubuntu/Debian systems this can be done as follows\n'
        msg += 'sudo apt-get install gfortran'
        raise Exception(msg)
    
    #------------------------------------------
    # Check that Python and friends are present
    #------------------------------------------
    err = os.system('python -V 2> /dev/null')
    if err != 0:
        msg = 'Python must be present\n'
        msg += 'On Ubuntu/Debian systems this can be done as follows\n'
        msg += 'sudo apt-get install python'
        raise Exception(msg)
        
    err = os.system('python -c "import numpy" 2> /dev/null')
    if err != 0:
        msg = 'Python module numpy must be present\n'
        msg += 'On Ubuntu/Debian systems this can be done as follows\n'
        msg += 'sudo apt-get install python-numpy'
        raise Exception(msg)        
        
    err = os.system('python -c "import osgeo" 2> /dev/null')
    if err != 0:
        msg = 'Python module python-gdal must be present\n'
        msg += 'On Ubuntu/Debian systems this can be done as follows\n'
        msg += 'sudo apt-get install python-gdal'
        raise Exception(msg)                
        
    err = os.system('gdalinfo --help-general 2> /dev/null')
    if err != 0:
        msg = 'GDAL must be present\n'
        msg += 'On Ubuntu/Debian systems this can be done as follows\n'
        msg += 'sudo apt-get install gdal-bin'
        raise Exception(msg)                        
        
        
    
    #--------------------------------------------------------------------
    # Determine AIMHOME - this is what needs to be assigned to PYTHONPATH
    #--------------------------------------------------------------------
    cwd = os.getcwd()
    AIMHOME = os.path.split(cwd)[0] # Parent dir

    
    #-----------------------------
    # Verify environment variables
    #-----------------------------    

    modified = False
    ok_to_modify = False
    askuser = True
    for envvar in ['FALL3DHOME', 'PYTHONPATH', 'TEPHRADATA']:
        variable_set = False
        if os.environ.has_key(envvar):
        
            # In case of PYTHONPATH check that it is correct
            if envvar == 'PYTHONPATH':
                pythonpath = os.environ['PYTHONPATH']
                paths = pythonpath.split(':')
                for path in paths:
                    try:
                        files = os.listdir(path)
                    except:
                        pass
                    else:
                        if 'aim' in files:
                            files = os.listdir(os.path.join(path, 'aim'))
                            if __file__ in files:
                                variable_set = True
            else:
                value = os.environ[envvar]
                if value:            
                    variable_set = True
        
        if not variable_set:
            print 'Environment variable %s has not been set' % envvar        
            
            # If we are using the bash shell ask for permission to modify .bashrc
            if get_shell() == 'bash':
                if not ok_to_modify and askuser:
                    answer = raw_input('Would you like me to update your .bashrc file? (Y,N)[Y]')
                    askuser = False # Don't ask again
                    if answer.lower() == 'n':                    
                        print 'OK - you may want to set this variable later'                    
                        ok_to_modify = False
                    else:
                        print 'OK - updated lines in ~/.bashrc will be marked with %s' % update_marker
                        ok_to_modify = True                    
                    print
                
                if ok_to_modify:
                    if envvar == 'PYTHONPATH':
                        # We already know what it should be                    
                        envvalue = AIMHOME
                        print 'Setting it to %s' % AIMHOME
                    else: 
                        # Ask user
                        print 'The environment variable %s should point to a directory where you have permission to write ' % envvar,
                        if envvar == 'TEPHRADATA':
                            print 'e.g. /model_area/tephra'
                        elif envvar == 'FALL3DHOME':
                            print 'e.g. ~/fall3d'
                        envvalue = raw_input('Please enter the directory for %s: ' % envvar)
                    
                    # Modify .bashrc
                    set_bash_variable(envvar, envvalue)
                    modified = True
                    print
        
    if modified:
        print 'Bash configuration file ~/.bashrc has been modified'
        print
        print 'You must run the command'
        print 'source ~/.bashrc'
        print 'or start a new shell. '
        print 
        print 'Then run %s again.' % __file__
        import sys; sys.exit() 
        
    
    #---------------------
    # Determine FALL3DHOME
    #---------------------
    if 'FALL3DHOME' in os.environ:
        FALL3DHOME = os.environ['FALL3DHOME']
    else:
        FALL3DHOME = os.getcwd()
        
    header('Fall3d will be installed in %s' % FALL3DHOME)
        
    makedir(FALL3DHOME)
    os.chdir(FALL3DHOME)
                
    #----------------
    # Download Fall3d
    #----------------
    fall3d = 'Fall3d-5.1.1'
    tarball = fall3d + '.tar.gz'
    url = 'http://www.aifdr.org/projects/aim/raw-attachment/wiki/WikiStart/'
    path = os.path.join(url, tarball)

    if not os.path.isfile(tarball):
        cmd = 'wget ' + path
        run(cmd)

    #----------------------------------------
    # Start installation procedure in earnest
    #----------------------------------------

    # Cleanup
    s = '/bin/rm -rf %s' % fall3d
    run(s)

    print 'Unpacking tarball'
    print
    # Unpack FALL3D using tar:
    #
    # x: Extract
    # v: Be verbose
    # f: Filename coming up
    # z: Uncompress as well
    #
    err = run('tar xvfz %s > /dev/null' % tarball, verbose=False)
    if err != 0:
        msg = 'Could not unpack %s' % tarball
        raise Exception(msg)

    # Get origin directory
    os.chdir(fall3d)
    fall3dpath = os.getcwd()

    # Run makefile
    for directory in ['Sources',
                      'Utilities/SetSrc/Sources',
                      'Utilities/SetGrn/Sources',
                      'Utilities/SetDbs/Sources',
                      'Utilities/Fall3dPostp/Sources']:
        
        os.chdir(directory)
        print 'Changed to', os.getcwd()
        set_compiler('Makefile')

        print 'Compiling'
        err = run('make > make.log 2> make.err', verbose=False)
        if err != 0:
            msg = 'Make in directory %s exited with error code = %d.\n' % (directory, err)
            msg += 'See make.log and make.err for details.'
            raise Exception(msg)
        print    
            
        os.chdir(fall3dpath)


    print 'Done'
    print
    
    
    header('Test the installation and try the examples')
    print 'To test the installation, go to %s and run' % os.path.join(AIMHOME, 
                                                                      'testing')
    print 'python test_all.py'
    print
    print 'You can also run the provided examples individually, e.g.'
    print
    print 'python tambora.py'
    print
    print 'and check the results in tambora_output'
    

    
