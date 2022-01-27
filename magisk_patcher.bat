:: Batch script by affggh 879632264@qq.com
:: Busybox from github compiled by myself. busybox-w32
:: Shell script Edited from magisk canary flashable apk file...
:: magiskboot for cygwin64 is based on magisk source 20220127...also compiled by myself

:: This script based on Apache 2.0 License
::
::                            Apache License
::                       Version 2.0, January 2004
::                  http://www.apache.org/licenses/

::   TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION

::   1. Definitions.

::   "License" shall mean the terms and conditions for use, reproduction,
::   and distribution as defined by Sections 1 through 9 of this document.

::   "Licensor" shall mean the copyright owner or entity authorized by
::   the copyright owner that is granting the License.

::   "Legal Entity" shall mean the union of the acting entity and all
::   other entities that control, are controlled by, or are under common
::   control with that entity. For the purposes of this definition,
::   "control" means (i) the power, direct or indirect, to cause the
::   direction or management of such entity, whether by contract or
::   otherwise, or (ii) ownership of fifty percent (50%) or more of the
::   outstanding shares, or (iii) beneficial ownership of such entity.

::   "You" (or "Your") shall mean an individual or Legal Entity
::   exercising permissions granted by this License.

::   "Source" form shall mean the preferred form for making modifications,
::   including but not limited to software source code, documentation
::   source, and configuration files.

::   "Object" form shall mean any form resulting from mechanical
::   transformation or translation of a Source form, including but
::   not limited to compiled object code, generated documentation,
::   and conversions to other media types.

::   "Work" shall mean the work of authorship, whether in Source or
::   Object form, made available under the License, as indicated by a
::   copyright notice that is included in or attached to the work
::   (an example is provided in the Appendix below).

::   "Derivative Works" shall mean any work, whether in Source or Object
::   form, that is based on (or derived from) the Work and for which the
::   editorial revisions, annotations, elaborations, or other modifications
::   represent, as a whole, an original work of authorship. For the purposes
::   of this License, Derivative Works shall not include works that remain
::   separable from, or merely link (or bind by name) to the interfaces of,
::   the Work and Derivative Works thereof.

::   "Contribution" shall mean any work of authorship, including
::   the original version of the Work and any modifications or additions
::   to that Work or Derivative Works thereof, that is intentionally
::   submitted to Licensor for inclusion in the Work by the copyright owner
::   or by an individual or Legal Entity authorized to submit on behalf of
::   the copyright owner. For the purposes of this definition, "submitted"
::   means any form of electronic, verbal, or written communication sent
::   to the Licensor or its representatives, including but not limited to
::   communication on electronic mailing lists, source code control systems,
::   and issue tracking systems that are managed by, or on behalf of, the
::   Licensor for the purpose of discussing and improving the Work, but
::   excluding communication that is conspicuously marked or otherwise
::   designated in writing by the copyright owner as "Not a Contribution."

::   "Contributor" shall mean Licensor and any individual or Legal Entity
::   on behalf of whom a Contribution has been received by Licensor and
::   subsequently incorporated within the Work.

::   2. Grant of Copyright License. Subject to the terms and conditions of
::   this License, each Contributor hereby grants to You a perpetual,
::   worldwide, non-exclusive, no-charge, royalty-free, irrevocable
::   copyright license to reproduce, prepare Derivative Works of,
::   publicly display, publicly perform, sublicense, and distribute the
::   Work and such Derivative Works in Source or Object form.

::   3. Grant of Patent License. Subject to the terms and conditions of
::   this License, each Contributor hereby grants to You a perpetual,
::   worldwide, non-exclusive, no-charge, royalty-free, irrevocable
::   (except as stated in this section) patent license to make, have made,
::   use, offer to sell, sell, import, and otherwise transfer the Work,
::   where such license applies only to those patent claims licensable
::   by such Contributor that are necessarily infringed by their
::   Contribution(s) alone or by combination of their Contribution(s)
::   with the Work to which such Contribution(s) was submitted. If You
::   institute patent litigation against any entity (including a
::   cross-claim or counterclaim in a lawsuit) alleging that the Work
::   or a Contribution incorporated within the Work constitutes direct
::   or contributory patent infringement, then any patent licenses
::   granted to You under this License for that Work shall terminate
::   as of the date such litigation is filed.

::   4. Redistribution. You may reproduce and distribute copies of the
::   Work or Derivative Works thereof in any medium, with or without
::   modifications, and in Source or Object form, provided that You
::   meet the following conditions:

::   (a) You must give any other recipients of the Work or
::         Derivative Works a copy of this License; and

::   (b) You must cause any modified files to carry prominent notices
::         stating that You changed the files; and

::   (c) You must retain, in the Source form of any Derivative Works
::         that You distribute, all copyright, patent, trademark, and
::         attribution notices from the Source form of the Work,
::         excluding those notices that do not pertain to any part of
::         the Derivative Works; and

::   (d) If the Work includes a "NOTICE" text file as part of its
::         distribution, then any Derivative Works that You distribute must
::         include a readable copy of the attribution notices contained
::         within such NOTICE file, excluding those notices that do not
::         pertain to any part of the Derivative Works, in at least one
::         of the following places: within a NOTICE text file distributed
::         as part of the Derivative Works; within the Source form or
::         documentation, if provided along with the Derivative Works; or,
::         within a display generated by the Derivative Works, if and
::         wherever such third-party notices normally appear. The contents
::         of the NOTICE file are for informational purposes only and
::         do not modify the License. You may add Your own attribution
::         notices within Derivative Works that You distribute, alongside
::         or as an addendum to the NOTICE text from the Work, provided
::         that such additional attribution notices cannot be construed
::         as modifying the License.

::   You may add Your own copyright statement to Your modifications and
::   may provide additional or different license terms and conditions
::   for use, reproduction, or distribution of Your modifications, or
::   for any such Derivative Works as a whole, provided Your use,
::   reproduction, and distribution of the Work otherwise complies with
::   the conditions stated in this License.

::   5. Submission of Contributions. Unless You explicitly state otherwise,
::   any Contribution intentionally submitted for inclusion in the Work
::   by You to the Licensor shall be under the terms and conditions of
::   this License, without any additional terms or conditions.
::   Notwithstanding the above, nothing herein shall supersede or modify
::   the terms of any separate license agreement you may have executed
::   with Licensor regarding such Contributions.

::   6. Trademarks. This License does not grant permission to use the trade
::   names, trademarks, service marks, or product names of the Licensor,
::   except as required for reasonable and customary use in describing the
::   origin of the Work and reproducing the content of the NOTICE file.

::   7. Disclaimer of Warranty. Unless required by applicable law or
::   agreed to in writing, Licensor provides the Work (and each
::   Contributor provides its Contributions) on an "AS IS" BASIS,
::   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
::   implied, including, without limitation, any warranties or conditions
::   of TITLE, NON-INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A
::   PARTICULAR PURPOSE. You are solely responsible for determining the
::   appropriateness of using or redistributing the Work and assume any
::   risks associated with Your exercise of permissions under this License.

::   8. Limitation of Liability. In no event and under no legal theory,
::   whether in tort (including negligence), contract, or otherwise,
::   unless required by applicable law (such as deliberate and grossly
::   negligent acts) or agreed to in writing, shall any Contributor be
::   liable to You for damages, including any direct, indirect, special,
::   incidental, or consequential damages of any character arising as a
::   result of this License or out of the use or inability to use the
::   Work (including but not limited to damages for loss of goodwill,
::   work stoppage, computer failure or malfunction, or any and all
::   other commercial damages or losses), even if such Contributor
::   has been advised of the possibility of such damages.

::   9. Accepting Warranty or Additional Liability. While redistributing
::   the Work or Derivative Works thereof, You may choose to offer,
::   and charge a fee for, acceptance of support, warranty, indemnity,
::   or other liability obligations and/or rights consistent with this
::   License. However, in accepting such obligations, You may act only
::   on Your own behalf and on Your sole responsibility, not on behalf
::   of any other Contributor, and only if You agree to indemnify,
::   defend, and hold each Contributor harmless for any liability
::   incurred by, or claims asserted against, such Contributor by reason
::   of your accepting any such warranty or additional liability.

::   END OF TERMS AND CONDITIONS

::   APPENDIX: How to apply the Apache License to your work.

::   To apply the Apache License to your work, attach the following
::   boilerplate notice, with the fields enclosed by brackets "[]"
::   replaced with your own identifying information. (Don't include
::   the brackets!)  The text should be enclosed in the appropriate
::   comment syntax for the file format. We also recommend that a
::   file or class name and description of purpose be included on the
::   same "printed page" as the copyright notice for easier
::   identification within third-party archives.

::   Copyright [yyyy] [name of copyright owner]

::   Licensed under the Apache License, Version 2.0 (the "License");
::   you may not use this file except in compliance with the License.
::   You may obtain a copy of the License at

::    http://www.apache.org/licenses/LICENSE-2.0

::   Unless required by applicable law or agreed to in writing, software
::   distributed under the License is distributed on an "AS IS" BASIS,
::   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
::   See the License for the specific language governing permissions and
::   limitations under the License.

@echo off & setlocal enabledelayedexpansion & goto :BeginOfBatch


#-- Begin of shell script -- boot_patch.sh
#!/bin/sh
############
# Functions
############

# Pure bash dirname implementation
getdir() {
  case "$1" in
    */*)
      dir=${1%/*}
      if [ -z $dir ]; then
        echo "/"
      else
        echo $dir
      fi
    ;;
    *) echo "." ;;
  esac
}

ui_print(){
	printf "%s\n" "$1"
}

abort(){
	printf "%s\n" "$1"
	exit 1
}
#################
# Initialization
#################

BOOTIMAGE="$1"
[ -e "$BOOTIMAGE" ] || abort "$BOOTIMAGE does not exist!"

# Flags
KEEPVERITY=$2
KEEPFORCEENCRYPT=$3
PATCHVBMETAFLAG=$4
RECOVERYMODE=false
export KEEPVERITY
export KEEPFORCEENCRYPT
export PATCHVBMETAFLAG

output=$5

chmod -R 755 .

#########
# Unpack
#########

CHROMEOS=false

ui_print "- Unpacking boot image"
./bin/magiskboot unpack "$BOOTIMAGE"

case $? in
  0 ) ;;
  1 )
    abort "! Unsupported/Unknown image format"
    ;;
  2 )
    ui_print "- ChromeOS boot image detected"
    CHROMEOS=true
    ;;
  * )
    abort "! Unable to unpack boot image"
    ;;
esac

###################
# Ramdisk Restores
###################

# Test patch status and do restore
ui_print "- Checking ramdisk status"
if [ -e ramdisk.cpio ]; then
  ./bin/magiskboot cpio ramdisk.cpio test
  STATUS=$?
else
  # Stock A only system-as-root
  STATUS=0
fi
case $((STATUS & 3)) in
  0 )  # Stock boot
    ui_print "- Stock boot image detected"
    SHA1=$(./bin/magiskboot sha1 "$BOOTIMAGE" 2>/dev/null)
    cat $BOOTIMAGE > stock_boot.img
    cp -af ramdisk.cpio ramdisk.cpio.orig 2>/dev/null
    ;;
  1 )  # Magisk patched
    ui_print "- Magisk patched boot image detected"
    # Find SHA1 of stock boot image
    [ -z $SHA1 ] && SHA1=$(./bin/magiskboot cpio ramdisk.cpio sha1 2>/dev/null)
    ./bin/magiskboot cpio ramdisk.cpio restore
    cp -af ramdisk.cpio ramdisk.cpio.orig
    rm -f stock_boot.img
    ;;
  2 )  # Unsupported
    ui_print "! Boot image patched by unsupported programs"
    abort "! Please restore back to stock boot image"
    ;;
esac

# Work around custom legacy Sony /init -> /(s)bin/init_sony : /init.real setup
INIT=init
if [ $((STATUS & 4)) -ne 0 ]; then
  INIT=init.real
fi

##################
# Ramdisk Patches
##################

ui_print "- Patching ramdisk"

echo "KEEPVERITY=$KEEPVERITY" > config
echo "KEEPFORCEENCRYPT=$KEEPFORCEENCRYPT" >> config
echo "PATCHVBMETAFLAG=$PATCHVBMETAFLAG" >> config
echo "RECOVERYMODE=$RECOVERYMODE" >> config
[ ! -z $SHA1 ] && echo "SHA1=$SHA1" >> config

# Compress to save precious ramdisk space
SKIP32="#"
SKIP64="#"
if [ -f magisk32 ]; then
  ./bin/magiskboot compress=xz magisk32 magisk32.xz
  unset SKIP32
fi
if [ -f magisk64 ]; then
  ./bin/magiskboot compress=xz magisk64 magisk64.xz
  unset SKIP64
fi

./bin/magiskboot cpio ramdisk.cpio \
"add 0750 $INIT magiskinit" \
"mkdir 0750 overlay.d" \
"mkdir 0750 overlay.d/sbin" \
"$SKIP32 add 0644 overlay.d/sbin/magisk32.xz magisk32.xz" \
"$SKIP64 add 0644 overlay.d/sbin/magisk64.xz magisk64.xz" \
"patch" \
"backup ramdisk.cpio.orig" \
"mkdir 000 .backup" \
"add 000 .backup/.magisk config"

rm -f ramdisk.cpio.orig config magisk*.xz

#################
# Binary Patches
#################

for dt in dtb kernel_dtb extra; do
  [ -f $dt ] && ./bin/magiskboot dtb $dt patch && ui_print "- Patch fstab in $dt"
done

if [ -f kernel ]; then
  # Remove Samsung RKP
  ./bin/magiskboot hexpatch kernel \
  49010054011440B93FA00F71E9000054010840B93FA00F7189000054001840B91FA00F7188010054 \
  A1020054011440B93FA00F7140020054010840B93FA00F71E0010054001840B91FA00F7181010054

  # Remove Samsung defex
  # Before: [mov w2, #-221]   (-__NR_execve)
  # After:  [mov w2, #-32768]
  ./bin/magiskboot hexpatch kernel 821B8012 E2FF8F12

  # Force kernel to load rootfs
  # skip_initramfs -> want_initramfs
  ./bin/magiskboot hexpatch kernel \
  736B69705F696E697472616D667300 \
  77616E745F696E697472616D667300
fi

#################
# Repack & Flash
#################

ui_print "- Repacking boot image"
./bin/magiskboot repack "$BOOTIMAGE" $output || abort "! Unable to repack boot image"

# Sign chromeos boot
# $CHROMEOS && sign_chromeos

# Restore the original boot partition path
[ -e "$BOOTNAND" ] && BOOTIMAGE="$BOOTNAND"

ui_print "Script by affggh"
# Reset any error code
true

ui_print "Clean up"
./bin/magiskboot cleanup
#-- End of shell script --
exit


:BeginOfBatch
:: Began of args detection
set funcs=patch autoconfig test
:: We need certutil extract busybox
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
	if not defined magisk set magisk=%~dp0prebuilt\magisk.apk
) else (
	echo Not define config file ,use default value
	if not defined keepverity set keepverity=true
	if not defined keepforceencrypt set keepforceencrypt=true
	if not defined patchvbmetaflag set patchvbmetaflag=false
	if not defined magisk set magisk=%~dp0prebuilt\magisk.apk
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
:: x86 and x86_64 no need to change
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

:: Get magisk version
for /f "tokens=2 delims==" %%i in ('busybox grep -rn "MAGISK_VER=" tmp\assets\*') do set MAGISK_VER=%%i

for %%i in (arm64-v8a x86_64) do (
	if "!arch!"=="%%i" set is64bit=true
)

for /r "tmp\lib" %%i in (lib*.so) do (
	if "%%~nxi"=="libmagiskinit.so" copy %%i .\magiskinit
	if "%%~nxi"=="libmagisk32.so" copy %%i .\magisk32
	if "%%~nxi"=="libmagisk64.so" (
		if "!is64bit!"=="true" copy %%i .\magisk64
	)
)

:: Show all type
echo  List your config :
echo                    Magisk version = !MAGISK_VER!
echo                    arch=!arch!
echo                    keepverity=!keepverity!
echo                    keepforceencrypt=!keepforceencrypt!
echo                    patchvbmetaflag=!patchvbmetaflag!
echo                    magisk=!magisk!
echo                    input=!input!
if defined output (
	echo                    output=!output!
) else (
	echo                    output=new-boot.img [default]
)

more +211 %0 | busybox ash -s !input! !keepverity! !keepforceencrypt! !patchvbmetaflag! !output!
set exitcode=%errorlevel%
goto :EndofBatch

:autoconfig
echo Function : autoconfig
if "!configdefault!"=="1" (
	if not defined arch set arch=arm64
	if not defined keepverity set keepverity=true
	if not defined keepforceencrypt set keepforceencrypt=true
	if not defined patchvbmetaflag set patchvbmetaflag=false
	if not defined magisk set magisk=%~dp0prebuilt\magisk.apk
	busybox printf "# var  type\n" > config.txt 
	busybox printf "arch=%%s\n" "!arch!" >> config.txt
	busybox printf "keepverity=%%s\n" "!keepverity!" >> config.txt
	busybox printf "keepforceencrypt=%%s\n" "!keepforceencrypt!" >> config.txt
	busybox printf "patchvbmetaflag=%%s\n" "!patchvbmetaflag!" >> config.txt
	if exist "!magisk!" (
		busybox printf "magisk=%%s\n" "!magisk!" >> config.txt
	) else (
		echo Warning... file var magisk
		echo         magisk=    not defined...
		busybox printf "magisk=\n" >> config.txt
	)
	if exist ".\config.txt" (
		rem type .\config.txt
		echo Successfully generate config.txt...
	) else (
		echo Generate config.txt failed...
	)
	rem show information
	exit /b 0
) else (
	echo Read config from device...
	tasklist /FI "IMAGENAME eq adb.exe" | findstr "adb.exe" >nul
	if "%errorlevel%"=="0" (
		rem kill adb.exe service if exist
		taskkill /F /FI "IMAGENAME eq adb.exe" /IM * >nul
	)
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
)
	busybox printf "# var  type\n" > config.txt
	rem Lots of device not support this new way ,use old way
	rem type "%~dp0bin\get_config.sh" | adb shell >> config.txt
	if "!state!"=="device" (
		set tmp=/data/local/tmp
	)
	if "!state!"=="recovery" (
		set tmp=/tmp
	)
	echo Device state is !state! , tmp as [!tmp!]...
	adb push %~dp0bin\get_config.sh !tmp! >nul
	adb shell chmod 0755 !tmp!/get_config.sh
	adb shell sh !tmp!/get_config.sh >> config.txt
	adb shell rm -f !tmp!/get_config.sh
	if not defined magisk set magisk=%~dp0prebuilt\magisk.apk
	busybox printf "magisk=%%s\n" "!magisk!" >> config.txt
	if exist ".\config.txt" (
		rem type config.txt
		echo Successfully generate config.txt...
	) else (
		echo Generate config.txt failed...
	)
)
adb kill-server
goto :EndofBatch

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
echo                                  default : [prebuilt\magisk.apk]
echo               Notice: Shell script part will auto detect file existance
echo                       if is a 64bit image.
echo.
echo          autoconfig : This function can auto detect config from device
echo                       and generate a confit.txt at %~dp0 
echo                       without root
echo             --default  generate with default instead read from device
echo             -m     Defined custom magisk path
echo.
echo   Example : 
echo           %~nx0 patch -i boot.img -c config.txt
echo           %~nx0 patch -i boot.img -a armeabi-v7a -kv true -ke true -pv false
echo           %~nx0 patch -i boot.img -c config.txt -m prebuilt\magisk.apk
echo.
echo           %~nx0 autoconfig
echo           %~nx0 autoconfig --default
echo           %~nx0 autoconfig -m prebuilt\magisk.apk

goto :eof


:: End of Batch script