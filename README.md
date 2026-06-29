# 📡 RF RADAR Studio Professional

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
[![PyQt5](https://img.shields.io/badge/PyQt5-5.15+-green.svg)](https://www.riverbankcomputing.com/software/pyqt/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/psbansode90090/RF-RADAR-Studio)](https://github.com/psbansode90090/RF-RADAR-Studio/issues)
[![GitHub stars](https://img.shields.io/github/stars/psbansode90090/RF-RADAR-Studio)](https://github.com/psbansode90090/RF-RADAR-Studio/stargazers)

## 📡 Overview

**RF RADAR Studio Professional** is a professional FMCW (Frequency Modulated Continuous Wave) radar visualization and analysis tool built with Python, PyQt5, and PyQtGraph. It provides real-time radar data visualization with an intuitive dark-themed interface, designed for OPS241B radar modules.


## ✨ Features

### 🎯 Core Features
- **Real-time Radar Visualization** - Live radar view with dynamic scaling
- **Variable Detection Range** - Adjustable 0-20m detection range with 1m steps
- **Multi-Target Tracking** - Track and display multiple targets simultaneously
- **Color-Coded Targets** - Each target gets a unique color for easy identification
- **Speed Detection** - Real-time speed calculation for moving targets
- **Fixed Radar View** - No zoom/pan to maintain stable visualization

### 📊 Data Visualization
- **Live Radar View** - Interactive radar display with distance rings and sweep animation
- **Distance vs Time Graph** - Track closest target distance over time
- **Speed vs Time Graph** - Monitor target speed changes
- **Target Count Graph** - View number of detected targets over time
- **Average Distance Graph** - Track average distance of all targets
- **Motion Distribution** - Bar chart showing stationary/approaching/receding targets

### 💾 Data Logging
- **CSV Export** - Log target data (Timestamp, Target ID, Distance, Angle)
- **Screenshot Capture** - Save current view as PNG/JPEG

### 🎨 User Interface
- **Professional Dark Theme** - Eye-friendly dark gray interface
- **Responsive Design** - Optimized for all screen sizes
- **Customizable Range** - Easy range adjustment via sliders or spin boxes
- **Dropdown Menus** - COM port and baud rate selection with arrows
- **Company Logo** - Branded splash screen and toolbar

## 📋 Requirements

- Python 3.7 or higher
- Windows / Linux / macOS
- OPS241-B Radar Module (or compatible serial radar)

## 🚀 Installation

### Method 1: From Source

1. **Clone the Repository**
```bash
git clone https://github.com/psbansode90090/RF-RADAR-Studio.git
cd RF-RADAR-Studio
