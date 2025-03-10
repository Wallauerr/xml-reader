# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['src\\app.py'],
    pathex=[],  # Adicione o caminho do projeto, se necessário
    binaries=[],
    datas=[('src/assets/favicon-sulmag_96x96.ico', 'assets')],  # Inclui o ícone
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Gerador de etiqueta',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,  # Desativar UPX para evitar falsos positivos no antivírus
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Executar sem console
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='src/assets/favicon-sulmag_96x96.ico',  # Ícone do executável
)