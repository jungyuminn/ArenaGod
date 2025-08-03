# 🎮 ArenaGod

<div align="center">
  <a href="README.md">한국어</a> | <a href="README_EN.md">English</a>

  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
  ![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
  ![PyQt](https://img.shields.io/badge/PyQt-6.0+-green.svg)
  [![GitHub issues](https://img.shields.io/github/issues/jungyuminn/ArenaGod)](https://github.com/jungyuminn/ArenaGod/issues)
</div>

<div align="center">
  <img src="docs/images/preview.png" alt="ArenaGod Preview" width="800"/>
</div>

A desktop application for managing champion statistics and victory records in League of Legends Arena Mode.

## ✨ Features

### 📊 Champion Rankings (Left)
<img src="docs/images/left_view.gif" alt="Champion Ranking Demo" width="700"/>

- Real-time Arena Mode champion rankings
- Smart search with Korean initial consonants
- Click to view detailed champion statistics
- Color-coded tiers for quick performance assessment

### 🎯 Champion Grid (Center)
<img src="docs/images/grid_winner_check.gif" alt="Grid Winner Check Demo" width="700"/>

- Left-click for detailed champion statistics
- Right-click to toggle victory status
- Victory counter at the top
- Synchronized victory status across views

#### Advanced Filtering
<img src="docs/images/grid_filter.gif" alt="Grid Filter Demo" width="700"/>

- Multiple sorting options
  - Alphabetical order
  - Victory count
  - Non-victory count
- Quick 'Non-winners only' toggle
- Combinable search, filter, and toggle options

#### Flexible Layout
<img src="docs/images/grid_expand.gif" alt="Grid Expand Demo" width="700"/>

- Responsive grid column adjustment
- Grid show/hide functionality
<img src="docs/images/grid_hide.gif" alt="Grid Hide Demo" width="700"/>

### 📝 Champion Details (Right)
<img src="docs/images/right_view.gif" alt="Champion Detail Demo" width="700"/>

- Champion Basic Information
  - Pick rate, win rate, tier data
  - Left-click to toggle victory status
- Synergy Champion Recommendations
  - Top 8 synergistic champions
  - Click to view their statistics
- Augment Recommendations
  - Silver/Gold/Prismatic tier categorization
  - Detailed augment information
- Item Build Guides
  - Starting item recommendations
  - Core item builds
  - Prismatic item options

### 🎨 User Experience

- Dark mode support
- Responsive layout
- Intuitive UI/UX
- Real-time data synchronization

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