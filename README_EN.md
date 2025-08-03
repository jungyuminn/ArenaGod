# 🎮 ArenaGod

<div align="center">
  <img src="docs/images/detail_view_1.png" alt="ArenaGod Preview" width="800"/>
  
  [한국어](README.md) | [English](README_EN.md)

  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
  ![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
  ![PyQt](https://img.shields.io/badge/PyQt-6.0+-green.svg)
  [![GitHub issues](https://img.shields.io/github/issues/jungyuminn/ArenaGod)](https://github.com/jungyuminn/ArenaGod/issues)
</div>

A desktop application for League of Legends Arena Mode champion guides and statistics tracking.

## ✨ Features

### 🎯 Champion Grid View
- View all champions at a glance
- Tier indicators based on win rates
- Track your champion victories
- Toggle between grid/list views
- Champion name search

### 📊 Champion Rankings
- Champion rankings based on win rates
- Tier classification (Tier 1-5)
- Real-time search filtering

### 📝 Champion Details
- Basic information and statistics
- Synergy champion recommendations
- Tier-based augment recommendations
  - Silver augments 🥈
  - Gold augments 🥇
  - Prismatic augments 💎
- Item build guides
  - Starting items 🏃
  - Core items ⚔️
  - Prismatic items 💎

## 🖼️ Screenshots

<details>
<summary>View more screenshots</summary>

### Champion Details
<img src="docs/images/detail_view_2.png" alt="Champion Detail" width="600"/>

### Augment Recommendations
<img src="docs/images/detail_view_3.png" alt="Augments" width="600"/>

### Item Builds
<img src="docs/images/detail_view_4.png" alt="Items" width="600"/>
</details>

## 🚀 Installation & Usage

1. Clone the repository
```bash
git clone https://github.com/jungyuminn/ArenaGod.git
cd ArenaGod
```

2. Install required packages
```bash
pip install -r requirements.txt
```

3. Run the application
```bash
python src/main.py
```

## 🔨 Build

Generate Windows executable:
```bash
pyinstaller ArenaGod.spec
```

## 🛠️ Tech Stack

- Python 3.9+ 🐍
- PyQt6 🎨
- Qt Designer 🎯
- PyInstaller 📦

## 🤝 Contributing

Please submit bug reports and feature suggestions through GitHub Issues.

## 📄 License

This project is licensed under the MIT License.