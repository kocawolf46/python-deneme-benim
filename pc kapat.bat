@echo off
color 0A
title PC Kapatma Programi
echo Bilgisayari kapatmak istediginiz sureyi saniye cinsinden girin.
echo Ornek: 1 saat icin 3600 yazabilirsiniz.
set /p sure=Saniye girin: 
shutdown -s -f -t %sure%
echo Bilgisayar %sure% saniye sonra kapatilacak.
pause