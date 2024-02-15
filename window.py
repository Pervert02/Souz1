import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect
from PyQt5.QtGui import QColor, QIcon, QPainter, QBrush, QPen
from ctypes import windll

window_width = 1280
window_height = 720


class DraggableWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        # Устанавливаем флаг FramelessWindowHint
        self.setWindowFlags(Qt.FramelessWindowHint)
        
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground) #удаляем фон

        # Устанавливаем минимальный размер окна
        self.setMinimumSize(window_width, window_height)

        # Создаем область для перетаскивания окна
        self.draggable_area = QWidget(self)
        self.draggable_area.setGeometry(0, 0, self.width(), 50)
        self.draggable_area.setStyleSheet("background-color: blue; border-top-left-radius: 10px; border-top-right-radius: 10px;")

        # Создаем кнопку закрытия окна
        self.close_button = QPushButton('X', self)
        self.minimize_button = QPushButton('—', self)

        self.setWindowTitle('СОЮЗ')
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.setStyleSheet("background-color: #1D1D1D;") #Отдельная функция и т.д. передача цвета

        

    def showEvent(self, event):
        super().showEvent(event)
        self.close_button.setGeometry(self.width() - 50, 10, 35, 35)
        self.close_button.setStyleSheet("background-color: red; color: white; border-radius: 15px;")
        self.close_button.clicked.connect(self.close)
        self.close_button.setFont(QtGui.QFont("Arial", 13))

        self.minimize_button.setGeometry(self.width() - 90, 10, 35, 35)
        self.minimize_button.setStyleSheet("background-color: gray; color: white; border-radius: 15px;")
        self.minimize_button.clicked.connect(self.showMinimized)
        self.minimize_button.setFont(QtGui.QFont("Arial", 13))


    
    def mousePressEvent(self, event):
        # Проверяем, что нажата левая кнопка мыши и событие произошло внутри области перетаскивания
        if event.button() == Qt.LeftButton and self.draggable_area.geometry().contains(event.pos()):
            # Сохраняем смещение
            self.offset = event.globalPos() - self.pos()
            self.mousePressed = True  # Устанавливаем флаг нажатия кнопки

    def mouseMoveEvent(self, event):
        # Проверяем, произошло ли событие внутри области перетаскивания и нажата ли левая кнопка мыши
        if hasattr(self, 'offset') and self.mousePressed:
            # Перемещаем окно в соответствии с перемещением мыши
            self.move(event.globalPos() - self.offset)

    def mouseReleaseEvent(self, event):
        # Сбрасываем флаг нажатия кнопки
        self.mousePressed = False
    #\/рисуем окно\/#
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rounded_rect = self.rect().adjusted(0, 0, 0, 0)
        painter.setBrush(QBrush(QColor("#1D1D1D")))
        painter.setPen(QPen(Qt.PenStyle.NoPen))
        painter.drawRoundedRect(rounded_rect, 10, 10)


def main():
    # Путь к новому рабочему каталогу
    new_directory = 'C:/Users/User/Desktop/программы/SOUZ' #ПЕРЕДЕЛАТЬ (и иконку тоже)
    os.chdir(new_directory)

    # Создание экземпляра приложения
    app = QApplication(sys.argv)

    # Создание главного окна
    window = DraggableWindow()

    # Отображение окна
    window.show()

    # Запуск главного цикла приложения
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()