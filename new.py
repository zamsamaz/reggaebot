#CONFERIR PULLUP E PULLDOWN DO SENSOR DE NIVEL


import RPi.GPIO as gpio
import time, datetime
import json

gpio.setmode(gpio.BCM)

# SETUP DO PINO DO SENSOR SUPERIOR DE NIVEL DO TANQUE
pino_sensor_superior_nivel = 10
gpio.setup(pino_sensor_superior_nivel, gpio.IN, pull_up_down = gpio.PUD_DOWN)

# SETUP DO PINO DO SENSOR INFERIOR DE NIVEL DO TANQUE
pino_sensor_inferior_nivel = 11
gpio.setup(pino_sensor_inferior_nivel, gpio.IN, pull_up_down = gpio.PUD_DOWN)

# SETUP DO RELE DA SOLENOIDE DA AGUA
pino_solenoide = 12
gpio.setup(pino_solenoide, gpio.OUT)

def callback_tanque_cheio(pino_sensor_superior_nivel):
    if gpio.input(pino_sensor_superior_nivel):
        #desativa solenoide da agua
        gpio.output(pino_solenoide, LOW)
        #faz solucao nutritiva
        

def callback_tanque_vazio(pino_sensor_inferior_nivel):
    #ativa solenoide da agua
    gpio.output(pino_solenoide, HIGH)

        
gpio.add_event_detect(pino_sensor_inferior_nivel, gpio.HIGH, bouncetime=300)
gpio.add_event_callback(pino_sensor_inferior_nivel, callback_tanque_vazio)

gpio.add_event_detect(pino_sensor_superior_nivel, gpio.LOW, bouncetime=300)
gpio.add_event_callback(pino_sensor_superior_nivel, callback_tanque_cheio)


while True:

    atualiza_fila_de_alimentacao
        get_umidade_vasos()
        add_vasos_fila

    alimenta(fila_de_alimentacao)
        while 





###################
###serial comms####
###################

import serial

full_json = ""

ser0 = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
ser0.reset_input_buffer()

ser1 = serial.Serial('/dev/ttyACM1', 9600, timeout=1)
ser1.reset_input_buffer()

ser2 = serial.Serial('/dev/ttyACM02', 9600, timeout=1)
ser2.reset_input_buffer()


while True:
    if ser0.in_waiting > 0:
        line0 = ser0.readline().decode('utf-8').rstrip()
        full_json = full_json+line0
    if ser1.in_waiting > 0:
        line1 = ser1.readline().decode('utf-8').rstrip()
        full_json = full_json+line1
    if ser2.in_waiting > 0:
        line2 = ser2.readline().decode('utf-8').rstrip()
        full_json = full_json+line2


full_json = json.loads(full_json)

tds_list = []
tds_list.append(full_json["vaso_1"]["tds"])
tds_list.append(full_json["vaso_2"]["tds"])
tds_list.append(full_json["vaso_3"]["tds"])
tds_list.append(full_json["vaso_4"]["tds"])
tds_list.append(full_json["vaso_5"]["tds"])
tds_list.append(full_json["vaso_6"]["tds"])
tds_list.append(full_json["vaso_7"]["tds"])
tds_list.append(full_json["vaso_8"]["tds"])
tds_list.append(full_json["vaso_9"]["tds"])

umidade_list = []
umidade_list.append(full_json["vaso_1"]["umidade"])
umidade_list.append(full_json["vaso_2"]["umidade"])
umidade_list.append(full_json["vaso_3"]["umidade"])
umidade_list.append(full_json["vaso_4"]["umidade"])
umidade_list.append(full_json["vaso_5"]["umidade"])
umidade_list.append(full_json["vaso_6"]["umidade"])
umidade_list.append(full_json["vaso_7"]["umidade"])
umidade_list.append(full_json["vaso_8"]["umidade"])
umidade_list.append(full_json["vaso_9"]["umidade"])

tanque_tds = full_json["tanque"]["tds"]
tanque_pH = full_json["tanque"]["pH"]


