from PyQt5.QtCore import QTimer, Qt, QObject, QSize, QRect
from PyQt5.QtWidgets import QProgressBar, QWidget, QLabel, QPushButton, \
    QLineEdit, QGroupBox, QComboBox, QScrollArea, QTableWidget, QTableWidgetItem, \
    QFormLayout, QDialog, QDialogButtonBox, QVBoxLayout, QButtonGroup, QMainWindow, QHeaderView, QCalendarWidget, QFileDialog
from PyQt5.QtGui import QImage, QPalette, QBrush, QIcon, QPixmap, QFont, QColor
import json

SCREEN_WIDTH = 768
SCREEN_HEIGHT = 1366

# col, TABS, SCREEN_WIDTH y SCREEN_HEIGHT salen de constants.py

newfont = QFont("Times", 10)
bigfont = QFont("Times", 12)

row, col = (SCREEN_HEIGHT*0.05, SCREEN_WIDTH*0.1)
col1, col2, col3, col4, col5, col6, col7, col8, col9, col10 = [col * x for x in range(1, 11)]
row1, row2, row3, row4, row5, row6, row7, row8, row9, row10, row11, row12, row12, row14, row15, row16, row17, row18, row19, row20 = [row * x for x in range(1, 21)]


class Tab(QLabel):
    id = 0
    def __init__(self, parent, col_number, name = None, focused = False):
        super().__init__(parent)
        self.setGeometry((col3 + 25) * col_number , 0, col3, row/2)
        self.setStyleSheet("background-color: rgba(0,0,0,20%); border-radius: 2px" if focused else 'background-color: rgb(130,130,130); border-radius: 2px')
        self.name = "New tab" if not name else name
        self.setText("  " + self.name)
        self.setFont(newfont)
        self.show()
        self. id = Tab.id
        Tab.id += 1
        self._focused = focused

    @property
    def focused(self):
        return self._focused

    @focused.setter
    def focused(self, value):
        if value:
            self.setStyleSheet("background-color: rgba(0,0,0,20%); border-radius: 2px")
        else:
            self.setStyleSheet('background-color: rgb(130,130,130); border-radius: 2px')
        self._focused  = value

    def mousePressEvent(self, event):
        self.parent().change_tab(self)
        self.parent().mousePressEvent(event)
        self.focused = True


class Buylayout(QGroupBox):
    def __init__(self, parent):
        super().__init__(parent)
        self.setGeometry(0,0, SCREEN_WIDTH, SCREEN_HEIGHT)

        self.label = QLabel("Escanea tu Producto", self)
        self.label.setGeometry(270, 200, 300, 70)
        self.label.setFont(QFont("Times",18))

        self.cart_label = QLabel("Tu Carro", self)
        self.cart_label.setGeometry(20, 515, 150, 40)
        self.cart_label.setFont(QFont("Times", 15))

        self.cart_background = QGroupBox(self)
        self.cart_background.setGeometry(0, 500, 768, 866)
        self.cart_background.setStyleSheet('background-color: rgb(100,255,100)')
        self.cart_background.lower()

        self.cart_layout = QGroupBox(self)
        self.cart_layout.setGeometry(20, 560, 728, 786)
        self.cart_layout.setStyleSheet('background-color: white')


        self.layout = QGroupBox(self)
        self.layout.setGeometry(0,0, 768,500)
        self.layout.lower()

        self.code = QLineEdit(self)
        self.code.setGeometry(0,0,0,0)
        self.code.setFocus()

        self.cart = {}
        self.total = 0

        self.label_total = QLabel("   Total: $0", self)
        self.label_total.setGeometry(20, 1250, 328, 90)
        self.label_total.setFont(QFont("Times", 20))
        self.label_total.setStyleSheet('background-color: rgb(255, 255, 255)')

        self.boton_cancelar = QPushButton("Cancelar", self)
        self.boton_cancelar.setGeometry(300, 1250, 200, 90)
        self.boton_cancelar.setFont(QFont("Times", 18))
        self.boton_cancelar.clicked.connect(self.cancelar)

        self.boton_imprimir = QPushButton("Imprimir", self)
        self.boton_imprimir.setGeometry(500, 1250, 200, 90)
        self.boton_imprimir.setFont(QFont("Times", 18))

        self.icono = QLabel(self)
        self.icono.setPixmap(QPixmap('logo.svg').scaled(300, 100))
        self.icono.move(234, 50)

        self.imageShower = QLabel(self)
        self.imageShower.setGeometry(500, 250, 200, 200)

    def cancelar(self):
        self.label.show()
        self.layout.hide()
        self.cart = {}
        self.cart_layout.hide()
        self.total = 0

        self.cart_layout = QGroupBox(self)
        self.cart_layout.setGeometry(20, 560, 728, 786)
        self.cart_layout.lower()
        self.cart_background.lower()
        self.cart_layout.setStyleSheet('background-color: rgb(255, 255, 255)')
        self.cart_layout.show()

        self.label_total.setText("   Total: ${}".format(str(self.total)))
        self.code.setFocus()

        self.imageShower.show()

    def keyPressEvent(self, event):
        self.searchCode()

    def mousePressEvent(self, event):
        self.code.setFocus()

    def searchCode(self):
        self.label.hide()
        self.layout.hide()

        self.layout = QGroupBox(self)
        self.layout.setGeometry(0,0, 768, 500)
        self.layout.lower()
        try:
            item = self.parent().database[self.code.text()]
            if int(item['Cantidad'] )> 0:
                label = QLabel('Nombre: ' + item['Nombre'], self.layout)
                label.setGeometry(20, 250, 450, 50)
                label.setFont(QFont("Times", 16))
                label = QLabel('Marca: ' + item['Marca'], self.layout)
                label.setGeometry(20, 340, 450, 50)
                label.setFont(QFont("Times", 16))
                label = QLabel('Precio: $' + item['Precio'], self.layout)
                label.setGeometry(20, 430, 450, 50)
                label.setFont(QFont("Times", 16))

                self.imageShower.setPixmap(QPixmap(item['Imagen']).scaled(200, 200))
                self.imageShower.show()
                self.layout.show()
                self.total += int(item['Precio'])
                self.label_total.setText("   Total: ${}".format(str(self.total)))

                if item['Nombre'] in list(self.cart.keys()):
                    self.cart[item['Nombre']][0] += 1
                    self.cart[item['Nombre']][1].setText(str(self.cart[item['Nombre']][0]))
                else:
                    label = QLabel(item['Nombre'], self.cart_layout)
                    label.setGeometry(30, len(self.cart) * 40, 250, 30)
                    label.show()
                    label.setFont(QFont("Times",13))

                    label = QLabel('1', self.cart_layout)
                    label.setGeometry(300, len(self.cart) * 40, 100, 30)
                    label.show()
                    label.setFont(QFont("Times",13))
                    self.cart[item['Nombre']] = [1, label]
                self.parent().database[self.code.text()]['Cantidad'] = str(int(self.parent().database[self.code.text()]['Cantidad']) - 1)
                with open('db.json','w') as file:
                    json.dump(self.parent().database, file)
            else:
                self.label.setText('''Lo sentimos, ese
producto no está disponible''')
                self.label.show()
        except:
            pass

        self.code.setText('')
        self.code.setFocus()


class AddLayout(QGroupBox):
    placeholders = {
    'Codigo': '0000',
    'Nombre':'Producto',
    'Marca': 'Marca',
    'Precio': '100',
    'Cantidad': '1'
    }

    def __init__(self, parent):
        super().__init__(parent)
        self.setGeometry(0,0, SCREEN_WIDTH, SCREEN_HEIGHT)

        self.photofield = QPushButton('Seleccionar imagen',self)
        self.photofield.clicked.connect(self.addImage)
        self.photofield.setGeometry(col3, row12, col4,row)
        self.photofield.setFont(QFont("Times", 15))

        self.acceptButton = QPushButton('Aceptar', self)
        self.acceptButton.setGeometry(col4, row18, col2, row)
        self.acceptButton.setFont(QFont("Times", 15))
        self.acceptButton.clicked.connect(self.createItem)

        self.imageshower = QLabel(self)
        self.imageshower.setGeometry(col3,row14,col4,row3)
        self.imageshower.setPixmap(QPixmap('default.png').scaled(col4, row3))

        self.fileName = 'default.png'

        self.fields = {
        'Codigo':QLineEdit(self),
        'Nombre':QLineEdit(self),
        'Marca':QLineEdit(self),
        'Precio':QLineEdit(self),
        'Cantidad':QLineEdit(self)
        }
        contador = 0
        for i in self.fields:
            label = QLabel(i + ': ', self)
            label.setGeometry(col2, (row + 70) * contador + 150, col + 20, row)
            label.setFont(QFont("Times",15))

            edit = self.fields[i]
            edit.setGeometry(col3 + 20, (row +70) * contador + 150, col4, row)
            edit.setFont(QFont("Times",15))
            edit.setPlaceholderText(AddLayout.placeholders[i])

            contador += 1


    def addImage(self):
        fileName, _ = QFileDialog.getOpenFileName(self, 'Single File', '' , '*.png')
        nombre = fileName
        if len(fileName) > 15:
            nombre = '...' + fileName[-13:]
        self.photofield.setText(nombre)
        self.fileName = fileName
        self.imageshower.setPixmap(QPixmap(fileName).scaled(col4, row3))

    def createItem(self):
        try:
            item = self.parent().database[self.fields['Codigo'].text()]
            self.popup = AddMoreLayout(self)
        except:
            item = {}
            for i in self.fields:
                if not self.fields[i].text():
                    self.fields[i].setText(AddLayout.placeholders[i])
                item[i] = self.fields[i].text()
            item['Imagen'] = self.fileName
            self.parent().database[self.fields['Codigo'].text()] = item
            with open('db.json', 'w') as file:
                json.dump(self.parent().database, file)
            for i in self.fields.values():
                i.setText('')
            self.photofield.setText('Seleccionar imagen')
            self.fileName = ''
            self.imageshower.setPixmap(QPixmap('default.png').scaled(col4, row3))

class AddMoreLayout(QWidget):

    def __init__(self, parent = None):
        super().__init__(None)
        self.parent = parent

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setGeometry(col2, row5, col6, row5)
        self.setStyleSheet('background-color: rgb(255, 255, 255)')

        self.label = QLabel('''Ese producto ya está inscrito.
¿Deseas aumentar la Cantidad?''', self)
        self.label.setFont(QFont("Times",15))
        self.label.setGeometry(col, row/2, col4, row2)

        self.label_qty = QLabel('1', self)
        self.label_qty.setGeometry(col3, row2 + row/3, col, row)
        self.label_qty.setFont(QFont("Times", 12))

        self.boton_add = QPushButton('+', self)
        self.boton_add.setGeometry(col3 + col/2, row2 + row/2, col/2, row/2)
        self.boton_add.setFont(QFont("Times", 12))
        self.boton_add.setStyleSheet('background-color: gray')
        self.boton_add.clicked.connect(self.addQty)

        self.boton_rest = QPushButton('-', self)
        self.boton_rest.setGeometry(col2, row2 + row/2, col/2, row/2)
        self.boton_rest.setFont(QFont("Times", 12))
        self.boton_rest.setStyleSheet('background-color: gray')
        self.boton_rest.clicked.connect(self.restQty)

        self.boton_aceptar = QPushButton('Aceptar', self)
        self.boton_aceptar.setGeometry(col3, row3 + row/2, col + col/2, row)
        self.boton_aceptar.setFont(QFont("Times", 12))
        self.boton_aceptar.setStyleSheet('background-color: gray')

        self.boton_cancelar = QPushButton('Cancelar', self)
        self.boton_cancelar.setGeometry(col, row3 + row/2, col + col/2, row)
        self.boton_cancelar.setFont(QFont("Times", 12))
        self.boton_cancelar.setStyleSheet('background-color: gray')


        self.show()

    def addQty(self):
        self.label_qty.setText(str(int(self.label_qty.text() ) + 1))
        self.boton_rest.setEnabled(True)

    def restQty(self):
        self.label_qty.setText(str(int(self.label_qty.text() ) - 1))
        if self.label_qty.text() == '0':
            self.boton_rest.setEnabled(False)


class CheckItem(QGroupBox):
    def __init__(self, parent):
        super().__init__(parent)
        self.setGeometry(0,0, SCREEN_WIDTH, SCREEN_HEIGHT)

        self.label = QLabel('Escanée un producto',self)
        self.label.setGeometry(col3, row, col4, row)
        self.label.setFont(QFont("Times", 15))
        self.loaded = False

        self.codeInput = QLineEdit(self)
        self.codeInput.setGeometry(0, 0, 0, 0)
        self.codeInput.setFocus()
        self.codeInput.setFont(QFont("Times", 15))

        self.itemShower = QGroupBox(self)
        self.itemShower.setGeometry(col1, 150, col8, row17)

    def loadQty(self):
        self.codeInput.setFocus()
        if self.loaded:
            self.fields['Cantidad'].setText(self.parent().database[self.fields['Codigo'].text()]['Cantidad'])
            if self.fields['Cantidad'].text() == '0':
                self.plus_button.setEnabled(False)
            self.take_value.setText('0')
            self.less_button.setEnabled(False)

    def showItem(self):
        self.itemShower.hide()

        self.itemShower = QGroupBox(self)
        self.itemShower.setGeometry(col1, 150, col8, row17)
        try:
            item = self.parent().database[self.codeInput.text()]
            self.loaded = True
            self.takeButton = QPushButton('Retirar', self.itemShower)
            self.takeButton.setGeometry(col3, row15, col2, row)
            self.takeButton.setFont(QFont("Times", 15))
            self.takeButton.clicked.connect(self.takeItem)
            self.takeButton.show()
            self.imageshower = QLabel(self.itemShower)
            self.imageshower.setGeometry(col2,row11 ,col4,row3)
            self.imageshower.show()

            self.plus_button = QPushButton('+', self.itemShower)
            self.plus_button.setGeometry(col5, row9, col, row)
            self.plus_button.show()
            self.plus_button.clicked.connect(self.add)

            self.take_value = QLabel('0', self.itemShower)
            self.take_value.setGeometry(col4 + 30, row9, col / 2 ,row)
            self.take_value.show()
            self.take_value.setFont(QFont("Times", 15))

            self.less_button = QPushButton('-', self.itemShower)
            self.less_button.setGeometry(col3, row9, col, row)
            self.less_button.show()
            self.less_button.clicked.connect(self.less)
            self.less_button.setEnabled(False)

            self.fileName = ''

            self.fields = {
            'Codigo':QLabel(item['Codigo'], self.itemShower),
            'Nombre':QLabel(item['Nombre'], self.itemShower),
            'Marca':QLabel(item['Marca'], self.itemShower),
            'Precio':QLabel(item['Precio'], self.itemShower),
            'Cantidad':QLabel(item['Cantidad'], self.itemShower)
            }
            self.imageshower.setPixmap(QPixmap(item['Imagen']).scaled(col4, row3))
            contador = 0
            for i in self.fields:
                label = QLabel(i + ': ', self.itemShower)
                label.setGeometry(col, (row + 70) * contador , col + 40, row)
                label.setFont(QFont("Times",15))
                label.show()

                edit = self.fields[i]
                edit.setGeometry(col2 + 50, (row +70) * contador , col6, row)
                edit.setFont(QFont("Times",15))
                edit.show()

                contador += 1
            self.itemShower.show()
            if self.fields['Cantidad'].text() == '0':
                self.plus_button.setEnabled(False)

        except:
            pass
        self.codeInput.setFocus()
        self.codeInput.setText('')


    def takeItem(self):
        if int(self.fields['Cantidad'].text()) >= int(self.take_value.text()):
            self.parent().database[self.fields['Codigo'].text()]['Cantidad'] = str(int(self.parent().database[self.fields['Codigo'].text()]['Cantidad']) - int(self.take_value.text()))
            self.loadQty()
            with open('db.json','w') as file:
                json.dump(self.parent().database, file)
        self.codeInput.setFocus()
        self.codeInput.setText('')

    def add(self):
        if int(self.take_value.text()) + 1 >= int(self.fields['Cantidad'].text()):
            self.plus_button.setEnabled(False)
        self.take_value.setText(str(int(self.take_value.text()) + 1))
        self.less_button.setEnabled(True)

    def less(self):
        self.take_value.setText(str(int(self.take_value.text()) - 1))
        self.plus_button.setEnabled(True)
        if self.take_value.text() == '0':
            self.less_button.setEnabled(False)

    def keyPressEvent(self, event):
        self.showItem()
        self.codeInput.setFocus()
