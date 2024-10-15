import sys
import os
import whisper
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QFileDialog, QTextEdit
from PyQt5.QtCore import Qt, QThread, pyqtSignal

class TranscriptionThread(QThread):
    finished = pyqtSignal(str)

    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path

    def run(self):
        model = whisper.load_model("base")
        result = model.transcribe(self.file_path)
        self.finished.emit(result["text"])

class Voice2TranscriptApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Voice to Transcript')
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.file_label = QLabel('No file selected', self)
        layout.addWidget(self.file_label)

        self.upload_button = QPushButton('Upload Audio File', self)
        self.upload_button.clicked.connect(self.upload_file)
        layout.addWidget(self.upload_button)

        self.transcribe_button = QPushButton('Transcribe', self)
        self.transcribe_button.clicked.connect(self.transcribe)
        self.transcribe_button.setEnabled(False)
        layout.addWidget(self.transcribe_button)

        self.result_text = QTextEdit(self)
        self.result_text.setReadOnly(True)
        layout.addWidget(self.result_text)

        self.setLayout(layout)

    def upload_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Audio File", "", "Audio Files (*.mp3 *.mp4)")
        if file_path:
            self.file_label.setText(os.path.basename(file_path))
            self.file_path = file_path
            self.transcribe_button.setEnabled(True)

    def transcribe(self):
        self.result_text.clear()
        self.result_text.setText("Transcribing... Please wait.")
        self.transcribe_button.setEnabled(False)
        self.upload_button.setEnabled(False)

        self.transcription_thread = TranscriptionThread(self.file_path)
        self.transcription_thread.finished.connect(self.update_result)
        self.transcription_thread.start()

    def update_result(self, result):
        self.result_text.setText(result)
        self.transcribe_button.setEnabled(True)
        self.upload_button.setEnabled(True)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Voice2TranscriptApp()
    ex.show()
    sys.exit(app.exec_())
