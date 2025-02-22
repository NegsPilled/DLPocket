import sys
import os
import yt_dlp
import subprocess
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLineEdit, QPushButton, QLabel, QComboBox, 
                            QFileDialog, QScrollArea, QMenu)
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QIcon

# CustomTitleBar and URLWidget classes remain unchanged for brevity
class CustomTitleBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 5, 0, 5)
        layout.setSpacing(0)
        
        self.title = QLabel("DLPocket")
        self.title.setStyleSheet("font-size: 18px; color: white; font-weight: bold; padding: 5px;")
        
        self.minimize_button = QPushButton("-")
        self.minimize_button.setFixedSize(38, 30)
        self.minimize_button.clicked.connect(self.parent.showMinimized)
        self.minimize_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: white;
                border: none;
                font-size: 18px;
                font-weight: bold;
                font-family: Arial, sans-serif;
                padding-bottom: 10px;
            }
            QPushButton:hover {
                background-color: #555;
            }
        """)
        
        self.maximize_button = QPushButton("🗖")
        self.maximize_button.setFixedSize(38, 30)
        self.maximize_button.clicked.connect(self.toggle_maximize)
        self.maximize_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: white;
                border: none;
                font-size: 10px;
                padding-bottom: 8px;
            }
            QPushButton:hover {
                background-color: #555;
            }
        """)
        
        self.close_button = QPushButton("×")
        self.close_button.setFixedSize(38, 30)
        self.close_button.clicked.connect(self.parent.close)
        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: white;
                border: none;
                font-size: 12px;
                padding-bottom: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #ff4444;
            }
        """)
        
        layout.addWidget(self.title)
        layout.addStretch()
        layout.addWidget(self.minimize_button, alignment=Qt.AlignVCenter)
        layout.addWidget(self.maximize_button, alignment=Qt.AlignVCenter)
        layout.addWidget(self.close_button, alignment=Qt.AlignVCenter)
        
        self.setLayout(layout)
        self.setStyleSheet("background-color: #202020;")
        self.setFixedHeight(50)

    def toggle_maximize(self):
        if self.parent.isMaximized():
            self.parent.showNormal()
            self.maximize_button.setText("🗖")
        else:
            self.parent.showMaximized()
            self.maximize_button.setText("🗗")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and event.pos().y() < 50:
            self.parent.drag_position = event.globalPos() - self.parent.pos()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.parent.move(event.globalPos() - self.parent.drag_position)
            event.accept()

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton and event.pos().y() < 50:
            self.toggle_maximize()

class URLWidget(QWidget):
    def __init__(self, url, title, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.url = url
        self.label = QLabel(f"• {title}")
        self.label.setStyleSheet("color: white; padding: 5px;")
        self.label.setMaximumWidth(350)
        self.label.setWordWrap(False)
        self.label.setText(self.label.fontMetrics().elidedText(f"• {title}", Qt.ElideRight, 350))
        
        self.remove_btn = QPushButton("×")
        self.remove_btn.setFixedSize(20, 20)
        self.remove_btn.setStyleSheet("""
            QPushButton {
                background-color: #666;
                border-radius: 10px;
                color: white;
                font-weight: bold;
                padding: 0px;
            }
            QPushButton:hover {
                background-color: #ff4444;
            }
        """)
        
        layout.addWidget(self.label)
        layout.addWidget(self.remove_btn, alignment=Qt.AlignRight)
        self.setLayout(layout)

class DownloaderApp(QWidget):
    def __init__(self):
        super().__init__()
        self.drag_position = QPoint()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowIcon(QIcon("dlpocket.ico"))
        self.setMinimumSize(400, 300)
        
        # Stylesheet unchanged for brevity
        self.setStyleSheet("""
            QWidget {
                background-color: #2e2e2e; 
                font-family: Arial, sans-serif; 
                color: white;
            }
            QLineEdit {
                padding: 12px;
                font-size: 16px;
                border-radius: 8px;
                border: 1px solid #555;
                background-color: #444;
                color: white;
            }
            QLineEdit:focus {
                border: 1px solid #66ccff;
            }
            QComboBox {
                font-size: 16px;
                border-radius: 8px;
                padding: 12px;
                background-color: #444;
                color: white;
                border: 1px solid #555;
                min-width: 250px;
            }
            QComboBox:hover {
                background-color: #555;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                border: none;
                background: none;
                image: none;
            }
            QComboBox QAbstractItemView {
                background-color: #333;
                color: white;
                selection-background-color: #66ccff;
                selection-color: white;
                border: 1px solid #555;
            }
            QPushButton {
                font-size: 16px;
                padding: 12px;
                background-color: #4CAF50;
                color: white;
                border-radius: 8px;
                border: none;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
            QLabel {
                font-size: 14px;
                color: #aaa;
            }
            QMenu {
                background-color: #333;
                color: white;
                border: 1px solid #555;
            }
            QMenu::item {
                padding: 5px 20px;
            }
            QMenu::item:selected {
                background-color: #66ccff;
            }
            QScrollBar:vertical {
                border: none;
                background: #2e2e2e;
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #666;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        self.title_bar = CustomTitleBar(self)
        main_layout.addWidget(self.title_bar)
        
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(10, 10, 10, 10)
        content_layout.setSpacing(10)

        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText("Enter Video URL")
        content_layout.addWidget(self.url_input)

        self.quality_select = QComboBox(self)
        quality_options = [
            ("Best Quality", "bestvideo+bestaudio/best"),
            ("1080p", "bestvideo[height<=1080]+bestaudio/best[height<=1080]"),
            ("720p", "bestvideo[height<=720]+bestaudio/best[height<=720]"),
            ("480p", "bestvideo[height<=480]+bestaudio/best[height<=480]"),
            ("360p", "bestvideo[height<=360]+bestaudio/best[height<=360]"),
            ("240p", "bestvideo[height<=240]+bestaudio/best[height<=240]"),
            ("Audio Only (MP3)", "bestaudio/best")
        ]
        for label, format_id in quality_options:
            self.quality_select.addItem(label, format_id)
        content_layout.addWidget(self.quality_select)

        self.add_url_button = QPushButton("Add URL", self)
        self.add_url_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.add_url_button.clicked.connect(self.add_url)
        content_layout.addWidget(self.add_url_button)

        self.urls_area = QScrollArea(self)
        self.urls_area.setWidgetResizable(True)
        self.urls_area.setStyleSheet("""
            QScrollArea {
                border: 1px solid #555;
                border-radius: 8px;
                background-color: #444;
                min-height: 100px;
            }
        """)
        self.urls_container = QWidget()
        self.urls_layout = QVBoxLayout(self.urls_container)
        self.urls_layout.addStretch()
        self.urls_area.setWidget(self.urls_container)
        content_layout.addWidget(self.urls_area)
        self.url_list = []

        self.start_button = QPushButton("Start Download", self)
        self.start_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        self.start_button.clicked.connect(self.start_download)
        content_layout.addWidget(self.start_button)

        self.progress_label = QLabel("Ready to download", self)
        self.progress_label.setStyleSheet("font-size: 14px; color: #aaa; margin-top: 10px;")
        content_layout.addWidget(self.progress_label)

        self.folder_button = QPushButton("Select Download Folder", self)
        self.folder_button.setStyleSheet("""
            QPushButton {
                font-size: 12px;
                padding: 6px 12px;
                background-color: #555;
            }
            QPushButton:hover {
                background-color: #666;
            }
        """)
        self.folder_button.clicked.connect(self.select_folder)
        self.folder_button.setFixedSize(160, 30)
        content_layout.addWidget(self.folder_button, alignment=Qt.AlignRight)

        content_widget = QWidget()
        content_widget.setLayout(content_layout)
        main_layout.addWidget(content_widget)
        
        self.setLayout(main_layout)

        self.download_folder = os.path.expanduser("~/Downloads")
        
        self.show()

    def get_ffmpeg_path(self):
        """Updated to raise errors if FFmpeg is missing and return the directory path."""
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
            ffmpeg_path = os.path.join(base_path, 'ffmpeg.exe')
            if not os.path.exists(ffmpeg_path):
                self.progress_label.setText("Error: FFmpeg not found in app bundle. Reinstall the app.")
                raise FileNotFoundError("FFmpeg not found in bundled app. Ensure it's included.")
            return os.path.dirname(ffmpeg_path)
        else:
            default_path = 'C:/ffmpeg/bin'
            ffmpeg_exe = os.path.join(default_path, 'ffmpeg.exe')
            if not os.path.exists(ffmpeg_exe):
                self.progress_label.setText("Error: FFmpeg not found at C:/ffmpeg/bin. Please install FFmpeg.")
                raise FileNotFoundError("FFmpeg not found. Install it and update the path.")
            return default_path

    def remove_url(self, url_widget):
        self.url_list.remove(url_widget.url)
        url_widget.deleteLater()
        if not self.url_list:
            self.progress_label.setText("Ready to download")

    def add_url(self):
        url = self.url_input.text().strip()
        if not url:
            self.progress_label.setText("Please enter a URL")
            return

        if url in self.url_list:
            self.progress_label.setText("URL already added")
            return

        self.progress_label.setText("Fetching video info...")
        
        try:
            ydl_opts = {'quiet': True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                url_widget = URLWidget(url, info.get('title', url))
                url_widget.remove_btn.clicked.connect(lambda: self.remove_url(url_widget))
                self.urls_layout.insertWidget(self.urls_layout.count() - 1, url_widget)
                
                self.url_list.append(url)
                self.progress_label.setText("URL added successfully")
                self.url_input.clear()

        except Exception as e:
            self.progress_label.setText(f"Error: {str(e)}")

    def start_download(self):
        if not self.url_list:
            self.progress_label.setText("Please add URLs first")
            return

        selected_format = self.quality_select.currentData()
        try:
            ffmpeg_location = self.get_ffmpeg_path()
        except FileNotFoundError:
            return  # Error message already set in get_ffmpeg_path

        # Validate FFmpeg execution
        try:
            subprocess.run(
                [os.path.join(ffmpeg_location, 'ffmpeg.exe'), '-version'],
                check=True, capture_output=True, text=True
            )
        except subprocess.CalledProcessError as e:
            self.progress_label.setText(f"FFmpeg error: {e.stderr.splitlines()[0]}")
            return

        print(f"FFmpeg path: {ffmpeg_location}")
        print(f"FFmpeg exists: {os.path.exists(os.path.join(ffmpeg_location, 'ffmpeg.exe'))}")
        
        for url in self.url_list.copy():
            self.progress_label.setText(f"Downloading: {url}")
            
            ydl_opts = {
                'format': selected_format,
                'outtmpl': os.path.join(self.download_folder, '%(title)s.%(ext)s'),
                'progress_hooks': [self._progress_hook],
                'ffmpeg_location': ffmpeg_location,
                'merge_output_format': 'mkv',  # Force MKV container for robust merging
                'postprocessors': [{
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mkv',  # Ensure compatibility
                }],
                'verbose': True,
            }
            if selected_format == 'bestaudio/best':
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]
            
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)  # Simulate first
                    print("Available formats:")
                    for f in info['formats']:
                        print(f"ID: {f['format_id']}, Height: {f.get('height')}, Note: {f.get('format_note')}, Ext: {f['ext']}")
                    print(f"Selected format: {info['format_id']}, Height: {info.get('height')}")
                    ydl.download([url])
            except Exception as e:
                self.progress_label.setText(f"Error downloading {url}: {str(e)}")
                continue

        self.url_list.clear()
        for i in reversed(range(self.urls_layout.count() - 1)):
            widget = self.urls_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        
        self.progress_label.setText("All downloads completed!")

    def _progress_hook(self, d):
        if d['status'] == 'downloading':
            try:
                downloaded = d.get('downloaded_bytes', 0)
                total = d.get('total_bytes', 0) or d.get('total_bytes_estimate', 0)
                if total:
                    percentage = (downloaded / total) * 100
                    self.progress_label.setText(f"Downloading: {percentage:.1f}%")
                else:
                    self.progress_label.setText("Downloading...")
            except:
                self.progress_label.setText("Downloading...")
        elif d['status'] == 'finished':
            self.progress_label.setText("Processing download...")

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Download Folder", self.download_folder)
        if folder:
            self.download_folder = folder

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet("""
        QMenu {
            background-color: #333;
            color: white;
            border: 1px solid #555;
        }
        QMenu::item {
            padding: 5px 20px;
        }
        QMenu::item:selected {
            background-color: #66ccff;
        }
    """)
    window = DownloaderApp()
    sys.exit(app.exec_())