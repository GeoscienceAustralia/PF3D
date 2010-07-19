      subroutine readres
!************************************************************
!*
!*    Reads data (attributes) from the NetCDF results file 
!*
!************************************************************
      use Master
	  use InpOut
	  use Res_nc
      use netcdf
      implicit none 
!
      logical :: found
      character(len=s_mess) :: message
      integer(ip)    :: istat,icut,kcut
!
!*** Open netCDF file and get ncID
!
     if( nf90_open(TRIM(fres),NF90_NOWRITE, ncID) /= 0 ) call runend('readres : Error in nf90_open')
!
!*** Global Inquire. Gets nDim nVar nAttr
!
     if( nf90_inquire(ncID, nDim, nVar, nAttr) /= 0 ) call runend('readres : Error in nf90_inquire')
!
!**  Inquires the names and lengths of the dimensions  
!
     write(nlog,'(a)') '------------------ '
     write(nlog,'(a)') 'List of dimensions:'
     write(nlog,'(a)') '------------------ '
     do iDim = 1,nDim
        if( nf90_inquire_dimension(ncID,iDim,dimName(iDim),dimLen(iDim)) /= 0 ) &
	        call runend('readres : Error in nf90_inquire_dimension')
        write(nlog,'(a,1x,i5)') TRIM(dimName(iDim)),dimLen(iDim)
     end do
!
!*** Inquires the names and dimensions of variables
!
     write(nlog,'(a)') '----------------- '
     write(nlog,'(a)') 'List of variables:'
     write(nlog,'(a)') '----------------- '
     do iVar = 1,nVar
        if( nf90_inquire_variable(ncID,iVar,varName(iVar),varType(iVar),varDims(iVar),ivoid) /= 0 ) &
	     call runend('readres : Error in nf90_inquire_variable')
        write(nlog,10) TRIM(varName(iVar)),ivoid(1:varDims(iVar))
 10     format(a,' (',100(i2,','))       
        varDimID(iVar,1:maxdim) = ivoid(1:maxdim)     
     end do
!
!*** Reads global attributes
!
     write(nlog,'(a)') '------------------ '
     write(nlog,'(a)') 'List of attributes:'
     write(nlog,'(a)') '------------------ '
!  
!***  First title and averiguates FALL3D version
!
     if( nf90_get_att(ncID, NF90_GLOBAL, nc_title_name, title_nc) /= 0 ) & 
         call runend('readres : Error in f90_get_att for '//TRIM(nc_title_name))
     write(nlog,'(a,1x,a)') TRIM(nc_title_name),TRIM(title_nc)
!
     fall3d_version = '6.0'  ! default
     if(TRIM(title_nc).eq.'Fall3d 6.0 results') then
        fall3d_version = '6.0'
     else if(TRIM(title_nc).eq.'Fall3d 6.1 results') then
        fall3d_version = '6.1'        
     else if(TRIM(title_nc).eq.'Fall3d 6.2 results') then
        fall3d_version = '6.2'
     end if
!
!***  Rest of attributes
!
     if( nf90_get_att(ncID, NF90_GLOBAL, nc_iyr_name, iyr) /= 0 ) & 
         call runend('readres : Error in f90_get_att for '//TRIM(nc_iyr_name))
     write(nlog,20) TRIM(nc_iyr_name),iyr
 20  format(a,1x,i7)
!
     if( nf90_get_att(ncID, NF90_GLOBAL, nc_imo_name, imo) /= 0 ) & 
         call runend('readres : Error in f90_get_att for '//TRIM(nc_imo_name))
     write(nlog,20) TRIM(nc_imo_name),imo
!
     if( nf90_get_att(ncID, NF90_GLOBAL, nc_idy_name, idy) /= 0 ) & 
         call runend('readres : Error in f90_get_att for '//TRIM(nc_idy_name))
     write(nlog,20) TRIM(nc_idy_name),idy
!
     if( nf90_get_att(ncID, NF90_GLOBAL, nc_irunb_name, irunb) /= 0 ) & 
         call runend('readres : Error in f90_get_att for '//TRIM(nc_irunb_name))
     write(nlog,20) TRIM(nc_irunb_name),irunb
!
     if( nf90_get_att(ncID, NF90_GLOBAL, nc_irune_name, irune) /= 0 ) & 
         call runend('readres : Error in f90_get_att for '//TRIM(nc_irune_name))
     write(nlog,20) TRIM(nc_irune_name),irune
!
     ihr = irunb/3600        
     imi = (irunb - (3600*ihr))/60
!     
     if( nf90_get_att(ncID, NF90_GLOBAL, nc_coord_name, coord_sys) /= 0 ) & 
         call runend('readres : Error in f90_get_att for '//TRIM(nc_coord_name))
     write(nlog,'(a,1x,a)') TRIM(nc_coord_name),TRIM(coord_sys)
!
     SELECT CASE(coord_sys)
     case('LON-LAT')
!
       if( nf90_get_att(ncID, NF90_GLOBAL, nc_lonmin_name, lonmin) /= 0 ) & 
           call runend('readres : Error in f90_get_att for '//TRIM(nc_lonmin_name))
       write(nlog,21) TRIM(nc_lonmin_name),lonmin
 21    format(a,1x,f9.4)
!     
       if( nf90_get_att(ncID, NF90_GLOBAL, nc_lonmax_name, lonmax) /= 0 ) & 
           call runend('readres : Error in f90_get_att for '//TRIM(nc_lonmax_name))
       write(nlog,21) TRIM(nc_lonmax_name),lonmax
!
       if( nf90_get_att(ncID, NF90_GLOBAL, nc_latmin_name, latmin) /= 0 ) & 
           call runend('readres : Error in f90_get_att for '//TRIM(nc_latmin_name))
       write(nlog,21) TRIM(nc_latmin_name),latmin
!
       if( nf90_get_att(ncID, NF90_GLOBAL, nc_latmax_name, latmax) /= 0 ) & 
           call runend('readres : Error in f90_get_att for '//TRIM(nc_latmax_name))
       write(nlog,21) TRIM(nc_latmax_name),latmax
!
       do iDim=1,nDim
          if(TRIM(dimName(iDim)).eq.TRIM(nc_lon_name)) then
             nx = dimLEN(iDim)
          else if(TRIM(dimName(iDim)).eq.TRIM(nc_lat_name)) then
             ny = dimLEN(iDim)
          else if(TRIM(dimName(iDim)).eq.TRIM(nc_alt_name)) then
             nz = dimLEN(iDim)
          else if(TRIM(dimName(iDim)).eq.TRIM(nc_time_name)) then
             nt = dimLEN(iDim)
             allocate(times(nt))
          end if
       end do
!                              
       dlon = (lonmax-lonmin)/(nx-1)
       dlat = (latmax-latmin)/(ny-1)
!
     case('UTM')
!
       if( nf90_get_att(ncID, NF90_GLOBAL, nc_xmin_name, xmin) /= 0 ) & 
           call runend('readres : Error in f90_get_att for '//TRIM(nc_xmin_name))
       write(nlog,22) TRIM(nc_xmin_name),xmin
 22    format(a,1x,f9.1)
!     
       if( nf90_get_att(ncID, NF90_GLOBAL, nc_xmax_name, xmax) /= 0 ) & 
           call runend('readres : Error in f90_get_att for '//TRIM(nc_xmax_name))
       write(nlog,22) TRIM(nc_xmax_name),xmax
!
       if( nf90_get_att(ncID, NF90_GLOBAL, nc_ymin_name, ymin) /= 0 ) & 
           call runend('readres : Error in f90_get_att for '//TRIM(nc_ymin_name))
       write(nlog,22) TRIM(nc_ymin_name),ymin
!
       if( nf90_get_att(ncID, NF90_GLOBAL, nc_ymax_name, ymax) /= 0 ) & 
           call runend('readres : Error in f90_get_att for '//TRIM(nc_ymax_name))
       write(nlog,22) TRIM(nc_ymax_name),ymax
!
       do iDim=1,nDim
          if(TRIM(dimName(iDim)).eq.TRIM(nc_x_name)) then
             nx = dimLEN(iDim)
          else if(TRIM(dimName(iDim)).eq.TRIM(nc_y_name)) then
             ny = dimLEN(iDim)
          else if(TRIM(dimName(iDim)).eq.TRIM(nc_alt_name)) then
             nz = dimLEN(iDim)
          else if(TRIM(dimName(iDim)).eq.TRIM(nc_time_name)) then
             nt = dimLEN(iDim)
             allocate(times(nt))
          end if
       end do
!                              
       dx = (xmax-xmin)/(nx-1)
       dy = (ymax-ymin)/(ny-1)
!     
     END SELECT 
!
!*** Reads vertical layers
!
     found = .false.
     iVar = 0
     do while(.not.found)
        iVar = iVar + 1
        if( iVar == nVar+1 ) & 
	    call runend('readres : variable '//TRIM(nc_alt_name)//' not found')
        if( TRIM(varName(iVar)) == TRIM(nc_alt_name) ) then
           if( nf90_get_var(ncID,iVar,zlayer(1:nz))  /= 0) & 
	       call runend('readres : error reading variable '//TRIM(nc_alt_name))
           found = .true.
        end if
     end do   
!
!*** Reads time instants and converts into seconds
!
     found = .false.
     iVar = 0
     do while(.not.found)
        iVar = iVar + 1
        if( iVar == nVar+1 ) & 
	    call runend('readres : variable '//TRIM(nc_time_name)//' not found')
        if( TRIM(varName(iVar)) == TRIM(nc_time_name) ) then
           if( nf90_get_var(ncID,iVar,times(1:nt))  /= 0) & 
	       call runend('readres : error reading variable '//TRIM(nc_time_name))
           found = .true.
        end if
     end do   
     times = times*3600.0_rp
!
!*** If necessary correct the cuts 
!
     kcut = ncut
     do icut = ncut,1,-1
        if(zcut(icut).gt.zlayer(nz))  kcut = kcut-1
     end do
     ncut = kcut
!
!***  Ends
!     
     return
     end subroutine readres