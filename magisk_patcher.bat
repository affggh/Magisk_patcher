:: Batch script by affggh 879632264@qq.com
:: Busybox from github compiled by myself. busybox-w32
:: Shell script Edited from magisk canary flashable apk file...
:: magiskboot for cygwin64 is based on magisk source 20220124...also compiled by myself

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


#-- Begin of shell script -- get_config.sh
#!/system/bin/sh

ui_print() {
  if $BOOTMODE; then
    echo "$1"
  else
    echo -e "ui_print $1\nui_print" >> /proc/self/fd/$OUTFD
  fi
}

toupper() {
  echo "$@" | tr '[:lower:]' '[:upper:]'
}

grep_cmdline() {
  local REGEX="s/^$1=//p"
  { echo $(cat /proc/cmdline)$(sed -e 's/[^"]//g' -e 's/""//g' /proc/cmdline) | xargs -n 1; \
    sed -e 's/ = /=/g' -e 's/, /,/g' -e 's/"//g' /proc/bootconfig; \
  } 2>/dev/null | sed -n "$REGEX"
}

grep_prop() {
  local REGEX="s/^$1=//p"
  shift
  local FILES=$@
  [ -z "$FILES" ] && FILES='/system/build.prop'
  cat $FILES 2>/dev/null | dos2unix | sed -n "$REGEX" | head -n 1
}

grep_get_prop() {
  local result=$(grep_prop $@)
  if [ -z "$result" ]; then
    # Fallback to getprop
    getprop "$1"
  else
    echo $result
  fi
}

getvar() {
  local VARNAME=$1
  local VALUE
  local PROPPATH='/data/.magisk /cache/.magisk'
  [ ! -z $MAGISKTMP ] && PROPPATH="$MAGISKTMP/config $PROPPATH"
  VALUE=$(grep_prop $VARNAME $PROPPATH)
  [ ! -z $VALUE ] && eval $VARNAME=\$VALUE
}

is_mounted() {
  grep -q " $(readlink -f $1) " /proc/mounts 2>/dev/null
  return $?
}

abort() {
  ui_print "$1"
  $BOOTMODE || recovery_cleanup
  [ ! -z $MODPATH ] && rm -rf $MODPATH
  rm -rf $TMPDIR
  exit 1
}

resolve_vars() {
  MAGISKBIN=$NVBASE/magisk
  POSTFSDATAD=$NVBASE/post-fs-data.d
  SERVICED=$NVBASE/service.d
}

print_title() {
  local len line1len line2len bar
  line1len=$(echo -n $1 | wc -c)
  line2len=$(echo -n $2 | wc -c)
  len=$line2len
  [ $line1len -gt $line2len ] && len=$line1len
  len=$((len + 2))
  bar=$(printf "%${len}s" | tr ' ' '*')
  ui_print "$bar"
  ui_print " $1 "
  [ "$2" ] && ui_print " $2 "
  ui_print "$bar"
}

######################
# Environment Related
######################

setup_flashable() {
  ensure_bb
  $BOOTMODE && return
  if [ -z $OUTFD ] || readlink /proc/$$/fd/$OUTFD | grep -q /tmp; then
    # We will have to manually find out OUTFD
    for FD in `ls /proc/$$/fd`; do
      if readlink /proc/$$/fd/$FD | grep -q pipe; then
        if ps | grep -v grep | grep -qE " 3 $FD |status_fd=$FD"; then
          OUTFD=$FD
          break
        fi
      fi
    done
  fi
  recovery_actions
}

ensure_bb() {
  if set -o | grep -q standalone; then
    # We are definitely in busybox ash
    set -o standalone
    return
  fi

  # Find our busybox binary
  local bb
  if [ -f $TMPDIR/busybox ]; then
    bb=$TMPDIR/busybox
  elif [ -f $MAGISKBIN/busybox ]; then
    bb=$MAGISKBIN/busybox
  else
    abort "! Cannot find BusyBox"
  fi
  chmod 755 $bb

  # Busybox could be a script, make sure /system/bin/sh exists
  if [ ! -f /system/bin/sh ]; then
    umount -l /system 2>/dev/null
    mkdir -p /system/bin
    ln -s $(command -v sh) /system/bin/sh
  fi

  export ASH_STANDALONE=1

  # Find our current arguments
  # Run in busybox environment to ensure consistent results
  # /proc/<pid>/cmdline shall be <interpreter> <script> <arguments...>
  local cmds="$($bb sh -c "
  for arg in \$(tr '\0' '\n' < /proc/$$/cmdline); do
    if [ -z \"\$cmds\" ]; then
      # Skip the first argument as we want to change the interpreter
      cmds=\"sh\"
    else
      cmds=\"\$cmds '\$arg'\"
    fi
  done
  echo \$cmds")"

  # Re-exec our script
  echo $cmds | $bb xargs $bb
  exit
}

recovery_actions() {
  # Make sure random won't get blocked
  mount -o bind /dev/urandom /dev/random
  # Unset library paths
  OLD_LD_LIB=$LD_LIBRARY_PATH
  OLD_LD_PRE=$LD_PRELOAD
  OLD_LD_CFG=$LD_CONFIG_FILE
  unset LD_LIBRARY_PATH
  unset LD_PRELOAD
  unset LD_CONFIG_FILE
}

recovery_cleanup() {
  local DIR
  ui_print "- Unmounting partitions"
  (umount_apex
  if [ ! -d /postinstall/tmp ]; then
    umount -l /system
    umount -l /system_root
  fi
  umount -l /vendor
  umount -l /persist
  umount -l /metadata
  for DIR in /apex /system /system_root; do
    if [ -L "${DIR}_link" ]; then
      rmdir $DIR
      mv -f ${DIR}_link $DIR
    fi
  done
  umount -l /dev/random) 2>/dev/null
  [ -z $OLD_LD_LIB ] || export LD_LIBRARY_PATH=$OLD_LD_LIB
  [ -z $OLD_LD_PRE ] || export LD_PRELOAD=$OLD_LD_PRE
  [ -z $OLD_LD_CFG ] || export LD_CONFIG_FILE=$OLD_LD_CFG
}

#######################
# Installation Related
#######################

# find_block [partname...]
find_block() {
  local BLOCK DEV DEVICE DEVNAME PARTNAME UEVENT
  for BLOCK in "$@"; do
    DEVICE=`find /dev/block \( -type b -o -type c -o -type l \) -iname $BLOCK | head -n 1` 2>/dev/null
    if [ ! -z $DEVICE ]; then
      readlink -f $DEVICE
      return 0
    fi
  done
  # Fallback by parsing sysfs uevents
  for UEVENT in /sys/dev/block/*/uevent; do
    DEVNAME=`grep_prop DEVNAME $UEVENT`
    PARTNAME=`grep_prop PARTNAME $UEVENT`
    for BLOCK in "$@"; do
      if [ "$(toupper $BLOCK)" = "$(toupper $PARTNAME)" ]; then
        echo /dev/block/$DEVNAME
        return 0
      fi
    done
  done
  # Look just in /dev in case we're dealing with MTD/NAND without /dev/block devices/links
  for DEV in "$@"; do
    DEVICE=`find /dev \( -type b -o -type c -o -type l \) -maxdepth 1 -iname $DEV | head -n 1` 2>/dev/null
    if [ ! -z $DEVICE ]; then
      readlink -f $DEVICE
      return 0
    fi
  done
  return 1
}

# setup_mntpoint <mountpoint>
setup_mntpoint() {
  local POINT=$1
  [ -L $POINT ] && mv -f $POINT ${POINT}_link
  if [ ! -d $POINT ]; then
    rm -f $POINT
    mkdir -p $POINT
  fi
}

# mount_name <partname(s)> <mountpoint> <flag>
mount_name() {
  local PART=$1
  local POINT=$2
  local FLAG=$3
  setup_mntpoint $POINT
  is_mounted $POINT && return
  # First try mounting with fstab
  mount $FLAG $POINT 2>/dev/null
  if ! is_mounted $POINT; then
    local BLOCK=$(find_block $PART)
    mount $FLAG $BLOCK $POINT || return
  fi
  ui_print "- Mounting $POINT"
}

# mount_ro_ensure <partname(s)> <mountpoint>
mount_ro_ensure() {
  # We handle ro partitions only in recovery
  $BOOTMODE && return
  local PART=$1
  local POINT=$2
  mount_name "$PART" $POINT '-o ro'
  is_mounted $POINT || abort "! Cannot mount $POINT"
}

mount_partitions() {
  # Check A/B slot
  SLOT=`grep_cmdline androidboot.slot_suffix`
  if [ -z $SLOT ]; then
    SLOT=`grep_cmdline androidboot.slot`
    [ -z $SLOT ] || SLOT=_${SLOT}
  fi
  [ -z $SLOT ] || ui_print "- Current boot slot: $SLOT"

  # Mount ro partitions
  if is_mounted /system_root; then
    umount /system 2&>/dev/null
    umount /system_root 2&>/dev/null
  fi
  mount_ro_ensure "system$SLOT app$SLOT" /system
  if [ -f /system/init -o -L /system/init ]; then
    SYSTEM_ROOT=true
    setup_mntpoint /system_root
    if ! mount --move /system /system_root; then
      umount /system
      umount -l /system 2>/dev/null
      mount_ro_ensure "system$SLOT app$SLOT" /system_root
    fi
    mount -o bind /system_root/system /system
  else
    SYSTEM_ROOT=false
    grep ' / ' /proc/mounts | grep -qv 'rootfs' || grep -q ' /system_root ' /proc/mounts && SYSTEM_ROOT=true
  fi
  # /vendor is used only on some older devices for recovery AVBv1 signing so is not critical if fails
  [ -L /system/vendor ] && mount_name vendor$SLOT /vendor '-o ro'
  $SYSTEM_ROOT && ui_print "- Device is system-as-root"

  # Allow /system/bin commands (dalvikvm) on Android 10+ in recovery
  $BOOTMODE || mount_apex
}

# loop_setup <ext4_img>, sets LOOPDEV
loop_setup() {
  unset LOOPDEV
  local LOOP
  local MINORX=1
  [ -e /dev/block/loop1 ] && MINORX=$(stat -Lc '%T' /dev/block/loop1)
  local NUM=0
  while [ $NUM -lt 64 ]; do
    LOOP=/dev/block/loop$NUM
    [ -e $LOOP ] || mknod $LOOP b 7 $((NUM * MINORX))
    if losetup $LOOP "$1" 2>/dev/null; then
      LOOPDEV=$LOOP
      break
    fi
    NUM=$((NUM + 1))
  done
}

mount_apex() {
  $BOOTMODE || [ ! -d /system/apex ] && return
  local APEX DEST
  setup_mntpoint /apex
  mount -t tmpfs tmpfs /apex -o mode=755
  local PATTERN='s/.*"name":[^"]*"\([^"]*\).*/\1/p'
  for APEX in /system/apex/*; do
    if [ -f $APEX ]; then
      # handle CAPEX APKs, extract actual APEX APK first
      unzip -qo $APEX original_apex -d /apex
      [ -f /apex/original_apex ] && APEX=/apex/original_apex # unzip doesn't do return codes
      # APEX APKs, extract and loop mount
      unzip -qo $APEX apex_payload.img -d /apex
      DEST=$(unzip -qp $APEX apex_manifest.pb | strings | head -n 1)
      [ -z $DEST ] && DEST=$(unzip -qp $APEX apex_manifest.json | sed -n $PATTERN)
      [ -z $DEST ] && continue
      DEST=/apex/$DEST
      mkdir -p $DEST
      loop_setup /apex/apex_payload.img
      if [ ! -z $LOOPDEV ]; then
        ui_print "- Mounting $DEST"
        mount -t ext4 -o ro,noatime $LOOPDEV $DEST
      fi
      rm -f /apex/original_apex /apex/apex_payload.img
    elif [ -d $APEX ]; then
      # APEX folders, bind mount directory
      if [ -f $APEX/apex_manifest.json ]; then
        DEST=/apex/$(sed -n $PATTERN $APEX/apex_manifest.json)
      elif [ -f $APEX/apex_manifest.pb ]; then
        DEST=/apex/$(strings $APEX/apex_manifest.pb | head -n 1)
      else
        continue
      fi
      mkdir -p $DEST
      ui_print "- Mounting $DEST"
      mount -o bind $APEX $DEST
    fi
  done
  export ANDROID_RUNTIME_ROOT=/apex/com.android.runtime
  export ANDROID_TZDATA_ROOT=/apex/com.android.tzdata
  export ANDROID_ART_ROOT=/apex/com.android.art
  export ANDROID_I18N_ROOT=/apex/com.android.i18n
  local APEXJARS=$(find /apex -name '*.jar' | sort | tr '\n' ':')
  local FWK=/system/framework
  export BOOTCLASSPATH=${APEXJARS}\
$FWK/framework.jar:$FWK/ext.jar:$FWK/telephony-common.jar:\
$FWK/voip-common.jar:$FWK/ims-common.jar:$FWK/telephony-ext.jar
}

umount_apex() {
  [ -d /apex ] || return
  umount -l /apex
  for loop in /dev/block/loop*; do
    losetup -d $loop 2>/dev/null
  done
  unset ANDROID_RUNTIME_ROOT
  unset ANDROID_TZDATA_ROOT
  unset ANDROID_ART_ROOT
  unset ANDROID_I18N_ROOT
  unset BOOTCLASSPATH
}

# After calling this method, the following variables will be set:
# KEEPVERITY, KEEPFORCEENCRYPT, RECOVERYMODE, PATCHVBMETAFLAG,
# ISENCRYPTED, VBMETAEXIST
get_flags() {
  getvar KEEPVERITY
  getvar KEEPFORCEENCRYPT
  getvar RECOVERYMODE
  getvar PATCHVBMETAFLAG
  if [ -z $KEEPVERITY ]; then
    if $SYSTEM_ROOT; then
      KEEPVERITY=true
      #ui_print "- System-as-root, keep dm/avb-verity"
    else
      KEEPVERITY=false
    fi
  fi
  ISENCRYPTED=false
  grep ' /data ' /proc/mounts | grep -q 'dm-' && ISENCRYPTED=true
  [ "$(getprop ro.crypto.state)" = "encrypted" ] && ISENCRYPTED=true
  if [ -z $KEEPFORCEENCRYPT ]; then
    # No data access means unable to decrypt in recovery
    if $ISENCRYPTED || ! $DATA; then
      KEEPFORCEENCRYPT=true
      #ui_print "- Encrypted data, keep forceencrypt"
    else
      KEEPFORCEENCRYPT=false
    fi
  fi
  VBMETAEXIST=false
  local VBMETAIMG=$(find_block vbmeta vbmeta_a)
  [ -n "$VBMETAIMG" ] && VBMETAEXIST=true
  if [ -z $PATCHVBMETAFLAG ]; then
    if $VBMETAEXIST; then
      PATCHVBMETAFLAG=false
    else
      PATCHVBMETAFLAG=true
      #ui_print "- Cannot find vbmeta partition, patch vbmeta in boot image"
    fi
  fi
  [ -z $RECOVERYMODE ] && RECOVERYMODE=false
  printf "keepverity=%s\n" "$KEEPVERITY"
  printf "keepforceencrypt=%s\n" "$KEEPFORCEENCRYPT"
  printf "patchvbmetaflag=%s\n" "$PATCHVBMETAFLAG"
}

find_boot_image() {
  BOOTIMAGE=
  if $RECOVERYMODE; then
    BOOTIMAGE=`find_block recovery_ramdisk$SLOT recovery$SLOT sos`
  elif [ ! -z $SLOT ]; then
    BOOTIMAGE=`find_block ramdisk$SLOT recovery_ramdisk$SLOT boot$SLOT`
  else
    BOOTIMAGE=`find_block ramdisk recovery_ramdisk kern-a android_boot kernel bootimg boot lnx boot_a`
  fi
  if [ -z $BOOTIMAGE ]; then
    # Lets see what fstabs tells me
    BOOTIMAGE=`grep -v '#' /etc/*fstab* | grep -E '/boot(img)?[^a-zA-Z]' | grep -oE '/dev/[a-zA-Z0-9_./-]*' | head -n 1`
  fi
}

flash_image() {
  case "$1" in
    *.gz) CMD1="gzip -d < '$1' 2>/dev/null";;
    *)    CMD1="cat '$1'";;
  esac
  if $BOOTSIGNED; then
    CMD2="$BOOTSIGNER -sign"
    ui_print "- Sign image with verity keys"
  else
    CMD2="cat -"
  fi
  if [ -b "$2" ]; then
    local img_sz=$(stat -c '%s' "$1")
    local blk_sz=$(blockdev --getsize64 "$2")
    [ "$img_sz" -gt "$blk_sz" ] && return 1
    blockdev --setrw "$2"
    local blk_ro=$(blockdev --getro "$2")
    [ "$blk_ro" -eq 1 ] && return 2
    eval "$CMD1" | eval "$CMD2" | cat - /dev/zero > "$2" 2>/dev/null
  elif [ -c "$2" ]; then
    flash_eraseall "$2" >&2
    eval "$CMD1" | eval "$CMD2" | nandwrite -p "$2" - >&2
  else
    ui_print "- Not block or char device, storing image"
    eval "$CMD1" | eval "$CMD2" > "$2" 2>/dev/null
  fi
  return 0
}

# Common installation script for flash_script.sh and addon.d.sh
install_magisk() {
  cd $MAGISKBIN

  if [ ! -c $BOOTIMAGE ]; then
    eval $BOOTSIGNER -verify < $BOOTIMAGE && BOOTSIGNED=true
    $BOOTSIGNED && ui_print "- Boot image is signed with AVB 1.0"
  fi

  # Source the boot patcher
  SOURCEDMODE=true
  . ./boot_patch.sh "$BOOTIMAGE"

  ui_print "- Flashing new boot image"
  flash_image new-boot.img "$BOOTIMAGE"
  case $? in
    1)
      abort "! Insufficient partition size"
      ;;
    2)
      abort "! $BOOTIMAGE is read only"
      ;;
  esac

  ./magiskboot cleanup
  rm -f new-boot.img

  run_migrations
}

sign_chromeos() {
  ui_print "- Signing ChromeOS boot image"

  echo > empty
  ./chromeos/futility vbutil_kernel --pack new-boot.img.signed \
  --keyblock ./chromeos/kernel.keyblock --signprivate ./chromeos/kernel_data_key.vbprivk \
  --version 1 --vmlinuz new-boot.img --config empty --arch arm --bootloader empty --flags 0x1

  rm -f empty new-boot.img
  mv new-boot.img.signed new-boot.img
}

remove_system_su() {
  if [ -f /system/bin/su -o -f /system/xbin/su ] && [ ! -f /su/bin/su ]; then
    ui_print "- Removing system installed root"
    blockdev --setrw /dev/block/mapper/system$SLOT 2>/dev/null
    mount -o rw,remount /system
    # SuperSU
    if [ -e /system/bin/.ext/.su ]; then
      mv -f /system/bin/app_process32_original /system/bin/app_process32 2>/dev/null
      mv -f /system/bin/app_process64_original /system/bin/app_process64 2>/dev/null
      mv -f /system/bin/install-recovery_original.sh /system/bin/install-recovery.sh 2>/dev/null
      cd /system/bin
      if [ -e app_process64 ]; then
        ln -sf app_process64 app_process
      elif [ -e app_process32 ]; then
        ln -sf app_process32 app_process
      fi
    fi
    rm -rf /system/.pin /system/bin/.ext /system/etc/.installed_su_daemon /system/etc/.has_su_daemon \
    /system/xbin/daemonsu /system/xbin/su /system/xbin/sugote /system/xbin/sugote-mksh /system/xbin/supolicy \
    /system/bin/app_process_init /system/bin/su /cache/su /system/lib/libsupol.so /system/lib64/libsupol.so \
    /system/su.d /system/etc/install-recovery.sh /system/etc/init.d/99SuperSUDaemon /cache/install-recovery.sh \
    /system/.supersu /cache/.supersu /data/.supersu \
    /system/app/Superuser.apk /system/app/SuperSU /cache/Superuser.apk
  elif [ -f /cache/su.img -o -f /data/su.img -o -d /data/adb/su -o -d /data/su ]; then
    ui_print "- Removing systemless installed root"
    umount -l /su 2>/dev/null
    rm -rf /cache/su.img /data/su.img /data/adb/su /data/adb/suhide /data/su /cache/.supersu /data/.supersu \
    /cache/supersu_install /data/supersu_install
  fi
}

api_level_arch_detect() {
  API=$(grep_get_prop ro.build.version.sdk)
  ABI=$(grep_get_prop ro.product.cpu.abi)
  if [ "$ABI" = "x86" ]; then
    ARCH=x86
    ABI32=x86
    IS64BIT=false
  elif [ "$ABI" = "arm64-v8a" ]; then
    ARCH=arm64
    ABI32=armeabi-v7a
    IS64BIT=true
  elif [ "$ABI" = "x86_64" ]; then
    ARCH=x64
    ABI32=x86
    IS64BIT=true
  else
    ARCH=arm
    ABI=armeabi-v7a
    ABI32=armeabi-v7a
    IS64BIT=false
  fi
  printf "arch=%s\n" "$ARCH"
}

check_data() {
  DATA=false
  DATA_DE=false
  if grep ' /data ' /proc/mounts | grep -vq 'tmpfs'; then
    # Test if data is writable
    touch /data/.rw && rm /data/.rw && DATA=true
    # Test if data is decrypted
    $DATA && [ -d /data/adb ] && touch /data/adb/.rw && rm /data/adb/.rw && DATA_DE=true
    $DATA_DE && [ -d /data/adb/magisk ] || mkdir /data/adb/magisk || DATA_DE=false
  fi
  NVBASE=/data
  $DATA || NVBASE=/cache/data_adb
  $DATA_DE && NVBASE=/data/adb
  resolve_vars
}

find_magisk_apk() {
  local DBAPK
  [ -z $APK ] && APK=$NVBASE/magisk.apk
  [ -f $APK ] || APK=$MAGISKBIN/magisk.apk
  [ -f $APK ] || APK=/data/app/com.topjohnwu.magisk*/*.apk
  [ -f $APK ] || APK=/data/app/*/com.topjohnwu.magisk*/*.apk
  if [ ! -f $APK ]; then
    DBAPK=$(magisk --sqlite "SELECT value FROM strings WHERE key='requester'" 2>/dev/null | cut -d= -f2)
    [ -z $DBAPK ] && DBAPK=$(strings $NVBASE/magisk.db | grep -oE 'requester..*' | cut -c10-)
    [ -z $DBAPK ] || APK=/data/user_de/*/$DBAPK/dyn/*.apk
    [ -f $APK ] || [ -z $DBAPK ] || APK=/data/app/$DBAPK*/*.apk
    [ -f $APK ] || [ -z $DBAPK ] || APK=/data/app/*/$DBAPK*/*.apk
  fi
  [ -f $APK ] || ui_print "! Unable to detect Magisk app APK for BootSigner"
}

run_migrations() {
  local LOCSHA1
  local TARGET
  # Legacy app installation
  local BACKUP=$MAGISKBIN/stock_boot*.gz
  if [ -f $BACKUP ]; then
    cp $BACKUP /data
    rm -f $BACKUP
  fi

  # Legacy backup
  for gz in /data/stock_boot*.gz; do
    [ -f $gz ] || break
    LOCSHA1=`basename $gz | sed -e 's/stock_boot_//' -e 's/.img.gz//'`
    [ -z $LOCSHA1 ] && break
    mkdir /data/magisk_backup_${LOCSHA1} 2>/dev/null
    mv $gz /data/magisk_backup_${LOCSHA1}/boot.img.gz
  done

  # Stock backups
  LOCSHA1=$SHA1
  for name in boot dtb dtbo dtbs; do
    BACKUP=$MAGISKBIN/stock_${name}.img
    [ -f $BACKUP ] || continue
    if [ $name = 'boot' ]; then
      LOCSHA1=`$MAGISKBIN/magiskboot sha1 $BACKUP`
      mkdir /data/magisk_backup_${LOCSHA1} 2>/dev/null
    fi
    TARGET=/data/magisk_backup_${LOCSHA1}/${name}.img
    cp $BACKUP $TARGET
    rm -f $BACKUP
    gzip -9f $TARGET
  done
}

copy_sepolicy_rules() {
  # Remove all existing rule folders
  rm -rf /data/unencrypted/magisk /cache/magisk /metadata/magisk /persist/magisk /mnt/vendor/persist/magisk

  # Find current active RULESDIR
  local RULESDIR
  local ACTIVEDIR=$(magisk --path)/.magisk/mirror/sepolicy.rules
  if [ -L $ACTIVEDIR ]; then
    RULESDIR=$(readlink $ACTIVEDIR)
    [ "${RULESDIR:0:1}" != "/" ] && RULESDIR="$(magisk --path)/.magisk/mirror/$RULESDIR"
  elif ! $ISENCRYPTED; then
    RULESDIR=$NVBASE/modules
  elif [ -d /data/unencrypted ] && ! grep ' /data ' /proc/mounts | grep -qE 'dm-|f2fs'; then
    RULESDIR=/data/unencrypted/magisk
  elif grep ' /cache ' /proc/mounts | grep -q 'ext4' ; then
    RULESDIR=/cache/magisk
  elif grep ' /metadata ' /proc/mounts | grep -q 'ext4' ; then
    RULESDIR=/metadata/magisk
  elif grep ' /persist ' /proc/mounts | grep -q 'ext4' ; then
    RULESDIR=/persist/magisk
  elif grep ' /mnt/vendor/persist ' /proc/mounts | grep -q 'ext4' ; then
    RULESDIR=/mnt/vendor/persist/magisk
  else
    ui_print "- Unable to find sepolicy rules dir"
    return 1
  fi

  if [ -d ${RULESDIR%/magisk} ]; then
    ui_print "- Sepolicy rules dir is ${RULESDIR%/magisk}"
  else
    ui_print "- Sepolicy rules dir ${RULESDIR%/magisk} not found"
    return 1
  fi

  # Copy all enabled sepolicy.rule
  for r in $NVBASE/modules*/*/sepolicy.rule; do
    [ -f "$r" ] || continue
    local MODDIR=${r%/*}
    [ -f $MODDIR/disable ] && continue
    [ -f $MODDIR/remove ] && continue
    local MODNAME=${MODDIR##*/}
    mkdir -p $RULESDIR/$MODNAME
    cp -f $r $RULESDIR/$MODNAME/sepolicy.rule
  done
}

#################
# Module Related
#################

set_perm() {
  chown $2:$3 $1 || return 1
  chmod $4 $1 || return 1
  local CON=$5
  [ -z $CON ] && CON=u:object_r:system_file:s0
  chcon $CON $1 || return 1
}

set_perm_recursive() {
  find $1 -type d 2>/dev/null | while read dir; do
    set_perm $dir $2 $3 $4 $6
  done
  find $1 -type f -o -type l 2>/dev/null | while read file; do
    set_perm $file $2 $3 $5 $6
  done
}

mktouch() {
  mkdir -p ${1%/*} 2>/dev/null
  [ -z $2 ] && touch $1 || echo $2 > $1
  chmod 644 $1
}

request_size_check() {
  reqSizeM=`du -ms "$1" | cut -f1`
}

request_zip_size_check() {
  reqSizeM=`unzip -l "$1" | tail -n 1 | awk '{ print int(($1 - 1) / 1048576 + 1) }'`
}

boot_actions() { return; }

# Require ZIPFILE to be set
is_legacy_script() {
  unzip -l "$ZIPFILE" install.sh | grep -q install.sh
  return $?
}

# Require OUTFD, ZIPFILE to be set
install_module() {
  rm -rf $TMPDIR
  mkdir -p $TMPDIR
  cd $TMPDIR

  setup_flashable
  mount_partitions
  api_level_arch_detect

  # Setup busybox and binaries
  if $BOOTMODE; then
    boot_actions
  else
    recovery_actions
  fi

  # Extract prop file
  unzip -o "$ZIPFILE" module.prop -d $TMPDIR >&2
  [ ! -f $TMPDIR/module.prop ] && abort "! Unable to extract zip file!"

  local MODDIRNAME=modules
  $BOOTMODE && MODDIRNAME=modules_update
  local MODULEROOT=$NVBASE/$MODDIRNAME
  MODID=`grep_prop id $TMPDIR/module.prop`
  MODNAME=`grep_prop name $TMPDIR/module.prop`
  MODAUTH=`grep_prop author $TMPDIR/module.prop`
  MODPATH=$MODULEROOT/$MODID

  # Create mod paths
  rm -rf $MODPATH
  mkdir -p $MODPATH

  if is_legacy_script; then
    unzip -oj "$ZIPFILE" module.prop install.sh uninstall.sh 'common/*' -d $TMPDIR >&2

    # Load install script
    . $TMPDIR/install.sh

    # Callbacks
    print_modname
    on_install

    [ -f $TMPDIR/uninstall.sh ] && cp -af $TMPDIR/uninstall.sh $MODPATH/uninstall.sh
    $SKIPMOUNT && touch $MODPATH/skip_mount
    $PROPFILE && cp -af $TMPDIR/system.prop $MODPATH/system.prop
    cp -af $TMPDIR/module.prop $MODPATH/module.prop
    $POSTFSDATA && cp -af $TMPDIR/post-fs-data.sh $MODPATH/post-fs-data.sh
    $LATESTARTSERVICE && cp -af $TMPDIR/service.sh $MODPATH/service.sh

    ui_print "- Setting permissions"
    set_permissions
  else
    print_title "$MODNAME" "by $MODAUTH"
    print_title "Powered by Magisk"

    unzip -o "$ZIPFILE" customize.sh -d $MODPATH >&2

    if ! grep -q '^SKIPUNZIP=1$' $MODPATH/customize.sh 2>/dev/null; then
      ui_print "- Extracting module files"
      unzip -o "$ZIPFILE" -x 'META-INF/*' -d $MODPATH >&2

      # Default permissions
      set_perm_recursive $MODPATH 0 0 0755 0644
      set_perm_recursive $MODPATH/system/bin 0 2000 0755 0755
      set_perm_recursive $MODPATH/system/xbin 0 2000 0755 0755
      set_perm_recursive $MODPATH/system/system_ext/bin 0 2000 0755 0755
      set_perm_recursive $MODPATH/system/vendor/bin 0 2000 0755 0755 u:object_r:vendor_file:s0
    fi

    # Load customization script
    [ -f $MODPATH/customize.sh ] && . $MODPATH/customize.sh
  fi

  # Handle replace folders
  for TARGET in $REPLACE; do
    ui_print "- Replace target: $TARGET"
    mktouch $MODPATH$TARGET/.replace
  done

  if $BOOTMODE; then
    # Update info for Magisk app
    mktouch $NVBASE/modules/$MODID/update
    rm -rf $NVBASE/modules/$MODID/remove 2>/dev/null
    rm -rf $NVBASE/modules/$MODID/disable 2>/dev/null
    cp -af $MODPATH/module.prop $NVBASE/modules/$MODID/module.prop
  fi

  # Copy over custom sepolicy rules
  if [ -f $MODPATH/sepolicy.rule ]; then
    ui_print "- Installing custom sepolicy rules"
    copy_sepolicy_rules
  fi

  # Remove stuff that doesn't belong to modules and clean up any empty directories
  rm -rf \
  $MODPATH/system/placeholder $MODPATH/customize.sh \
  $MODPATH/README.md $MODPATH/.git*
  rmdir -p $MODPATH

  cd /
  $BOOTMODE || recovery_cleanup
  rm -rf $TMPDIR

  ui_print "- Done"
}

##########
# Presets
##########

api_level_arch_detect
get_flags

#-- End of shell script -- get_config.sh
exit 0


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

for /r "tmp\lib" %%i in (lib*.so) do (
	if "%%~nxi"=="libmagiskinit.so" copy %%i .\magiskinit
	if "%%~nxi"=="libmagisk32.so" copy %%i .\magisk32
	if "%%~nxi"=="libmagisk64.so" copy %%i .\magisk64
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
		echo Successfully generate config.txt...
	) else (
		echo Generate config.txt failed...
	)
) else (
	echo Read config from device...
	for /f "delims=" %%i in ('adb get-state 1^>nul 2^>nul') do set "state=%%i"
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
	more +410 %0 | adb shell >> config.txt
	if not defined magisk set magisk=%~dp0prebuilt\magisk.apk
	busybox printf "magisk=%%s\n" "!magisk!" >> config.txt
	if exist ".\config.txt" (
		echo Successfully generate config.txt...
	) else (
		echo Generate config.txt failed...
	)
)

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