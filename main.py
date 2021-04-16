from time import sleep

from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QFormLayout, QWidget, QApplication, QLabel, QTextEdit, QSpinBox, QPushButton, QProgressBar, \
    QMessageBox
from pynput.keyboard import Controller, Key
from pyperclip import copy


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # --------------------------Set Window-------------------
        self.setWindowTitle('Rajazap 6.0 BY D0C_')
        self.window_layout = QFormLayout()
        self.setLayout(self.window_layout)
        self.setWindowIcon(QIcon("monke.ico"))
        self.setFixedSize(450, 600)

        # ---------------------------Widgets---------------------
        # Labels
        self.title = QLabel("Rajador Foda\n6.0")
        self.title.setFont(QFont("HELVETICA", 25))
        self.title.setAlignment(Qt.AlignCenter)

        self.msg_label = QLabel("Mensagem\nPara spam")
        self.msg_label.setFont(QFont("HELVETICA", 10,
                                     weight=QFont.Bold))

        self.qnt_label = QLabel("quantidade")
        self.qnt_label.setFont(QFont("HELVETICA", 10,
                                     weight=QFont.Bold))

        self.timer_label = QLabel("")
        self.timer_label.setFont(QFont("HELVETICA", 20,
                                       weight=QFont.Bold))
        self.timer_label.setAlignment(Qt.AlignCenter)

        # Entry boxes
        self.msg_entry_box = QTextEdit(self)
        self.msg_entry_box.setPlaceholderText("Digite a frase para spam")

        self.qnt_entry_box = QSpinBox(self)
        self.qnt_entry_box.setMaximum(10000)
        self.qnt_entry_box.setValue(400)

        # Button
        self.butao_raja = QPushButton("Raja")
        self.butao_raja.setFixedSize(150, 30)

        self.butao_para = QPushButton("parar")
        self.butao_para.setFixedSize(150, 30)
        self.butao_para.setEnabled(False)

        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedSize(300, 30)
        self.progress_bar.setAlignment(Qt.AlignCenter)

        # -------------------events------------------------------
        self.butao_raja.clicked.connect(self.raja)

        self.butao_para.clicked.connect(self.parar)

        # ------------------Organize layout----------------------
        self.window_layout.addRow(self.title)
        self.window_layout.addRow(self.msg_label, self.msg_entry_box)
        self.window_layout.addRow(self.qnt_label, self.qnt_entry_box)
        self.window_layout.addRow(self.butao_raja, self.butao_para)
        self.window_layout.addRow("enviadas", self.progress_bar)
        self.window_layout.addRow(self.timer_label)

        # Show
        self.show()

    def raja(self):
        self.progress_bar.setMaximum(self.qnt_entry_box.value())
        self.spammer = SpamWorker(self.qnt_entry_box.value(), self.msg_entry_box.toPlainText())
        self.spammer.start()
        # Events
        self.spammer.timer.connect(self.timer_update)
        self.spammer.update_pgr_bar.connect(self.pgr_bar_update)
        self.spammer.btn_tf.connect(self.atv_dtv_btn)
        self.spammer.finished.connect(self.terminado)

    def timer_update(self, count):
        self.timer_label.setText(count)

    def terminado(self):
        QMessageBox.information(self, "Terminado", "Mensagens enviadas com sucesso!")
        self.butao_raja.setEnabled(True)
        self.qnt_entry_box.setEnabled(True)
        self.msg_entry_box.setEnabled(True)

    def pgr_bar_update(self, box):
        self.progress_bar.setValue(box)

    def atv_dtv_btn(self, btn_para_atv):
        self.butao_para.setEnabled(btn_para_atv)
        self.butao_raja.setEnabled(False)
        self.msg_entry_box.setEnabled(False)
        self.qnt_entry_box.setEnabled(False)

    def parar(self):
        self.spammer.stop()


class SpamWorker(QThread):
    def __init__(self, quantidade, mensagem):
        QThread.__init__(self)
        self.quantt = quantidade
        self.mensgim = mensagem
        self.go_for_raja = True

    update_pgr_bar = pyqtSignal(int)
    btn_tf = pyqtSignal(bool)
    timer = pyqtSignal(str)

    def run(self):
        copy(self.mensgim)
        keyboard = Controller()
        self.btn_tf.emit(True)

        # Timer
        for y in range(5, 0, -1):
            if not self.go_for_raja:
                break
            self.timer.emit(str(y))
            sleep(1)

        self.timer.emit('Rajando!!!')

        # Rajazap code
        if self.go_for_raja:
            for x in range(1, self.quantt + 1):
                keyboard.press(Key.ctrl)
                keyboard.press("v")
                keyboard.release(Key.ctrl)
                keyboard.release('v')
                keyboard.press(Key.enter)
                keyboard.release(Key.enter)
                sleep(0.03)
                self.update_pgr_bar.emit(x)
                if not self.go_for_raja:
                    self.update_pgr_bar.emit(self.quantt)
                    self.btn_tf.emit(False)
                    self.timer.emit("")
                    self.go_for_raja = True
                    break
        self.btn_tf.emit(False)
        self.timer.emit("")

    def stop(self):
        self.go_for_raja = False


if __name__ == "__main__":
    app = QApplication([])
    root = MainWindow()

    # Run
    app.exec_()
