       subroutine readres0
!*******************************************************************
!*  
!*
!*******************************************************************
       use KindType
       use Master
       use InpOut
       use TimeFun
       use netcdf
       implicit none   
!
       logical     :: found        
       integer(ip) :: ipyr0,ipmo0,ipdy0,iphr0,ipmi0,ipse0
!
!***  Opens file
!
      if( nf90_open(TRIM(lunchname),NF90_NOWRITE, ncID) /= 0 ) & 
         call runend('readres0 : Error in nf90_open')       
!
!*** Global Inquire. Gets nDim nVar nAttr
!
     if( nf90_inquire(ncID, nDim, nVar, nAttr) /= 0 ) call runend('readres0 : Error in nf90_inquire')
     nDimMax = NF90_MAX_VAR_DIMS
! 
     allocate( dimName (nDim) )
     allocate( varName (nVar) )
     allocate( dimLen  (nDim) )
     allocate( varDims (nVar) )
     allocate( varType (nVar) )
     allocate( ivoid   (nDimMax) )
!
!*** Averiguates dimensions
!     
     do iDim = 1,nDim
        if( nf90_inquire_dimension(ncID,iDim,dimName(iDim),dimLen(iDim)) /= 0 ) &
	        call runend('readres0 : Error in nf90_inquire_dimension')
        if(TRIM(dimName(iDim)).eq.'lon') then
           nx = dimLEN(iDim)
        else if(TRIM(dimName(iDim)).eq.'lat') then
           ny = dimLEN(iDim)
        else if(TRIM(dimName(iDim)).eq.'level') then
           nz = dimLEN(iDim)
        end if
     end do
!
!*** allocates 
!
     allocate(lon  (nx))
     allocate(lat  (ny))
     allocate(level(nz))
!
!*** Reads lon/lat/levels
!
     if( nf90_inq_varid(ncID,'lon',iD) /= 0) call runend('readres0 : Error getting iD for lon')
     if( nf90_get_var(ncID,iD,lon,start=(/1/),count=(/nx/)) /=0 ) &
           call runend('readres0: Error reading lon')      
!
     if( nf90_inq_varid(ncID,'lat',iD) /= 0) call runend('readres0 : Error getting iD for lat')
     if( nf90_get_var(ncID,iD,lat,start=(/1/),count=(/ny/)) /=0 ) &
           call runend('readres0: Error reading lat')
!
     if( nf90_inq_varid(ncID,'level',iD) /= 0) call runend('readres0 : Error getting iD for level')
     if( nf90_get_var(ncID,iD,level,start=(/1/),count=(/nz/)) /=0 ) &
           call runend('readres0: Error reading level')
!
!***  Reads attributes to check time and space consistency 
!
     if( nf90_inq_varid(ncID,'lon',varID) /= 0) &
        call runend('readres0 : Error getting var_ID')
     if( nf90_get_att(ncID, varID,'actual_range', data_lon_range) /= 0 ) & 
         call runend('readres0 : Error in f90_get_att for lon:actual_range')
!
     if( nf90_inq_varid(ncID,'lat',varID) /= 0) &
        call runend('readres0 : Error getting var_ID')
     if( nf90_get_att(ncID, varID,'actual_range', data_lat_range) /= 0 ) & 
         call runend('readres0 : Error in f90_get_att for lat:actual_range')
!
     if( nf90_inq_varid(ncID,'level',varID) /= 0) &
        call runend('readres0 : Error getting var_ID')
     if( nf90_get_att(ncID, varID,'actual_range', data_level_range) /= 0 ) & 
         call runend('readres0 : Error in f90_get_att for lat:actual_range')
!
     if( nf90_inq_varid(ncID,'time',varID) /= 0) &
        call runend('readres0 : Error getting var_ID')
     if( nf90_get_att(ncID, varID,'actual_range', data_time_range) /= 0 ) & 
         call runend('readres0 : Error in f90_get_att for time:actual_range')
!
	   write(lulog,20) data_lon_range,data_lat_range,data_level_range,data_time_range
    20 format(/, &
              'ncep1 data',/, &
              'lon:actual_range   : ',2(f6.1,1x),/,& 
              'lat:actual_range   : ',2(f6.1,1x),/,& 
              'level:actual_range : ',2(f6.1,1x),/,& 
              'time:actual_range  : ',2(f12.1,1x)) 
!
!*** Close the file
!
      if( nf90_close(ncID) /= 0) & 
         call runend('readres0 : Error in nf90_close')        
!
!***  Determines the number of times 
!
      t1 = data_time_range(1)
      t2 = data_time_range(2)
!
!***  Computes ibyr,ibmo,ibdy,ibhr and ieyr,iemo,iedy,iehr
!***  WARNING: It is necessary to add 13 extra days because NCEP1 refers
!***  to Gregorian calendar whereas addtime routine computes in Julian
!
      call addtime(1,1,1,0,ibyr,ibmo,ibdy,ibhr,ibmi,ibse,(3600*data_time_range(1)+13*86400) )
      write(lulog,30) ibyr,ibmo,ibdy,ibhr
  30  format('From       ',/,    &
             '  year   : ',i6,/, &  
             '  month  : ',i6,/, &
             '  day    : ',i6,/, &         
             '  hour   : ',i6) 
!
      call addtime(1,1,1,0,ieyr,iemo,iedy,iehr,iemi,iese,(3600*data_time_range(2)+13*86400) )
      write(lulog,40) ieyr,iemo,iedy,iehr
  40  format('To         ',/,    &
             '  year   : ',i6,/, &  
             '  month  : ',i6,/, &
             '  day    : ',i6,/, &         
             '  hour   : ',i6)                 
!
!***  Determines the number of time steps
!
      dt =  6 
      nt = INT((t2-t1)/dt+1)
!
!***  Determines the extraction first and last step and checks time consistency
!
      found = .false.
      it1 = 0
      do while(.not.found)
         it1 = it1 + 1
         call addtime(ibyr,ibmo,ibdy,ibhr,ipyr0,ipmo0,ipdy0,iphr0,ipmi0,ipse0,((it1-1)*6*3600.0_rp) )        
         if( (ipyr0.eq.pbyr).and.(ipmo0.eq.pbmo).and.(ipdy0.eq.pbdy).and.(iphr0.eq.pbhr) ) then
             found = .true.
         end if
         if( (it1.eq.nt).and.(.not.found) ) then
             call runend('Initial extract time not found in the ncep interval')
         end if
      end do
!
      found = .false.
      it2 = 0
      do while(.not.found)
         it2 = it2 + 1
         call addtime(ibyr,ibmo,ibdy,ibhr,ipyr0,ipmo0,ipdy0,iphr0,ipmi0,ipse0,((it2-1)*6*3600.0_rp) )        
         if( (ipyr0.eq.peyr).and.(ipmo0.eq.pemo).and.(ipdy0.eq.pedy).and.(iphr0.eq.pehr) ) then
             found = .true.
         end if
         if( (it2.eq.nt).and.(.not.found) ) then
             call runend('Final extract time not found in the ncep interval')
         end if
      end do         
!
!***  Determines ix and iy (the nearest point) and checks 
!***  WARNING: latitude is ordered from N to S
!
      found = .false.
      ix = 0
      do while(.not.found)
        ix = ix + 1
        if( (lon_v.ge.lon(ix)).and.(lon_v.lt.lon(ix+1)) ) then
           found = .true.
        end if
        if( (ix.eq.(nx-1)).and.(.not.found) ) then
             call runend('Vent longitude not found in the ncep interval')
         end if
      end do
! 
      found = .false.      
      iy = 0
      do while(.not.found)
        iy = iy + 1
        if( (lat_v.le.lat(iy)).and.(lat_v.gt.lat(iy+1)) ) then
           found = .true.
        end if
        if( (iy.eq.(ny-1)).and.(.not.found) ) then
             call runend('Vent latitude not found in the ncep interval')
         end if
      end do
!
!***  Writes the file
!
      write(lulog,50) nt,nz,it1,it2,lon(ix),lat(iy)
  50  format(/, &
             'Extraction',/, &
             'Number of time steps    : ',i6,/,&
             'Number of pressure lev  : ',i6,/,&
             'Extract from ncep1 step : ',i6,/,&
             'To           ncep1 step : ',i6,/,&
             'ncep longitude          : ',f7.2,/,&
             'ncep latitude           : ',f7.2)                
!
!*** allocates
!
     np = it2-it1+1                   ! number of profiles 
     allocate(u    (nz,np))
     allocate(v    (nz,np))
     allocate(T    (nz,np))
     allocate(H    (nz,np))
     allocate(umod (nz,np))
     allocate(udir (nz,np))
     allocate(work (nx,ny,nz))
!
      return
      end subroutine readres0         