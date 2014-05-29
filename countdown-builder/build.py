#!/usr/bin/env python

import os
from os.path import join
import sys
import subprocess
import shutil


env = os.environ
wineprefix = join(os.getcwd(),'wine-folder')
env['WINEPREFIX'] = wineprefix
pyinstaller = os.path.expanduser('~/pymisc/pyinstaller-2.0/pyinstaller.py')

def make_wine_tarball():
    #Install python
    python_msi = 'python-2.7.3.msi'
    subprocess.call(['wineboot','-i'],env=env)
    subprocess.call(['wget','http://www.python.org/ftp/python/2.7.3/'+python_msi])
    subprocess.call(['wine','msiexec','/i',python_msi,'/qb'],env=env)
    os.remove(python_msi)
    #Install pygtk
    pygtk_msi = 'pygtk-all-in-one-2.24.2.win32-py2.7.msi'
    subprocess.call(['wget','http://ftp.gnome.org/pub/GNOME/binaries/win32/pygtk/2.24/'+pygtk_msi])
    subprocess.call(['wine','msiexec','/i',pygtk_msi,r'TARGETDIR=C:\Python27','/qb'],env=env)
    os.remove(pygtk_msi)
    #Install pywin32
    pywin32_exe = 'pywin32-218.win32-py2.7.exe'
    subprocess.call(['wget','http://downloads.sourceforge.net/pywin32/'+pywin32_exe])
    subprocess.call(['winetricks','vcrun2008','vcrun2010'],env=env)
    subprocess.call(['wine',pywin32_exe],env=env)
    os.remove(pywin32_exe)
    #Make tarball
    subprocess.call(['tar','-czf','wine-frozen.tar.gz','wine-folder'])
    shutil.rmtree(wineprefix)


def make_windows_exe():
    if not os.path.exists('wine-frozen.tar.gz'):
        make_wine_tarball()
    #Make the exe.
    subprocess.call(['tar','-xzf','wine-frozen.tar.gz'])
    subprocess.call(['wine',r'C:\Python27\python.exe',pyinstaller,'pyinst_windows.spec'],env=env)
    shutil.rmtree(wineprefix)

if __name__=='__main__':
    make_windows_exe()
