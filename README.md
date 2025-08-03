# 🎮 ArenaGod

<div align="center">
  <img src="docs/images/detail_view_1.png" alt="ArenaGod Preview" width="800"/>
  
  [한국어](README.md) | [English](README_EN.md)

  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
  ![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
  ![PyQt](https://img.shields.io/badge/PyQt-6.0+-green.svg)
  [![GitHub issues](https://img.shields.io/github/issues/jungyuminn/ArenaGod)](https://github.com/jungyuminn/ArenaGod/issues)
</div>

리그 오브 레전드 아레나 모드를 위한 챔피언 가이드 및 통계 추적 데스크톱 애플리케이션입니다.

## ✨ 주요 기능

### 🎯 챔피언 그리드 뷰
- 모든 챔피언을 한눈에 보기
- 승률 기반 티어 표시
- 승리한 챔피언 체크 기능
- 그리드/리스트 뷰 전환
- 챔피언 이름 검색

### 📊 챔피언 랭킹
- 승률 기반 챔피언 순위
- 티어별 분류 (1~5티어)
- 실시간 검색 필터링

### 📝 챔피언 상세 정보
- 기본 정보 및 통계
- 시너지 챔피언 추천
- 티어별 증강체 추천
  - 실버 증강체 🥈
  - 골드 증강체 🥇
  - 프리즈매틱 증강체 💎
- 아이템 빌드 가이드
  - 시작 아이템 🏃
  - 핵심 아이템 ⚔️
  - 프리즈매틱 아이템 💎

## 🖼️ 스크린샷

<details>
<summary>더 많은 스크린샷 보기</summary>

### 챔피언 상세 정보
<img src="docs/images/detail_view_2.png" alt="Champion Detail" width="600"/>

### 증강체 추천
<img src="docs/images/detail_view_3.png" alt="Augments" width="600"/>

### 아이템 빌드
<img src="docs/images/detail_view_4.png" alt="Items" width="600"/>
</details>

## 🚀 설치 및 실행

1. 저장소 클론
```bash
git clone https://github.com/jungyuminn/ArenaGod.git
cd ArenaGod
```

2. 필요한 패키지 설치
```bash
pip install -r requirements.txt
```

3. 애플리케이션 실행
```bash
python src/main.py
```

## 🔨 빌드

Windows 실행 파일 생성:
```bash
pyinstaller ArenaGod.spec
```

## 🛠️ 기술 스택

- Python 3.9+ 🐍
- PyQt6 🎨
- Qt Designer 🎯
- PyInstaller 📦

## 🤝 기여

버그 리포트나 새로운 기능 제안은 GitHub Issues를 통해 제출해주세요.

## 📄 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다.