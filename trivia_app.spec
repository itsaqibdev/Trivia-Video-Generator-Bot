# -*- mode: python ; coding: utf-8 -*-

block_cipher = pyi_crypto.PyiBlockCipher(key='YourEncryptionKey')

excluded_modules = [
    'matplotlib', 'numpy.random', 'numpy.core', 'numpy.testing', 'numpy.lib',
    'pandas', 'scipy', 'PyQt5', 'PySide2', 'wx', 'test', 'distutils',
    'IPython', 'PIL.ImageQt', 'PyQt4', 'sphinx', 'twisted', 'zope', 'h5py',
    'zmq', 'babel', 'curses', 'cvxopt', 'tornado', 'tcl', 'tk', 'docutils',
    'setuptools', 'distribute', 'pip', 'pycparser', 'sqlite3', 'email',
    '_ssl', 'unittest', 'pdb', 'difflib', 'pyreadline'
]

a = Analysis(
    ['trivia_gui.py'],
    pathex=[],
    binaries=[],
    datas=[('think.gif', '.')],
    hiddenimports=['PIL._tkinter_finder'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=excluded_modules,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Remove unnecessary binaries and data
def exclude_from_binaries(binaries, patterns):
    return [b for b in binaries if not any(pattern in b[0].lower() for pattern in patterns)]

excluded_binary_patterns = [
    'tcl8', 'tk8', '_tkinter', 'sqlite3', 'libopenblas',
    'mkl', 'libiomp5md', 'pywintypes', 'pythoncom',
    'qt5', 'qt6', 'webkit', 'webengine', 'designer',
    'qwindows', 'platforms/', 'imageformats/', 'audio/',
    'libcrypto', 'libssl', 'libffi', '_decimal', '_queue',
    '_asyncio', '_overlapped', '_ctypes', '_multiprocessing'
]

a.binaries = exclude_from_binaries(a.binaries, excluded_binary_patterns)

# Remove unnecessary data files
a.datas = [d for d in a.datas if not any(pattern in d[0].lower() 
    for pattern in ['qt5', 'qt6', 'tcl', 'tk', 'matplotlib', 'scipy'])]

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Trivia Video Generator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='ico.ico',
    version='file_version_info.txt',
    uac_admin=True,
    compress=True
)
