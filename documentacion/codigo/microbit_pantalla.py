// Codigo microbit_pantalla


from microbit import *
# import machine  # DHT11 desactivado
# import utime     # DHT11 desactivado

sensor_suelo = pin1
# dht_pin = pin2  # DHT11 desactivado

led_verde = pin8
led_amarillo = pin13
led_rojo = pin12

i2c.init(freq=400000, sda=pin20, scl=pin19)


class OLED:
    def __init__(self, width=128, height=64, addr=0x3C):
        self.width = width
        self.height = height
        self.addr = addr
        self.buffer = bytearray(self.width * self.height // 8)
        self.init_display()

    def command(self, cmd):
        i2c.write(self.addr, bytearray([0x00, cmd]))

    def init_display(self):
        for cmd in [
            0xAE, 0x20, 0x00, 0xB0, 0xC8, 0x00, 0x10,
            0x40, 0x81, 0x7F, 0xA1, 0xA6, 0xA8, 0x3F,
            0xA4, 0xD3, 0x00, 0xD5, 0x80, 0xD9, 0xF1,
            0xDA, 0x12, 0xDB, 0x40, 0x8D, 0x14, 0xAF
        ]:
            self.command(cmd)
        self.clear()

    def clear(self):
        for i in range(len(self.buffer)):
            self.buffer[i] = 0
        self.show()

    def show(self):
        for page in range(8):
            self.command(0xB0 + page)
            self.command(0x00)
            self.command(0x10)
            start = self.width * page
            end = start + self.width
            i2c.write(self.addr, b'\x40' + self.buffer[start:end])

    def pixel(self, x, y, color):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return

        index = x + (y // 8) * self.width

        if color:
            self.buffer[index] |= 1 << (y % 8)
        else:
            self.buffer[index] &= ~(1 << (y % 8))

    def text(self, text, x, y):
        for char in text:
            self.char(char, x, y)
            x += 6

    def char(self, char, x, y):
        font = {
            " ": [0,0,0,0,0], "%": [98,100,8,19,35], ":": [0,54,54,0,0],
            "0": [62,81,73,69,62], "1": [0,66,127,64,0],
            "2": [98,81,73,73,70], "3": [34,65,73,73,54],
            "4": [24,20,18,127,16], "5": [39,69,69,69,57],
            "6": [60,74,73,73,48], "7": [1,113,9,5,3],
            "8": [54,73,73,73,54], "9": [6,73,73,41,30],
            "A": [126,17,17,17,126], "B": [127,73,73,73,54],
            "C": [62,65,65,65,34], "D": [127,65,65,34,28],
            "E": [127,73,73,73,65], "F": [127,9,9,9,1],
            "G": [62,65,73,73,122], "H": [127,8,8,8,127],
            "I": [0,65,127,65,0], "J": [32,64,65,63,1],
            "K": [127,8,20,34,65], "L": [127,64,64,64,64],
            "M": [127,2,12,2,127], "N": [127,4,8,16,127],
            "O": [62,65,65,65,62], "P": [127,9,9,9,6],
            "Q": [62,65,81,33,94], "R": [127,9,25,41,70],
            "S": [70,73,73,73,49], "T": [1,1,127,1,1],
            "U": [63,64,64,64,63], "V": [31,32,64,32,31],
            "W": [63,64,56,64,63], "X": [99,20,8,20,99],
            "Y": [7,8,112,8,7], "Z": [97,81,73,69,67],
        }

        data = font.get(char, [0,0,0,0,0])

        for col in range(5):
            line = data[col]
            for row in range(8):
                self.pixel(x + col, y + row, line & 1)
                line >>= 1


oled = OLED()


# =====================================================
# DHT11 - DESACTIVADO TEMPORALMENTE
# Para volver a utilizarlo, quitar los comentarios (#)
# de este bloque y de las otras secciones DHT11.
# =====================================================

# def leer_dht11():
#     dht_pin.write_digital(0)
#     utime.sleep_ms(20)
#     dht_pin.write_digital(1)
#     utime.sleep_us(30)
#
#     datos = []
#
#     try:
#         machine.time_pulse_us(dht_pin, 0, 1000)
#         machine.time_pulse_us(dht_pin, 1, 1000)
#
#         for i in range(40):
#             machine.time_pulse_us(dht_pin, 0, 1000)
#             tiempo = machine.time_pulse_us(dht_pin, 1, 1000)
#
#             if tiempo > 50:
#                 datos.append(1)
#             else:
#                 datos.append(0)
#
#         bytes_dht = []
#
#         for i in range(5):
#             valor = 0
#             for j in range(8):
#                 valor = valor << 1
#                 valor = valor | datos[i * 8 + j]
#             bytes_dht.append(valor)
#
#         checksum = (
#             bytes_dht[0] + bytes_dht[1] +
#             bytes_dht[2] + bytes_dht[3]
#         ) & 255
#
#         if checksum == bytes_dht[4]:
#             return bytes_dht[2], bytes_dht[0]
#
#     except:
#         pass
#
#     return None, None


# =====================================================
# SENSOR DE HUMEDAD DEL SUELO
# =====================================================

def leer_humedad_suelo():
    valor = sensor_suelo.read_analog()

    porcentaje = int((1023 - valor) * 100 / 1023)

    if porcentaje < 0:
        porcentaje = 0
    if porcentaje > 100:
        porcentaje = 100

    return porcentaje


# =====================================================
# CONTROL DE LEDS
# =====================================================

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


# =====================================================
# INICIO DEL PROGRAMA
# =====================================================

display.show(Image.HAPPY)
sleep(1000)


# =====================================================
# BUCLE PRINCIPAL
# =====================================================

while True:

    humedad_suelo = leer_humedad_suelo()

    # DHT11 DESACTIVADO
    # temperatura, humedad_ambiente = leer_dht11()

    estado = actualizar_estado(humedad_suelo)

    oled.clear()
    oled.text("SMARTPLANT", 0, 0)
    oled.text("HUMEDAD: " + str(humedad_suelo) + "%", 0, 16)
    oled.text("ESTADO:", 0, 28)
    oled.text(estado, 0, 40)

    # =================================================
    # MOSTRAR TEMPERATURA - DHT11 DESACTIVADO
    # =================================================

    # if temperatura is not None:
    #     oled.text("TEMP: " + str(temperatura) + "C", 0, 52)
    # else:
    #     oled.text("DHT ERROR", 0, 52)

    oled.show()

    sleep(1500)



// Codigo v2 "Completo"


from microbit import *
import radio

# ============================================
# SMARTPLANT - MICROBIT 2
# HUMEDAD SUELO + OLED + LEDS + RADIO
# ============================================

# Pines
sensor_suelo = pin1

led_verde = pin8
led_amarillo = pin13
led_rojo = pin12

# Configuracion de radio
radio.config(group=1, channel=7, length=64, queue=10)
radio.on()

# Configuracion OLED
i2c.init(freq=400000, sda=pin20, scl=pin19)


# ============================================
# CONTROLADOR OLED
# ============================================

class OLED:
    def __init__(self, width=128, height=64, addr=0x3C):
        self.width = width
        self.height = height
        self.addr = addr
        self.buffer = bytearray(
            self.width * self.height // 8
        )
        self.init_display()

    def command(self, cmd):
        i2c.write(
            self.addr,
            bytearray([0x00, cmd])
        )

    def init_display(self):
        for cmd in [
            0xAE, 0x20, 0x00, 0xB0,
            0xC8, 0x00, 0x10, 0x40,
            0x81, 0x7F, 0xA1, 0xA6,
            0xA8, 0x3F, 0xA4, 0xD3,
            0x00, 0xD5, 0x80, 0xD9,
            0xF1, 0xDA, 0x12, 0xDB,
            0x40, 0x8D, 0x14, 0xAF
        ]:
            self.command(cmd)

        self.clear()

    def clear(self):
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

        if color:
            self.buffer[index] |= 1 << (y % 8)
        else:
            self.buffer[index] &= ~(1 << (y % 8))

    def text(self, text, x, y):
        for char in text:
            self.char(char, x, y)
            x += 6

    def char(self, char, x, y):
        font = {
            " ": [0,0,0,0,0],
            "%": [98,100,8,19,35],
            ":": [0,54,54,0,0],
            "-": [8,8,8,8,8],
            ".": [0,96,96,0,0],
            "0": [62,81,73,69,62],
            "1": [0,66,127,64,0],
            "2": [98,81,73,73,70],
            "3": [34,65,73,73,54],
            "4": [24,20,18,127,16],
            "5": [39,69,69,69,57],
            "6": [60,74,73,73,48],
            "7": [1,113,9,5,3],
            "8": [54,73,73,73,54],
            "9": [6,73,73,41,30],
            "A": [126,17,17,17,126],
            "B": [127,73,73,73,54],
            "C": [62,65,65,65,34],
            "D": [127,65,65,34,28],
            "E": [127,73,73,73,65],
            "F": [127,9,9,9,1],
            "G": [62,65,73,73,122],
            "H": [127,8,8,8,127],
            "I": [0,65,127,65,0],
            "J": [32,64,65,63,1],
            "K": [127,8,20,34,65],
            "L": [127,64,64,64,64],
            "M": [127,2,12,2,127],
            "N": [127,4,8,16,127],
            "O": [62,65,65,65,62],
            "P": [127,9,9,9,6],
            "Q": [62,65,81,33,94],
            "R": [127,9,25,41,70],
            "S": [70,73,73,73,49],
            "T": [1,1,127,1,1],
            "U": [63,64,64,64,63],
            "V": [31,32,64,32,31],
            "W": [63,64,56,64,63],
            "X": [99,20,8,20,99],
            "Y": [7,8,112,8,7],
            "Z": [97,81,73,69,67],
        }

        data = font.get(char, [0,0,0,0,0])

        for col in range(5):
            line = data[col]

            for row in range(8):
                self.pixel(
                    x + col,
                    y + row,
                    line & 1
                )
                line >>= 1


# Crear pantalla
oled = OLED()


# ============================================
# VARIABLES DEL DHT11 REMOTO
# ============================================

temperatura = None
humedad_ambiente = None
ultima_recepcion = -1


# ============================================
# RECIBIR DATOS POR RADIO
# ============================================

def recibir_datos():
    global temperatura
    global humedad_ambiente
    global ultima_recepcion

    while True:
        paquete = radio.receive_bytes()

        if paquete is None:
            break

        try:
            # Paquete de texto de MakeCode
            if len(paquete) < 13:
                continue

            if paquete[3] != 2:
                continue

            longitud = paquete[12]

            if len(paquete) < 13 + longitud:
                continue

            mensaje = paquete[
                13:13 + longitud
            ].decode("ascii")

            if mensaje.startswith("T:"):
                temperatura = float(
                    mensaje[2:]
                )
                ultima_recepcion = running_time()

            elif mensaje.startswith("H:"):
                humedad_ambiente = float(
                    mensaje[2:]
                )
                ultima_recepcion = running_time()

        except (ValueError, UnicodeError, IndexError):
            pass


# ============================================
# HUMEDAD DEL SUELO
# ============================================

def leer_humedad_suelo():
    valor = sensor_suelo.read_analog()

    porcentaje = int(
        (1023 - valor) * 100 / 1023
    )

    if porcentaje < 0:
        porcentaje = 0

    if porcentaje > 100:
        porcentaje = 100

    return porcentaje


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

display.show(Image.HAPPY)
sleep(1000)


# ============================================
# BUCLE PRINCIPAL
# ============================================

while True:

    # Recibir informacion del DHT11
    recibir_datos()

    # Leer humedad del suelo
    humedad_suelo = leer_humedad_suelo()

    # Actualizar estado de los LEDs
    estado = actualizar_estado(
        humedad_suelo
    )

    # Comprobar conexion por radio
    conexion = (
        ultima_recepcion >= 0
        and running_time() - ultima_recepcion < 10000
    )

    # Actualizar OLED
    oled.clear()

    oled.text("SMARTPLANT", 0, 0)

    oled.text(
        "SUELO: " + str(humedad_suelo) + "%",
        0, 12
    )

    oled.text(
        "ESTADO: " + estado,
        0, 24
    )

    if conexion and temperatura is not None:
        oled.text(
            "TEMP: " + str(temperatura) + "C",
            0, 36
        )
    else:
        oled.text("TEMP: --", 0, 36)

    if conexion and humedad_ambiente is not None:
        oled.text(
            "H.AIRE: " + str(humedad_ambiente) + "%",
            0, 48
        )
    else:
        oled.text("H.AIRE: --", 0, 48)

    oled.show()

    sleep(500)
