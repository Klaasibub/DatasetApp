# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['D:\\Projects\\Implementation\\DatasetApp'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

exclude_binaries = [
    'MSVCP140.dll',
    'tcl86t.dll',
    'tk86t.dll',
    'MSVCP140_1.dll',
    'Qt5DBus.dll',
    'Qt5Qml.dll',
    'Qt5QmlModels.dll',
    'Qt5Quick.dll',
    'Qt5WebSockets.dll',
    'Qt5Svg.dll',
    'opengl32sw.dll',
    'VCRUNTIME140_1.dll',
    'd3dcompiler_47.dll',
    'ucrtbase.dll',
    'VCRUNTIME140.dll',
    '_tkinter',
]
for exclude in exclude_binaries:
    for item in a.binaries:
        if exclude in item:
            a.binaries.remove(item)
for item in a.datas:
    if 'nltk_data' in item[0]:
        a.datas.remove(item)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
