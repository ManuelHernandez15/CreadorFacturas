from fpdf import FPDF

title = 'Factura'
subTitle = 'Generada Existosamente'
pathLogo = 'logo.png'

class PDF(FPDF):
    def header(self):
        if pathLogo is not None:
            self.image(pathLogo,
                   x = 10, y = 0, w = 30, h = 30)

        self.set_font('Arial', '', 15)

        self.tcol_set('darkblue')
        self.tfont_size(35)
        self.tfont('B')
        self.cell(w = 0, h = 10, txt = title, border = 0, ln=1,
                align = 'C', fill = 0)

        self.tfont_size(10)
        self.tcol_set('blue')
        self.tfont('I')
        self.cell(w = 0, h = 10, txt = subTitle, border = 0, ln=2,
                  align = 'C', fill = 0)

        self.ln(5)

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-20)

        # Arial italic 8
        self.set_font('Arial', 'I', 12)

        # Page number
        self.cell(w = 0, h = 10, txt =  'Gracias por su confianza',
                 border = 0,
                align = 'C', fill = 0)


    def diccionario_colores(self,color):
        colores = {
            'black': (0, 0, 0),
            'white': (255, 255, 255),
            'green': (96, 218, 117),
            'darkblue': (20, 104, 131),
            'blue': (18, 127, 166),
            'lightblue': (218, 240, 246),
            'red': (239, 71, 71),
            'rose': (214, 74, 236),
            'gray': (103, 103, 103),
            'gray2': (233, 233, 233),
        }

        return colores[color]


    def dcol_set(self, color):
        cr, cg, cb = self.diccionario_colores(color)
        self.set_draw_color(r=cr, g=cg, b=cb)


    def bcol_set(self, color):
        cr, cg, cb = self.diccionario_colores(color)
        self.set_fill_color(r=cr, g=cg, b=cb)


    def tcol_set(self, color):
        cr, cg, cb = self.diccionario_colores(color)
        self.set_text_color(r=cr, g=cg, b=cb)


    def tfont_size(self, size):
        self.set_font_size(size)


    def tfont(self, estilo, fuente='Arial'):
        self.set_font(fuente, style=estilo)

def setTitle(text):
    global title
    title = text

def setLogo(path):
    global pathLogo
    pathLogo = path

def set_subTitle(text):
    global subTitle
    subTitle = text
