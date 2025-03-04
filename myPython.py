import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import Slot
from PySide6.QtWidgets import QApplication, QLabel,QPushButton, QVBoxLayout,QTableWidget,QTableWidgetItem,QWidget,QFileDialog
'''
初始化qt应用程序
'''
class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        
        self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]
        #设置按钮和文本
        self.button = QtWidgets.QPushButton("Click me!")
        self.text = QtWidgets.QLabel("Hello World",
                                     alignment=QtCore.Qt.AlignCenter)
        #加入table
        colors=[("Red", "#FF0000"),
          ("Green", "#00FF00"),
          ("Blue", "#0000FF"),
          ("Black", "#000000"),
          ("White", "#FFFFFF"),
          ("Electric Green", "#41CD52"),
          ("Dark Blue", "#222840"),
          ("Yellow", "#F9E56d")]
        self.table=QTableWidget()
        self.table.setColumnCount(len(colors[0])+1)
        self.table.setRowCount(len(colors))
        self.table.setHorizontalHeaderLabels(["Color","Hex"])
        #添加table items
        for i, (name, hex) in enumerate(colors):
            self.table.setItem(i, 0, QTableWidgetItem(name))
            self.table.setItem(i, 1, QTableWidgetItem(hex))
        #添加filedialog
        

        #设置布局
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)#添加文本
        self.layout.addWidget(self.button)#添加按钮
        self.layout.addWidget(self.table)#添加table

        #触发按钮点击事件
        self.button.clicked.connect(self.magic)
    #每次点击按钮，都会调用这个函数，切换显示的文本
    #触发方法。
    @QtCore.Slot()
    def magic(self):
        self.text.setText(random.choice(self.hello))
    
    def get_rgb_from_hex(code):
        code_hex = code.replace("#", "")
        rgb = tuple(int(code_hex[i:i+2], 16) for i in (0, 2, 4))
        return QColor.fromRgb(rgb[0], rgb[1], rgb[2])
#启动应用程序
if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    #启动widget类的对象。
    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())