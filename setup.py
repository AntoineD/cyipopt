# -*- coding: utf-8 -*-
"""
cyipopt: Python wrapper for the Ipopt optimization package, written in Cython.

Copyright (C) 2012-2015 Amit Aides
Copyright (C) 2015-2017 Matthias Kümmerer
Copyright (C) 2017-2024 cyipopt developers

License: EPL 2.0
"""

import sys
import os.path
from distutils.sysconfig import get_python_lib

from setuptools import setup
from setuptools.extension import Extension

import pkgconfig
import numpy as np



def handle_ext_modules_win_32_conda_forge_ipopt():
    conda_prefix = os.path.split(sys.executable)[0]

    IPOPT_INCLUDE_DIRS = [os.path.join(conda_prefix, "Library", "include",
                                       "coin-or"), np.get_include()]
    IPOPT_LIBS = ["ipopt-3"]
    IPOPT_LIB_DIRS = [os.path.join(conda_prefix, "Library", "lib")]
    EXT_MODULES = [Extension("ipopt_wrapper",
                             ["cyipopt/cython/ipopt_wrapper.pyx"],
                             include_dirs=IPOPT_INCLUDE_DIRS,
                             libraries=IPOPT_LIBS,
                             library_dirs=IPOPT_LIB_DIRS)]
    DATA_FILES = None
    include_package_data = True
    return EXT_MODULES, DATA_FILES, include_package_data


def handle_ext_modules_win_32_other_ipopt():
    IPOPT_INCLUDE_DIRS = [os.path.join(ipoptdir, "include", "coin-or"),
                          np.get_include()]

    # These are the specific binaries in the IPOPT 3.13.2 binary download:
    # https://github.com/coin-or/Ipopt/releases/download/releases%2F3.13.2/Ipopt-3.13.2-win64-msvs2019-md.zip
    IPOPT_LIBS = ["ipopt.dll", "ipoptamplinterface.dll"]
    IPOPT_LIB_DIRS = [os.path.join(ipoptdir, "lib")]

    bin_folder = os.path.join(ipoptdir, "bin")
    IPOPT_DLL = [file for file in os.listdir(bin_folder) if file.endswith(".dll")]
    print("Found ipopt binaries {}".format(IPOPT_DLL))
    IPOPT_DLL_DIRS = [bin_folder]
    EXT_MODULES = [Extension("ipopt_wrapper",
                             ["cyipopt/cython/ipopt_wrapper.pyx"],
                             include_dirs=IPOPT_INCLUDE_DIRS,
                             libraries=IPOPT_LIBS,
                             library_dirs=IPOPT_LIB_DIRS)]
    DATA_FILES = [(get_python_lib(),
                  [os.path.join(IPOPT_DLL_DIRS[0], dll)
                   for dll in IPOPT_DLL])] if IPOPT_DLL else None
    include_package_data = False
    return EXT_MODULES, DATA_FILES, include_package_data


def handle_ext_modules_general_os():
    ipopt_wrapper_ext = Extension("ipopt_wrapper",
                                  ["cyipopt/cython/ipopt_wrapper.pyx"],
                                  include_dirs=[np.get_include()],
                                  )
    pkgconfig.configure_extension(ipopt_wrapper_ext, 'ipopt')
    EXT_MODULES = [ipopt_wrapper_ext]
    DATA_FILES = None
    include_package_data = True
    return EXT_MODULES, DATA_FILES, include_package_data


if __name__ == "__main__":

    ipoptdir = os.environ.get("IPOPTWINDIR", "")

    # conda-forge hosts a windows version of ipopt for ipopt versions >= 3.13.
    # The location of the headers and binaries are in $CONDA_PREFIX/Library/
    # and the library binary is named "libipopt.lib". If the IPOPTWINDIR
    # environment variable is set to USECONDAFORGEIPOPT then this setup will be
    # run.
    if sys.platform == "win32" and ipoptdir == "USECONDAFORGEIPOPT":
        print('Using Conda Forge Ipopt on Windows.')
        ext_module_data = handle_ext_modules_win_32_conda_forge_ipopt()
    elif sys.platform == "win32" and ipoptdir:
        print('Using Ipopt in {} directory on Windows.'.format(ipoptdir))
        ext_module_data = handle_ext_modules_win_32_other_ipopt()
    elif sys.platform == "win32" and not ipoptdir:
        ipoptdir = os.path.abspath(os.path.dirname(__file__))
        msg = 'Using Ipopt adjacent to setup.py in {} on Windows.'
        print(msg.format(ipoptdir))
        ext_module_data = handle_ext_modules_win_32_other_ipopt()
    else:
        print('Using Ipopt found with pkg-config.')
        ext_module_data = handle_ext_modules_general_os()
    EXT_MODULES, DATA_FILES, include_package_data = ext_module_data
    # NOTE : The `name` kwarg here is the distribution name, i.e. the name that
    # PyPi uses for a collection of packages. Historically this has been
    # `ipopt`, but as of 1.1.0 is `cyipopt`. `pip install cyipopt` will install
    # the `cyipopt` and `ipopt` packages into the `site-packages` directory.
    # Both `import cyipopt` and `import ipopt` will work, with the later giving
    # a deprecation warning.
    setup(
          include_package_data=include_package_data,
          data_files=DATA_FILES,
          ext_modules=EXT_MODULES,
          )
