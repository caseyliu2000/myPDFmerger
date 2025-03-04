import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import Slot
from PySide6.QtWidgets import QApplication,QFileDialog,QTextBrowser,QMessageBox

from PyPDF2 import PdfMerger
'''
初始化qt应用程序
'''
class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        
        self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]
        #设置按钮和文本
        self.button = QtWidgets.QPushButton("select file")
        self.merge_button=QtWidgets.QPushButton('merge files')
        #添加文本框
        self.text = QTextBrowser()
        self.text.setPlaceholderText("please select file...")
        #选择保存的地址
        self.output_path_button=QtWidgets.QPushButton('select output path')
        #显示选择的地址
        self.show_target_path=QtWidgets.QLabel('target path:')
        self.output_path=QtWidgets.QLabel('')
        #选择保存的文件名称
        self.output_name=QtWidgets.QLineEdit()
        self.output_name.setPlaceholderText('enter output file name: (output.pdf as default)')

        #设置布局
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.button)#添加按钮
        self.layout.addWidget(self.text)#添加文本框
        self.layout.addWidget(self.output_path_button)
        
        self.layout.addWidget(self.output_name)#编写文件名
        
        self.layout.addWidget(self.show_target_path)#显示文件地址
        self.layout.addWidget(self.output_path)#要保存的文件地址

        self.layout.addWidget(self.merge_button)#添加按钮


        #触发按钮点击事件
        self.button.clicked.connect(self.uploadFile)
        self.merge_button.clicked.connect(self.mergeFile)
        self.output_path_button.clicked.connect(self.selectOutputPath)

        #触发自启动事件
        self.output_name.editingFinished.connect(self.onEditingFinished)
        
    #每次点击按钮，都会调用这个函数，切换显示的文本
    #触发方法。
    @Slot()
    def uploadFile(self):
        fileName, _ = QFileDialog.getOpenFileNames(self, "Open Image File", "/home", "pdf files (*.pdf)")
        if fileName:
            #设置所选的text
            all_path=''
            for path in fileName:
                all_path+=path+'\n'
            
            self.text.setText(all_path)
    #合并文件
    @Slot()
    def mergeFile(self):
        #默认文件名
        the_file_name='output.pdf'
        if not self.text.toPlainText():
            # print('please select file first')
            QMessageBox.information(self, "Warning", "please select file first")
            return
        #如果用户没有选择保存的地址，则提示用户选择
        if not self.output_path.text():
            # print('please select output path first')
            QMessageBox.information(self, "Warning", "please select output path first")
            return
        
        #合并一个或多个pdf文件
        merger=PdfMerger()
        paths=self.text.toPlainText().split('\n')
        for path in paths:
            if path:
                merger.append(path)
        #写入pdf到指定地址
        the_path=self.output_path.text()
         #如果用户输入了文件名，则使用用户输入的文件名
        if self.output_name.text():
            the_file_name=self.output_path.text()
        else:
            the_path+='/'+the_file_name #'/output.pdf'
        print('the path:',the_path)
        
        merger.write(the_path)
        merger.close()
        print('merge success')
    #选择保存的位置
    @Slot()
    def selectOutputPath(self):
        path = QFileDialog.getExistingDirectory(self, "Open Directory",
                                                 "/home",
                                                 QFileDialog.ShowDirsOnly
                                                 | QFileDialog.DontResolveSymlinks)
        if path:
            self.output_path.setText(path)
        print(path)
        self.output_path.setText(path)
    
    #其他自触发
    #当输入文字完成后，触发这个方法
    @Slot()
    def onEditingFinished(self):
        the_file_name=self.output_name.text()

        #加入到output_path中
        output_path=self.output_path.text()
        output_path+='/'+the_file_name+'.pdf'
        self.output_path.setText(output_path)
#启动应用程序
if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    #启动widget类的对象。
    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())