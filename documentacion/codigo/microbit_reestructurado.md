from microbit import *

# ============================================
# SMARTPLANT: SUELO + OLED + LEDS
# ============================================

sensor_suelo = pin1

led_verde = pin8
led_amarillo = pin13
led_rojo = pin12

# Calibracion: reemplazar por mediciones reales.
# Estos dos valores deben ser distintos.
VALOR_SECO = 850
VALOR_HUMEDO = 350

# OLED SSD1306 de 128 x 64, direccion 0x3C
i2c.init(freq=400000, sda=pin20, scl=pin19)

# ============================================
# FUENTE PARA LA PANTALLA
# ============================================

FUENTE = {
    " ": [0, 0, 0, 0, 0],
    "%": [98, 100, 8, 19, 35],
    ":": [0, 54, 54, 0, 0],
    "0": [62, 81, 73, 69, 62],
    "1": [0, 66, 127, 64, 0],
    "2": [98, 81, 73, 73, 70],
    "3": [34, 65, 73, 73, 54],
    "4": [24, 20, 18, 127, 16],
    "5": [39, 69, 69, 69, 57],
    "6": [60, 74, 73, 73, 48],
    "7": [1, 113, 9, 5, 3],
    "8": [54, 73, 73, 73, 54],
    "9": [6, 73, 73, 41, 30],
    "A": [126, 17, 17, 17, 126],
    "B": [127, 73, 73, 73, 54],
    "C": [62, 65, 65, 65, 34],
    "D": [127, 65, 65, 34, 28],
    "E": [127, 73, 73, 73, 65],
    "F": [127, 9, 9, 9, 1],
    "G": [62, 65, 73, 73, 122],
    "H": [127, 8, 8, 8, 127],
    "I": [0, 65, 127, 65, 0],
    "J": [32, 64, 65, 63, 1],
    "K": [127, 8, 20, 34, 65],
    "L": [127, 64, 64, 64, 64],
    "M": [127, 2, 12, 2, 127],
    "N": [127, 4, 8, 16, 127],
    "O": [62, 65, 65, 65, 62],
    "P": [127, 9, 9, 9, 6],
    "Q": [62, 65, 81, 33, 94],
    "R": [127, 9, 25, 41, 70],
    "S": [70, 73, 73, 73, 49],
    "T": [1, 1, 127, 1, 1],
    "U": [63, 64, 64, 64, 63],
    "V": [31, 32, 64, 32, 31],
    "W": [63, 64, 56, 64, 63],
    "X": [99, 20, 8, 20, 99],
    "Y": [7, 8, 112, 8, 7],
    "Z": [97, 81, 73, 69, 67],
}

# ============================================
# CONTROLADOR OLED
# ============================================

class OLED:
    def __init__(self, addr=0x3C):
        self.width = 128
        self.height = 64
        self.addr = addr
        self.buffer = bytearray(1024)
        self.init_display()

    def command(self, cmd):
        i2c.write(self.addr, bytearray([0x00, cmd]))

    def init_display(self):
        for cmd in [
            0xAE, 0x20, 0x02, 0xB0,
            0xC8, 0x00, 0x10, 0x40,
            0x81, 0x7F, 0xA1, 0xA6,
            0xA8, 0x3F, 0xA4, 0xD3,
            0x00, 0xD5, 0x80, 0xD9,
            0xF1, 0xDA, 0x12, 0xDB,
            0x40, 0x8D, 0x14, 0xAF
        ]:
            self.command(cmd)

        self.clear()
        self.show()

    def clear(self):
        # Limpia la memoria sin actualizar la pantalla.
        for i in range(len(self.buffer)):
            self.buffer[i] = 0

    def show(self):
        for page in range(8):
            self.command(0xB0 + page)
            self.command(0x00)
            self.command(0x10)

            start = self.width * page
            end = start + self.width

            i2c.write(
                self.addr,
                b'\x40' + self.buffer[start:end]
            )

    def pixel(self, x, y, color):
        if x < 0 or x >= self.width:
            return
        if y < 0 or y >= self.height:
            return

        index = x + (y // 8) * self.width
        bit = 1 << (y % 8)

        if color:
            self.buffer[index] |= bit
        else:
            self.buffer[index] &= 255 ^ bit

    def text(self, texto, x, y):
        for caracter in texto:
            self.char(caracter, x, y)
            x += 6

    def char(self, caracter, x, y):
        datos = FUENTE.get(caracter, FUENTE[" "])

        for columna in range(5):
            linea = datos[columna]

            for fila in range(8):
                self.pixel(
                    x + columna,
                    y + fila,
                    linea & 1
                )
                linea >>= 1


# ============================================
# SENSOR DE HUMEDAD DEL SUELO
# ============================================

def leer_humedad_suelo():
    suma = 0

    # Promedia diez lecturas para reducir variaciones.
    for i in range(10):
        suma += sensor_suelo.read_analog()
        sleep(10)

    valor = suma // 10

    porcentaje = (
        (VALOR_SECO - valor) * 100
        // (VALOR_SECO - VALOR_HUMEDO)
    )

    porcentaje = max(0, min(100, porcentaje))

    print("Lectura suelo:", valor, "Humedad:", porcentaje)

    return valor, porcentaje


# ============================================
# CONTROL DE LEDS
# ============================================

def apagar_leds():
    led_verde.write_digital(0)
    led_amarillo.write_digital(0)
    led_rojo.write_digital(0)


def actualizar_estado(humedad):
    apagar_leds()

    if humedad >= 60:
        led_verde.write_digital(1)
        return "VERDE"

    elif humedad >= 30:
        led_amarillo.write_digital(1)
        return "AMARILLO"

    else:
        led_rojo.write_digital(1)
        return "ROJO"


# ============================================
# INICIO
# ============================================

apagar_leds()
oled = OLED()

if VALOR_SECO == VALOR_HUMEDO:
    oled.text("ERROR CALIBRACION", 0, 0)
    oled.text("SECO Y HUMEDO", 0, 16)
    oled.text("DEBEN SER DISTINTOS", 0, 28)
    oled.show()

    while True:
        sleep(1000)

display.show(Image.HAPPY)

# ============================================
# BUCLE PRINCIPAL
# ============================================

while True:
    lectura, humedad = leer_humedad_suelo()
    estado = actualizar_estado(humedad)

    oled.clear()

    oled.text("SMARTPLANT", 0, 0)
    oled.text("HUMEDAD: " + str(humedad) + "%", 0, 16)
    oled.text("ESTADO: " + estado, 0, 32)
    oled.text("LECTURA: " + str(lectura), 0, 48)

    oled.show()
    sleep(1000)
