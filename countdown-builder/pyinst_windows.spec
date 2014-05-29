# -*- mode: python -*-

gtkdir = os.path.join('C:','Python27','Lib','site-packages','gtk-2.0','runtime')
gtkrc_dir = os.path.join('share','themes','MS-Windows','gtk-2.0')
engines_dir = os.path.join('lib','gtk-2.0','2.10.0','engines')

extra_datas = [ ('gtkrc',os.path.join(gtkdir,gtkrc_dir,'gtkrc'),'DATA') ]
extra_binaries = [ (os.path.join(engines_dir,'libwimp.dll'),
                    os.path.join(gtkdir,engines_dir,'libwimp.dll'),'BINARY') ]

extra_file = [ ('countdownGUI.ui','../countdownGUI.ui','DATA') ]

a = Analysis(['../countdownGUI.py'],
             pathex=['../..'],
             hiddenimports=[],
             hookspath=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          #a.binaries + extra_binaries,
          a.binaries,
          a.zipfiles,
          #a.datas + extra_datas + extra_file,
          a.datas + extra_file,
          name=os.path.join('dist', 'countdown.exe'),
          debug=False,
          strip=None,
          upx=True,
          console=False )
app = BUNDLE(exe,
             name=os.path.join('dist', 'countdown.exe.app'))
