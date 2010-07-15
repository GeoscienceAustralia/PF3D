#! /bin/sh -f
#----------------------------------------
#  MergeNCEP1 utility program
#----------------------------------------
#

include /client_filesystems/shared/home/nielso/fall3d/Fall3d-6.2-PUB/Install/make_configuration.txt

#----------------------------------------
# Do not change anything beyond this line
#----------------------------------------
#
# Compiler selection
#
ifeq ($(FC),gfortran)
  FFLAGS= -ffixed-line-length-132   
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
#
# Lists
#
FMODS= KindType.o Master.o InpOut.o TimeFun.o
FOBJS= nc2prof.o openinp.o runend.o readinp.o readres0.o readres.o wripro.o
#
.SUFFIXES:.o .f90
#
#  Tasks
#
.f90.o:
	$(FC) -c $(FFLAGS) ${INC_NetCDF} $<
#
nc2prof: $(FMODS) $(FOBJS)
	$(LINKER) $(LFLAGS) -o nc2prof.exe $(FMODS) $(FOBJS) $(LIB_NetCDF) $(LIB_Master)
	@chmod 770 nc2prof.exe
	@mv nc2prof.exe ..
	@echo '---------------------------->>> END OF COMPILATION'
#
new:
	@rm -rf *.o *.mod core*
	@make
#
clean:
	@rm -f core core.* *~ *.o *.mod
