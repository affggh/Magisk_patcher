@chcp 65001 > nul
:: Use utf-8 codec
:: Begin of Batch

@echo off & setlocal enabledelayedexpansion 

set Version=20200129

:: Began of args detection
set funcs=patch patchondevice autoconfig test
:: cd %~dp0
:: Add bin to envrionment at once time
set "Path=%~dp0bin;%Path%"

for /f "delims=" %%i in ('busybox uname -m') do set OS_TYPE=%%i
if /I not "!OS_TYPE!"=="x86_64" (
	echo Error... your windows is 32bit,but script require 64bit...
	exit /b 1
)

if "%1"=="" call :Usage & exit /b 0
if "%1"=="-h" call :Usage & exit /b 0
for %%i in (!funcs!) do (
	if "%1"=="%%i" set fun=%%i
)
if not defined fun (
	echo Function you choose does not exist...
	exit /b 1
)

if "!fun!"=="test" goto :!fun!

:GetArgs
if "%1"=="-i" set input=%2
if "%1"=="-o" set output=%2
if "%1"=="-c" set config=%2
if "%1"=="-a" set arch=%2
if "%1"=="-kv" (
	if "%2"=="true" (
		set keepverity=true
	) else (
		set keepverity=false
	)
)
if "%1"=="-ke" (
	if "%2"=="true" (
		set keepforceencrypt=true
	) else (
		set keepforceencrypt=false
	)
)
if "%1"=="-pv" (
	if "%2"=="true" (
		set patchvbmetaflag=true
	) else (
		set patchvbmetaflag=false
	)
)
if "%1"=="-m" set magisk=%2
if "%1"=="--default" set configdefault=1
if "%1"=="-r" set recoverymode=true
shift /1
if not "%1"=="" (
	goto :GetArgs
) else (
	goto :!fun!
)

:patch
echo Function : patch
if not exist !input! echo File input does not exist! & exit /b 1
if defined config (
	echo Use !config! insted of default options...
	if not exist !config! echo Config file !config! not exist! & exit /b 1
	for /f "delims=" %%i in ('findstr /b /v "#" !config!') do (
		set %%i
	)
	rem if some not defined script will use default type
	if not defined keepverity set keepverity=true
	if not defined keepforceencrypt set keepforceencrypt=true
	if not defined patchvbmetaflag set patchvbmetaflag=false
	if not defined magisk set magisk=%~dp0prebuilt\Magisk-v24.1.apk
) else (
	echo Not define config file ,use default value
	if not defined keepverity set keepverity=true
	if not defined keepforceencrypt set keepforceencrypt=true
	if not defined patchvbmetaflag set patchvbmetaflag=false
	if not defined magisk set magisk=%~dp0prebuilt\Magisk-v24.1.apk
)
if not defined arch (
	echo Error arch not defined ,script dont know your image type...
	exit /b 1
)

for %%i in (arm arm64 x86 x86_64) do (
	if "!arch!"=="%%i" set arch_detective=1
)
if not "!arch_detective!"=="1" echo The arch type [!arch!] your defined not support... & exit /b 1

if "!arch!"=="arm" set arch=armeabi-v7a
if "!arch!"=="arm64" set arch=arm64-v8a
if "!arch!"=="x86" set arch=x86
if "!arch!"=="x86_64" set arch=x86_64
:: x86 and x86_64 just for some read bug
if exist tmp\ rd /s /q tmp\
busybox unzip "!magisk!" -od tmp "assets/*" "lib/!arch!/*"
for /f "tokens=1 delims=" %%i in ('busybox du -s tmp\lib\!arch!') do set dirsize=%%i
if "!dirsize!" lss "128" (
	echo 64bit file at 32bit dir ,re unzipping ....
	if "!arch!"=="arm64-v8a" (
		set subarch=armeabi-v7a
		busybox unzip "!magisk!" -od tmp "lib/!subarch!/*"
	)
	if "!arch!"=="x86_64" (
		set subarch=x86
		busybox unzip "!magisk!" -od tmp "lib/!subarch!/*"
	)
)
:: There is an issue we still need magisk32
if "!arch!"=="arm64-v8a" (
	busybox unzip "!magisk!" -od tmp "lib/armeabi-v7a/libmagisk32.so"
)
if "!arch!"=="x86_64" (
	busybox unzip "!magisk!" -od tmp "lib/x86/libmagisk32.so"
)

:: Get magisk version
for /f "tokens=2 delims==" %%i in ('busybox grep -rn "MAGISK_VER=" tmp\assets\*') do set MAGISK_VER=%%i

for %%i in (arm64-v8a x86_64) do (
	if "!arch!"=="%%i" set is64bit=true
)

for /r "tmp\lib" %%i in (lib*.so) do (
	if "%%~nxi"=="libmagiskinit.so" copy "%%i" .\magiskinit
	if "%%~nxi"=="libmagisk32.so" copy "%%i" .\magisk32
	if "%%~nxi"=="libmagisk64.so" (
		if "!is64bit!"=="true" copy "%%i" .\magisk64
	)
)

if not "!recoverymode!"=="true" set recoverymode=false

:: Show all type
echo  List your config :
echo                    Magisk version = !MAGISK_VER!
echo                    Batch Script Version = !Version!
echo                    arch=!arch!
echo                    keepverity=!keepverity!
echo                    keepforceencrypt=!keepforceencrypt!
echo                    patchvbmetaflag=!patchvbmetaflag!
echo                    recoverymode=!recoverymode!
echo                    magisk=!magisk!
echo                    input=!input!
if defined output (
	echo                    output=!output!
) else (
	echo                    output=new-boot.img [default]
)
if exist ".\new-boot.img" del /q ".\new-boot.img"
busybox ash "%~dp0bin\boot_patch.sh" !input! !keepverity! !keepforceencrypt! !patchvbmetaflag! !recoverymode!
if exist ".\new-boot.img" (
	if defined output move /y new-boot.img !output!
	echo Successfully generated...
) else (
	echo Failed...
)
%~dp0bin\magiskboot cleanup
set exitcode=%errorlevel%
goto :EndofBatch

:patchondevice
:: in some situation patch on windows will failed or bootloop
:: script allow your patch with adb on device environment...
echo Function: : patchondevice
if not defined magisk set magisk=%~dp0prebuilt\Magisk-v24.1.apk
if not exist "!magisk!" (
	echo file !magisk! not found...
	echo please check your config or use -m to choose one...
	exit /b 1
)
if not exist "!input!" echo Input file not exist... &exit /b 1
echo Get device state...
call :getdevice
echo Prepare files ...
busybox printf "Founding device arch : "
:: BUG ... failed on some device...
:: for /f %%i in ('adb shell getprop ro.product.cpu.abi') do (
::	set arch=%%i
:: )
:: As replace
	adb push %~dp0bin\get_config.sh !tmp! >nul
	adb shell chmod 0755 !tmp!/get_config.sh
	for /f "delims=" %%i in ('adb shell sh !tmp!/get_config.sh') do (
		set %%i
	)
	adb shell rm -f !tmp!/get_config.sh
:: End As
:: wreid bug... read config via script
if "!arch:~0,3!"=="arm" (
	if not "!arch:~0,5!"=="arm64" (
		set arch=armeabi-v7a
	)
)
if "!arch:~0,5!"=="arm64" set arch=arm64-v8a
if "!arch:~0~3!"=="x86" (
	if not "!arch:0~6!"=="x86_64" (
		set arch=x86
	)
)
if "!arch:0~6!"=="x86_64" set arch=x86_64
busybox printf "%%s\n" "!arch!"

busybox printf "Unzip !magisk!... \n"
:: x86 and x86_64 no need to change
if exist tmp\ rd /s /q tmp\
busybox unzip "!magisk!" -od tmp "assets/*" "lib/!arch!/*" >nul
for /f "tokens=1 delims=" %%i in ('busybox du -s tmp\lib\!arch!') do set dirsize=%%i
if "!dirsize!" lss "128" (
	busybox printf "64bit file at 32bit dir ,re unzipping .... "
	if "!arch!"=="arm64-v8a" (
		set subarch=armeabi-v7a
		busybox unzip "!magisk!" -od tmp "lib/!subarch!/*" >nul
	)
	if "!arch!"=="x86_64" (
		set subarch=x86
		busybox unzip "!magisk!" -od tmp "lib/!subarch!/*" >nul
	)
)
:: There is an issue we still need magisk32
if "!arch!"=="arm64-v8a" (
	busybox unzip "!magisk!" -od tmp "lib/armeabi-v7a/libmagisk32.so"
)
if "!arch!"=="x86_64" (
	busybox unzip "!magisk!" -od tmp "lib/x86/libmagisk32.so"
)

busybox printf "Done\n"
busybox printf "Find magisk version : "
:: Get magisk version
for /f "tokens=2 delims==" %%i in ('busybox grep -rn "MAGISK_VER=" tmp\assets\*') do set MAGISK_VER=%%i
busybox printf "%%s\n" "!MAGISK_VER!"
for %%i in (arm64-v8a x86_64) do (
	if "!arch!"=="%%i" set is64bit=true
)
if not exist magisk\ md magisk\
busybox printf "Copying files into magisk folder... "
for /r "tmp\lib" %%i in (lib*.so) do (
	if "%%~nxi"=="libmagiskinit.so" copy "%%i" .\magisk\magiskinit  >nul
	if "%%~nxi"=="libmagisk32.so" copy "%%i" .\magisk\magisk32  >nul
	if "%%~nxi"=="libmagisk64.so" (
		if "!is64bit!"=="true" copy "%%i" .\magisk\magisk64  >nul
	)
	if "%%~nxi"=="libbusybox.so" copy "%%i" .\magisk\busybox  >nul
	if "%%~nxi"=="libmagiskboot.so" copy "%%i" .\magisk\magiskboot  >nul
)
xcopy /e /y tmp\assets\* .\magisk\  >nul
busybox printf "done\n"
busybox printf "Notice : boot_patch.sh will auto read config from device...\n"
busybox printf "Wroking at [%%s]\n" "!tmp!"
busybox printf "Transporting files... "

copy !input! .\magisk\boot.img  >nul
adb push .\magisk !tmp! >nul
busybox printf "done\n"
busybox printf "Patching image...\n"
adb shell chmod -R 755 !tmp!/magisk
adb shell !tmp!/magisk/boot_patch.sh !tmp!/magisk/boot.img
busybox printf "Fetching boot.img... "
if exist "new-boot.img" del /q "new-boot.img"
adb pull !tmp!/magisk/new-boot.img .\new-boot.img >nul
busybox printf "done\n"
if exist "new-boot.img" (
	busybox printf "Success..."
	set exitcode=0
) else (
	busybox printf "Failed..."
	set exitcode=1
)
::pause
busybox printf "Cleanup [!tmp!] and temp files... "
adb shell rm -rf !tmp!/magisk
rd /s /q magisk\ 
rd /s /q tmp\
busybox printf "done\n"

goto :EndofBatch

:autoconfig
echo Function : autoconfig
if "!configdefault!"=="1" (
	if not defined arch set arch=arm64
	if not defined keepverity set keepverity=true
	if not defined keepforceencrypt set keepforceencrypt=true
	if not defined patchvbmetaflag set patchvbmetaflag=false
	if not defined magisk set magisk=%~dp0prebuilt\Magisk-v24.1.apk
	busybox printf "# var  type\n" > config.txt 
	busybox printf "arch=%%s\n" "!arch!" >> config.txt
	busybox printf "keepverity=%%s\n" "!keepverity!" >> config.txt
	busybox printf "keepforceencrypt=%%s\n" "!keepforceencrypt!" >> config.txt
	busybox printf "patchvbmetaflag=%%s\n" "!patchvbmetaflag!" >> config.txt
	if not "!recoverymode!"=="true" (
		busybox printf "recoverymode=false\n" >> config.txt
	) else (
		busybox printf "recoverymode=true\n" >> config.txt
	)
	if exist "!magisk!" (
		busybox printf "magisk=%%s\n" "!magisk!" >> config.txt
	) else (
		echo Warning... file var magisk
		echo         magisk=    not defined...
		busybox printf "magisk=\n" >> config.txt
	)
	if exist ".\config.txt" (
		echo Successfully generate config.txt...
		set exitcode=0
	) else (
		echo Generate config.txt failed...
		set exitcode=1
	)
) else (
	echo Read config from device...
	call :getdevice
	busybox printf "# var  type\n" > config.txt
	adb push %~dp0bin\get_config.sh !tmp! >nul
	adb shell chmod 0755 !tmp!/get_config.sh
	adb shell sh !tmp!/get_config.sh >> config.txt
	adb shell rm -f !tmp!/get_config.sh
	if not defined magisk set magisk=%~dp0prebuilt\Magisk-v24.1.apk
	busybox printf "magisk=%%s\n" "!magisk!" >> config.txt
	if not "!recoverymode!"=="true" (
		busybox printf "recoverymode=false\n" >> config.txt
	) else (
		busybox printf "recoverymode=true\n" >> config.txt
	)
	if exist ".\config.txt" (
		echo Successfully generate config.txt...
		set exitcode=0
	) else (
		echo Generate config.txt failed...
		set exitcode=1
	)
)
::adb kill-server
goto :EndofBatch

:getdevice
::tasklist /FI "IMAGENAME eq adb.exe" | findstr "adb.exe" >nul
::if "%errorlevel%"=="0" (
::	rem kill adb.exe service if exist
::	taskkill /F /FI "IMAGENAME eq adb.exe" /IM * >nul
::)
for /f "delims=" %%i in ('adb get-state 2^>nul') do set "state=%%i"
rem remove ' '
set state=!state: =!
if not defined state (
	echo Device not found...
	exit /b 1
) else (
	for %%i in (device recovery) do (
		if "%%i"=="!state!" set device_flag=1
	)
	if not "!device_flag!"=="1" (
		echo Can not load config via unkonw state...
		exit /b 1
	)
)
set device_flag=
rem Lots of device not support this new way ,use old way
rem type "%~dp0bin\get_config.sh" | adb shell >> config.txt
if "!state!"=="device" (
	set tmp=/data/local/tmp
)
if "!state!"=="recovery" (
	set tmp=/tmp
)
echo Device state is !state! , tmp as [!tmp!]...
rem This function will set variable tmp and state
goto :eof

rem End of batch script

:EndofBatch
:: Cleanup
if exist tmp\ rd /s /q tmp\
if exist magisk32 del /q magisk32
if exist magisk64 del /q magisk64
if exist magiskinit del /q magiskinit
exit /b !exitcode!

:test
echo Test function

exit /b 0

:: Usage
:Usage
echo Usage:
echo   %~nx0 command
echo             -h    Print this help information...
echo   Support Command:
for %%i in (!funcs!) do (
	echo                  %%i
)
echo   Explain:
echo          patch  : Patch a boot image with magisk on windows
echo             -i    input file
echo  [optional] -o    output file  default output is [new-boot.img]
echo             -c    read config.txt instead of -a -kv -ke -pv
echo    [must]   -a    arch of your device... this can be 
echo                                arm
echo                                arm64
echo                                x86
echo                                x86_64
echo  [optional] -kv    keep verity default is : [true]
echo                    If your device is system-as-root(sar)
echo                        make it true
echo  [optional] -ke    keep force encrypt default is : [true]
echo                    If your device is like forceencrypt=footer like [qsee] or else
echo                        make it true
echo  [optional] -pv    Patch vbmeta flag default is : [false]
echo                    If your device not have partition [vbmeta]
echo                        make it true
echo  [optional] -m     Choose a Magisk install apk/zip insted of 
echo                                  default : [prebuilt\Magisk-v24.1.apk]
echo             -r     image is a recovery image
echo                    this not work on function : patchondevice
echo               Notice: Shell script part will auto detect file existance
echo                       if is a 64bit image.
echo.
echo          autoconfig : This function can auto detect config from device
echo                       and generate a confit.txt at %~dp0 
echo                       without root
echo             --default  generate with default instead read from device
echo             -m     Defined custom magisk path
echo             -r     image is a recovery image
echo                    this not work on function : patchondevice
echo.
echo          patchondevice : patch on device
echo                     for some reason patch on windows could be failed...
echo                     you can run this function patch boot on your device
echo   Example : 
echo           %~nx0 patch -i boot.img -c config.txt
echo           %~nx0 patch -i boot.img -a armeabi-v7a -kv true -ke true -pv false
echo           %~nx0 patch -i boot.img -c config.txt -m prebuilt\Magisk-v24.1.apk
echo.
echo           %~nx0 autoconfig
echo           %~nx0 autoconfig --default
echo           %~nx0 autoconfig -m prebuilt\Magisk-v24.1.apk

goto :eof


:: End of Batch script