import os
import sipconfig
from PyQt4 import pyqtconfig

build_file = "bmain.sbf"

config = pyqtconfig.Configuration()

qt_sip_flags = config.pyqt_sip_flags

os.system(" ".join([config.sip_bin, "-c", ".", "-b", build_file, "-I", config.pyqt_sip_dir, qt_sip_flags, "bMain.sip"]))

content = {
    "bmain_sip_dir":    config.default_sip_dir,

    "bmain_sip_flags":  qt_sip_flags
}

sipconfig.create_config_module("bMainconfig.py", "bMainconfig.py.in", content)

