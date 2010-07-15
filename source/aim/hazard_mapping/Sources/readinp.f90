    subroutine readinp
!************************************************************
!*
!*    Reads data from the input file 
!*
!************************************************************
    use Master
    use InpOut
    implicit none 
!
    character(len=s_name) :: wvoid
    character(len=s_mess) :: message
    integer(ip)           :: istat
!
!***  Initializations
!
     pp_load  = .false.
     pp_FL050 = .false.
     pp_FL100 = .false.
     pp_FL150 = .false.
     pp_FL200 = .false.
     pp_FL250 = .false.
     pp_FL300 = .false.
!
!*** Reads vent coordinates
!
      call get_input_rea  &
	       (finp,'COORDINATES','LON_VENT',lon_v,1,istat,message)
      if(istat.gt.0) call wriwar(message)
      if(istat.lt.0) call runend('LON_VENT record not found')
!
      call get_input_rea  &
	       (finp,'COORDINATES','LAT_VENT',lat_v,1,istat,message)
      if(istat.gt.0) call wriwar(message)
      if(istat.lt.0) call runend('LAT_VENT record not found')
!
!***  Select which variables to plot
!
      call get_input_cha & 
           (finp,'POSTPROCESS','ISOCHRONES',wvoid,1,istat,message)
      if(istat.gt.0) call wriwar(message)
      if(TRIM(wvoid).eq.'yes'.or.TRIM(wvoid).eq.'YES') pp_isoc = .true.
 !     
      call get_input_cha & 
           (finp,'POSTPROCESS','LOAD',wvoid,1,istat,message)
      if(istat.gt.0) call wriwar(message)
      if(TRIM(wvoid).eq.'yes'.or.TRIM(wvoid).eq.'YES') pp_load = .true.
!
      call get_input_cha & 
           (finp,'POSTPROCESS','FL050',wvoid,1,istat,message)
      if(istat.gt.0) call wriwar(message)
      if(TRIM(wvoid).eq.'yes'.or.TRIM(wvoid).eq.'YES') pp_FL050 = .true.
!
      call get_input_cha & 
           (finp,'POSTPROCESS','FL100',wvoid,1,istat,message)
      if(istat.gt.0) call wriwar(message)
      if(TRIM(wvoid).eq.'yes'.or.TRIM(wvoid).eq.'YES') pp_FL100 = .true.
!
      call get_input_cha & 
           (finp,'POSTPROCESS','FL150',wvoid,1,istat,message)
      if(istat.gt.0) call wriwar(message)
      if(TRIM(wvoid).eq.'yes'.or.TRIM(wvoid).eq.'YES') pp_FL150 = .true.
!
      call get_input_cha & 
           (finp,'POSTPROCESS','FL200',wvoid,1,istat,message)
      if(istat.gt.0) call wriwar(message)
      if(TRIM(wvoid).eq.'yes'.or.TRIM(wvoid).eq.'YES') pp_FL200 = .true.
!
      call get_input_cha & 
           (finp,'POSTPROCESS','FL250',wvoid,1,istat,message)
      if(istat.gt.0) call wriwar(message)
      if(TRIM(wvoid).eq.'yes'.or.TRIM(wvoid).eq.'YES') pp_FL250 = .true.
!
      call get_input_cha & 
           (finp,'POSTPROCESS','FL300',wvoid,1,istat,message)
      if(istat.gt.0) call wriwar(message)
      if(TRIM(wvoid).eq.'yes'.or.TRIM(wvoid).eq.'YES') pp_FL300 = .true.
!
!*** Reads contours
!
     call get_input_npar &
          (finp,'VALUES','LOAD_VALUES',nload,istat,message)
      if(istat.gt.0) call wriwar(message)
      if(istat.lt.0) then
          nload = 1
          call wriwar('LOAD_VALUES not found in input file. One value assumed')
      end if   
      call get_input_rea  &
	       (finp,'VALUES','LOAD_VALUES',cload,nload,istat,message)
      if(istat.gt.0) call wriwar(message)
      if(istat.lt.0) then
         cload = 1.0
	  end if
!	  
     call get_input_npar &
          (finp,'VALUES','FL_VALUES',nfl,istat,message)
      if(istat.gt.0) call wriwar(message)
      if(istat.lt.0) then
          nfl = 1
          call wriwar('FL_VALUES not found in input file. One value assumed')
      end if   
      call get_input_rea  &
	       (finp,'VALUES','FL_VALUES',cfl,nfl,istat,message)
      if(istat.gt.0) call wriwar(message)
      if(istat.lt.0) then
         cfl = 1d-4
	  end if
!
      nload = min(nload,mxnval)
      nfl   = min(nfl  ,mxnval)
!
!***  Reads file list. 
!***  First determines the number of maps (files)
!
      wvoid = '' 
      istat = 0
      nmaps = -2
      open(ninp,file=TRIM(finp),status='unknown')
      do while( TRIM(wvoid).ne.'END_FILES' )
         read(ninp,*) wvoid
         if(TRIM(wvoid).eq.'FILES') then
            istat = 1
         end if
         if(istat.eq.1) nmaps = nmaps + 1
      end do   
!
      allocate(flist(nmaps))
!
      rewind(ninp)
      do while( TRIM(wvoid).ne.'FILES' )
         read(ninp,*) wvoid                     
      end do
      do imaps = 1,nmaps
         read(ninp,*) flist(imaps)
      end do
      close(ninp)
!
      return
      end subroutine readinp