#CONFERIR PULLUP E PULLDOWN DO SENSOR DE NIVEL


import RPi.GPIO as gpio
import time, datetime

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
