#! /bin/sh -f


include /client_filesystems/shared/home/nielso/fall3d/Fall3d-6.2-PUB/Install/make_configuration.txt


# Do not change anything beyond this line

# Compiler selection
ifeq ($(FC),gfortran)
  FFLAGS= -ffixed-line-length-132 -fdefault-real-8  
  LINKER= $(FC)
  LFLAGS=
endif	
ifeq ($(FC),f90)
  FFLAGS= -extend_source -64
  LINKER= $(FC) -64
  LFLAGS=
endif	
ifeq ($(FC),ifort)
  FFLAGS= -132 -r8 
  LINKER= $(FC) 
  LFLAGS=
endif
ifeq ($(FC),xlf90)
  LINKER= xlf90
  FOPT= -O3 -qstrict -qtune=ppc970 -qarch=ppc970 -qcache=auto -q64 -WF,-D__USE_LARGEFILE64
  FFLAGS= -qfree=f90 -qrealsize=4 -qextname=flush $(FOPT)
  LINKER= $(FC)
  LFLAGS= $(FFLAGS) 
endif


FMODS= KindType.o InpOut.o Master.o Res_nc.o
FOBJS= HazardMaps.o runend.o openinp.o readinp.o readres.o wrires.o readpts.o wripts.o
#
.SUFFIXES:.o .f90 .f
.f90.o:
	$(FC) -c $(FFLAGS) ${INC_NetCDF} $<
#
#----------------------------------------------
#  Tasks
#----------------------------------------------
#
HazardMaps: $(FMODS) $(FOBJS)
	$(LINKER) -o HazardMaps.exe $(FMODS) $(FOBJS) $(LIB_Master) $(LIB_NetCDF) -lnetcdf
	@chmod 770 HazardMaps.exe
	@mv HazardMaps.exe ..
	@echo '---------------------------->>> END OF COMPILATION'
#
new:
	@rm -rf *.o *.mod core*
	@make
#
clean:
	@rm -f core core.* *~ *.o *.mod

