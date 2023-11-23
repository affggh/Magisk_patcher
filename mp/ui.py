import customtkinter as ctk
from tkinter.ttk import Progressbar
from .magisk_logo import rawdata as logodata
from PIL import Image
from io import BytesIO
from os import getcwd, makedirs, walk
import os.path as op
from os import name as osname
from sys import version as pyversion
from sys import argv
import webbrowser
import logging
from multiprocessing.dummy import DummyProcess

from . import utils
from . import boot_patch

# multi lang support
from .lang import Language

if osname == 'nt':
    import ctypes

if osname == 'nt':
    EXT = ".exe"
else:
    EXT = ""

VERSION = "4.1.0"
AUTHOR = "affggh"
TITLE = "Magisk Patcher v%s by %s" % (VERSION, AUTHOR)
WIDTH = 900
HEIGHT = 420
OS, REL, ARCH = utils.retTypeAndMachine()
LICENSE = "GPLv3"
INTRODUCE = """\
- Native OS    \t: %s
- Native Arch  \t: %s
- Version      \t: %s
- Author       \t: %s
- License      \t: %s
- PythonVersion : %s
- Work Dir     \t: %s
- 介绍：
\tMagisk Patcher 是由 %s 开发的用来在桌面系统上修补手机magisk的一个简单的小程序，基于官方的magiskboot
- 感谢:
\t- magiskboot on mingw32 from https://github.com/svoboda18/magiskboot
\t- customtkinter ui界面库，有一说一确实好看
""" %(OS, ARCH, VERSION, AUTHOR, LICENSE, pyversion, getcwd(), AUTHOR)
if OS == 'windows':
    prebuilt_magiskboot = op.abspath(op.join(op.dirname(argv[0]), "bin", OS, ARCH, "magiskboot" + EXT))
elif OS == 'macos':
    prebuilt_magiskboot = op.abspath(op.join(op.dirname(argv[0]), "bin", OS, REL, ARCH, "magiskboot" + EXT))
else:
    prebuilt_magiskboot = op.abspath(op.join(op.dirname(argv[0]), "bin", "magiskboot"+EXT))

def visit_customtkinter_website(event):
    webbrowser.open("https://customtkinter.tomschimansky.com")

def visit_magisk_website(event):
    webbrowser.open("https://github.com/topjohnwu/Magisk")

class MagiskPatcherUI(ctk.CTk):
    def __init__(self, *args):
        super().__init__(*args)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.lang = ctk.StringVar(value=Language.supports[0])
        self.lang_dict = getattr(Language, self.lang.get())

        self.logo = ctk.CTkImage(Image.open(BytesIO(logodata), "r"), size=(240, 100))
        self.bootimg = ctk.StringVar()
        self.arch = ctk.StringVar()
        self.magisk_select = ctk.StringVar(value=self.langget('magisk is not select'))
        self.magisk_select_int = ctk.StringVar()

        self.keep_verity = ctk.BooleanVar(value=True)
        self.keep_forceencrypt = ctk.BooleanVar(value=True)
        self.patchvbmeta_flag = ctk.BooleanVar(value=False)
        self.recoverymode = ctk.BooleanVar(value=False)
        self.legacysar = ctk.BooleanVar(value=False)

        self.progress = ctk.DoubleVar(value=0)
        self.loglevel = ctk.IntVar(value=logging.WARNING)

        # download
        self.isproxy = ctk.BooleanVar(value=False)
        self.proxy = ctk.StringVar(value="127.0.0.1:7890") # default clash

        self.ismirror = ctk.BooleanVar(value=False)
        self.mirror = ctk.StringVar(value="")

        self.isjsdelivr = ctk.BooleanVar(value=True)

        self.uselocal = ctk.BooleanVar(value=True)
        self.usedeltamagisk = ctk.BooleanVar(value=False)

        # magisk list
        self.magisk_list = []

        self.__setup_widgets()

        # initial

        # log
        logging.basicConfig(level=logging.DEBUG)
        self.log = logging.getLogger()
        self.loghandler = logging.StreamHandler(self)
        logformatter = logging.Formatter("%(asctime)s - %(filename)s[line: %(lineno)d] - %(levelname)s: \n\t%(message)s")
        self.loghandler.setFormatter(logformatter)
        self.loghandler.setLevel(logging.DEBUG)
        self.log.addHandler(self.loghandler)

        self.log.setLevel(logging.WARN)

        print("- Detect env:", file=self)
        print(f"\tOS \t: {OS}", file=self)
        if OS == 'macos':
            print(f"\tREL\t: {REL}", file=self)
        print(f"\tARCH\t: {ARCH}", file=self)
        print(f"\tCurrent Dir\t: {getcwd()}", file=self)
        if OS in ['windows', 'macos']:
            print(f"- Windows/macOS Use prebuilt magiskboot.", file=self)
            print(f"\tFile should be here: {prebuilt_magiskboot}", file=self)
            if not prebuilt_magiskboot:
                print("- Error: Cannot find prebuilt magiskboot.", file=self)
                print("\tFix this to patch boot image correctly.", file=self)
                print(f"{prebuilt_magiskboot}")
        elif OS == 'linux':
            print(f"- Linux use magisk.apk inner magiskboot insted prebuilt magiskboot.", file=self)
            print(f"\t It will extract when patching a boot image.", file=self)
        
    # as stdout, you can print(..., file=self)
    def write(self, *args):
        self.textbox.insert('end', " ".join([str(i) for i in args]))
        self.textbox.yview('end')

    def flush(self): # void flush function
        pass

    def langget(self, key: str) -> str:
        if self.lang_dict.get(key):
            return self.lang_dict.get(key)
        else: return key

    def __setup_widgets(self):
        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0)
        self.navigation_label = ctk.CTkLabel(
            self.navigation_frame, image=self.logo, compound="left", text=""
        )
        self.navigation_label.bind("<Button-1>", visit_magisk_website)
        self.navigation_label.pack(side="top", fill="x")

        self.patcher_frame_button = ctk.CTkButton(
            self.navigation_frame,
            height=30,
            text=self.langget('Home'),
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            corner_radius=0,
            anchor="w",
            border_spacing=10,
            font=ctk.CTkFont(size=20),
            command=self.change_frame_patcher,
        )
        self.patcher_frame_button.pack(side="top", fill="x")
        self.download_frame_button = ctk.CTkButton(
            self.navigation_frame,
            height=30,
            text=self.langget('Select and Download'),
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            corner_radius=0,
            anchor="w",
            border_spacing=10,
            font=ctk.CTkFont(size=20),
            command=self.change_frame_download,
        )
        self.download_frame_button.pack(side="top", fill="x")
        self.other_frame_button = ctk.CTkButton(
            self.navigation_frame,
            height=30,
            text=self.langget('Other'),
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            corner_radius=0,
            anchor="w",
            border_spacing=10,
            font=ctk.CTkFont(size=20),
            command=self.change_frame_other,
        )
        self.other_frame_button.pack(side="top", fill="x")

        self.theme_select_button = ctk.CTkSegmentedButton(
            self.navigation_frame,
            corner_radius=0,
            values=["dark", "light", "system"],
            command=self.change_theme,
        )
        self.theme_select_button.set("system")
        self.theme_select_button.pack(side="bottom", fill="x")

        lang_frame = ctk.CTkFrame(self.navigation_frame, corner_radius=0)
        lang_label = ctk.CTkLabel(lang_frame, text="🌏", font=ctk.CTkFont(size=25), anchor='center', compound='center')
        lang_combo = ctk.CTkComboBox(lang_frame, corner_radius=0, values=Language.supports, variable=self.lang)
        lang_button = ctk.CTkButton(lang_frame, text="Confirm", command=self.refresh_widgets, width=80)
        lang_label.pack(side='left')
        lang_combo.pack(side='left', fill='x', expand='yes', padx=5)
        lang_button.pack(side='left')
        lang_frame.pack(side='bottom', pady=5, fill='x')

        base_on_label = ctk.CTkLabel(self.navigation_frame, text=self.langget('Based on CustomTkinter'), text_color=('blue', 'light blue'), font=ctk.CTkFont(underline=True), anchor='w')
        base_on_label.pack(side="bottom", fill="x", padx=5, pady=5)
        base_on_label.bind("<Button-1>", visit_customtkinter_website)

        self.navigation_frame.grid(row=0, rowspan=2, column=0, sticky="nsew")

        self.patcher_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.download_frame = ctk.CTkFrame(
            self, corner_radius=0, fg_color="transparent"
        )
        self.other_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")

        file_select_frame = ctk.CTkFrame(self.patcher_frame, corner_radius=5)
        file_select_label = ctk.CTkLabel(file_select_frame, text=self.langget('boot img'))
        file_select_entry = ctk.CTkEntry(file_select_frame, textvariable=self.bootimg)
        file_select_button = ctk.CTkButton(
            file_select_frame, text=self.langget('choose file'), command=self.file_choose_dialog
        )
        file_select_label.pack(side="left", padx=5, pady=5)

        file_select_entry.pack(side="left", fill="x", expand="yes")
        file_select_button.pack(side="right", padx=5, pady=5)
        file_select_frame.pack(side="top", fill="x", padx=5, pady=5)

        config_frame = ctk.CTkFrame(self.patcher_frame, corner_radius=5)

        arch_select_label = ctk.CTkLabel(config_frame, text=self.langget('arch')+'\t')
        arch_select_button = ctk.CTkSegmentedButton(
            config_frame,
            values=["arm64", "arm", "x86_64", "x86"],
            corner_radius=50,
            variable=self.arch,
        )
        arch_select_label.grid(column=0, row=0, padx=5, pady=5)
        arch_select_button.grid(
            column=1, columnspan=4, row=0, sticky="nsew", padx=5, pady=5
        )
        arch_select_button.set("arm64")

        keep_verify_check = ctk.CTkSwitch(config_frame, text=self.langget('keep verity'), variable=self.keep_verity)
        keep_verify_check.grid(column=1, row=1, padx=5, pady=5)

        keep_forceencrypt_check = ctk.CTkSwitch(config_frame, text=self.langget('keep encypt'), variable=self.keep_forceencrypt)
        keep_forceencrypt_check.grid(column=2, row=1, padx=5, pady=5)

        patch_vbmeta_flag = ctk.CTkSwitch(config_frame, text=self.langget('patch vbmeta flag'), variable=self.patchvbmeta_flag)
        patch_vbmeta_flag.grid(column=3, row=1, padx=5, pady=5)

        recovery_flag = ctk.CTkSwitch(config_frame, text=self.langget('recovery'), variable=self.recoverymode)
        recovery_flag.grid(column=4, row=1, padx=5, pady=5)

        legacy_sar_flag = ctk.CTkSwitch(config_frame, text=self.langget('legacy sar'), variable=self.legacysar)
        legacy_sar_flag.grid(column=1, row=2, sticky='nsew', padx=5, pady=5, columnspan=4)

        config_frame.pack(side="top", fill="x", expand="no", padx=5, pady=5)

        confirm_frame = ctk.CTkFrame(self.patcher_frame, corner_radius=5)
        confirm_info = ctk.CTkLabel(confirm_frame, textvariable=self.magisk_select)
        confirm_info.pack(side="left", padx=5, pady=5, fill="x")
        confirm_button = ctk.CTkButton(
            confirm_frame, text=self.langget('start patch'), fg_color="green", hover_color="dark green", command=self.start_patch
        )
        confirm_button.pack(side="right", anchor="e", padx=5, pady=5)

        confirm_frame.pack(side="top", fill="x", padx=5, pady=5)

        progress_frame = ctk.CTkFrame(self, corner_radius=0)
        self.progress_label = ctk.CTkLabel(progress_frame, text=self.langget('progress')+":")
        #progress_bar = ctk.CTkProgressBar(progress_frame, variable=self.progress)
        #progress_bar._determinate_value = 100
        progress_bar = Progressbar(progress_frame, variable=self.progress, maximum=100)

        self.progress_label.pack(side='left', padx=5)
        progress_bar.pack(side='left', expand='yes', padx=5, fill='x')


        progress_process = ctk.CTkLabel(progress_frame, textvariable=self.progress, width=25, anchor='e')
        progress_process.pack(side='left', padx=5)
        ctk.CTkLabel(progress_frame, text="%").pack(side='left', padx=(0, 5))

        progress_frame.grid(row=1, column=1, sticky='ew')

        # keep_verity_checkbox = ctk.CTkCheckBox(self.patcher)

        self.textbox = ctk.CTkTextbox(self.patcher_frame, border_width=0, corner_radius=20, font=ctk.CTkFont("console"))
        self.textbox.pack(side='top', fill='both', padx=5, pady=5, expand='yes')

        textbox_clear_button = ctk.CTkButton(confirm_frame, text=self.langget('clean'), command=lambda: self.textbox.delete(1.0, 'end'))
        textbox_clear_button.pack(side='right', padx=5, pady=5)

        # Download Frame
        self.download_list_frame = ctk.CTkScrollableFrame(self.download_frame, corner_radius=5, label_text=self.langget('available magisk list'))
        download_config_frame = ctk.CTkFrame(self.download_frame, corner_radius=5)

        download_setting_label = ctk.CTkButton(download_config_frame, state='disable', text=self.langget('settints'), fg_color=('grey78', 'grey23'), text_color=('black', 'grey85'), width=200)
        download_setting_label.pack(side='top', fill='x', padx=5, pady=5)

        download_proxy_frame = ctk.CTkFrame(download_config_frame)
        download_proxy_checkbox = ctk.CTkSwitch(download_proxy_frame, text=self.langget('use proxy'), variable=self.isproxy)
        download_proxy_checkbox.pack(side='top', fill='x', anchor='w', padx=5, pady=5)
        # bind if proxy is not allow, then forget proxy url label
        download_proxy_checkbox.bind("<Button-1>", self.update_proxy_widgets)

        self.download_proxy_url = ctk.CTkEntry(download_proxy_frame, textvariable=self.proxy)
        #self.download_proxy_url.pack(side='top', fill='x', anchor='w', padx=5, pady=5)

        download_proxy_frame.pack(side='top', fill='x', padx=5, pady=5, expand='no')
        
        
        # mirror source list
        download_mirror_frame = ctk.CTkFrame(download_config_frame)
        download_mirror_checkbox = ctk.CTkSwitch(download_mirror_frame, text=self.langget('github mirror'), variable=self.ismirror)
        download_mirror_checkbox.pack(side='top', fill='x', padx=5, pady=5, expand='no')
        download_mirror_checkbox.bind("<Button-1>", self.update_mirror_widgets)

        self.download_mirror_label = ctk.CTkEntry(download_mirror_frame, placeholder_text=self.langget('input your git mirror here'))

        download_mirror_frame.pack(side='top', fill='x', padx=5, pady=5, expand='no')

        # jsdelivr
        downlaod_jsdelivr = ctk.CTkSwitch(download_config_frame, text=self.langget('use jsdelivr'), variable=self.isjsdelivr)
        downlaod_jsdelivr.pack(side='top', padx=10, pady=5, fill='x')

        download_config_local_frame = ctk.CTkFrame(download_config_frame)
        download_use_local_checkbox = ctk.CTkSwitch(download_config_local_frame, text=self.langget('use native file'), variable=self.uselocal)
        download_use_local_checkbox.bind("<Button-1>", self.update_local_widgets)
        download_use_local_checkbox.pack(side='top', padx=5, pady=5, fill='x')

        # delta switch
        self.download_delta_magisk = ctk.CTkSwitch(download_config_local_frame, text=self.langget('use delta magisk'), variable=self.usedeltamagisk)
        download_config_local_frame.pack(side='top', fill='x', padx=5, pady=5)

        download_refresh_button = ctk.CTkButton(download_config_frame, text=self.langget('refresh list'), command=self.refresh_magisk)
        download_refresh_button.pack(side='bottom', fill='x', padx=10, pady=5)

        download_config_frame.pack(side='left', fill='both', padx=5, pady=5, expand='no')
        self.download_list_frame.pack(side='left', fill='both', padx=5, pady=5, expand='yes')

        # other frame
        other_frame = ctk.CTkFrame(self.other_frame)
        other_introduce_label = ctk.CTkButton(other_frame, state='disable', text=self.langget('introduce'), fg_color=('grey78', 'grey23'), text_color=('black', 'grey85'))
        other_introduce_label.pack(side='top', padx=5, pady=5, fill='x')
        other_introduce_logo = ctk.CTkLabel(other_frame, text="        Magisk Patcher", font=ctk.CTkFont(size=30, weight='bold'), image=ctk.CTkImage(Image.open(BytesIO(logodata)), size=(240,100)), compound='left', anchor='sw')
        other_introduce_logo.pack(side='top', fill='x', anchor='w')
        other_introduce_full = ctk.CTkTextbox(other_frame, font=ctk.CTkFont("console"), height=160)
        other_introduce_full.insert('end', INTRODUCE)
        other_introduce_full.configure(state='disable')
        other_introduce_full.pack(side='top', padx=5, pady=5, fill='both', anchor='w', expand='yes')
        #other_introduce_longlabel = ctk.CTkLabel()
        other_button_frame = ctk.CTkFrame(other_frame)
        other_visit_button = ctk.CTkButton(other_button_frame, text=self.langget('vist github'), command=lambda: webbrowser.open("https://github.com/affggh/magisk_patcher"))
        other_visit_button.grid(column=0, row=0, padx=5, pady=5)

        loglevel_label = ctk.CTkLabel(other_button_frame, text=self.langget('log level'))
        loglevel_label.grid(column=1, row=0, padx=5, pady=5)

        loglevel_slide_bar = ctk.CTkSlider(other_button_frame, from_=logging.DEBUG, to=logging.CRITICAL, number_of_steps=4, variable=self.loglevel, command=self.set_log_level)
        loglevel_slide_bar.grid(column=2, row=0, padx=5, pady=5)
        loglevel_slide_bar.set(logging.WARN) # Default loglevel
        ctk.CTkLabel(other_button_frame, textvariable=self.loglevel).grid(column=3, row=0, padx=5, pady=5)

        ctk.CTkLabel(other_button_frame, text=self.langget('scaling')+":").grid(column=4, row=0, padx=(5,0), pady=5)
        scaling_bar = ctk.CTkOptionMenu(other_button_frame, values=["0.75", "0.8", "1.0", "1.25", "1.5", "2"], command=self.ui_scaling_event)
        scaling_bar.set("1.0")
        scaling_bar.grid(column=5, row=0, padx=5, pady=5)
        other_button_frame.pack(side='top', padx=5, pady=5, fill='x', expand='no')

        other_frame.pack(side='top', padx=5, pady=5, fill='both', expand='yes')

        self._change_frame_byname("patcher")

    def start_patch(self):
        if not op.isfile(self.bootimg.get()):
            print(self.langget('please select a exist boot image'), file=self)
            return
        
        if not op.isfile(op.join("prebuilt", self.magisk_select_int.get())):
            print(self.langget('please select a valid magisk apk'), file=self)
            return

        magisk_version = utils.getMagiskApkVersion(op.join("prebuilt", self.magisk_select_int.get()))
        print(f"{self.langget('detect select magisk version is')} [{str(utils.convertVercode2Ver(magisk_version))}]", file=self)

        utils.parseMagiskApk(op.join("prebuilt", self.magisk_select_int.get()), arch=self.arch.get(), log=self)

        patcher = boot_patch.BootPatcher(prebuilt_magiskboot,
                                         self.keep_verity.get(),
                                         self.keep_forceencrypt.get(),
                                         self.patchvbmeta_flag.get(),
                                         self.recoverymode.get(),
                                         self.legacysar.get(),
                                         self.progress,
                                         self)
        th = DummyProcess(target=patcher.patch, args=[self.bootimg.get(),])
        th.start()

    def refresh_magisk(self):
        def download(magisk: str):
            if not self.uselocal.get():
                if not op.isdir(op.join("prebuilt")):
                    makedirs("prebuilt", exist_ok=True)

                if not op.isfile(op.join("prebuilt", magisk)):
                    print(f"{self.langget('file not exist, ready to download')} [{magisk}]", file=self)
                    if not self.isjsdelivr.get() and self.ismirror.get():
                        print(self.langget('use mirror download'), file=self)
                        url = magisk_list[magisk].replace(self.mirror.get().rstrip('/'), "https://github.com")
                    else:
                        url = magisk_list[magisk]
                    utils.thdownloadFile(url, 
                                         op.join("prebuilt", magisk), 
                                         self.isproxy.get(), 
                                         self.proxy.get(), 
                                         self.progress, 
                                         self)
                else:
                    print(self.langget('file exist, no need download'), file=self)
            self.magisk_select.set(f"- {self.langget('current magisk')} [{magisk}]")
            self.change_frame_patcher()

        print(self.langget('refresh magisk list'), file=self)

        # delete widgets
        for i in self.magisk_list:
            i.destroy()
        self.magisk_list = []

        if self.uselocal.get():
            print(self.langget('use from native prebuilt dir'), file=self)
            if not op.isdir("prebuilt"):
                print(self.langget('no magisk in prebuilt, please downloadn and place'), file=self)
                print(f"\t{self.langget('work dir')}: {getcwd()}", file=self)
                makedirs("prebuilt", exist_ok=True)
                
            magisk_list = []
            
            for root, dirs, files in walk("prebuilt"):
                for file in files:
                    if ".apk" in file:
                        magisk_list.append(file)

            if magisk_list.__len__() == 0:
                print(self.langget('cannot find any apk, please download and put them into prebuilt dir'), file=self)
                self.change_frame_patcher()

            for index, current in enumerate(magisk_list):
                self.magisk_list.append(
                    ctk.CTkRadioButton(self.download_list_frame, 
                                       text=current, 
                                       command=lambda x=current: download(x),
                                       value=current, 
                                       variable=self.magisk_select_int)
                )
    
        else:
            magisk_list = utils.getReleaseList(url=utils.DEFAULT_MAGISK_API_URL if not self.usedeltamagisk.get() else utils.DELTA_MAGISK_API_URL,
                                               isproxy=self.isproxy.get(),
                                               proxyaddr=self.proxy.get(),
                                               isjsdelivr=self.isjsdelivr.get(),
                                               log=self.log)
            for index, current in enumerate(magisk_list):
                self.magisk_list.append(
                    ctk.CTkRadioButton(self.download_list_frame, 
                                       text=current, 
                                       command=lambda x=current: download(x), 
                                       value=current, 
                                       variable=self.magisk_select_int)
                )

        # place all widgets
        for i in self.magisk_list:
            i.pack(side='top', fill='x', anchor='w', padx=10, pady=5)

    def change_theme(self, theme: str):
        ctk.set_appearance_mode(theme)

    def file_choose_dialog(self):
        fname = ctk.filedialog.askopenfilename(title=self.langget('select a boot image'), initialdir=getcwd())
        self.bootimg.set(fname)
    
    def set_progress(self, value: int):
        self.progress.set("%d" %value/100)
        self.progress.trace_variable

    def set_log_level(self, value):
        self.log.setLevel(int(value))

    def update_local_widgets(self, event):
        if not self.uselocal.get():
            self.download_delta_magisk.pack(side='top', fill='x', anchor='w', padx=5, pady=5)
        else:
            self.download_delta_magisk.pack_forget()

    def update_proxy_widgets(self, event):
        if self.isproxy.get():
            self.download_proxy_url.pack(side='top', fill='x', anchor='w', padx=5, pady=5)
        else:
            self.download_proxy_url.pack_forget()

    def update_mirror_widgets(self, event):
        if self.ismirror.get():
            self.download_mirror_label.pack(side='top', fill='x', anchor='w', padx=5, pady=5)
        else:
            self.download_mirror_label.pack_forget()

    def _change_frame_byname(self, name: str):
        self.patcher_frame_button.configure(
            fg_color=("gray75", "gray25") if name == "patcher" else "transparent"
        )
        self.download_frame_button.configure(
            fg_color=("gray75", "gray25") if name == "download" else "transparent"
        )
        self.other_frame_button.configure(
            fg_color=("gray75", "gray25") if name == "other" else "transparent"
        )

        if name == "patcher":
            self.patcher_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.patcher_frame.grid_forget()

        if name == "download":
            self.download_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.download_frame.grid_forget()

        if name == "other":
            self.other_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.other_frame.grid_forget()

    def change_frame_patcher(self):
        self._change_frame_byname("patcher")

    def change_frame_download(self):
        self._change_frame_byname("download")

    def change_frame_other(self):
        self._change_frame_byname("other")

    def ui_scaling_event(self, value):
        ctk.set_widget_scaling(float(value))
        ctk.set_window_scaling(float(value))

    def refresh_widgets(self):
        for child in self.winfo_children():
            child.destroy()
        
        Language.select = self.lang.get()
        self.lang_dict = getattr(Language, self.lang.get())
        self.magisk_select.set(self.langget('magisk is not select'))
        for i in self.magisk_list:
            i.destory()
        self.magisk_list = []
        self.__setup_widgets()

def centerWindow(parent: ctk.CTk):
    width, height = parent.winfo_screenwidth(), parent.winfo_screenheight()
    parent.geometry("+%d+%d" % ((width / 2) - (WIDTH / 2), (height / 2) - (HEIGHT / 2)))

if __name__ == "__main__":
    root = MagiskPatcherUI()
    root.title(TITLE)
    root.geometry("%dx%d" % (WIDTH, HEIGHT))

    # Fix high dpi
    if osname == 'nt':
        # Tell system using self dpi adapt
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
        # Get screen resize scale factor
        scalefactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
        root.tk.call('tk', 'scaling', scalefactor/75)

    root.update()
    centerWindow(root)
    #ctk.set_window_scaling(1.25)

    root.mainloop()
