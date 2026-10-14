# Pruebas de codigo
## 2026 10 14

### Prueba 1
```python
# funcion para leer humedad y temperatura por serial

def on_forever():
    dht11_dht22.query_data(DHTtype.DHT11, DigitalPin.P0, True, False, True)
    humidity = dht11_dht22.read_data(dataType.HUMIDITY)
    temp = dht11_dht22.read_data(dataType.TEMPERATURE)
    serial.write_value("H", humidity)
    serial.write_value("T", temp)
    basic.pause(1000)
basic.forever(on_forever)
```

### Prueba 2
```python
# funcion para transmitir por radio los datos a la otra microbit
# con condicion if sobre los datos/valores "-999"

def on_forever():
    dht11_dht22.query_data(DHTtype.DHT11, DigitalPin.P0, True, False, True)
    humidity = dht11_dht22.read_data(dataType.HUMIDITY)
    temp = dht11_dht22.read_data(dataType.TEMPERATURE)
    #serial.write_value("H", humidity)
    #serial.write_value("T", temp)

    if humidity < 101 and humidity > -1 :
        radio.send_number(humidity)
        basic.pause(1000)

    if temp < 101 and temp > -1 :
        radio.send_number(temp)
        basic.pause(1000)

basic.forever(on_forever)
```
### Prueba 3
```python
# mas adelante se cambia los llamados por serial y pasaria a ser llamado por radio

# Codigo v.2 


# SMARTPLANT - MICROBIT 1
# DHT11 + ENVIO POR RADIO

radio.set_group(1)

def on_forever():
    # Leer DHT11 conectado a P0
    dht11_dht22.query_data(
        DHTtype.DHT11,
        DigitalPin.P0,
        True,
        False,
        True
    )

    humidity = dht11_dht22.read_data(dataType.HUMIDITY)
    temp = dht11_dht22.read_data(dataType.TEMPERATURE)

    # Mostrar datos por serial
    serial.write_value("H", humidity)
    serial.write_value("T", temp)

    # Enviar temperatura por radio
    radio.send_string("T:" + str(temp))

    # Enviar humedad ambiente por radio
    radio.send_string("H:" + str(humidity))

    # Esperar 2 segundos
    basic.pause(2000)

basic.forever(on_forever)
```
