!***************************************************************
!*
!*		Module for input/output
!*
!***************************************************************
 MODULE InpOut
   use KindType
   IMPLICIT NONE
   SAVE
!
!***  File logical units
!
      integer(ip), parameter  :: nlog = 10     ! Log file
      integer(ip), parameter  :: ninp = 11     ! Input file
	  integer(ip), parameter  :: nres = 12     ! Results file    
!
!***  File names
!
      character(len=s_file) :: flog = 'HazardMaps.log'
      character(len=s_file) :: finp = 'HazardMaps.inp'
      character(len=s_file) :: fpts = 'HazardMaps.pts'
      character(len=s_file) :: fout = 'HazardMaps.res.nc'
      character(len=s_file) :: fptsout = 'HazardMaps.res.pts'      
      character(len=s_file) :: fres
      character(len=s_file), allocatable :: flist(:)
!
!***  List of Warnings 
!
      integer(ip), parameter :: maxwarn = 100
      integer(ip)            :: nwarn = 0
      character(len=s_mess)  :: warning(maxwarn) 
!
      CONTAINS
!
!
!
      real(rp) function stof(string,nstr)
!**************************************************************
!*
!*    This routine converts a real/integer number stored in a
!*    string(1:nstr) into a real(rp)  digit format
!*
!**************************************************************
      implicit none
      integer(ip) ::   nstr
	  character(len=*) :: string
!
      integer(ip) :: i,ipos,nsign,esign,nvalu
      integer(ip) :: expo,valu(s_file)  
	  logical     :: next
!
      stof = 0_rp 
!
!***  Sing decoding
!
      ipos = 1
      if(ichar(string(ipos:ipos)).eq.43) then         !  + sign
        nsign = 1
	    ipos  = ipos + 1
      else if(ichar(string(ipos:ipos)).eq.45) then    !  - sign
        nsign = -1
	    ipos  = ipos + 1
	  else                                       !  no sing (+)
	    nsign = 1
	    ipos  = ipos 
	  end if
!
!***  Base decoding
!
      nvalu = 0
      next  = .true.
      do while(next)
        if((ichar(string(ipos:ipos)).eq.68 ).or. &       ! D
           (ichar(string(ipos:ipos)).eq.69 ).or. &       ! E
           (ichar(string(ipos:ipos)).eq.100).or. &       ! d
           (ichar(string(ipos:ipos)).eq.101).or. &       ! e
           (ichar(string(ipos:ipos)).eq.46 )) then       ! .
           next = .false.
	    else
	      nvalu = nvalu + 1
	      valu(nvalu) = stof1(string(ipos:ipos))
	      ipos = ipos + 1
           if(ipos.eq.(nstr+1)) then
	        next = .false.
            ipos = ipos - 1
	       end if
	    end if
	  end do
      do i = 1,nvalu
	   stof = stof + valu(i)*1d1**(nvalu-i)
      end do
!
!***  Decimal decoding
!
      if((ichar(string(ipos:ipos)).eq.46   ).and.  &
                       ipos  .ne.nstr) then
        ipos = ipos + 1
        nvalu = 0
        next  = .true.
        do while(next)
          if((ichar(string(ipos:ipos)).eq.68 ).or. &        ! D
             (ichar(string(ipos:ipos)).eq.69 ).or. &       ! E
             (ichar(string(ipos:ipos)).eq.100).or. &       ! d
             (ichar(string(ipos:ipos)).eq.101)) then      ! e
             next = .false.
	      else
	         nvalu = nvalu + 1
	         valu(nvalu) = stof1(string(ipos:ipos))
	         ipos = ipos + 1
             if(ipos.eq.(nstr+1)) then
	          next = .false.
              ipos = ipos - 1
	         end if
	      end if
	    end do
	    do i = 1,nvalu
	       stof = stof + valu(i)*1d1**(-i)
        end do
	  end if
!
!***  Exponent
!
      if(((ichar(string(ipos:ipos)).eq.68 ).or. &        ! D
          (ichar(string(ipos:ipos)).eq.69 ).or. &        ! E
          (ichar(string(ipos:ipos)).eq.100).or. &        ! d
          (ichar(string(ipos:ipos)).eq.101)).and. &      ! e
                        ipos  .ne.nstr) then
        ipos = ipos + 1
        if(ichar(string(ipos:ipos)).eq.43) then         !  + sign
           esign = 1
	       ipos  = ipos + 1
        else if(ichar(string(ipos:ipos)).eq.45) then    !  - sign
           esign = -1
	       ipos  = ipos + 1
	    else                                       !  no sing (+)
	       esign = 1
	       ipos  = ipos 
	    end if     
!        
        nvalu = 0
        next  = .true.
        do while(next)
           nvalu = nvalu + 1
           valu(nvalu) = stof1(string(ipos:ipos))
	       ipos = ipos + 1
           if(ipos.eq.(nstr+1)) then
	          next = .false.
              ipos = ipos - 1
	       end if
	    end do
	    expo = 0
	    do i = 1,nvalu
	     expo = expo + valu(i)*10**(nvalu-i)
        end do
!
        if(esign.eq.1) then
           stof = stof*(10_rp**expo)
        else if(esign.eq.-1) then
           stof = stof/(10_rp**expo)
        end if
!
	 end if
!
      stof = nsign*stof
	end function stof
!
!
!
     integer(ip) function stof1(string1)
!**************************************************************
!*
!*    Decodes a character*1 string
!*
!**************************************************************
    implicit none
	character(len=1) :: string1
!      
	if(string1.eq.'0') then
	  stof1 = 0
	else if(string1.eq.'1') then
	  stof1 = 1	 
	else if(string1.eq.'2') then
	  stof1 = 2	 
      else if(string1.eq.'3') then
	  stof1 = 3	 
	else if(string1.eq.'4') then
	  stof1 = 4	 
	else if(string1.eq.'5') then
	  stof1 = 5	 
	else if(string1.eq.'6') then
	  stof1 = 6	 
	else if(string1.eq.'7') then
	  stof1 = 7	 
	else if(string1.eq.'8') then
	  stof1 = 8	 
	else if(string1.eq.'9') then
	  stof1 = 9
	end if
	return
	end function stof1
!
!
!
 END MODULE InpOut 