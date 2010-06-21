      subroutine runend(message)
!*************************************************************************
!*
!*    This routine stops the run and writes termination status
!*
!*************************************************************************
      use kindType 
      use InpOut
      use Master
      implicit none
!
      integer(ip)      :: iwarn
      character(len=*) :: message
!
!***  Writes header
!
	  write(nlog,10)                        
 10   format('---------------------------------------------------',/,  & 
             '                                                   ',/   &
             '         nc2grd : END OF SIMULATION                ',/,  &
             '                                                   ',/,  &
             '---------------------------------------------------',/)
!
!***  Warning list
!
      write(nlog,21) nwarn
  21  format('  WARNINGS : ',i2)
      do iwarn = 1,nwarn
         write(nlog,22) iwarn,warning(iwarn)
      end do  
  22  format(3x,i2,' : ',a)
!
!*** Write message and stop the run.
!
      if(TRIM(message).ne.'OK') then             ! Abnormal termination
! 
	    write(nlog,31) TRIM(message)
 31     format('  STATUS   :  ABNORMAL TERMINATION',/,                &
               '  ERROR    : ',a )	   
	    close(nlog)
        stop 1 ! environment 1
!
	  else                                     ! Normal termination
!
	    write(nlog,32) 
 32     format('  STATUS   :  NORMAL TERMINATION')	    
        close(nlog)
        stop 0   ! environment 0   
!
      end if
      end subroutine runend
!
!
!
      subroutine wriwar(message)
!*************************************************************************
!*
!*    This routine writes a warning message to the warnings list
!*
!*************************************************************************
      use InpOut
      implicit none
      character(len=*) :: message
!
      nwarn = nwarn + 1
      nwarn = MIN(nwarn,maxwarn)
      warning(nwarn) = message(1:LEN_TRIM(message))
!
      return      
      end subroutine wriwar
