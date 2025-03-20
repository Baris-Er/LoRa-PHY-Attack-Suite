import os
import numpy as np
from gnuradio import gr
from PyQt5 import QtWidgets, QtCore

class gui_file_source(gr.sync_block):
    """
    This block creates a GUI (combo box, refresh button, and send button) listing message files 
    (msg_*.dat or msg_*.bin) in the specified directory (e.g., "C:\\Users\\hakan\\Documents\\lora_recordings"). 
    Once the user selects a file and clicks the "Send" button, the file is read via np.fromfile() and replayed 
    as an IQ (np.complex64) stream. After the entire file has been sent (when replay is finished), 
    the block produces zero (0) samples and waits for a new selection.
    """
    def __init__(self, directory=r"C:\Users\hakan\Documents\lora_recordings"):
        gr.sync_block.__init__(
            self,
            name="gui_file_source",
            in_sig=None,
            out_sig=[np.complex64]
        )
        self.directory = directory
        self.data = None
        self.pointer = 0
        self.file_selected = False
        self.pending_file = None
        QtCore.QTimer.singleShot(0, self._init_gui)

    def _init_gui(self):
        app = QtWidgets.QApplication.instance()
        if app is None:
            app = QtWidgets.QApplication([])
        self.widget = QtWidgets.QWidget()
        self.widget.setWindowTitle("Mesaj Dosyası Seçici")
        layout = QtWidgets.QHBoxLayout(self.widget)
        self.combo = QtWidgets.QComboBox(self.widget)
        self.refresh_button = QtWidgets.QPushButton("Yenile", self.widget)
        self.send_button = QtWidgets.QPushButton("Gönder", self.widget)
        layout.addWidget(self.combo)
        layout.addWidget(self.refresh_button)
        layout.addWidget(self.send_button)
        self.widget.setLayout(layout)
        self.refresh_button.clicked.connect(self.refresh_files)
        self.combo.currentIndexChanged.connect(self.selection_changed)
        self.send_button.clicked.connect(self.send_file)
        self.refresh_files()
        self.widget.show()

    def refresh_files(self):
        self.combo.clear()
        try:
            files = [
                f for f in os.listdir(self.directory)
                if f.startswith("msg_") and (f.endswith(".dat") or f.endswith(".bin"))
            ]
            files.sort()
            self.combo.addItems(files)
        except Exception as e:
            print("Error listing files:", e)

    def selection_changed(self, index):
        if index < 0:
            return
        filename = self.combo.itemText(index)
        full_path = os.path.join(self.directory, filename)
        self.pending_file = full_path
        print("Selected file, click 'Gönder' to send:", full_path)

    def send_file(self):
        if self.pending_file is not None:
            print("Send button clicked. Loading file:", self.pending_file)
            self.load_file(self.pending_file)
        else:
            print("Send button clicked but no file selected.")

    def load_file(self, file_path):
        if os.path.exists(file_path) and os.path.isfile(file_path):
            try:
                self.data = np.fromfile(file_path, dtype=np.complex64)
                self.pointer = 0
                self.file_selected = True
                print("File loaded:", file_path, "Number of samples:", len(self.data))
            except Exception as e:
                print("Error loading file:", e)
                self.data = None
                self.file_selected = False
        else:
            print("File does not exist:", file_path)
            self.data = None
            self.file_selected = False

    def work(self, input_items, output_items):
        out = output_items[0]
        n_out = len(out)
        if self.data is None or not self.file_selected:
            out[:] = np.zeros(n_out, dtype=np.complex64)
            return n_out
        remaining = len(self.data) - self.pointer
        if remaining >= n_out:
            out[:] = self.data[self.pointer:self.pointer+n_out]
            self.pointer += n_out
            if self.pointer >= len(self.data):
                print("File transmission completed.")
                self.file_selected = False
            return n_out
        else:
            out[:remaining] = self.data[self.pointer:]
            out[remaining:] = np.zeros(n_out - remaining, dtype=np.complex64)
            self.pointer = len(self.data)
            print("File transmission completed.")
            self.file_selected = False
            return n_out


