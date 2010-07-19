
compiler = 'gfortran'

update_marker = '# Updated by AIM'
tephra_output_dir = 'tephra' # Name for generated data
make_configuration_filename = 'make_configuration.txt'

# Installation info
fall3d_distro = 'Fall3d-6.2-PUB' # Name of subdir where Fall3d lives
tarball = 'Fall3d-PUB.tar.gz' # Name of compressed distro file
#url = 'http://www.bsc.es/projects/earthscience/fall3d/Downloads' # Original 
#url = 'http://www.aifdr.org/projects/aim/raw-attachment/wiki/WikiStart' # AIFDR mirror (to keep things stable!)
url = 'http://datasim.ov.ingv.it/Downloads' # Location as of late May 2010




# Patching info

# Must be supplied with string interpolation (compiler, fall3dpath, fall3dpath)
make_configuration_content = """
#------------------------------------------
#  Fall3d program - user supplied variables
#------------------------------------------

# Define the compiler (gfortran, f90, xlf90)
FC = %s
                
# Location of the NetCDF library
LIB_NetCDF = -L/usr/lib -lnetcdf -lnetcdff
INC_NetCDF = -I/usr/include
  
# Version
ver = 6.2

# Location of Fall3d
HOME = %s

# Master library
LIB_Master = %s/Utilities/LibMaster/LibMaster.a
"""
    
# Must be supplied with string interpolation (fall3dpath, makefile_configuration_filename, fmods, fobjs, program_name)
# For example
# makefile_content % ('KindType.o Master.o InpOut.o Plume.o Air.o Coordinates.o',
#                      'SetSrc.o openinp.o readinp.o runend.o solvepoint.o solvesuzuki.o....',
#                      'SetSrc.PUB.exe')       

makefile_content = """
#! /bin/sh -f

#----------------------------------------
#  Makefile generated my AIM
#----------------------------------------

include %s/Install/%s


# Compiler selection
ifeq ($(FC),gfortran)
  F90FLAGS = -ffixed-line-length-132  -fdefault-real-8  
  F77FLAGS = -ffixed-line-length-132     
  LINKER = $(FC)
  LFLAGS =
endif	
ifeq ($(FC),f90)
  F90FLAGS = -extend_source -r8 -64
  F77FLAGS = -extend_source -r4 -64  
  LINKER = $(FC) -64
  LFLAGS =
endif	
ifeq ($(FC),ifort)
  F90FLAGS = -132 -r8 
  F77FLAGS = -132   
  LINKER = $(FC) 
  LFLAGS =
endif
ifeq ($(FC),xlf90)
  FOPT = -O3 -qstrict -qtune=ppc970 -qarch=ppc970 -qcache=auto -q64 -qextname=flush 
  F90FLAGS = -qfree=f90 -qrealsize=8 $(FOPT)  
  F77FLAGS = -qrealsize=4 $(FOPT)  
  LINKER = $(FC)
  LFLAGS = $(F90FLAGS) 
endif


.SUFFIXES:.o .f90 .f


.f90.o:
	$(FC) -c $(F90FLAGS) ${INC_NetCDF} $<
.f.o:
	$(FC) -c $(F77FLAGS) $<

#----------------------------------------------
#  Tasks
#----------------------------------------------

FMODS = %s
FOBJS = %s
PROG = %s

target: $(FMODS) $(FOBJS)
	$(LINKER) $(LFLAGS) -o $(PROG) $(FMODS) $(FOBJS) $(LIB_Master) $(LIB_NetCDF) 
	@chmod 770 $(PROG)
	@mv $(PROG) ..
	@echo '---------------------------->>> END OF COMPILATION'


new:
	@rm -rf *.o *.mod core*
	@make target

clean:
	@rm -f core core.* *~ *.o *.mod
"""
    
class Module:
    def __init__(self):
        self.file = None
        
modules = {}        

# LibMaster
mod = Module()
mod.file = 'makefile_libmaster'
mod.prog = 'LibMaster.a'
mod.path = 'Utilities/LibMaster/Sources'
modules['LibMaster'] = mod

# MergeNCEP1
mod = Module()
mod.path = 'Utilities/MergeNCEP1/Sources'
mod.prog = 'MergeNCEP1.PUB.exe'
mod.mods = 'KindType.o Master.o InpOut.o TimeFun.o'
mod.objs = 'MergeNCEP1.o openinp.o inival.o runend.o nc_var3d.o nc_var2d.o write_nc_grid.o'
modules['MergeNCEP1'] = mod

# SetDbs
mod = Module()
mod.path = 'Utilities/SetDbs/Sources'
mod.prog = 'SetDbs.PUB.exe'
mod.mods = 'KindType.o Master.o InpOut.o TimeFun.o MathFun.o Coordinates.o PROF_nc.o CAL_nc.o DBS_nc.o NCEP1_nc.o'
mod.objs = 'SetDbs.PUB.o openinp.o readinp.o runend.o writim.o get_par_ABL.o write_DBS_grid.o write_DBS_data.o read_PROF_grid.o read_CAL_grid.o read_NCEP1_grid.o read_PROF_data.o read_CAL_data.o read_NCEP1_data.o checktime_CAL.o checktime_PROF.o checktime_NCEP1.o'
modules['SetDbs'] = mod

# SetGrn
mod = Module()
mod.path = 'Utilities/SetGrn/Sources'
mod.prog = 'SetGrn.PUB.exe'
mod.mods = 'KindType.o Master.o InpOut.o'
mod.objs = 'SetGrn.o openinp.o readinp.o runend.o setfrac.o wrigrn.o'
modules['SetGrn'] = mod

# SetSrc
mod = Module()
mod.path = 'Utilities/SetSrc/Sources'
mod.prog = 'SetSrc.PUB.exe'
mod.mods = 'KindType.o Master.o InpOut.o Plume.o Air.o Coordinates.o'
mod.objs = 'SetSrc.o openinp.o readinp.o runend.o solvepoint.o solvesuzuki.o getsrc.o getnsrc.o wrisrc_mesh.o wrisrc_nomesh.o wrisrc_void.o openplumef.o readdbs.o setpsi.o wriplumeprop.o wriplumefmass.o wriplumeheight.o solveplume.o lsode.o wriplumetem.o'
modules['SetSrc'] = mod

# Sources_ser
mod = Module()
mod.path = 'Sources_ser'
mod.prog = 'Fall3d_ser.PUB.exe'
mod.mods = 'KindType.o Numeric.o Master.o InpOut.o'
mod.objs = 'Fall3d.PUB.o runend.o setup.o inidat.o reagrn.o readat.PUB.o setpsi.o reagrd.o wridat.o addtime.o meteo.PUB.o reamet.o setrho.o kappa3.o setvset.o source.o reasrc.o corvver.o finddt.o setsrc.PUB.o endstep.o writim.o cmass3d.o cmass2d.o printres_nc.o setvdrydep.o sizloop.o setbcc.o advctzc.o advctx.o advcty.o diffx.o diffy.o diffz.o accum.o setcut.o reaout.o  writps.o wrirst.o rearst.o ter2asl.o' 
modules['Sources_ser'] = mod


#--------------------------------------------------------------------
# Modules that are not part of the Fall3D distro, but included in AIM
# These modules are assumed to sit in the AIM directory
#--------------------------------------------------------------------

# NetCDF to Surfer Grid format
mod = Module()
mod.path = 'aftermarket_modules/nc2grd'
mod.prog = 'nc2grd.exe'
mod.mods = 'KindType.o Master.o InpOut.o Res_nc.o TimeFun.o'
mod.objs = 'nc2grd.o runend.o openinp.o readat.o readres.o wrigrd.o'
modules['nc2grd'] = mod


# Convert NCEP data to wind profile
mod = Module()
mod.path = 'aftermarket_modules/nc2prof'
mod.prog = 'nc2prof.exe'
mod.mods = 'KindType.o Master.o InpOut.o TimeFun.o'
mod.objs = 'nc2prof.o openinp.o runend.o readinp.o readres0.o readres.o wripro.o'
modules['nc2prof'] = mod


# Hazard mapping module aggrating multiple result files
mod = Module()
mod.path = 'aftermarket_modules/HazardMaps'
mod.prog = 'HazardMapping.exe'
mod.mods = 'KindType.o InpOut.o Master.o Res_nc.o'
mod.objs = 'HazardMaps.o runend.o openinp.o readinp.o readres.o wrires.o readpts.o wripts.o'
modules['HazardMaps'] = mod

