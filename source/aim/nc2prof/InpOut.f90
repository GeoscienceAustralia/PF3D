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
      integer(ip), parameter  :: lulog = 11   ! log file
!
!***  File names
!
      character(len=s_file) :: lulogname,luinpname,luncname, &
                               luncuname,luncvname,lunctname,lunchname,luresname
!
!***  List of Warnings 
!
      integer(ip), parameter :: maxwarn = 100
      integer(ip)            :: nwarn = 0
      character(len=s_mess)  :: warning(maxwarn) 
!        
 END MODULE InpOut