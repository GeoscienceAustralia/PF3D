     subroutine readat
!************************************************************
!*
!*    Reads data from the input master file 
!*
!************************************************************
     use Master
	 use InpOut
     implicit none 
!
     character(len=s_mess) :: message
     character(len=25 ) :: cvoid
     integer(ip)    :: istat
     real   (rp)    :: rvoid
!
!***  topography (wirtten in m)
!
      call get_input_cha  &
          (finp,'POSTPROCESS','MAP_TOPOGRAPHY',cvoid,1,istat,message)
      if(istat.ne.0) then
         if(istat.gt.0) call wriwar(message)
         pp_topog = .false.
	  else if(TRIM(cvoid).eq.'YES'.or.TRIM(cvoid).eq.'yes') then
	     pp_topog = .true.          
	  end if
!
      fact_topog = 1.0_rp
      unit_topog = 'm'
!
!***  total load (wirtten in kg/m2)
!
      call get_input_cha  &
          (finp,'POSTPROCESS','MAP_TOTAL_LOAD',cvoid,1,istat,message)
      if(istat.ne.0) then
         if(istat.gt.0) call wriwar(message)
          pp_load0 = .false.
	  else if(TRIM(cvoid).eq.'YES'.or.TRIM(cvoid).eq.'yes') then
	     pp_load0 = .true.          
	  end if
!
      fact_load0 = 1.0_rp
      unit_load0 = 'kg/m2'
!
!***  class load (wirtten in kg/m2)
!
      call get_input_cha  &
          (finp,'POSTPROCESS','MAP_CLASS_LOAD',cvoid,1,istat,message)
      if(istat.ne.0) then
         if(istat.gt.0) call wriwar(message)
          pp_loadc = .false.
	  else if(TRIM(cvoid).eq.'YES'.or.TRIM(cvoid).eq.'yes') then
	     pp_loadc = .true.          
	  end if
!
      fact_loadc = 1.0_rp
      unit_loadc = 'kg/m2'
!
!***  Thickness (written in cm)
!
      call get_input_cha  &
          (finp,'POSTPROCESS','MAP_DEPOSIT_THICKNESS',cvoid,1,istat,message)
      if(istat.ne.0) then
         if(istat.gt.0) call wriwar(message)
	     pp_thick = .false.
	  else if(TRIM(cvoid).eq.'YES'.or.TRIM(cvoid).eq.'yes') then
	     pp_thick = .true.          
!
         call get_input_cha  &
          (finp,'MAP_DEPOSIT_THICKNESS','UNITS',cvoid,1,istat,message)
         if(TRIM(cvoid).eq.'CM'.or.TRIM(cvoid).eq.'cm') then
            unit_thick = 'cm'
            fact_thick = 1.0_rp
	     else if(TRIM(cvoid).eq.'MM'.or.TRIM(cvoid).eq.'mm') then
            fact_thick = 1e1_rp
            unit_thick = 'mm'
	     else if(TRIM(cvoid).eq.'M'.or.TRIM(cvoid).eq.'m') then
            fact_thick = 1e-2_rp
            unit_thick = 'm'
		 else
		    fact_thick = 1.0_rp
            unit_thick = 'cm'
		 end if
!
         call get_input_rea  &
          (finp,'MAP_DEPOSIT_THICKNESS','COMPACTATION_FACTOR',rvoid,1,istat,message)
         if(istat.ne.0) then
	        fact_thick = fact_thick
	     else 
	        fact_thick = fact_thick/rvoid
		 end if   
!
	  end if
!
!***  Particle ground concentration (written in gr/m3)
!
      call get_input_cha  &
          (finp,'POSTPROCESS','MAP_CONCE_GROUND',cvoid,1,istat,message)
      if(istat.ne.0) then
         if(istat.gt.0) call wriwar(message)
	     pp_concg = .false.
	  else if(TRIM(cvoid).eq.'YES'.or.TRIM(cvoid).eq.'yes') then
	     pp_concg = .true.
	  end if
      fact_concg = 1.0_rp
      unit_concg = 'gr/m3'
!
!***  PMxx ground concentration (written in gr/m3)
!
      call get_input_cha  &
          (finp,'POSTPROCESS','MAP_PMxx_GROUND',cvoid,1,istat,message)
      if(istat.ne.0) then
         if(istat.gt.0) call wriwar(message)
	     pp_pm05g = .false.
	     pp_pm10g = .false.
  	     pp_pm20g = .false.
	  else if(TRIM(cvoid).eq.'YES'.or.TRIM(cvoid).eq.'yes') then
	     pp_pm05g = .true.
	     pp_pm10g = .true.
	     pp_pm20g = .true.
	  end if
      fact_PMxxg = 1.0_rp
      unit_PMxxg = 'gr/m3'
!
!***  Cummulative concentration or column mass (written in Tn/km2 = gr/m2)
!
      call get_input_cha  &
          (finp,'POSTPROCESS','MAP_COLUMN_MASS',cvoid,1,istat,message)
      if(istat.ne.0) then
         if(istat.gt.0) call wriwar(message)
	     pp_cumul = .false.
	  else if(TRIM(cvoid).eq.'YES'.or.TRIM(cvoid).eq.'yes') then
	     pp_cumul = .true.
	  end if
      fact_cumul = 1.0_rp
      unit_cumul = 'Tn/km2'
!
!***  Column mass GAS 
!
      call get_input_cha  &
          (finp,'POSTPROCESS','MAP_GAS_CUMMUL',cvoid,1,istat,message)
      if(istat.ne.0) then
         if(istat.gt.0) call wriwar(message)
	     pp_cumug = .false.
	  else if(TRIM(cvoid).eq.'YES'.or.TRIM(cvoid).eq.'yes') then
	     pp_cumug = .true.
	  end if
      fact_cumug = 1.0_rp
      unit_cumug = 'Tn/km2'
!
!***  PMxx cummulative concentration (written in gr/m2)
!
      call get_input_cha  &
          (finp,'POSTPROCESS','MAP_PMxx_CUMMUL',cvoid,1,istat,message)
      if(istat.ne.0) then
         if(istat.gt.0) call wriwar(message)
	     pp_pm05c = .false.
	     pp_pm10c = .false.
  	     pp_pm20c = .false.
	  else if(TRIM(cvoid).eq.'YES'.or.TRIM(cvoid).eq.'yes') then
	     pp_pm05c = .true.
	     pp_pm10c = .true.
	     pp_pm20c = .true.
	  end if
      fact_PMxxc = 1.0_rp
      unit_PMxxc = 'Tn/km2'
!
!***  AOT 
!
      call get_input_cha  &
          (finp,'POSTPROCESS','MAP_AOT',cvoid,1,istat,message)
      if(istat.ne.0) then
         if(istat.gt.0) call wriwar(message)
	     pp_aot05 = .false.
	  else if(TRIM(cvoid).eq.'YES'.or.TRIM(cvoid).eq.'yes') then
	     pp_aot05 = .true.
	  end if
      fact_aot05 = 1.0_rp
      unit_aot05 = '-'
!
!***  FL (written in gr/m3)
!
      call get_input_cha  &
          (finp,'POSTPROCESS','MAP_FLIGHT_LEVEL',cvoid,1,istat,message)
      if(istat.ne.0) then
         if(istat.gt.0) call wriwar(message)
	     pp_fl = .false.
	  else if(TRIM(cvoid).eq.'YES'.or.TRIM(cvoid).eq.'yes') then
	     pp_fl = .true.
	  end if
      fact_fl = 1.0_rp
      unit_fl = 'gr/m3'  
!  
!***  Cuts (concentration in gr/m3)
!
      call get_input_cha  &
          (finp,'POSTPROCESS','MAP_TOTAL_CONCENTRATION',cvoid,1,istat,message)
      if(istat.ne.0) then
         if(istat.gt.0) call wriwar(message)
	     pp_cut3d = .false.
	  else if(TRIM(cvoid).eq.'YES'.or.TRIM(cvoid).eq.'yes') then
	     pp_cut3d = .true.
!
         call get_input_npar &
	          (finp,'MAP_TOTAL_CONCENTRATION','Z_CUTS_(M)',ncut,istat,message)
         if(istat.gt.0) call wriwar(message)
         if(istat.lt.0) call runend(message)
!
         call get_input_rea &
	          (finp,'MAP_TOTAL_CONCENTRATION','Z_CUTS_(M)',zcut,ncut,istat,message)
         if(istat.gt.0) call wriwar(message)
         if(istat.lt.0) call runend(message)
!
	  end if
      fact_cut3d = 1.0_rp
      unit_cut3d = 'gr/m3'
!
!***  Cuts (gas concentration in gr/m3)
!
      call get_input_cha  &
          (finp,'POSTPROCESS','MAP_GAS_CONCENTRATION',cvoid,1,istat,message)
      if(istat.ne.0) then
         if(istat.gt.0) call wriwar(message)
	     pp_cut3g = .false.
	  else if(TRIM(cvoid).eq.'YES'.or.TRIM(cvoid).eq.'yes') then
	     pp_cut3g = .true.
       end if
       fact_cut3g = 1.0_rp
       unit_cut3g = 'gr/m3'
! 
!***  Cuts (class concentration in gr/m3)
!
      call get_input_cha  &
          (finp,'POSTPROCESS','MAP_CLASS_CONCENTRATION',cvoid,1,istat,message)
      if(istat.ne.0) then
         if(istat.gt.0) call wriwar(message)
	     pp_cut3c = .false.
	  else if(TRIM(cvoid).eq.'YES'.or.TRIM(cvoid).eq.'yes') then
	     pp_cut3c = .true.
	  end if
      fact_cut3c = 1.0_rp
      unit_cut3c = 'gr/m3'
!
      return
      end subroutine readat