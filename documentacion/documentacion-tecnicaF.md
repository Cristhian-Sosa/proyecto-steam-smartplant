# Documentación Técnica

*Fecha: 04 de noviembre de 2026*

Este documento contiene la documentación técnica del proyecto **SmartPlant – Maceta Inteligente**, desarrollado para el proyecto STEAM del curso **Laboratorio STEAM+** de la tecnicatura **Redes y Software** del **Instituto Superior Brazo Oriental** de **UTU**, año 2026.

# Proyecto: SmartPlant – Maceta Inteligente

## 1. Integrantes
- Cristhian Sosa
- Agustin Antelo
- Emiliano Pérez
- Gabriel Perlas

## 2. Descripción
SmartPlant es un prototipo de maceta inteligente cuyo objetivo es facilitar el seguimiento de la humedad del suelo de una planta. El sistema utiliza una **BBC Micro:bit V2** para leer la señal de un **sensor capacitivo de humedad del suelo** y está diseñado para presentar la información en una **pantalla OLED**.

El sensor capacitivo detecta cambios relacionados con la humedad de la tierra. La Micro:bit procesa las lecturas y permite determinar si el sustrato está más seco o más húmedo, según los valores de referencia obtenidos durante la calibración. La pantalla OLED facilita la consulta de las mediciones sin necesidad de conectar el proyecto a una computadora.

El alcance de este documento corresponde a los componentes indicados por el equipo. Las conexiones y el programa de ejemplo se deberán ajustar al modelo concreto de pantalla OLED y a las pruebas realizadas con el prototipo.

## 3. Materiales

| Imagen | Descripción | Función |
| --- | --- | --- |
| *Agregar foto de la Micro:bit V2* | **BBC Micro:bit V2** | Microcontrolador que recibe y procesa las mediciones. |
| *Agregar foto del sensor* | **Sensor capacitivo de humedad del suelo** | Detecta cambios de humedad en el sustrato. |
| *Agregar foto de la pantalla* | **Pantalla OLED** | Visualiza la información de humedad. |
| *Agregar foto de los cables* | **Cables jumper** | Realizan las conexiones eléctricas entre los módulos. |

**Nota:** Se debe verificar cómo se conecta físicamente cada módulo a los pines de la Micro:bit. Si el montaje utiliza una tarjeta de expansión, incluirla en esta tabla y documentar su modelo.

## 4. Diseño Mecánico

El prototipo SmartPlant se organiza alrededor de una maceta con tierra y una planta. El **sensor capacitivo** se coloca dentro del sustrato, en una posición adecuada para registrar los cambios de humedad. La **Micro:bit V2** y la **pantalla OLED** se ubican fuera de la tierra, en una zona protegida de salpicaduras y del contacto directo con el agua.

Los **cables jumper** conectan el sensor y la pantalla con la Micro:bit. Durante el montaje se debe procurar que los cables queden ordenados y que la electrónica permanezca accesible para realizar pruebas, ajustes y mantenimiento. La forma definitiva del soporte o de la caja protectora queda pendiente de documentar según el prototipo construido.

**Registro fotográfico pendiente:**

- Fotografía general de la maceta y los componentes instalados.
- Fotografía de la posición del sensor capacitivo en el sustrato.
- Fotografía de la Micro:bit y la pantalla OLED conectadas.

## 5. Diseño Electrónico

La Micro:bit recibe la señal del sensor capacitivo mediante una entrada analógica. Para una **pantalla OLED con interfaz I²C**, la comunicación se realiza a través de las líneas SDA y SCL. Las conexiones siguientes son una **propuesta de referencia**, no un registro confirmado del cableado final del equipo.

### Conexión propuesta del sensor capacitivo

| Pin del sensor | Conexión de referencia | Función |
| --- | --- | --- |
| VCC | 3V de la Micro:bit | Alimentación, **solo si el módulo admite 3,3 V**. |
| GND | GND de la Micro:bit | Tierra común. |
| AOUT / AO | P0 de la Micro:bit | Lectura analógica de humedad. |

El modelo exacto del sensor debe verificarse antes de conectarlo. La entrada analógica de la Micro:bit no debe recibir señales superiores a 3,3 V.

### Conexión propuesta de la pantalla OLED

**Si la pantalla es un modelo I²C compatible con 3,3 V y tiene cuatro pines:**

| Pin OLED | Conexión de referencia | Función |
| --- | --- | --- |
| VCC | 3V de la Micro:bit | Alimentación, previa comprobación de compatibilidad. |
| GND | GND de la Micro:bit | Tierra común. |
| SDA | P20 de la Micro:bit | Datos I²C. |
| SCL | P19 de la Micro:bit | Reloj I²C. |

Si la pantalla utiliza SPI, otros nombres de pines o requiere una tensión diferente, **esta tabla no corresponde** y debe sustituirse por el esquema específico del módulo.

### Cables jumper

Los cables jumper transportan las conexiones de alimentación, tierra y señal entre los componentes. Antes de encender el circuito se debe revisar la identificación de cada pin, la polaridad y la continuidad de las conexiones.

**Diagrama pendiente:** insertar una fotografía o croquis del cableado real una vez confirmados el modelo de OLED y los pines empleados.

## 6. Diseño Software

La programación se realiza en **MicroPython para BBC Micro:bit V2**. El funcionamiento previsto consiste en leer periódicamente el valor analógico del sensor capacitivo, interpretar la medición según una calibración y mostrar el resultado en la pantalla OLED.

### Medición de la humedad del suelo

El sensor capacitivo entrega una señal que cambia según las condiciones del sustrato. La Micro:bit puede leerla mediante `read_analog()`, que devuelve valores entre 0 y 1023. Para convertir esa lectura en un porcentaje orientativo de humedad es necesario medir previamente los valores de referencia en condiciones secas y húmedas. El sentido del cambio puede variar según el módulo.

### Código de prueba de lectura analógica

El siguiente código es un **ejemplo básico de prueba**, no el programa final validado del proyecto. Permite comprobar la lectura del sensor conectado a P0 utilizando la pantalla LED integrada de la Micro:bit.

```python
from microbit import *

while True:
    lectura = pin0.read_analog()
    display.scroll(str(lectura))
    sleep(1000)
```

### Visualización en la pantalla OLED

Para mostrar la humedad en la pantalla OLED se necesita identificar su **controlador** (por ejemplo, SSD1306, si corresponde), su **interfaz de comunicación** y la **biblioteca MicroPython compatible con Micro:bit V2**. El programa final deberá inicializar la pantalla, leer el sensor, aplicar la calibración y actualizar el texto mostrado.

**Pendiente de incorporar:** código real de la OLED, valores de calibración y código integrado utilizado por el equipo. No se incluye una biblioteca no verificada para evitar documentar un programa que podría no funcionar con el módulo adquirido.

### Pruebas y verificación

Para validar el prototipo se propone registrar lecturas del sensor en tierra seca y húmeda, comprobar que los valores cambian de forma coherente y verificar que la OLED muestra los resultados correctamente. Los resultados concretos deberán añadirse una vez obtenidos.

## 7. Referencias y recursos

- Repositorio del proyecto SmartPlant: https://github.com/Cristhian-Sosa/proyecto-steam-smartplant
- Referencia oficial de MicroPython para Micro:bit: https://python.microbit.org/v/3/reference
- Sitio oficial de Micro:bit: https://microbit.org/
- Sitio oficial de Microsoft para Microbit: https://makecode.microbit.org
- Sitio para diseñar componentes físicos con sensores o dispositivos IoT: https://vento.build/es/
- Documentación técnica del fabricante del sensor capacitivo: *pendiente de agregar según modelo*.
- Documentación técnica de la pantalla OLED: *pendiente de agregar según modelo y controlador*.
