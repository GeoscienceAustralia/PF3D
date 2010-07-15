       subroutine readres
!*******************************************************************
!*  
!*     Reads the results
!*
!*******************************************************************
       use KindType
       use Master
       use InpOut
       use netcdf
       implicit none
!
       integer(ip) :: ipass
       real   (rp) :: pi = 4.0_rp*atan(1.0_rp) 
       
!       
!*** Open netCDF file and get ncID
! 
      if( nf90_open(TRIM(luncname),NF90_NOWRITE, ncID) /= 0 ) & 
          call runend('readres : Error in nf90_open')       
!
!***  Reads offset and scale factor
!
      if( nf90_inq_varid(ncID,TRIM(vancname),iD) /= 0) & 
          call runend('readres : Error getting iD')
      if( nf90_get_att(ncID, iD,'add_offset', add_offset) /= 0 ) & 
         call runend('readres : Error in f90_get_att for time:add_offset')
      if( nf90_get_att(ncID, iD,'scale_factor', scale_factor) /= 0 ) & 
         call runend('readres : Error in f90_get_att for time:scale_factor')
!
!*** Checks for consistence
!
!  
!*** Read variable (time, level, lat, lon) 
!   
      ipass = 0  
      do it = it1,it2
        if( nf90_get_var(ncID,iD,work,start=(/1,1,1,it/),count=(/nx,ny,nz,1/)) /=0 ) &
            call runend('readres: Error reading variable')       
!           
        ipass = ipass + 1  
        if(TRIM(vancname).eq.'hgt') then       
            H(1:nz,ipass) = work(ix,iy,1:nz)
            H(1:nz,ipass) = scale_factor*H(1:nz,ipass) + add_offset  
        else if(TRIM(vancname).eq.'air') then       
            T(1:nz,ipass) = work(ix,iy,1:nz)
            T(1:nz,ipass) = scale_factor*T(1:nz,ipass) + add_offset  
        else if(TRIM(vancname).eq.'uwnd') then       
            U(1:nz,ipass) = work(ix,iy,1:nz)
            U(1:nz,ipass) = scale_factor*U(1:nz,ipass) + add_offset  
        else if(TRIM(vancname).eq.'vwnd') then       
            V(1:nz,ipass) = work(ix,iy,1:nz)
            V(1:nz,ipass) = scale_factor*V(1:nz,ipass) + add_offset  
        end if 
!
      end do
!
!***  Computes umod and udir
!
      do it = 1,np
      do iz = 1,nz
!
        umod(iz,it) = sqrt( U(iz,it)*U(iz,it) + V(iz,it)*V(iz,it) )
!
!***    Gets air direction
!
         if(abs(umod(iz,it)).gt.1e-8_rp) then                     
	        udir(iz,it) = atan2(v(iz,it),u(iz,it))*180_rp/pi ! Ainge in (-180 180)
	     else 
		    if(v(iz,it).gt.1e-8_rp) then
	           udir(iz,it) = 90_rp
	        else if(v(iz,it).lt.-1e-8_rp) then
	           udir(iz,it) = 270_rp
	        else
	           udir(iz,it) = 0_rp
	        end if
	     end if
!
         if(udir(iz,it).lt.0_rp) udir(iz,it) = 360_rp + udir(iz,it)    ! Angle in deg. (0 to 360)
!
         udir(iz,it) = udir(iz,it) + 180_rp  ! income direction
         if(udir(iz,it).gt.360_rp) udir(iz,it) = udir(iz,it) - 360_rp 
!
!***     convert to azimut (origin at N)
!
         udir(iz,it) = udir(iz,it) - 90_rp    ! origin at N
         if(udir(iz,it).lt.0_rp) udir(iz,it) = 360_rp + udir(iz,it) 
!
!***     Clockwise
!
         udir(iz,it) = 360_rp - udir(iz,it)  
!
      end do
      end do
!
!*** Closes the file
!
     if ( nf90_close(ncID) /=0 ) call runend('readres: Error in closing the file')        
!       
       return
       end subroutine readres
