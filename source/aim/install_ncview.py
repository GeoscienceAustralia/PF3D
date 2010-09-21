"""Install ncview on Linux platform


"""


url = 'ftp://cirrus.ucsd.edu/pub/ncview'
ncview = 'ncview-1.93g'
tarball = '%s.tar.gz' % ncview



#----------------------------------------
# Auxiliary modules and functions
#----------------------------------------
import os
import sys
from utilities import makedir, run, header, get_shell, set_bash_variable, pipe

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


def install_ubuntu_packages():    
    """Get required Ubuntu packages for geoserver.
       It is OK if they are already installed
    """

    header('Installing Ubuntu packages')     
    
    s = 'apt-get clean'
    run(s, verbose=True)
    
    #s = 'apt-get update'
    #run(s, verbose=True) 

    for package in ['build-essential', 'libxaw7-dev']:
        # Possibly also 'netcdfg-dev'
        
        s = 'apt-get -y install %s' % package
        
        log_base = '%s_install' % package
        try:
            run(s,
                stdout=log_base + '.out',
                stderr=log_base + '.err',                  
                verbose=True)
        except:
            msg = 'Installation of package %s failed. ' % package
            msg += 'See log file %s.out and %s.err for details' % (log_base, log_base)
            raise Exception(msg)
            


def download():
    """ Download ncview
    """

    path = os.path.join(url, tarball)

    if not os.path.isfile(tarball): 
        # FIXME: Should also check integrity of tgz file.
        cmd = 'wget ' + path
        run(cmd, verbose=True)
    else:
        print 'Using tarball: %s' % tarball


def extract():
    """Extract files from tarball
    """
    
    # Cleanup
    #s = '/bin/rm -rf %s' % fall3d_distro
    #run(s, verbose=False)

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

def compile_ncview():
    """Configure and make
    """
    
    cmd = 'cd %s; ./configure' % ncview
    run(cmd)
    
    cmd = 'cd %s; make' % ncview
    run(cmd)    
    
    cmd = 'cd %s; make install' % ncview
    run(cmd)        
    
    


if __name__ == '__main__':

    install_ubuntu_packages()
    download()
    extract()
    compile_ncview()
    

    
