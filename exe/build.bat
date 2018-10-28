rd /s /q "build"
py -m setup build -b exe/build/ 

rm AoD.exe
makensis setup.nsi

pause