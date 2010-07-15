      subroutine runend(message)
!*************************************************************************
!*
!*    This routine stops the run and writes termination status
!*
!*************************************************************************
      use kindType 
      use InpOut
      implicit none
!
      integer(ip)      :: iwarn
      character(len=*) :: message
!
!***  Warning list
!
      write(lulog,1) nwarn
   1  format(/,'Number of warnings :',i2)
      do iwarn = 1,nwarn
         write(lulog,2) iwarn,warning(iwarn)
      end do  
   2  format(3x,i2,' : ',a)
!
!*** Write message and stop the run.
!
      if(TRIM(message).ne.'OK') then             ! Abnormal termination
!  
        write(lulog,10) TRIM(message)
  10    format('Number of errors : 1',/, &
               2x,a)
        write(lulog,11) 
  11    format('PROGRAM nc2prof ends abnormally')
        close(lulog) 
        stop 1                         ! environment 1
!
	  else                                     ! Normal termination
!   
        write(lulog,20) 
  20    format('Number of errors : 0',/, &
               'PROGRAM nc2prof ends normally')
        close(lulog)
        stop 0                         ! environment 0
!
      end if
!
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
