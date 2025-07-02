# app/gui_pyqt.py

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QProgressBar, QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal
from. import scraper, data_handler, config

class ScraperThread(QThread):
    finished = pyqtSignal(object)

    def __init__(self, url, use_login):
        super().__init__()
        self.url = url
        self.use_login = use_login

    def run(self):
        credentials = config.LOGIN_CREDENTIALS if self.use_login else None
        data = scraper.scrape_dynamic_site(self.url, login_credentials=credentials)
        self.finished.emit(data)

class PyQtApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Tier 3: 엔터프라이즈 맞춤 솔루션')
        self.setGeometry(300, 300, 600, 250)

        layout = QVBoxLayout()

        layout.addWidget(QLabel('타겟 URL:'))
        self.url_input = QLineEdit(self)
        self.url_input.setText(config.DYNAMIC_URL)
        layout.addWidget(self.url_input)

        layout.addWidget(QLabel('출력 포맷:'))
        self.format_combo = QComboBox(self)
        self.format_combo.addItems()
        layout.addWidget(self.format_combo)
        
        layout.addWidget(QLabel('로그인 필요:'))
        self.login_combo = QComboBox(self)
        self.login_combo.addItems(['아니요', '예'])
        layout.addWidget(self.login_combo)

        self.run_button = QPushButton('크롤링 실행', self)
        self.run_button.clicked.connect(self.run_scraping)
        layout.addWidget(self.run_button)

        self.progress = QProgressBar(self)
        layout.addWidget(self.progress)

        self.status_label = QLabel('상태: 대기 중', self)
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def run_scraping(self):
        url = self.url_input.text()
        if not url:
            QMessageBox.warning(self, '경고', 'URL을 입력해주세요.')
            return
            
        use_login = self.login_combo.currentText() == '예'
        
        self.run_button.setEnabled(False)
        self.status_label.setText('상태: 크롤링 진행 중...')
        self.progress.setRange(0, 0)

        self.thread = ScraperThread(url, use_login)
        self.thread.finished.connect(self.on_finished)
        self.thread.start()

    def on_finished(self, data):
        self.progress.setRange(0, 1)
        self.progress.setValue(1)
        self.run_button.setEnabled(True)
        self.status_label.setText('상태: 대기 중')

        if data:
            output_format = self.format_combo.currentText()
            saved = data_handler.save_data(data, output_format, 'enterprise_output')
            if saved:
                QMessageBox.information(self, '완료', f"크롤링 완료! 'output' 폴더에 {output_format} 파일로 저장되었습니다.")
            else:
                QMessageBox.critical(self, '오류', '데이터 저장에 실패했습니다.')
        else:
            QMessageBox.critical(self, '오류', '크롤링에 실패했습니다.')