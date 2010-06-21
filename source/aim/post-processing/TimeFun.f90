!***************************************************************
!*
!*    Module for time operations
!* 
!***************************************************************
     MODULE TimeFun
     use kindType, ONLY :  ip,rp
     implicit none
!
     CONTAINS
!
!
!
     subroutine get_date(iyr,imo,idy,ihr,imi,date)
!***************************************************************     
!*
!*   Gets date in the form hh:mmZddmmmyyyy
!*
!***************************************************************
     implicit none
     integer(ip)       :: iyr,imo,idy,ihr,imi
     character(len=15) ::date
!
     write(date(1:2),'(i2.2)') ihr
     write(date(3:3),'(a)'   ) ':'
     write(date(4:5),'(i2.2)') imi
     write(date(6:6),'(a)'   ) 'Z'
     write(date(7:8),'(i2.2)') idy
     if(imo.eq.1) then
          write(date(9:11),'(a)') 'jan'
     else if(imo.eq.2) then
          write(date(9:11),'(a)') 'feb'
     else if(imo.eq.3) then
          write(date(9:11),'(a)') 'mar'
     else if(imo.eq.4) then
          write(date(9:11),'(a)') 'apr'
     else if(imo.eq.5) then
          write(date(9:11),'(a)') 'may'
     else if(imo.eq.6) then
          write(date(9:11),'(a)') 'jun'
     else if(imo.eq.7) then
          write(date(9:11),'(a)') 'jul'
     else if(imo.eq.8) then
          write(date(9:11),'(a)') 'aug'
     else if(imo.eq.9) then
          write(date(9:11),'(a)') 'sep'
     else if(imo.eq.10) then
          write(date(9:11),'(a)') 'oct'
     else if(imo.eq.11) then
          write(date(9:11),'(a)') 'nov'
     else 
          write(date(9:11),'(a)') 'dec'                                                                                          
     end if
     write(date(12:15),'(i4.4)') iyr
!
     return
     end subroutine get_date    
!
!
!
!
!
!
     subroutine get_date_google(iyr,imo,idy,ihr,imi,date)
!***************************************************************     
!*
!*   Gets date in the form yyyy-mm-ddThh:mm:ssZ
!*
!***************************************************************
     implicit none
     integer(ip)       :: iyr,imo,idy,ihr,imi
     character(len=20) :: date
!
     write(date(1 :4 ),'(i4.4)') iyr
     write(date(5 :5 ),'(a)'   ) '-'
     write(date(6 :7 ),'(i2.2)') imo
     write(date(8 :8 ),'(a)'   ) '-'
     write(date(9 :10),'(i2.2)') idy
     write(date(11:11),'(a)'   ) 'T'
     write(date(12:13),'(i2.2)') ihr
     write(date(14:14),'(a)'   ) ':'
     write(date(15:16),'(i2.2)') imi
     write(date(17:20),'(a)'   ) ':00Z'
!
     return
     end subroutine get_date_google  
!
!
!
     subroutine addtime(iyr0,imo0,idy0,ihr0,imi0,iyr,imo,idy,ihr,imi,ise,time0)
!*********************************************************************
!*
!*    Adds time seconds to the initial date YYYY-MM-DD-HH
!*
!*    INPUTS:
!*      IYR0    - integer - Current year
!*      IMO0    - integer - Current month (1-12)
!*      IDY0    - integer - Current day
!*      IHR0    - integer - Current hour (0-23)
!*      TIME    - real    - time increment in seconds
!*
!**********************************************************************
      implicit none
	  integer(ip) :: iyr0,imo0,idy0,ihr0,imi0,iyr,imo,idy,ihr,imi,ise 
      integer(ip) :: nhincr,ijl
	  real(rp)    :: time0,time,work
!
!***  Initialization
!
      iyr = iyr0
      imo = imo0
	  idy = idy0
	  ihr = ihr0 
      imi = imi0
      ise = 0
      time = time0 

!
!***  Time < 1 min
!
      if(time.lt.60.0_rp) then
	   imi = 0
	   ise = int(time)
	   return
!
!***  Time < 1 h
!
      else if(time.lt.3600.0_rp) then
	   imi = int(time/60.0_rp)
	   ise = int(time)-60*imi
       return
      else
!
!***  Time > 1 h
!
        nhincr = int(time/3600.0_rp)
        work   = time - nhincr*3600.0_rp
        imi    = int(work/60.0_rp)
        ise    = int(work)-60*imi

        call julday  (iyr,imo,idy,ijl)      ! Computes the Julian day ijl
        call timeincr(iyr,ijl,ihr,nhincr)   ! Updates the  Julian day
        call grday   (iyr,ijl,imo,idy)      ! Converts back to Gregorian
        return
  	  end if
	end subroutine addtime


    subroutine julday(iyr,imo,iday,ijuldy)
!*********************************************************************
!*
!*    Computes the Julian day number from the Gregorian date
!*    (month, day)
!*
!*********************************************************************
      implicit none
	  integer(ip) :: iyr,imo,iday,ijuldy,ierr
	  integer(ip), dimension(12) :: kday =(/0,31,59,90,120,151,181,212,243,273,304,334/)
!
      ierr=0
!
!***  Check for valid month
!
      if(imo.lt.1.or.imo.gt.12) ierr=1
!
!***  Check for valid day in 30-day months
!
      if(imo.eq.4.or.imo.eq.6.or.imo.eq.9.or.imo.eq.11)then
         if(iday.gt.30)ierr=1
      else if(imo.eq.2)then
         if(mod(iyr,4).eq.0)then  ! February in a leap year
           if(iday.gt.29)ierr=1
         else                     ! February in a non-leap year
            if(iday.gt.28)ierr=1
         endif
      else
!
!***  Check for valid day in 31-day months
!
         if(iday.gt.31) ierr=1
      endif
!
      if(ierr.eq.1)call runend('Wrong computation of the julian day')
!
!***  Compute the Julian day
!
      ijuldy=kday(imo)+iday
      if(imo.le.2) return
      if(mod(iyr,4).EQ.0) ijuldy=ijuldy+1
      return
      end subroutine julday
!
      subroutine grday(iyr,ijul,imo,iday)
!**********************************************************************
!*
!*    Compute the Gregorian date (month, day) from the Julian day
!*
!**********************************************************************
      implicit none
!
      integer(ip) :: iyr,ijul,imo,iday,ileap,i
      integer(ip), dimension(12,2) :: kday =reshape((/31,59,90,120,151,181,212,243,273,304,334,365,  &
                                         31,60,91,121,152,182,213,244,274,305,335,366/),shape(kday))
!
      ileap=1
      if(mod(iyr,4).eq.0) ileap=2
      if(ijul.lt.1.or.ijul.gt.kday(12,ileap))go to 11
!
      do 10 i=1,12
      if(ijul.gt.kday(i,ileap))go to 10
      imo=i
      iday=ijul
      if(imo.ne.1)iday=ijul-kday(imo-1,ileap)
      return
   10 continue

   11 call runend('Wrong computation of the gregorian day')
      end subroutine grday


      subroutine timeincr(iyr,ijul,ihr,nhrinc)
!**********************************************************************
!*
!*    Increments the time and date by "NHRINC" hours
!*
!*
!*    INPUTS:
!*       IYR    - integer - Current year
!*       IJUL   - integer - Current Julian day
!*       IHR    - integer - Current hour (00-23)
!*       NHRINC - integer - Time increment (hours)
!*
!*       NOTE: "NHRINC" must >= -24
!*             Hour is between 00-23
!*
!*    OUTPUT:
!*       IYR    - integer - Updated year
!*       IJUL   - integer - Updated Julian day
!*       IHR    - integer - Updated hour (00-23)
!*
!**********************************************************************
      implicit none
!
	  integer(ip) :: iyr,ijul,ihr,nhrinc
	  integer(ip) :: nleft,ninc,ileap
!
!***  Check nhrinc
!
      if(nhrinc.lt.0) call runend('TIMEINCR invalid time increment')
!
!***  Save increment remaining (needed if nhrinc > 8760)
!
      nleft=nhrinc
!
!***  Process change in hour
!
      if(nhrinc.gt.0)then
!
10       ninc=MIN0(nleft,8760)
         nleft=nleft-ninc
!
!***  Increment time
!
         ihr=ihr+ninc
         if(ihr.le.23) return
!
!***  Increment day
!
         ijul=ijul+ihr/24
         ihr=mod(ihr,24)
!
!***  ILEAP = 0 (non-leap year) or 1 (leap year)
!
         if(mod(iyr,4).eq.0)then
            ileap=1
         else
            ileap=0
         endif
!
!***  Update year
!
         if(ijul.gt.365+ileap) then
            iyr=iyr+1
            ijul=ijul-(365+ileap)
         endif
!
!***  Repeat if more hours need to be added
!
         if(nleft.GT.0) goto 10
!
         elseif(nhrinc.lt.0)then
!***     Decrement time
         ihr=ihr+nhrinc
         if(ihr.lt.0)then
            ihr=ihr+24
            ijul=ijul-1
            if(ijul.lt.1)then
               iyr=iyr-1
               if(mod(iyr,4).eq.0)then
                  ijul=366
               else
                  ijul=365
               endif
            endif
         endif
      endif
!
      return
      end subroutine timeincr
!
!
!
     END MODULE TimeFun