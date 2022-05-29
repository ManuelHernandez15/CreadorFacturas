import sys
from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtWidgets import QTableWidgetItem, QFileDialog
from PyQt5.QtGui import QPixmap
from editPDF import *
from datetime import datetime

qtCreatorFile = "Facturas.ui"  # Nombre del archivo aquí.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        # Cargar encabezados
        self.loadHeader()

        # Variables
        self.pathImg = None
        self.datos = []
        self.now = datetime.now()
        date = str(self.now.date().strftime("%d/%m/%Y"))
        self.txt_fecha.setText(date)
        self.total = 0

        # Área de los Signals y Configuraciones Iniciales
        self.btn_cargar.clicked.connect(self.agregar)
        self.btn_cargarImg.clicked.connect(self.loadImg)
        self.btn_generar.clicked.connect(self.generarFacturar)

    def agregar(self):
        descripcion = self.txt_descripcion.text()
        importe = self.txt_importe.text()

        if len(descripcion) != 0 and len(importe) != 0:
            if importe.replace(',','').isdigit():
                rowCount = self.tableWidget.rowCount()
                self.tableWidget.insertRow(rowCount)
                self.tableWidget.setItem(rowCount, 0, QTableWidgetItem(descripcion))
                self.tableWidget.setItem(rowCount, 1, QTableWidgetItem(importe))
            else:
                QtWidgets.QMessageBox.about(self, 'Importe invalido', 'Porfavor ingrese un valor numerico')
        else:
            QtWidgets.QMessageBox.about(self, 'Casilla Vacia', 'Porfavor ingrese la descripcion y el importe')

    def loadHeader(self):
        self.tableWidget.setColumnCount(2)

        self.tableWidget.setHorizontalHeaderLabels(('Descripción', 'Importe'))

        self.tableWidget.setColumnWidth(0, 350)
        self.tableWidget.setColumnWidth(1, 80)

    def readDatos(self):
        filas = self.tableWidget.rowCount()
        self.datos = []
        self.total = 0
        for f in range(filas):
            desc = self.tableWidget.item(f, 0).text()
            importe = '$' + self.tableWidget.item(f, 1).text() + '.00'
            self.total += float(self.tableWidget.item(f, 1).text().replace(',',''))
            self.datos.append([desc, importe])
        print(self.datos)

    def loadImg(self):
        self.pathImg = self.browsefiles()
        im = QPixmap(self.pathImg)
        self.lbl_img.setPixmap(im.scaled(100, 100, QtCore.Qt.KeepAspectRatio))

    def generarFacturar(self):
        if self.verficar():
            # Encabezado
            self.readDatos()
            now = datetime.now()
            hora = str(now.time())[:5]

            fecha = self.txt_fecha.text()

            imgLogo = self.pathImg

            idFactura = self.txt_factura.text()

            pathSave = self.savefiles() + '\\\\'

            namePDF = 'Factura ' + str(idFactura) + '_' + fecha.replace('/', '-') + '_' + hora.replace(':', '') + '.pdf'

            nombre = self.txt_nombre.text()
            empresa = self.txt_empresa.text()
            direccion = self.txt_direccion.text()

            nombreP = self.txt_nombreP.text()

            setTitle('Factura')
            set_subTitle(empresa)
            setLogo(imgLogo)

            pdf = PDF(orientation='P', unit='mm', format='A4')
            pdf.alias_nb_pages()

            pdf.add_page()

            # Div informacion factura
            pdf.bcol_set('lightblue')
            pdf.rect(x=10, y=30, w=130, h=35, style='F')

            pdf.bcol_set('darkblue')
            pdf.rect(x=140, y=30, w=60, h=35, style='F')

            # Fuente Texto
            pdf.set_font('Arial', '', 15)

            pdf.tfont('B')
            pdf.tcol_set('darkblue')
            pdf.multi_cell(w=0, h=5, txt='Facturar a: ', border=0,
                           align='L', fill=0)

            # informacion primer fila
            pdf.tfont_size(12)
            h_info = 5

            pdf.tfont('')
            pdf.cell(w=15, h=h_info, txt=nombre, border=0,
                     align='L', fill=0)

            pdf.tfont('B')
            pdf.tcol_set('white')
            pdf.cell(w=140, h=h_info, txt='Fecha:', border=0,
                     align='R', fill=0)

            pdf.tfont('')
            pdf.multi_cell(w=0, h=h_info, txt=fecha, border=0,
                           align='L', fill=0)

            # Segunda Fila
            pdf.tcol_set('darkblue')
            pdf.cell(w=15, h=h_info, txt=empresa, border=0,
                     align='L', fill=0)

            pdf.tfont('B')
            pdf.tcol_set('white')
            pdf.cell(w=140, h=h_info, txt='Factura:', border=0,
                     align='R', fill=0)

            pdf.tfont('')
            pdf.multi_cell(w=0, h=h_info, txt=idFactura, border=0,
                           align='L', fill=0)

            # Tercer Fila
            pdf.tcol_set('darkblue')
            pdf.cell(w=15, h=h_info, txt=direccion, border=0,
                     align='L', fill=0)

            pdf.tfont('B')
            pdf.tcol_set('white')
            pdf.cell(w=140, h=h_info, txt='Para:', border=0,
                     align='R', fill=0)

            pdf.tfont('')
            pdf.multi_cell(w=0, h=h_info, txt=nombreP, border=0,
                           align='L', fill=0)

            pdf.ln(20)
            # tabla ----
            pdf.tfont_size(13)
            pdf.tcol_set('white')
            pdf.bcol_set('darkblue')
            pdf.cell(w=150, h=10, txt='DESCRIPCIÓN', border=0, align='C', fill=1)
            pdf.multi_cell(w=0, h=10, txt='IMPORTE', border=0, align='C', fill=1)

            pdf.tcol_set('black')
            c = 0
            for datos in self.datos:
                c += 1
                if c % 2 == 0:
                    pdf.bcol_set('lightblue')
                else:
                    pdf.bcol_set('white')
                pdf.cell(w=150, h=10, txt=datos[0], border=0, align='L', fill=1)
                pdf.multi_cell(w=0, h=10, txt=datos[1], border=0, align='C', fill=1)

            # Total
            pdf.ln(2)
            pdf.tcol_set('black')
            pdf.tfont('B')
            pdf.cell(w=160, h=h_info, txt='Total:', border=0,
                     align='R', fill=0)

            pdf.tfont('')
            pdf.multi_cell(w=0, h=h_info, txt='$'+str(self.total) + '0', border=0,
                           align='L', fill=0)

            pdf.output(pathSave + namePDF, 'F')

    def verficar(self):
        if len(self.txt_nombre.text()) == 0:
            QtWidgets.QMessageBox.about(self, 'Casilla Vacia', 'Porfavor ingrese el nombre')
            return False
        if len(self.txt_empresa.text()) == 0:
            QtWidgets.QMessageBox.about(self, 'Casilla Vacia', 'Porfavor ingrese el nombre de la empresa')
            return False
        if len(self.txt_direccion.text()) == 0:
            QtWidgets.QMessageBox.about(self, 'Casilla Vacia', 'Porfavor ingrese la direccion')
            return False
        if len(self.txt_fecha.text()) == 0:
            QtWidgets.QMessageBox.about(self, 'Casilla Vacia', 'nmms cabron, esta madre te rellena la fecha en automatico')
            return False
        if len(self.txt_factura.text()) == 0:
            QtWidgets.QMessageBox.about(self, 'Casilla Vacia', 'Porfavor ingrese el numero de factura')
            return False
        if len(self.txt_nombreP.text()) == 0:
            QtWidgets.QMessageBox.about(self, 'Casilla Vacia', 'Porfavor ingrese para quién es la factura')
            return False
        return True


    def browsefiles(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', 'C:/Users/DELL/Documents', 'Images (*.png, *.xmp *.jpg)')
        return fname[0]

    def savefiles(self):
        #Obtiene el directorio
        fname = QFileDialog.getExistingDirectory(self, 'Saving file', 'C:/Users/DELL/Documents')
        return fname.replace('/', '\\\\')


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
