# -*- mode: python ; coding: utf-8 -*-

import os
import sys
from PyInstaller.utils.hooks import collect_data_files

block_cipher = None

# 모든 파일을 수집할 리스트
all_files = []

# 챔피언 이미지 수집
champion_path = os.path.join('resources', 'images', 'champions')
if os.path.exists(champion_path):
    champion_files = [(os.path.join(champion_path, f), os.path.join('resources', 'images', 'champions'))
                     for f in os.listdir(champion_path) if f.endswith('.png')]
    all_files.extend(champion_files)

# 증강 이미지 수집 (티어별)
augment_tiers = ['silver', 'gold', 'prismatic']
for tier in augment_tiers:
    tier_path = os.path.join('resources', 'images', 'augments', tier)
    if os.path.exists(tier_path):
        tier_files = [(os.path.join(tier_path, f), os.path.join('resources', 'images', 'augments', tier))
                     for f in os.listdir(tier_path) if f.endswith('.png')]
        all_files.extend(tier_files)

# 아이템 이미지 수집 (타입별)
item_types = ['legendary', 'prismatic', 'boots', 'start_items']
for item_type in item_types:
    type_path = os.path.join('resources', 'images', 'items', item_type)
    if os.path.exists(type_path):
        type_files = [(os.path.join(type_path, f), os.path.join('resources', 'images', 'items', item_type))
                     for f in os.listdir(type_path) if f.endswith('.png')]
        all_files.extend(type_files)

# 스킬 이미지 수집
skills_path = os.path.join('resources', 'images', 'skills')
if os.path.exists(skills_path):
    skills_files = [(os.path.join(skills_path, f), os.path.join('resources', 'images', 'skills'))
                   for f in os.listdir(skills_path) if f.endswith('.png')]
    all_files.extend(skills_files)

# 폰트 파일 수집
font_files = [(f, 'resources/fonts') for f in [
    'resources/fonts/Pretendard-Regular.ttf',
    'resources/fonts/Pretendard-Bold.ttf',
    'resources/fonts/Pretendard-Medium.ttf',
    'resources/fonts/Pretendard-Light.ttf',
    'resources/fonts/Pretendard-ExtraLight.ttf',
    'resources/fonts/Pretendard-Thin.ttf',
    'resources/fonts/Pretendard-Black.ttf',
    'resources/fonts/Pretendard-ExtraBold.ttf',
    'resources/fonts/Pretendard-SemiBold.ttf',
]]
all_files.extend(font_files)

# 아이콘 파일 수집
icon_files = [(f, 'resources/icons') for f in [
    'resources/icons/app_icon.ico'
]]
all_files.extend(icon_files)

# data 파일 수집
data_files = [(f, 'data') for f in [
    'data/champion_records.json'
]]
all_files.extend(data_files)

a = Analysis(
    ['src/main.py'],
    pathex=[],
    binaries=[],
    datas=all_files,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='ArenaGod',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,  # UPX 압축 비활성화하여 안티바이러스 오탐 방지
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # 터미널 창 숨기기
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='.\\resources\\icons\\app_icon.ico',
    version='version.txt'  # 버전 정보 및 저작권 정보 추가
)
