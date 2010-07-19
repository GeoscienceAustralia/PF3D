      subroutine readres
!************************************************************
!*
!*    Reads data from the NetCDF results file 
!*
!************************************************************
      use Master
	  use InpOut
	  use Res_nc
      use netcdf
      implicit none 
!
!***  Reads dimensions and allocates memory. this is done for each file because
!***  the number of time steps may vary from run to run
!
      call readres0
!
!*** Open netCDF file and get ncID
!
     if( nf90_open(TRIM(fres),NF90_NOWRITE, ncID) /= 0 ) call runend('readres : Error in nf90_open')
!
!*** Reads data for the current map
!
     if(pp_load) then
      do it = 1,nt
        if( nf90_inq_varid(ncID,nc_load0_name,iD) /= 0) call runend('readres : Error getting iD')
        if( nf90_get_var(ncID,iD,work2d,start=(/1,1,it/),count=(/nx,ny/)) /=0 ) &
           call runend('readres: Error reading load')   
        do iy = 1,ny
           do ix = 1,nx
              load(ix,iy,it) = work2d(ix,iy)
           end do
        end do    
      end do
    end if
!
    if(pp_fl050) then
     do it = 1,nt
        if( nf90_inq_varid(ncID,nc_FL050_name,iD) /= 0) call runend('readres : Error getting iD for FL050')
        if( nf90_get_var(ncID,iD,work2d,start=(/1,1,it/),count=(/nx,ny/)) /=0 ) &
           call runend('readres: Error reading FL050')   
        do iy = 1,ny
           do ix = 1,nx
              FL050(ix,iy,it) = work2d(ix,iy)
           end do
        end do    
     end do
    end if
!
    if(pp_fl100) then
     do it = 1,nt
        if( nf90_inq_varid(ncID,nc_FL100_name,iD) /= 0) call runend('readres : Error getting iD for FL050')
        if( nf90_get_var(ncID,iD,work2d,start=(/1,1,it/),count=(/nx,ny/)) /=0 ) &
           call runend('readres: Error reading FL100')   
        do iy = 1,ny
           do ix = 1,nx
              FL100(ix,iy,it) = work2d(ix,iy)
           end do
        end do    
     end do
    end if
!
    if(pp_fl150) then
     do it = 1,nt
        if( nf90_inq_varid(ncID,nc_FL150_name,iD) /= 0) call runend('readres : Error getting iD for FL050')
        if( nf90_get_var(ncID,iD,work2d,start=(/1,1,it/),count=(/nx,ny/)) /=0 ) &
           call runend('readres: Error reading FL150')   
        do iy = 1,ny
           do ix = 1,nx
              FL150(ix,iy,it) = work2d(ix,iy)
           end do
        end do    
     end do
    end if
!
    if(pp_fl200) then
     do it = 1,nt
        if( nf90_inq_varid(ncID,nc_FL200_name,iD) /= 0) call runend('readres : Error getting iD for FL050')
        if( nf90_get_var(ncID,iD,work2d,start=(/1,1,it/),count=(/nx,ny/)) /=0 ) &
           call runend('readres: Error reading FL200')   
        do iy = 1,ny
           do ix = 1,nx
              FL200(ix,iy,it) = work2d(ix,iy)
           end do
        end do    
     end do
    end if
!
    if(pp_fl250) then
     do it = 1,nt
        if( nf90_inq_varid(ncID,nc_FL250_name,iD) /= 0) call runend('readres : Error getting iD for FL050')
        if( nf90_get_var(ncID,iD,work2d,start=(/1,1,it/),count=(/nx,ny/)) /=0 ) &
           call runend('readres: Error reading FL250')   
        do iy = 1,ny
           do ix = 1,nx
              FL250(ix,iy,it) = work2d(ix,iy)
           end do
        end do    
     end do
    end if
!
    if(pp_fl300) then
     do it = 1,nt
        if( nf90_inq_varid(ncID,nc_fl300_name,iD) /= 0) call runend('readres : Error getting iD')
        if( nf90_get_var(ncID,iD,work2d,start=(/1,1,it/),count=(/nx,ny/)) /=0 ) &
           call runend('readres: Error reading FL300')   
        do iy = 1,ny
           do ix = 1,nx
              fl300(ix,iy,it) = work2d(ix,iy)
           end do
        end do    
     end do
    end if
!
!*** Closes the file
!
     if ( nf90_close(ncID) /=0 ) call runend('readres: Error in closing the file')     
!
     return
     end subroutine readres
!
!
!
      subroutine readres0
!************************************************************
!*
!*    Reads dimensions and allocates memory. Also it reads
!*    coordinate variables
!*
!************************************************************
      use Master
	  use InpOut
	  use Res_nc
      use netcdf
      implicit none 
!
      integer(ip), save :: ipass = 0 
      logical           :: found
!
!*** Counter
!
     ipass = ipass + 1
!
!*** Dellocates memory related to times
!
     if(ipass.gt.1) then
        deallocate(times)
        if(pp_load ) deallocate(load )    
        if(pp_fl300) deallocate(FL300)
        if(pp_fl250) deallocate(FL250)
        if(pp_fl200) deallocate(FL200)
        if(pp_fl150) deallocate(FL150)
        if(pp_fl100) deallocate(FL100)
        if(pp_fl050) deallocate(FL050)
     end if
!
!*** Open netCDF file and get ncID
!
     if( nf90_open(TRIM(fres),NF90_NOWRITE, ncID) /= 0 ) call runend('readres0 : Error in nf90_open')
!
!*** Global Inquire. Gets nDim nVar nAttr
!
     if( nf90_inquire(ncID, nDim, nVar, nAttr) /= 0 ) call runend('readres0 : Error in nf90_inquire')
!
!**  Inquires the names and lengths of the dimensions  
!
     if(ipass == 1) then
        write(nlog,'(a)') '------------------ '
        write(nlog,'(a)') 'List of dimensions:'
        write(nlog,'(a)') '------------------ '
     end if
     do iDim = 1,nDim
        if( nf90_inquire_dimension(ncID,iDim,dimName(iDim),dimLen(iDim)) /= 0 ) &
	        call runend('readres0 : Error in nf90_inquire_dimension')
        if(ipass == 1) write(nlog,'(a,1x,i5)') TRIM(dimName(iDim)),dimLen(iDim)
     end do
!
!*** Inquires the names and dimensions of variables
!
     if(ipass == 1) then
       write(nlog,'(a)') '----------------- '
       write(nlog,'(a)') 'List of variables:'
       write(nlog,'(a)') '----------------- '
     end if
     do iVar = 1,nVar
        if( nf90_inquire_variable(ncID,iVar,varName(iVar),varType(iVar),varDims(iVar),ivoid) /= 0 ) &
	        call runend('readres0 : Error in nf90_inquire_variable')
        if(ipass == 1) write(nlog,10) TRIM(varName(iVar)),ivoid(1:varDims(iVar))
 10     format(a,' (',100(i2,','))       
        varDimID(iVar,1:maxdim) = ivoid(1:maxdim)     
     end do
!
!*** Reads global attributes
!
     if(ipass == 1) then
        write(nlog,'(a)') '------------------ '
        write(nlog,'(a)') 'List of attributes:'
        write(nlog,'(a)') '------------------ '      
     end if 
!     

     if( nf90_get_att(ncID, NF90_GLOBAL, nc_coord_name, coord_sys) /= 0 ) & 
         call runend('readres : Error in f90_get_att for '//TRIM(nc_coord_name))
     if(ipass == 1) write(nlog,'(a,1x,a)') TRIM(nc_coord_name),TRIM(coord_sys)
!
     SELECT CASE(coord_sys)
     case('LON-LAT')
!
       if( nf90_get_att(ncID, NF90_GLOBAL, nc_lonmin_name, lonmin0) /= 0 ) & 
           call runend('readres : Error in f90_get_att for '//TRIM(nc_lonmin_name))
       if(ipass == 1) write(nlog,21) TRIM(nc_lonmin_name),lonmin0
 21    format(a,1x,f9.4)
!     
       if( nf90_get_att(ncID, NF90_GLOBAL, nc_lonmax_name, lonmax0) /= 0 ) & 
           call runend('readres : Error in f90_get_att for '//TRIM(nc_lonmax_name))
       if(ipass == 1) write(nlog,21) TRIM(nc_lonmax_name),lonmax0
!
       if( nf90_get_att(ncID, NF90_GLOBAL, nc_latmin_name, latmin0) /= 0 ) & 
           call runend('readres : Error in f90_get_att for '//TRIM(nc_latmin_name))
       if(ipass == 1) write(nlog,21) TRIM(nc_latmin_name),latmin0
!
       if( nf90_get_att(ncID, NF90_GLOBAL, nc_latmax_name, latmax0) /= 0 ) & 
           call runend('readres : Error in f90_get_att for '//TRIM(nc_latmax_name))
       if(ipass == 1) write(nlog,21) TRIM(nc_latmax_name),latmax0
!
       do iDim=1,nDim
          if(TRIM(dimName(iDim)).eq.TRIM(nc_lon_name)) then
             nx0 = dimLEN(iDim)
          else if(TRIM(dimName(iDim)).eq.TRIM(nc_lat_name)) then
             ny0 = dimLEN(iDim)
          else if(TRIM(dimName(iDim)).eq.TRIM(nc_alt_name)) then
             nz0 = dimLEN(iDim)
          else if(TRIM(dimName(iDim)).eq.TRIM(nc_tim_name)) then
             nt0 = dimLEN(iDim)
          end if
       end do
!                              
       dlon = (lonmax0-lonmin0)/(nx0-1)
       dlat = (latmax0-latmin0)/(ny0-1)
!
!***   Checks       
!
       if(ipass.gt.1) then
          if(lonmin.ne.lonmin0) call runend('Different values for lonmin0 in files')
          if(lonmax.ne.lonmax0) call runend('Different values for lonmax0 in files')
          if(latmin.ne.latmin0) call runend('Different values for latmin0 in files')
          if(latmax.ne.latmax0) call runend('Different values for latmax0 in files')        
          if(nx.ne.nx0) call runend('Different values for nx0 in files')
          if(ny.ne.ny0) call runend('Different values for ny0 in files')
          if(nz.ne.nz0) call runend('Different values for nz0 in files')
       else
          continue
       end if
!
       lonmin = lonmin0
       lonmax = lonmax0
       latmin = latmin0
       latmax = latmax0      
       nx = nx0
       ny = ny0
       nz = nz0
       nt = nt0 
!                
     case('UTM')
!
       if( nf90_get_att(ncID, NF90_GLOBAL, nc_xmin_name, xmin0) /= 0 ) & 
           call runend('readres : Error in f90_get_att for '//TRIM(nc_xmin_name))
       if(ipass == 1) write(nlog,22) TRIM(nc_xmin_name),xmin0
 22    format(a,1x,f9.1)
!     
       if( nf90_get_att(ncID, NF90_GLOBAL, nc_xmax_name, xmax0) /= 0 ) & 
           call runend('readres : Error in f90_get_att for '//TRIM(nc_xmax_name))
       if(ipass == 1) write(nlog,22) TRIM(nc_xmax_name),xmax0
!
       if( nf90_get_att(ncID, NF90_GLOBAL, nc_ymin_name, ymin0) /= 0 ) & 
           call runend('readres : Error in f90_get_att for '//TRIM(nc_ymin_name))
       if(ipass == 1) write(nlog,22) TRIM(nc_ymin_name),ymin0
!
       if( nf90_get_att(ncID, NF90_GLOBAL, nc_ymax_name, ymax0) /= 0 ) & 
           call runend('readres : Error in f90_get_att for '//TRIM(nc_ymax_name))
       if(ipass == 1) write(nlog,22) TRIM(nc_ymax_name),ymax0
!
       do iDim=1,nDim
          if(TRIM(dimName(iDim)).eq.TRIM(nc_x_name)) then
             nx0 = dimLEN(iDim)
          else if(TRIM(dimName(iDim)).eq.TRIM(nc_y_name)) then
             ny0 = dimLEN(iDim)
          else if(TRIM(dimName(iDim)).eq.TRIM(nc_alt_name)) then
             nz0 = dimLEN(iDim)
          else if(TRIM(dimName(iDim)).eq.TRIM(nc_tim_name)) then
             nt0 = dimLEN(iDim)
          end if
       end do
!                              
       dx = (xmax0-xmin0)/(nx0-1)
       dy = (ymax0-ymin0)/(ny0-1)
!
!***   Checks       
!
       if(ipass.gt.1) then
          if(xmin.ne.xmin0) call runend('Different values for xmin0 in files')
          if(xmax.ne.xmax0) call runend('Different values for xmax0 in files')
          if(ymin.ne.ymin0) call runend('Different values for ymin0 in files')
          if(ymax.ne.ymax0) call runend('Different values for ymax0 in files')        
          if(nx.ne.nx0) call runend('Different values for nx0 in files')
          if(ny.ne.ny0) call runend('Different values for ny0 in files')
          if(nz.ne.nz0) call runend('Different values for nz0 in files')
       else
          continue
       end if
!
       xmin = xmin0
       xmax = xmax0
       ymin = ymin0
       ymax = ymax0      
       nx = nx0
       ny = ny0
       nz = nz0
       nt = nt0 
!     
     END SELECT 
!
!*** Reads time instants (do not convert into seconds)
!
     allocate(times(nt))
     found = .false.
     iVar = 0
     do while(.not.found)
        iVar = iVar + 1
        if( iVar == nVar+1 ) & 
	    call runend('readres : variable '//TRIM(nc_tim_name)//' not found')
        if( TRIM(varName(iVar)) == TRIM(nc_tim_name) ) then
           if( nf90_get_var(ncID,iVar,times(1:nt))  /= 0) & 
	       call runend('readres : error reading variable '//TRIM(nc_tim_name))
           found = .true.
        end if
     end do   
!
!***  Writes the log file
!
      write(nlog,100) TRIM(fres),nt,times(1),times(nt)
      call flush(nlog)
  100 format('Reading netCDF file : ',a,/, &
             'Numer of time steps : ',i5,' from ',f9.2,' to ',f9.2)
!
!*** Allocates memory
!
     if( ipass.eq.1) then
        allocate(lon   (nx))
        allocate(lat   (ny))
        allocate(work2d(nx,ny))
        work2d = 0.
        allocate(isoc  (nx,ny,nload))
        isoc = 0.
        allocate(nmaps_isoc(nx,ny,nload))
        nmaps_isoc = 0
!
        if(pp_isoc) then
          allocate(pisoc (nx,ny,nload))
          pisoc  = 0.
        end if
        if(pp_load) then
           allocate(pload (nx,ny,nload))
           pload  = 0.
        end if
        if(pp_fl300) then
          allocate(pfl300(nx,ny,nfl  ))
          pfl300 = 0.
        end if
        if(pp_fl250) then
          allocate(pfl250(nx,ny,nfl  ))
          pfl250 = 0.
        end if
        if(pp_fl200) then
          allocate(pfl200(nx,ny,nfl  ))
          pfl200 = 0.
        end if
        if(pp_fl150) then
          allocate(pfl150(nx,ny,nfl  ))
          pfl150 = 0.
        end if
        if(pp_fl100) then
          allocate(pfl100(nx,ny,nfl  ))
          pfl100 = 0.
        end if        
        if(pp_fl050) then         
          allocate(pFL050 (nx,ny,nfl  ))
          pFL050 = 0.
        end if
     end if
 !
     if(pp_load ) allocate(load (nx,ny,nt))    
     if(pp_fl300) allocate(FL300(nx,ny,nt))
     if(pp_fl250) allocate(FL250(nx,ny,nt))
     if(pp_fl200) allocate(FL200(nx,ny,nt))
     if(pp_fl150) allocate(FL150(nx,ny,nt))
     if(pp_fl100) allocate(FL100(nx,ny,nt))
     if(pp_fl050) allocate(FL050(nx,ny,nt))
!
!*** Reads coordinate variables
!
     if(ipass.eq.1) then
       SELECT CASE(coord_sys)
       case('LON-LAT')
!
      if( nf90_inq_varid(ncID,nc_lon_name,iD) /= 0) call runend('readres0 : Error getting iD')
      if( nf90_get_var(ncID,iD,lon,count=(/nx/)) /=0 ) call runend('readres0: Error reading lon')   
!
      if( nf90_inq_varid(ncID,nc_lat_name,iD) /= 0) call runend('readres0 : Error getting iD')
      if( nf90_get_var(ncID,iD,lat,count=(/ny/)) /=0 ) call runend('readres0: Error reading lat') 
!
       case('UTM')
!
      if( nf90_inq_varid(ncID,nc_x_name,iD) /= 0) call runend('readres0 : Error getting iD')
      if( nf90_get_var(ncID,iD,lon,count=(/nx/)) /=0 ) call runend('readres0: Error reading lon')   
!
      if( nf90_inq_varid(ncID,nc_y_name,iD) /= 0) call runend('readres0 : Error getting iD')
      if( nf90_get_var(ncID,iD,lat,count=(/ny/)) /=0 ) call runend('readres0: Error reading lat') 
!
       END SELECT
     end if
!
!*** Closes the file
!
     if ( nf90_close(ncID) /=0 ) call runend('readres0: Error in closing the file') 
!
!***  Ends
!     
     return
     end subroutine readres0