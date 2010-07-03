"""Install Fall3d-6.2 on Linux platform

An environment variable, FALL3DHOME, may be specified to determine
the location of the Fall3d installation.
If it is not specified, Fall3d will be installed within the AIM source tree.
"""

#----------------------------------------
# Auxiliary modules and functions
#----------------------------------------
import os
import sys
from utilities import makedir, run, header, get_shell, set_bash_variable
from config import update_marker, compiler, modules, makefile_content
from config import make_configuration_filename, make_configuration_content
from config import fall3d_distro, url, tarball


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

#def set_compiler(filename):
#    replace_string_in_file(filename, 'FC= ifort',  '#FC= ifort')
#    replace_string_in_file(filename, 'LINKER= ifort',  '#LINKER= ifort')
#    replace_string_in_file(filename, 'FFLAGS= -132',  '#FFLAGS= -132')
#    replace_string_in_file(filename, 'LINKFLAGS= -132',  '#LINKFLAGS= -132')
#
#    replace_string_in_file(filename, '#FC= gfortran',  'FC= gfortran')
#    replace_string_in_file(filename, '#LINKER= gfortran',  'LINKER= gfortran')
#    replace_string_in_file(filename, '#FFLAGS= -ffixed',  'FFLAGS= -ffixed')
#    replace_string_in_file(filename, '#LINKFLAGS= -ffixed',  'LINKFLAGS= -ffixed')


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
        
    err = os.system('gdalinfo --help-general > /dev/null 2> /dev/null')
    if err != 0:
        msg = 'GDAL must be present\n'
        msg += 'On Ubuntu/Debian systems this can be done as follows\n'
        msg += 'sudo apt-get install gdal-bin'
        raise Exception(msg)                        
        
    if not os.path.isfile('/usr/include/netcdf.mod'): 
        msg = 'The NetCDF library must be present\n'
        msg += 'On Ubuntu/Debian systems this can be done as follows\n'
        msg += 'sudo apt-get install libnetcdf-dev'
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
                # Otherwise, just verify that it has been set.
                value = os.environ[envvar]
                if value:            
                    variable_set = True
        
        if not variable_set:
            print 'Environment variable %s has not been set' % envvar        
            
            # If we are using the bash shell ask for permission to modify .bashrc
            if get_shell() == 'bash':
                if not ok_to_modify and askuser:
                    answer = raw_input('Would you like me to update your .bashrc file with reasonable default values? (Y,N)[Y]')
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
                    elif envvar == 'FALL3DHOME':
                        # Use ~/fall3d as default        
                        envvalue = os.path.expanduser('~/fall3d')
                    elif envvar == 'TEPHRADATA': 
                        if os.path.isdir('/model_area'):
                            # Use /model_area/tephra as default if possible
                            makedir('/model_area/tephra')
                            envvalue = '/model_area/tephra'
                        else:
                            # Otherwise use ~/tephra as default                
                            envvalue = os.path.expanduser('~/tephra')

                    
                    # Modify .bashrc
                    print 'Setting environment variable %s to %s' % (envvar, envvalue)
                    set_bash_variable(envvar, envvalue)
                    modified = True
                    
                    # Also assign variables for the rest of this session
                    os.environ[envvar] = envvalue
                    print

                
        
    if modified:
        print 'Bash configuration file ~/.bashrc has been modified'
        print 'You can change it manually if you wish.'
        print
        
        
    
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
    # Download Fall3d version 6 (public version)
    # http://www.bsc.es/projects/earthscience/fall3d/Downloads/Fall3d-PUB.tar.gz
    #----------------

    path = os.path.join(url, tarball)

    if not os.path.isfile(tarball): 
        # FIXME: Should also check integrity of tgz file.
        cmd = 'wget ' + path
        run(cmd, verbose=True)

        
    #----------------------------------------
    # Start installation procedure in earnest
    #----------------------------------------

    # Cleanup
    s = '/bin/rm -rf %s' % fall3d_distro
    run(s, verbose=False)

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
    os.chdir(fall3d_distro)
    fall3dpath = os.getcwd()
    
    #----------
    # Makefiles
    #----------    
    
    # Generate common makefile configuration
    make_configuration = os.path.join(fall3dpath, 'Install', make_configuration_filename)
    fid = open(make_configuration, 'w')
    fid.write(make_configuration_content % (compiler, fall3dpath, fall3dpath) )
    fid.close()
    
    # Generate and run specific makefiles
    for program in ['LibMaster', 'MergeNCEP1', 'SetDbs', 'SetGrn', 'SetSrc', 'Sources_ser']:
    
        mod = modules[program]
        
        if mod.file is None:
            # Generate standard makefile
            fid = open(os.path.join(mod.path, 'Makefile'), 'w')
            fid.write(makefile_content % (fall3dpath, make_configuration_filename, mod.mods, mod.objs, mod.prog))
            fid.close()
        else:
            # Use predefined makefile
            makefile = os.path.join(mod.path, 'Makefile')
            s = 'cp %s %s' % (os.path.join(cwd, mod.file), makefile) 
            run(s, verbose=False)
            
            # Patch include statement
            replace_string_in_file(makefile, 
                                   'include <insert config>', 
                                   'include %s' % make_configuration, 
                                   verbose=False)

        sys.stdout.write('Compiling %s: ' % program)
        run('cd %s; make' % mod.path, 
            stdout=os.path.join(cwd, 'make_%s.stdout' % program), 
            stderr=os.path.join(cwd, 'make_%s.stderr' % program), 
            verbose=False)
    
        #-----------------------------
        # Test presence of executables
        #-----------------------------
        
        p = mod.path.split(os.sep)
        # Strip last dir off path as that is where makefiles put targets
        if len(p) > 1:
            p = os.path.join(*p[:-1])
        else:
            p = ''

        f = os.path.join(fall3dpath, p, mod.prog)     
        if os.path.isfile(f):
            res = 'OK'
        else:
            res = 'FAILED'
            
        print('%s' % res)

    #--------------------------------------------------------
    # Patch the Fall3d scripts to remove hardwired references (FIXME: unnecessary)
    #--------------------------------------------------------

    os.chdir(os.path.join(FALL3DHOME, fall3d_distro, 'Scripts'))
    for program in ['SetDbs', 'SetGrn', 'SetSrc', 'manager', 'Fall3d_Pub']:
        
        # Patch include statement
        replace_string_in_file('Script-' + program, 
                               'set HOME=/Users/arnaufolch/Documents/Software/Fall3d-6.0/PUB/Fall3d-6.2-PUB', 
                               'set HOME=%s' % os.path.join(FALL3DHOME, fall3d_distro),
                               verbose=False)

        

        
    #----------------------------------------------------------------------------
    # Compile and install post-processing source code which is not part of Fall3d
    #----------------------------------------------------------------------------
    
    
    # Write new Makefile relative to install dir (CWD)
    post_proc_path = os.path.join(cwd, 'post-processing')
    print post_proc_path
    fid = open(os.path.join(post_proc_path, 'Makefile'), 'w')
    mods = 'KindType.o Master.o InpOut.o Res_nc.o TimeFun.o'
    objs = 'nc2grd.o runend.o openinp.o readat.o readres.o wrigrd.o'
    prog = 'nc2grd.exe'
    fid.write(makefile_content % (fall3dpath, make_configuration_filename, mods, objs, prog))
    fid.close()
        
    run('cd %s; make' % post_proc_path, 
        stdout=os.path.join(cwd, 'make_%s.stdout' % prog), 
        stderr=os.path.join(cwd, 'make_%s.stderr' % prog), 
        verbose=True)
    
    post_dir = os.path.join(os.path.join(FALL3DHOME, fall3d_distro, 'Utilities', 'nc2grd'))
    run('mkdir %s' % post_dir)
    run('mv %s %s' % (os.path.join(cwd, prog), post_dir))
            
        
    #header('Test the installation and try the examples')
    #print 'To test the installation, go to %s and run' % os.path.join(AIMHOME, 
    #                                                                  'testing')
    #print 'python test_all.py'
    #print
    #print 'You can also run the provided examples individually, e.g.'
    #print
    #print 'python tambora.py'
    #print
    #print 'and check the results in tambora_output'
    

    
