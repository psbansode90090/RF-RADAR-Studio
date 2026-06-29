import sys
import time
import math
import serial
import serial.tools.list_ports
import numpy as np
import csv
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QGridLayout, QLabel, QComboBox, 
                             QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, 
                             QGroupBox, QMenuBar, QMenu, QToolBar, QAction, QFrame,
                             QFileDialog, QMessageBox, QSplashScreen, QSlider,
                             QSpinBox, QSizePolicy)
from PyQt5.QtCore import QTimer, QThread, pyqtSignal, Qt, QRect
from PyQt5.QtGui import QColor, QFont, QIcon, QPen, QPixmap, QPainter, QBrush, QLinearGradient, QRadialGradient
import pyqtgraph as pg

pg.setConfigOption('background', '#1a1a1a')  
pg.setConfigOption('foreground', '#e0e0e0')

# --- STYLE SHEET (QSS) - Professional Dark Gray Theme with Arrows ---
DARK_THEME = """
QMainWindow, QWidget { 
    background-color: #1a1a1a; 
    color: #e0e0e0; 
    font-family: 'Segoe UI', Arial, sans-serif; 
}
QMenuBar, QToolBar { 
    background-color: #252525; 
    border-bottom: 1px solid #3a3a3a; 
}
QMenuBar::item:selected { 
    background-color: #3a3a3a; 
}
QMenuBar::item:pressed {
    background-color: #3a3a3a;
}
QMenu {
    background-color: #252525;
    border: 1px solid #3a3a3a;
}
QMenu::item:selected {
    background-color: #3a3a3a;
}
QGroupBox { 
    border: 1px solid #3a3a3a; 
    border-radius: 4px; 
    margin-top: 1.5ex; 
    font-size: 11px; 
    color: #a0a0a0; 
}
QGroupBox::title { 
    subcontrol-origin: margin; 
    subcontrol-position: top left; 
    padding: 0 5px; 
}
QComboBox { 
    background-color: #2a2a2a; 
    border: 1px solid #3a3a3a; 
    border-radius: 3px; 
    padding: 4px; 
    color: #e0e0e0; 
    min-height: 20px;
}
QComboBox:hover { 
    background-color: #3a3a3a; 
}
QComboBox:focus { 
    border-color: #00E5FF; 
}
QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 20px;
    border-left: 1px solid #3a3a3a;
    background-color: #2a2a2a;
    border-top-right-radius: 3px;
    border-bottom-right-radius: 3px;
}
QComboBox::drop-down:hover {
    background-color: #3a3a3a;
}
QComboBox::down-arrow {
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid #e0e0e0;
    margin-right: 5px;
}
QComboBox QAbstractItemView {
    background-color: #2a2a2a;
    border: 1px solid #3a3a3a;
    selection-background-color: #3a3a3a;
    selection-color: #00E5FF;
    color: #e0e0e0;
}
QComboBox QAbstractItemView::item {
    padding: 4px;
}
QComboBox QAbstractItemView::item:selected {
    background-color: #3a3a3a;
    color: #00E5FF;
}
QPushButton { 
    background-color: #2a2a2a; 
    border: 1px solid #3a3a3a; 
    border-radius: 3px; 
    padding: 4px; 
    color: #e0e0e0; 
}
QPushButton:hover { 
    background-color: #3a3a3a; 
}
QPushButton:pressed { 
    background-color: #1a1a1a; 
    border-color: #00E5FF; 
}
QSlider::groove:horizontal { 
    border: 1px solid #3a3a3a; 
    height: 6px; 
    background: #2a2a2a; 
    border-radius: 3px; 
}
QSlider::handle:horizontal { 
    background: #00E5FF; 
    width: 16px; 
    margin: -5px 0; 
    border-radius: 8px; 
}
QSlider::handle:horizontal:hover { 
    background: #33FFCC; 
}
QSpinBox { 
    background-color: #2a2a2a; 
    border: 1px solid #3a3a3a; 
    border-radius: 3px; 
    padding: 4px; 
    color: #e0e0e0; 
    min-height: 20px;
}
QSpinBox:hover {
    background-color: #3a3a3a;
}
QSpinBox:focus {
    border-color: #00E5FF;
}
QSpinBox::up-button {
    subcontrol-origin: border;
    subcontrol-position: top right;
    width: 16px;
    height: 10px;
    border: none;
    background-color: #2a2a2a;
    border-top-right-radius: 3px;
}
QSpinBox::up-button:hover {
    background-color: #3a3a3a;
}
QSpinBox::up-button:pressed {
    background-color: #4a4a4a;
}
QSpinBox::up-arrow {
    image: none;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-bottom: 5px solid #e0e0e0;
    margin: 2px 4px;
}
QSpinBox::down-button {
    subcontrol-origin: border;
    subcontrol-position: bottom right;
    width: 16px;
    height: 10px;
    border: none;
    background-color: #2a2a2a;
    border-bottom-right-radius: 3px;
}
QSpinBox::down-button:hover {
    background-color: #3a3a3a;
}
QSpinBox::down-button:pressed {
    background-color: #4a4a4a;
}
QSpinBox::down-arrow {
    image: none;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 5px solid #e0e0e0;
    margin: 2px 4px;
}
QTableWidget { 
    background-color: #1a1a1a; 
    alternate-background-color: #252525; 
    color: #e0e0e0; 
    gridline-color: #3a3a3a; 
    border: 1px solid #3a3a3a; 
}
QHeaderView::section { 
    background-color: #252525; 
    color: #00E5FF; 
    border: 1px solid #3a3a3a; 
    font-weight: bold; 
    padding: 4px; 
}
QHeaderView::section:hover {
    background-color: #3a3a3a;
}
QScrollBar:vertical {
    background-color: #1a1a1a;
    width: 12px;
    margin: 0px;
}
QScrollBar::handle:vertical {
    background-color: #3a3a3a;
    min-height: 20px;
    border-radius: 6px;
}
QScrollBar::handle:vertical:hover {
    background-color: #4a4a4a;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}
QScrollBar:horizontal {
    background-color: #1a1a1a;
    height: 12px;
    margin: 0px;
}
QScrollBar::handle:horizontal {
    background-color: #3a3a3a;
    min-width: 20px;
    border-radius: 6px;
}
QScrollBar::handle:horizontal:hover {
    background-color: #4a4a4a;
}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px;
}
.DashBox { 
    background-color: #1e1e1e; 
    border: 1px solid #3a3a3a; 
    border-radius: 8px; 
}
.DashTitle { 
    font-size: 11px; 
    color: #a0aec0; 
    font-weight: bold; 
}
.DashValue { 
    font-size: 26px; 
    color: #00E5FF; 
    font-weight: bold; 
}
.DashValueSmall { 
    font-size: 18px; 
    color: #00E5FF; 
    font-weight: bold; 
}
.GraphGroup { 
    border: 1px solid #3a3a3a; 
    border-radius: 6px; 
    background-color: #1a1a1a; 
}
.LogoLabel { 
    background-color: transparent; 
}
QLabel {
    color: #e0e0e0;
}
"""

class LogoWidget(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(180, 90)
        self.setStyleSheet("background-color: transparent;")
        self.load_logo()
        
    def load_logo(self):
        try:
            pixmap = QPixmap("logo.png")
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(180, 90, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.setPixmap(scaled_pixmap)
            else:
                self.create_text_logo()
        except:
            self.create_text_logo()
    
    def create_text_logo(self):
        pixmap = QPixmap(180, 90)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QColor('#00E5FF'))
        font = QFont('Segoe UI', 30, QFont.Bold)
        painter.setFont(font)
        painter.drawText(0, 45, "RF")
        painter.setPen(QColor('#FFFFFF'))
        font = QFont('Segoe UI', 26, QFont.Bold)
        painter.setFont(font)
        painter.drawText(65, 45, "AAQUA")
        painter.setPen(QColor('#8899AA'))
        font = QFont('Segoe UI', 14)
        painter.setFont(font)
        painter.drawText(15, 72, "Solutions")
        painter.setPen(QPen(QColor('#00E5FF'), 1))
        painter.drawLine(15, 78, 165, 78)
        painter.setBrush(QBrush(QColor('#00E5FF'), Qt.SolidPattern))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(170, 36, 6, 6)
        painter.end()
        self.setPixmap(pixmap)

class SplashScreen(QSplashScreen):
    def __init__(self):
        splash_pixmap = QPixmap(700, 550)
        splash_pixmap.fill(QColor('#1a1a1a'))
        
        painter = QPainter(splash_pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        
        gradient = QLinearGradient(0, 0, 0, 550)
        gradient.setColorAt(0.0, QColor('#1a1a1a'))
        gradient.setColorAt(0.5, QColor('#252525'))
        gradient.setColorAt(1.0, QColor('#1a1a1a'))
        painter.fillRect(splash_pixmap.rect(), gradient)
        
        try:
            logo_pixmap = QPixmap("logo.png")
            if not logo_pixmap.isNull():
                scaled_logo = logo_pixmap.scaled(400, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                logo_x = (700 - scaled_logo.width()) // 2
                logo_y = 80
                painter.drawPixmap(logo_x, logo_y, scaled_logo)
            else:
                painter.setPen(QColor('#00E5FF'))
                font = QFont('Segoe UI', 56, QFont.Bold)
                painter.setFont(font)
                painter.drawText(QRect(0, 130, 700, 80), Qt.AlignCenter, "RF")
                painter.setPen(QColor('#FFFFFF'))
                font = QFont('Segoe UI', 46, QFont.Bold)
                painter.setFont(font)
                painter.drawText(QRect(0, 195, 700, 60), Qt.AlignCenter, "AAQUA")
                painter.setPen(QColor('#8899AA'))
                font = QFont('Segoe UI', 22)
                painter.setFont(font)
                painter.drawText(QRect(0, 250, 700, 35), Qt.AlignCenter, "Solutions")
        except:
            painter.setPen(QColor('#00E5FF'))
            font = QFont('Segoe UI', 56, QFont.Bold)
            painter.setFont(font)
            painter.drawText(QRect(0, 130, 700, 80), Qt.AlignCenter, "RF")
            painter.setPen(QColor('#FFFFFF'))
            font = QFont('Segoe UI', 46, QFont.Bold)
            painter.setFont(font)
            painter.drawText(QRect(0, 195, 700, 60), Qt.AlignCenter, "AAQUA")
            painter.setPen(QColor('#8899AA'))
            font = QFont('Segoe UI', 22)
            painter.setFont(font)
            painter.drawText(QRect(0, 250, 700, 35), Qt.AlignCenter, "Solutions")
        
        painter.setPen(QColor('#00E5FF'))
        font = QFont('Segoe UI', 26, QFont.Bold)
        painter.setFont(font)
        painter.drawText(QRect(0, 330, 700, 45), Qt.AlignCenter, "Radar Studio Pro")
        
        painter.setPen(QPen(QColor('#00E5FF'), 2))
        painter.drawLine(250, 380, 450, 380)
        
        painter.setPen(QColor('#8899AA'))
        font = QFont('Segoe UI', 13)
        painter.setFont(font)
        painter.drawText(QRect(0, 420, 700, 30), Qt.AlignCenter, "Initializing Radar System")
        
        painter.setPen(QColor('#00E5FF'))
        painter.drawText(QRect(310, 420, 80, 30), Qt.AlignLeft, "...")
        
        painter.setPen(QColor('#667788'))
        font = QFont('Segoe UI', 10)
        painter.setFont(font)
        painter.drawText(QRect(0, 510, 700, 25), Qt.AlignCenter, "Version 2.0")
        
        painter.end()
        super().__init__(splash_pixmap)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)

class SerialThread(QThread):
    data_received = pyqtSignal(list)
    def __init__(self):
        super().__init__()
        self.serial_port = None
        self.is_running = False
    def connect_radar(self, port, baudrate):
        try:
            self.serial_port = serial.Serial(port, baudrate, timeout=0.1)
            self.is_running = True
            self.start()
            return True
        except Exception as e:
            print(f"Connection Error: {e}")
            return False
    def disconnect_radar(self):
        self.is_running = False
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()
    def run(self):
        while self.is_running:
            if self.serial_port and self.serial_port.in_waiting > 0:
                try:
                    raw_line = self.serial_port.readline()
                    line = raw_line.decode('utf-8', errors='ignore').strip()
                    if line:
                        parts = line.replace(',', ' ').split()
                        distances = []
                        for p in parts:
                            try:
                                distances.append(float(p))
                            except ValueError:
                                pass 
                        if distances:
                            self.data_received.emit(distances)
                except Exception as e:
                    print(f"Read Error: {e}")
            time.sleep(0.01)

class DashboardPanel(QFrame):
    def __init__(self, title, default_val, is_small=False):
        super().__init__()
        self.setProperty("class", "DashBox")
        layout = QVBoxLayout(self)
        title_lbl = QLabel(title)
        title_lbl.setProperty("class", "DashTitle")
        title_lbl.setAlignment(Qt.AlignCenter)
        self.val_lbl = QLabel(default_val)
        self.val_lbl.setProperty("class", "DashValueSmall" if is_small else "DashValue")
        self.val_lbl.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_lbl)
        layout.addWidget(self.val_lbl)
        layout.setContentsMargins(10, 15, 10, 15)
    def update_value(self, text, color="#00E5FF"):
        self.val_lbl.setText(text)
        self.val_lbl.setStyleSheet(f"color: {color};")

class FixedPlotWidget(pg.PlotWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseEnabled(x=False, y=False)
        self.setMenuEnabled(False)
        self.setMouseTracking(False)
    def wheelEvent(self, event):
        event.ignore()
    def mousePressEvent(self, event):
        event.ignore()
    def mouseMoveEvent(self, event):
        event.ignore()
    def mouseReleaseEvent(self, event):
        event.ignore()

class RadarStudioPro(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RF RADAR Studio Professional")
        self.setGeometry(50, 50, 1600, 950)
        self.setStyleSheet(DARK_THEME)
        
        self.fov = 78 
        self.max_range = 20
        self.min_detection_range = 0.5
        self.max_detection_range = 20.0
        self.sweep_angle = -self.fov / 2
        self.sweep_direction = 1
        
        self.default_min = 0
        self.default_max = 20
        
        self.target_colors = [
            '#FF6B6B', '#FFD93D', '#6BCB77', '#4D96FF', 
            '#FF6BD6', '#00E5FF', '#FF9F43', '#A29BFE',
            '#FD79A8', '#00B894', '#E17055', '#74B9FF'
        ]
        
        self.targets = {} 
        self.target_counter = 1
        self.target_ttl = 0.5
        
        self.is_logging = False
        self.csv_file = None
        self.csv_writer = None
        
        self.graph_time_data = []
        self.graph_dist_data = []
        self.graph_speed_data = []
        self.graph_target_count_data = []
        self.graph_avg_dist_data = []
        self.start_time = time.time()
        
        self.serial_thread = SerialThread()
        self.serial_thread.data_received.connect(self.process_radar_data)
        
        self.build_graph_windows()
        self.build_menu_and_toolbar()
        self.init_ui()
        
        self.sweep_timer = QTimer()
        self.sweep_timer.timeout.connect(self.update_sweep)
        self.sweep_timer.start(33)
        
        self.graph_timer = QTimer()
        self.graph_timer.timeout.connect(self.update_graphs)
        self.graph_timer.start(100)

    def build_graph_windows(self):
        self.win_dist = pg.PlotWidget(title="Distance vs Time (Closest Target)")
        self.win_dist.setLabel('left', 'Distance', units='m')
        self.win_dist.setLabel('bottom', 'Time', units='s')
        self.win_dist.showGrid(x=True, y=True, alpha=0.3)
        self.curve_dist = self.win_dist.plot(pen=pg.mkPen('#00E5FF', width=2))
        self.win_speed = pg.PlotWidget(title="Speed vs Time (Closest Target)")
        self.win_speed.setLabel('left', 'Speed', units='m/s')
        self.win_speed.setLabel('bottom', 'Time', units='s')
        self.win_speed.showGrid(x=True, y=True, alpha=0.3)
        self.curve_speed = self.win_speed.plot(pen=pg.mkPen('#FFCC00', width=2))
        self.win_targets = pg.PlotWidget(title="Total Targets vs Time")
        self.win_targets.setLabel('left', 'Number of Targets')
        self.win_targets.setLabel('bottom', 'Time', units='s')
        self.win_targets.showGrid(x=True, y=True, alpha=0.3)
        self.curve_targets = self.win_targets.plot(pen=pg.mkPen('#FF6B6B', width=2))
        self.win_avg_dist = pg.PlotWidget(title="Average Distance vs Time")
        self.win_avg_dist.setLabel('left', 'Average Distance', units='m')
        self.win_avg_dist.setLabel('bottom', 'Time', units='s')
        self.win_avg_dist.showGrid(x=True, y=True, alpha=0.3)
        self.curve_avg_dist = self.win_avg_dist.plot(pen=pg.mkPen('#4ECDC4', width=2))
        self.win_motion = pg.PlotWidget(title="Motion Status Distribution")
        self.win_motion.setLabel('left', 'Count')
        self.win_motion.setLabel('bottom', 'Motion Type')
        self.win_motion.showGrid(x=True, y=True, alpha=0.3)
        for win in [self.win_dist, self.win_speed, self.win_targets, self.win_avg_dist, self.win_motion]:
            win.resize(600, 350)

    def build_menu_and_toolbar(self):
        menubar = self.menuBar()
        
        help_menu = menubar.addMenu("Help")
        about_act = QAction("About RF RADAR Studio", self)
        about_act.triggered.connect(self.show_about)
        doc_act = QAction("Documentation", self)
        doc_act.triggered.connect(self.show_docs)
        help_menu.addAction(about_act)
        help_menu.addAction(doc_act)
        
        graph_menu = menubar.addMenu("Graphs")
        graph_actions = [
            ("Distance vs Time", lambda: self.win_dist.show()),
            ("Speed vs Time", lambda: self.win_speed.show()),
            ("Target Count vs Time", lambda: self.win_targets.show()),
            ("Average Distance vs Time", lambda: self.win_avg_dist.show()),
            ("Motion Distribution", lambda: self.win_motion.show())
        ]
        for name, action in graph_actions:
            act = QAction(name, self)
            act.triggered.connect(action)
            graph_menu.addAction(act)
        
        tools_menu = menubar.addMenu("Tools")
        self.act_screenshot = QAction("📷 Screenshot", self)
        self.act_screenshot.triggered.connect(self.take_screenshot)
        tools_menu.addAction(self.act_screenshot)
        
        self.act_save = QAction("💾 Start CSV Save", self)
        self.act_save.triggered.connect(self.toggle_csv_logging)
        tools_menu.addAction(self.act_save)
        
        toolbar = QToolBar("Main Toolbar")
        toolbar.setMovable(False)
        toolbar.setStyleSheet("background-color: #252525; border: none;")
        self.addToolBar(toolbar)
        
        spacer_left = QWidget()
        spacer_left.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        toolbar.addWidget(spacer_left)
        
        self.logo_widget = LogoWidget()
        toolbar.addWidget(self.logo_widget)
        
        spacer_right = QWidget()
        spacer_right.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        toolbar.addWidget(spacer_right)

    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        top_layout = QHBoxLayout()
        left_panel = QWidget()
        left_panel.setFixedWidth(240)
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        
        conn_group = QGroupBox("Connection")
        conn_grid = QGridLayout(conn_group)
        
        # COM Port with dropdown arrow
        self.port_combo = QComboBox()
        self.port_combo.setMinimumHeight(25)
        self.refresh_ports()
        
        # Baud Rate with dropdown arrow
        self.baud_combo = QComboBox()
        self.baud_combo.setMinimumHeight(25)
        self.baud_combo.addItems(["9600", "19200", "38400", "57600", "115200", 
                                  "128000", "230400", "256000", "460800", 
                                  "500000", "921600", "1000000", "1500000", 
                                  "2000000", "3000000", "4000000"])
        self.baud_combo.setCurrentText("2000000") 
        
        btn_refresh = QPushButton("🔄 Refresh")
        btn_refresh.clicked.connect(self.refresh_ports)
        self.btn_connect = QPushButton("🔗 Connect")
        self.btn_connect.clicked.connect(self.toggle_connection)
        self.btn_disconnect = QPushButton("🔌 Disconnect")
        self.btn_disconnect.setEnabled(False)
        self.btn_disconnect.clicked.connect(self.toggle_connection)
        
        conn_grid.addWidget(QLabel("COM Port"), 0, 0)
        conn_grid.addWidget(self.port_combo, 0, 1, 1, 2)
        conn_grid.addWidget(QLabel("Baud Rate"), 1, 0)
        conn_grid.addWidget(self.baud_combo, 1, 1, 1, 2)
        conn_grid.addWidget(btn_refresh, 2, 0)
        conn_grid.addWidget(self.btn_connect, 2, 1)
        conn_grid.addWidget(self.btn_disconnect, 3, 0, 1, 3)
        left_layout.addWidget(conn_group)

        range_group = QGroupBox("Detection Range")
        range_layout = QVBoxLayout(range_group)
        
        # Min Range with SpinBox having up/down arrows
        min_range_layout = QHBoxLayout()
        min_range_layout.addWidget(QLabel("Min:"))
        self.min_range_slider = QSlider(Qt.Horizontal)
        self.min_range_slider.setMinimum(0)
        self.min_range_slider.setMaximum(20)
        self.min_range_slider.setValue(0)
        self.min_range_slider.valueChanged.connect(self.update_range)
        
        self.min_range_spin = QSpinBox()
        self.min_range_spin.setMinimumHeight(25)
        self.min_range_spin.setRange(0, 20)
        self.min_range_spin.setValue(0)
        self.min_range_spin.setButtonSymbols(QSpinBox.UpDownArrows)
        self.min_range_spin.valueChanged.connect(self.update_range_spin)
        
        min_range_layout.addWidget(self.min_range_slider)
        min_range_layout.addWidget(self.min_range_spin)
        range_layout.addLayout(min_range_layout)
        
        # Max Range with SpinBox having up/down arrows
        max_range_layout = QHBoxLayout()
        max_range_layout.addWidget(QLabel("Max:"))
        self.max_range_slider = QSlider(Qt.Horizontal)
        self.max_range_slider.setMinimum(1)
        self.max_range_slider.setMaximum(20)
        self.max_range_slider.setValue(20)
        self.max_range_slider.valueChanged.connect(self.update_range)
        
        self.max_range_spin = QSpinBox()
        self.max_range_spin.setMinimumHeight(25)
        self.max_range_spin.setRange(1, 20)
        self.max_range_spin.setValue(20)
        self.max_range_spin.setButtonSymbols(QSpinBox.UpDownArrows)
        self.max_range_spin.valueChanged.connect(self.update_range_spin)
        
        max_range_layout.addWidget(self.max_range_slider)
        max_range_layout.addWidget(self.max_range_spin)
        range_layout.addLayout(max_range_layout)
        
        restore_btn = QPushButton("↺ Restore Default Range (0-20m)")
        restore_btn.clicked.connect(self.restore_default_range)
        restore_btn.setStyleSheet("background-color: #2a2a2a; border-color: #00E5FF;")
        range_layout.addWidget(restore_btn)
        
        self.range_info = QLabel("Range: 0m - 20m")
        self.range_info.setAlignment(Qt.AlignCenter)
        self.range_info.setStyleSheet("color: #00E5FF; font-weight: bold;")
        range_layout.addWidget(self.range_info)
        left_layout.addWidget(range_group)

        dev_group = QGroupBox("Device")
        dev_grid = QGridLayout(dev_group)
        dev_grid.addWidget(QLabel("Model"), 0, 0)
        dev_grid.addWidget(QLabel("OPS241-B"), 0, 1)
        dev_grid.addWidget(QLabel("FOV"), 1, 0)
        dev_grid.addWidget(QLabel(f"{self.fov}°"), 1, 1)
        dev_grid.addWidget(QLabel("Max Range"), 2, 0)
        dev_grid.addWidget(QLabel(f"{self.max_range}m"), 2, 1)
        left_layout.addWidget(dev_group)

        status_group = QGroupBox("Status")
        stat_layout = QVBoxLayout(status_group)
        self.status_led = QLabel("🔴 Disconnected")
        self.status_led.setStyleSheet("font-weight: bold;")
        stat_layout.addWidget(self.status_led)
        self.ping_count = QLabel("Pings: 0")
        stat_layout.addWidget(self.ping_count)
        left_layout.addWidget(status_group)
        left_layout.addStretch()
        top_layout.addWidget(left_panel)

        radar_container = QVBoxLayout()
        radar_container.addWidget(QLabel("📡 LIVE RADAR VIEW"))
        self.radar_plot = FixedPlotWidget()
        self.radar_plot.setAspectLocked()
        self.radar_plot.setXRange(-15, 15)
        self.radar_plot.setYRange(0, 22)
        self.radar_plot.hideAxis('bottom')
        self.radar_plot.hideAxis('left')
        
        self.update_radar_grid()
        self.scatter = pg.ScatterPlotItem(size=15, pen=pg.mkPen('w'), brush=pg.mkBrush('r'))
        self.radar_plot.addItem(self.scatter)
        self.target_labels = []
        self.sweep_lines = []
        for i in range(8): 
            alpha = int(255 * (1.0 - (i / 8.0)))
            width = max(1, 4 - (i * 0.5))
            line = self.radar_plot.plot([0, 0], [0, 0], pen=pg.mkPen(color=(0, 255, 100, alpha), width=width))
            self.sweep_lines.append(line)
        radar_container.addWidget(self.radar_plot)
        top_layout.addLayout(radar_container, stretch=1)

        right_panel = QWidget()
        right_panel.setFixedWidth(250)
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.addWidget(QLabel("📊 LIVE STATISTICS"))
        self.dash_dist = DashboardPanel("CLOSEST TARGET DISTANCE", "-- m")
        self.dash_speed = DashboardPanel("CLOSEST TARGET SPEED", "-- m/s")
        self.dash_targets = DashboardPanel("TOTAL TARGETS", "0", is_small=True)
        self.dash_avg_dist = DashboardPanel("AVERAGE DISTANCE", "-- m", is_small=True)
        self.dash_motion = DashboardPanel("MOVING TARGETS", "0", is_small=True)
        right_layout.addWidget(self.dash_dist)
        right_layout.addWidget(self.dash_speed)
        right_layout.addWidget(self.dash_targets)
        right_layout.addWidget(self.dash_avg_dist)
        right_layout.addWidget(self.dash_motion)
        right_layout.addStretch()
        top_layout.addWidget(right_panel)
        main_layout.addLayout(top_layout, stretch=3)

        main_layout.addWidget(QLabel("<center><b>📋 LIVE DETECTION TABLE</b></center>"))
        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["Target ID", "Distance (m)", "Speed (m/s)", 
                                             "Motion", "Angle (°)"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setFixedHeight(180)
        main_layout.addWidget(self.table)
        self.ping_counter = 0

    def get_range_rings(self, max_range):
        if max_range == 20:
            return [0, 2, 5, 10, 15, 20]
        elif max_range <= 2:
            rings = []
            r = 0.5
            while r <= max_range:
                rings.append(r)
                r += 0.5
            return rings
        elif max_range <= 5:
            return list(range(1, int(max_range) + 1))
        elif max_range <= 10:
            return list(range(1, int(max_range) + 1))
        elif max_range <= 15:
            return list(range(0, int(max_range) + 1, 2))
        else:
            return list(range(0, int(max_range) + 1, 5))

    def update_radar_grid(self):
        items_to_remove = []
        for item in self.radar_plot.items():
            if isinstance(item, pg.PlotDataItem) and item not in self.sweep_lines and item != self.scatter:
                items_to_remove.append(item)
        for item in items_to_remove:
            self.radar_plot.removeItem(item)
        
        for item in self.radar_plot.items():
            if isinstance(item, pg.TextItem):
                if item not in self.target_labels:
                    self.radar_plot.removeItem(item)
        
        current_max_range = self.max_detection_range
        display_range = current_max_range * 1.08
        x_limit = display_range * math.sin(math.radians(self.fov / 2))
        y_limit = display_range + 1
        self.radar_plot.setXRange(-x_limit, x_limit)
        self.radar_plot.setYRange(0, y_limit)
        
        angle_rad = math.radians(self.fov / 2)
        x_edge = display_range * math.sin(angle_rad)
        y_edge = display_range * math.cos(angle_rad)
        self.radar_plot.plot([0, -x_edge], [0, y_edge], pen=pg.mkPen('#0088ff', width=2))
        self.radar_plot.plot([0, x_edge], [0, y_edge], pen=pg.mkPen('#0088ff', width=2))
        
        ring_values = self.get_range_rings(current_max_range)
        for r in ring_values:
            if r == 0:
                continue
            if r > display_range:
                break
            arc_x, arc_y = [], []
            for a in np.linspace(-self.fov/2, self.fov/2, 50):
                arc_x.append(r * math.sin(math.radians(a)))
                arc_y.append(r * math.cos(math.radians(a)))
            if self.min_detection_range <= r <= self.max_detection_range:
                pen_color = (0, 255, 100, 150)
            else:
                pen_color = (30, 80, 40, 100)
            self.radar_plot.plot(arc_x, arc_y, pen=pg.mkPen(color=pen_color, width=1))
            
            label_angle = self.fov / 2 - 5
            label_x = r * math.sin(math.radians(label_angle))
            label_y = r * math.cos(math.radians(label_angle))
            lbl = pg.TextItem(text=f"{r}m", color=(100, 180, 100), anchor=(0, 0.5))
            lbl.setPos(label_x + 0.3, label_y)
            self.radar_plot.addItem(lbl)
        
        if self.min_detection_range > 0:
            arc_x, arc_y = [], []
            for a in np.linspace(-self.fov/2, self.fov/2, 50):
                arc_x.append(self.min_detection_range * math.sin(math.radians(a)))
                arc_y.append(self.min_detection_range * math.cos(math.radians(a)))
            self.radar_plot.plot(arc_x, arc_y, pen=pg.mkPen(color=(255, 200, 0, 150), width=2, style=Qt.DashLine))

    def restore_default_range(self):
        self.min_range_slider.setValue(0)
        self.max_range_slider.setValue(20)
        self.min_range_spin.setValue(0)
        self.max_range_spin.setValue(20)
        self.min_detection_range = 0
        self.max_detection_range = 20.0
        self.range_info.setText("Range: 0m - 20m")
        self.update_radar_grid()

    def update_range(self):
        min_val = self.min_range_slider.value()
        max_val = self.max_range_slider.value()
        if min_val >= max_val:
            min_val = max_val - 1
            self.min_range_slider.setValue(min_val)
            self.min_range_spin.setValue(min_val)
        self.min_detection_range = float(min_val)
        self.max_detection_range = float(max_val)
        self.range_info.setText(f"Range: {min_val}m - {max_val}m")
        self.update_radar_grid()
        
    def update_range_spin(self):
        # Determine which spin box triggered the change
        sender = self.sender()
        if sender == self.min_range_spin:
            min_val = self.min_range_spin.value()
            max_val = self.max_range_slider.value()
            if min_val >= max_val:
                min_val = max_val - 1
                self.min_range_spin.setValue(min_val)
            self.min_range_slider.setValue(min_val)
            self.min_detection_range = float(min_val)
        elif sender == self.max_range_spin:
            max_val = self.max_range_spin.value()
            min_val = self.min_range_slider.value()
            if min_val >= max_val:
                max_val = min_val + 1
                self.max_range_spin.setValue(max_val)
            self.max_range_slider.setValue(max_val)
            self.max_detection_range = float(max_val)
        
        self.range_info.setText(f"Range: {self.min_range_slider.value()}m - {self.max_range_slider.value()}m")
        self.update_radar_grid()

    def get_target_color(self, target_id):
        try:
            num = int(target_id[1:])
            color_index = (num - 1) % len(self.target_colors)
            return self.target_colors[color_index]
        except:
            return self.target_colors[0]

    def get_motion_status(self, speed):
        if abs(speed) <= 0.3:
            return "Stationary"
        elif speed > 0.3:
            return "Receding ↗"
        elif speed < -0.3:
            return "Approaching ↙"
        return "Stationary"

    def take_screenshot(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Screenshot", "Radar_Screenshot.png", 
                                                   "PNG Files (*.png);;JPEG Files (*.jpg)", options=options)
        if file_path:
            pixmap = self.grab()
            pixmap.save(file_path)
            QMessageBox.information(self, "Success", f"Screenshot saved to:\n{file_path}")

    def toggle_csv_logging(self):
        if not self.is_logging:
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getSaveFileName(self, "Save CSV Data", "Radar_Data_Log.csv", 
                                                       "CSV Files (*.csv)", options=options)
            if file_path:
                try:
                    self.csv_file = open(file_path, mode='w', newline='')
                    self.csv_writer = csv.writer(self.csv_file)
                    self.csv_writer.writerow(["Timestamp", "Target_ID", "Distance_m", "Angle_deg"])
                    self.csv_file.flush()
                    self.is_logging = True
                    self.act_save.setText("⏹ Stop CSV Save")
                    QMessageBox.information(self, "Logging Started", f"Writing data to:\n{file_path}")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Could not create file: {e}")
        else:
            self.is_logging = False
            if self.csv_file:
                self.csv_file.close()
            self.act_save.setText("💾 Start CSV Save")
            QMessageBox.information(self, "Logging Stopped", "Data logging stopped.")

    def show_about(self):
        QMessageBox.about(self, "About", 
                         "<b>RFAAQUA Solutions - Radar Studio Pro</b><br><br>"
                         "Version 2.0<br>"
                         "Professional FMCW Radar GUI for OPS241B<br>"
                         "Built with PyQt5 and PyQtGraph<br><br>"
                         "© 2024 RFAAQUA Solutions")

    def show_docs(self):
        QMessageBox.information(self, "Documentation", 
                               "<b>How to use:</b><br><br>"
                               "1. Select COM Port<br>"
                               "2. Select Baud Rate<br>"
                               "3. Click Connect<br>"
                               "4. Adjust detection range using sliders or spin boxes<br>"
                               "5. Radar view automatically scales<br>"
                               "6. Click 'Restore Default Range' to reset<br>"
                               "7. Use 'Graphs' menu for analysis<br>"
                               "8. Use 'Tools' menu for Screenshot and CSV")

    def refresh_ports(self):
        self.port_combo.clear()
        for port in serial.tools.list_ports.comports():
            self.port_combo.addItem(port.device)

    def toggle_connection(self):
        if not self.serial_thread.is_running:
            port = self.port_combo.currentText()
            baud = int(self.baud_combo.currentText())
            if self.serial_thread.connect_radar(port, baud):
                self.btn_connect.setEnabled(False)
                self.btn_disconnect.setEnabled(True)
                self.status_led.setText("🟢 Connected")
                self.status_led.setStyleSheet("color: #00FF00; font-weight: bold;")
                self.start_time = time.time()
                self.ping_counter = 0
        else:
            self.serial_thread.disconnect_radar()
            self.btn_connect.setEnabled(True)
            self.btn_disconnect.setEnabled(False)
            self.status_led.setText("🔴 Disconnected")
            self.status_led.setStyleSheet("color: #FF0000; font-weight: bold;")
            if self.is_logging and self.csv_file:
                self.csv_file.close()
                self.is_logging = False
                self.act_save.setText("💾 Start CSV Save")

    def update_sweep(self):
        self.sweep_angle += self.sweep_direction * 1.5
        if self.sweep_angle >= self.fov / 2: self.sweep_direction = -1
        elif self.sweep_angle <= -self.fov / 2: self.sweep_direction = 1
        for i, line in enumerate(self.sweep_lines):
            offset = (i * 0.8) * -self.sweep_direction
            angle = self.sweep_angle + offset
            if angle > self.fov/2: angle = self.fov/2
            if angle < -self.fov/2: angle = -self.fov/2
            x = self.max_detection_range * math.sin(math.radians(angle))
            y = self.max_detection_range * math.cos(math.radians(angle))
            line.setData([0, x], [0, y])

    def process_radar_data(self, current_distances):
        current_time = time.time()
        self.ping_counter += 1
        self.ping_count.setText(f"Pings: {self.ping_counter}")
        filtered_distances = [d for d in current_distances 
                            if self.min_detection_range <= d <= self.max_detection_range]
        for dist in filtered_distances:
            matched_tid = None
            min_diff = 2.0 
            for tid, tdata in self.targets.items():
                diff = abs(dist - tdata['dist'])
                if diff < min_diff:
                    matched_tid = tid
                    min_diff = diff
            if matched_tid:
                dt = current_time - self.targets[matched_tid]['last_seen']
                if dt > 0.05:
                    speed = (dist - self.targets[matched_tid]['dist']) / dt
                    if abs(speed) > 10:
                        speed = self.targets[matched_tid]['speed']
                else:
                    speed = self.targets[matched_tid]['speed']
                self.targets[matched_tid]['dist'] = dist
                self.targets[matched_tid]['speed'] = speed
                self.targets[matched_tid]['last_seen'] = current_time
            else:
                offset_angle = (len(self.targets) % 3 - 1) * 15 + np.random.uniform(-5, 5)
                new_tid = f"T{self.target_counter}"
                self.target_counter += 1
                self.targets[new_tid] = {
                    'dist': dist, 
                    'speed': 0, 
                    'last_seen': current_time, 
                    'angle': offset_angle
                }
        stale_tids = [tid for tid, tdata in self.targets.items() if (current_time - tdata['last_seen']) > self.target_ttl]
        for tid in stale_tids:
            del self.targets[tid]
        self.update_ui()

    def update_ui(self):
        self.table.setRowCount(0)
        for txt in self.target_labels:
            self.radar_plot.removeItem(txt)
        self.target_labels.clear()
        primary_dist, primary_speed = None, None
        timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        x_points = []
        y_points = []
        colors = []
        sizes = []
        total_dist = 0
        moving_count = 0
        sorted_targets = sorted(self.targets.items(), key=lambda x: x[1]['dist'])
        
        if self.is_logging and self.csv_writer:
            for tid, data in sorted_targets:
                self.csv_writer.writerow([timestamp_str, tid, f"{data['dist']:.2f}", f"{data['angle']:.1f}"])
            self.csv_file.flush()
        
        for row, (tid, data) in enumerate(sorted_targets):
            color = self.get_target_color(tid)
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(tid))
            self.table.setItem(row, 1, QTableWidgetItem(f"{data['dist']:.2f}"))
            
            speed = data['speed']
            self.table.setItem(row, 2, QTableWidgetItem(f"{abs(speed):.2f}"))
            
            status = self.get_motion_status(speed)
            if abs(speed) > 0.3: 
                moving_count += 1
            self.table.setItem(row, 3, QTableWidgetItem(status))
            self.table.setItem(row, 4, QTableWidgetItem(f"{data['angle']:.1f}°"))
            
            angle_rad = math.radians(data['angle'])
            x = data['dist'] * math.sin(angle_rad)
            y = data['dist'] * math.cos(angle_rad)
            x_points.append(x)
            y_points.append(y)
            colors.append(color)
            sizes.append(18 if status != "Stationary" else 14)
            total_dist += data['dist']
            txt = pg.TextItem(html=f'<div style="color: {color}; font-size: 11pt; font-weight: bold;">{tid}</div>')
            txt.setPos(x + 0.5, y + 0.5)
            self.radar_plot.addItem(txt)
            self.target_labels.append(txt)
            if row == 0: 
                primary_dist = data['dist']
                primary_speed = speed
        if x_points:
            self.scatter.setData(x=x_points, y=y_points, 
                               brush=[pg.mkBrush(c) for c in colors],
                               size=sizes if sizes else 15)
        else:
            self.scatter.setData([], [])
        avg_dist = total_dist / len(self.targets) if self.targets else 0
        self.dash_targets.update_value(str(len(self.targets)), "#00E5FF")
        self.dash_avg_dist.update_value(f"{avg_dist:.2f} m", "#4ECDC4")
        self.dash_motion.update_value(str(moving_count), "#FF6B6B")
        if primary_dist is not None:
            self.dash_dist.update_value(f"{primary_dist:.2f} m")
            self.dash_speed.update_value(f"{abs(primary_speed):.2f} m/s")
            elapsed_time = time.time() - self.start_time
            self.graph_time_data.append(elapsed_time)
            self.graph_dist_data.append(primary_dist)
            self.graph_speed_data.append(abs(primary_speed))
            self.graph_target_count_data.append(len(self.targets))
            self.graph_avg_dist_data.append(avg_dist)
            max_points = 200
            for data_list in [self.graph_time_data, self.graph_dist_data, self.graph_speed_data,
                            self.graph_target_count_data, self.graph_avg_dist_data]:
                if len(data_list) > max_points:
                    data_list.pop(0)
        else:
            self.dash_dist.update_value("-- m")
            self.dash_speed.update_value("-- m/s")

    def update_graphs(self):
        if len(self.graph_time_data) > 1:
            self.curve_dist.setData(self.graph_time_data, self.graph_dist_data)
            self.curve_speed.setData(self.graph_time_data, self.graph_speed_data)
            self.curve_targets.setData(self.graph_time_data, self.graph_target_count_data)
            self.curve_avg_dist.setData(self.graph_time_data, self.graph_avg_dist_data)
            if len(self.targets) > 0:
                stationary = sum(1 for t in self.targets.values() if abs(t['speed']) <= 0.3)
                approaching = sum(1 for t in self.targets.values() if t['speed'] < -0.3)
                receding = sum(1 for t in self.targets.values() if t['speed'] > 0.3)
                self.win_motion.clear()
                if stationary > 0 or approaching > 0 or receding > 0:
                    x_pos = [0, 1, 2]
                    heights = [stationary, approaching, receding]
                    colors = ['#4ECDC4', '#FF6B6B', '#FFD93D']
                    for i, (pos, height, color) in enumerate(zip(x_pos, heights, colors)):
                        if height > 0:
                            bar = pg.BarGraphItem(x=[pos], height=[height], width=0.8, 
                                                 brush=pg.mkBrush(color), pen=None)
                            self.win_motion.addItem(bar)
                            txt = pg.TextItem(text=f"{int(height)}", color='white', anchor=(0.5, 0))
                            txt.setPos(pos, height)
                            self.win_motion.addItem(txt)
                    self.win_motion.setXRange(-0.5, 2.5)
                    self.win_motion.setYRange(0, max(heights) + 1 if max(heights) > 0 else 1)
                    self.win_motion.getAxis('bottom').setTicks([[(0, 'Stat'), (1, 'App'), (2, 'Rec')]])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    splash = SplashScreen()
    splash.show()
    app.processEvents()
    time.sleep(3)
    window = RadarStudioPro()
    window.show()
    splash.finish(window)
    sys.exit(app.exec_())