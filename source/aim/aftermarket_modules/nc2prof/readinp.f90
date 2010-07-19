    subroutine readinp
!************************************************************
!*
!*    Reads data from the input file 
!*
!************************************************************
    use Master
    use InpOut
    use KindType
    implicit none 
!
    character(len=s_mess) :: message
    integer(ip)           :: istat
!
!*** Reads vent coordinates
!
      call get_input_rea  &
	       (luinpname,'COORDINATES','LON_VENT',lon_v,1,istat,message)
      if(istat.gt.0) call wriwar(message)
      if(istat.lt.0) call runend('LON_VENT record not found')
!
      call get_input_rea  &
	       (luinpname,'COORDINATES','LAT_VENT',lat_v,1,istat,message)
      if(istat.gt.0) call wriwar(message)
      if(istat.lt.0) call runend('LAT_VENT record not found')
!
!***  Profile time interval
!
      call get_input_int  &
	       (luinpname,'EXTRACT_FROM','YEAR',pbyr,1,istat,message)
      if(istat.gt.0) call wriwar(message)
      if(istat.lt.0) call runend('YEAR record not found')
!
      call get_input_int  &
	       (luinpname,'EXTRACT_FROM','MONTH',pbmo,1,istat,message)
      if(istat.gt.0) call wriwar(message)
      if(istat.lt.0) call runend('MONTH record not found')
!
      call get_input_int  &
	       (luinpname,'EXTRACT_FROM','DAY',pbdy,1,istat,message)
      if(istat.gt.0) call wriwar(message)
      if(istat.lt.0) call runend('DAY record not found')
!
      call get_input_int  &
	       (luinpname,'EXTRACT_FROM','HOUR',pbhr,1,istat,message)
      if(istat.gt.0) call wriwar(message)
      if(istat.lt.0) call runend('DAY record not found')
!
      call get_input_int  &
	       (luinpname,'EXTRACT_TO','YEAR',peyr,1,istat,message)
      if(istat.gt.0) call wriwar(message)
      if(istat.lt.0) call runend('YEAR record not found')
!
      call get_input_int  &
	       (luinpname,'EXTRACT_TO','MONTH',pemo,1,istat,message)
      if(istat.gt.0) call wriwar(message)
      if(istat.lt.0) call runend('MONTH record not found')
!
      call get_input_int  &
	       (luinpname,'EXTRACT_TO','DAY',pedy,1,istat,message)
      if(istat.gt.0) call wriwar(message)
      if(istat.lt.0) call runend('DAY record not found')
!
      call get_input_int  &
	       (luinpname,'EXTRACT_TO','HOUR',pehr,1,istat,message)
      if(istat.gt.0) call wriwar(message)
      if(istat.lt.0) call runend('DAY record not found')
!
!***  Writes the log file
!
      write(lulog,10) lon_v,lat_v, &
                      pbyr,pbmo,pbdy,pbhr, &
                      peyr,pemo,pedy,pehr
  10  format('Vent coordinates  : ',f7.2,' ',f7.2, /,&
             'Extract from        ',/,    &
             '  year   : ',i6,/, &  
             '  month  : ',i6,/, &
             '  day    : ',i6,/, &         
             '  hour   : ',i6,/, & 
             'To         ',/,    &
             '  year   : ',i6,/, &  
             '  month  : ',i6,/, &
             '  day    : ',i6,/, &
             '  hour   : ',i6) 
!
      return
      end subroutine readinp      