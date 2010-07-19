    subroutine openinp
!**************************************************************
!*
!*    Opens the control file 
!*
!**************************************************************
    use InpOut
    implicit none
!
	character(len=10) rdate,stime
	character(len=8 ) rtime,sdate
    logical     :: found
    integer(ip) :: i,ilen,klen
!
!***  Opens log file
!
	 open(nlog,file=TRIM(flog),status='unknown')
!
!***  Clock
!
    call DATE_AND_TIME(sdate,stime)
! 
    rdate='  -  -    '
    rdate(1:2)=sdate(5:6)
    rdate(4:5)=sdate(7:8)
    rdate(7:10)=sdate(1:4)
    rtime='  :  :  '
    rtime(1:2)=stime(1:2)
    rtime(4:5)=stime(3:4)
    rtime(7:8)=stime(5:6)
!
!***  Writes the log file
!
	 write(nlog,1) rdate,rtime
   1 format('---------------------------------------------',/,  &
            '              PROGRAM nc2grd                 ',/,  &
            '---------------------------------------------',/,  &
            '  Starting date     : ',a10,' at time: ',a8)
!
	 write(nlog,2) TRIM(finp),TRIM(fres)
 2   format(2x,'Input file        : ',a,/, & 
            2x,'Results file      : ',a)
!     
     return
     end subroutine openinp

 
 
