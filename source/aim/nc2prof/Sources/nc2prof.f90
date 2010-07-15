       program nc2prof
!*******************************************************************************
!*
!*     Author : A.Folch
!*     Date   : JUL 2010
!*
!*     This program reads several NCEP-1 reanalysis 4-dayly netCDF files 
!*     an extracts a profile at a given location. 
!*
!*     4-dayly NCEP-1 data files (or time subsets) can be download at:
!*     http://www.esrl.noaa.gov/psd/data/gridded/data.ncep.reanalysis.html
!*
!*     Space/Time subsets can be created when downloading (otherwise NCEP1 files cover 
!*     1 year and the globe). If the contents of a file is inconsistent 
!*     with the rest, the program will stop. Only the 4-observations-per-day files 
!*     are contemplated.
!*
!*     The program assumes a single file for variable, and MUST have the following names:
!*
!*     HGT.nc           Geopotential             (pressure file)
!*     TMP.nc           Temperature              (pressure file)
!*     UGRD.nc          u-velocity               (pressure file)
!*     VGRD.nc          v-velocity               (pressure file)
!*
!*     It is the user's responsability to download, rename and place these 11 files
!*     (or a dynamic link) to the same folder of the executable. 
!*
!*******************************************************************************ç
      use KindType
      use InpOut
      use Master
      implicit none
!
!***  File names
!
      lulogname = 'nc2prof.log'  
      luinpname = 'nc2prof.inp'    
      luncuname = 'UGRD.nc'
      luncvname = 'VGRD.nc'   
      lunctname = 'TMP.nc'
      lunchname = 'HGT.nc'            
      luresname = 'profile.out'
!
!***  Opens the log file
!
      call openinp       
!
!***  Reads Input file
!      
      call readinp
!
!***  Reads properties of the ncep1 files
!
      call readres0 
!
!***  Reads the results (all the time steps simultaneously)
!
      vancname = 'hgt'          ! Geopotential height
      luncname = lunchname
      call readres
!
      vancname = 'air'          ! Air temperature
      luncname = lunctname
      call readres      
!
      vancname = 'uwnd'          ! U-velocity
      luncname = luncuname
      call readres  
!
      vancname = 'vwnd'          ! V-velocity
      luncname = luncvname
      call readres  
!
!***  Writes the results
!
      call wripro 
!
!***  Ends the program
!
      call runend('OK')
!      
      end program nc2prof