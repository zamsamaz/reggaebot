import RPi.GPIO as gpio
from time import sleep
from datetime import datetime
import json
from greenutils import GHMicroGrowChart as GH
import serial


config = open('config.json',mode='r')
config = json.load(config)
init_date = config['init_date']
ph_ideal = float(config['ph_ideal'])
init_date = datetime.strptime(init_date, '%b %d %Y %I:%M%p')
minimum_moisture = int(config['minimum_moisture'])
tanque_vazio = False
vazao_peristaltica = 0.666 # 0.666 ml/s

gpio.setmode(gpio.BOARD)

# SETUP DO PINO DO SENSOR SUPERIOR DE NIVEL DO TANQUE
pino_sensor_superior_nivel = 24
gpio.setup(pino_sensor_superior_nivel, gpio.IN, pull_up_down = gpio.PUD_DOWN)

# SETUP DO PINO DO SENSOR INFERIOR DE NIVEL DO TANQUE
pino_sensor_inferior_nivel = 26
gpio.setup(pino_sensor_inferior_nivel, gpio.IN, pull_up_down = gpio.PUD_DOWN)

# SETUP DO RELE DA SOLENOIDE DA AGUA
pino_solenoide = 38
gpio.setup(pino_solenoide, gpio.OUT)

# SETUP DOS PINOS DOS RELES DE BOMBAS DE AGUA DE ALIMENTACAO
pino_rele_vaso_1 = 33
gpio.setup(pino_rele_vaso_1, gpio.OUT)
pino_rele_vaso_2 = 35
gpio.setup(pino_rele_vaso_2, gpio.OUT)
pino_rele_vaso_3 = 37
gpio.setup(pino_rele_vaso_3, gpio.OUT)
pino_rele_vaso_4 = 12
gpio.setup(pino_rele_vaso_4, gpio.OUT)
pino_rele_vaso_5 = 16
gpio.setup(pino_rele_vaso_5, gpio.OUT)
pino_rele_vaso_6 = 18
gpio.setup(pino_rele_vaso_6, gpio.OUT)
pino_rele_vaso_7 = 22
gpio.setup(pino_rele_vaso_7, gpio.OUT)
pino_rele_vaso_8 = 32
gpio.setup(pino_rele_vaso_8, gpio.OUT)
pino_rele_vaso_9 = 36
gpio.setup(pino_rele_vaso_9, gpio.OUT)

# SETUP DOS PINOS DOS RELES DA BOMBA DE AGUA DO SHAKER
pino_rele_shaker = 31
gpio.setup(pino_rele_shaker, gpio.OUT)

# SETUP DOS PINOS DAS BOMBAS PERISTALTICAS
pino_rele_peristaltica_bloom = 7
gpio.setup(pino_rele_peristaltica_bloom, gpio.OUT)
pino_rele_peristaltica_gro = 11
gpio.setup(pino_rele_peristaltica_gro, gpio.OUT)
pino_rele_peristaltica_micro = 13
gpio.setup(pino_rele_peristaltica_micro, gpio.OUT)
pino_rele_peristaltica_phup = 15
gpio.setup(pino_rele_peristaltica_phup, gpio.OUT)
pino_rele_peristaltica_phdown = 29
gpio.setup(pino_rele_peristaltica_phdown, gpio.OUT)


ser0 = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
ser1 = serial.Serial('/dev/ttyUSB1', 9600, timeout=1)
ser2 = serial.Serial('/dev/ttyUSB2', 9600, timeout=1)


def get_sensor_data():

    full_json = ""

    ser0.reset_input_buffer()
    ser1.reset_input_buffer()
    ser2.reset_input_buffer()

    ser0.write(b"sendit\n")
    ser1.write(b"sendit\n")
    ser2.write(b"sendit\n")

    sleep(5)

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

    return tds_list, umidade_list, tanque_tds, tanque_pH


def atualiza_fila_de_alimentacao(umidade_list):
    i = 0
    fila = []
    while i<len(umidade_list):
        if umidade_list[i]<minimum_moisture:
            fila.append(i)
    return fila


def get_current_week(initial_date):
    days = (initial_date - datetime.now())
    if 1 <= days <= 7:
        return "a"
    if 8 <= days <= 14:
        return "b"
    if 15 <= days <= 21:
        return "c"
    if 22 <= days <= 28:
        return "d"
    if 29 <= days <= 35:
        return "1"
    if 36 <= days <= 42:
        return "2"
    if 43 <= days <= 49:
        return "3"
    if 50 <= days <= 56:
        return "4"
    if 57 <= days <= 63:
        return "5"
    if 64 <= days <= 70:
        return "6"
    if 71 <= days <= 77:
        return "7"
    if 78 <= days <= 84:
        return "8"
    if 85 <= days <= 91:
        return "9"


def alimenta(fila, week):

    tds = 0
    tank_capacity = 7 #7 litros
    growchart_getter = GH.Getters()
    todays_nutes = growchart_getter.get_nutrient_parameters_by_week_and_feeding_regime(week, "medium")
    todays_tds = (float(todays_nutes["PPM range (500 scale)"].split('-')[0])+float(todays_nutes["PPM range (500 scale)"].split('-')[1]))/2

    for vaso in fila:
        if tanque_vazio == False:
            turn_shaker_on()
            sleep(120)
            turn_shaker_off()
            while tds < todays_tds:
                tds_list, umidade_list, tanque_tds, tanque_pH = get_sensor_data()
                if vaso == 0:
                    gpio.output(pino_rele_vaso_1, HIGH)
                    tds = tds_list[0]
                if vaso == 1:
                    gpio.output(pino_rele_vaso_2, HIGH)
                    tds = tds_list[1]
                if vaso == 2:
                    gpio.output(pino_rele_vaso_3, HIGH)
                    tds = tds_list[2]
                if vaso == 3:
                    gpio.output(pino_rele_vaso_4, HIGH)
                    tds = tds_list[3]
                if vaso == 4:
                    gpio.output(pino_rele_vaso_5, HIGH)
                    tds = tds_list[4]
                if vaso == 5:
                    gpio.output(pino_rele_vaso_6, HIGH)
                    tds = tds_list[5]
                if vaso == 6:
                    gpio.output(pino_rele_vaso_7, HIGH)
                    tds = tds_list[6]
                if vaso == 7:
                    gpio.output(pino_rele_vaso_8, HIGH)
                    tds = tds_list[7]
                if vaso == 8:
                    gpio.output(pino_rele_vaso_9, HIGH)
                    tds = tds_list[8]
            else:
                if vaso == 0:
                    gpio.output(pino_rele_vaso_1, LOW)
                if vaso == 1:
                    gpio.output(pino_rele_vaso_2, LOW)
                if vaso == 2:
                    gpio.output(pino_rele_vaso_3, LOW)
                if vaso == 3:
                    gpio.output(pino_rele_vaso_4, LOW)
                if vaso == 4:
                    gpio.output(pino_rele_vaso_5, LOW)
                if vaso == 5:
                    gpio.output(pino_rele_vaso_6, LOW)
                if vaso == 6:
                    gpio.output(pino_rele_vaso_7, LOW)
                if vaso == 7:
                    gpio.output(pino_rele_vaso_8, LOW)
                if vaso == 8:
                    gpio.output(pino_rele_vaso_9, LOW)

        if tanque_vazio == True:
            #faz solucao nutritiva
            tank_capacity = 7 #7 litros
            growchart_getter = GH.Getters()
            todays_nutes = growchart_getter.adjust_solution_quantities_based_on_tank_capacity(todays_nutes, tank_capacity)
            todays_tds = todays_nutes["PPM range (500 scale)"]
            todays_micro = float(todays_nutes["FloraMicro"])
            todays_gro = float(todays_nutes["FloraGro"])
            todays_bloom = float(todays_nutes["FloraBloom"])
            todays_tds = todays_tds.split('-')
            todays_minimum_tds, todays_maximum_tds = float(todays_tds[0]), float(todays_tds[1])
            total_nutes = todays_gro + todays_bloom + todays_micro
            proportion_gro = todays_gro * (1/total_nutes)
            proportion_bloom = todays_bloom * (1/total_nutes)
            proportion_micro = todays_micro * (1/total_nutes)
            turn_shaker_on()
            sleep(120)
            tds_list, umidade_list, tanque_tds, tanque_pH = get_sensor_data()

            # as bombas peristalticas tem vazao de 40ml/min com 12v -> 0.666ml/s

            while not todays_minimum_tds < tanque_tds < todays_maximum_tds:

                gpio.output(pino_rele_peristaltica_bloom, HIGH)
                sleep(proportion_bloom*0.1)
                gpio.output(pino_rele_peristaltica_bloom, LOW)


                gpio.output(pino_rele_peristaltica_gro, HIGH)
                sleep(proportion_gro*0.1)
                gpio.output(pino_rele_peristaltica_gro, LOW)

                gpio.output(pino_rele_peristaltica_micro, HIGH)
                sleep(proportion_micro*0.1)
                gpio.output(pino_rele_peristaltica_micro, LOW)

                tds_list, umidade_list, tanque_tds, tanque_pH = get_sensor_data()

            while not ph_ideal-0.2 < tanque_pH < ph_ideal +0.2:

                if tanque_pH < ph_ideal:
                    gpio.output(pino_rele_peristaltica_phup, HIGH)
                    sleep(0.1)
                    gpio.output(pino_rele_peristaltica_phup, LOW)

                if tanque_pH > ph_ideal:
                    gpio.output(pino_rele_peristaltica_phdown, HIGH)
                    sleep(0.1)
                    gpio.output(pino_rele_peristaltica_phdown, LOW)

                tds_list, umidade_list, tanque_tds, tanque_pH = get_sensor_data()

            turn_shaker_off()
            tanque_vazio = False


def turn_shaker_on():
    gpio.output(pino_rele_shaker, HIGH)


def turn_shaker_off():
    gpio.output(pino_rele_shaker, LOW)


def callback_tanque_cheio(pino_sensor_superior_nivel):
    if gpio.input(pino_sensor_superior_nivel):
        #desativa solenoide da agua
        gpio.output(pino_solenoide, LOW)


def callback_tanque_vazio(pino_sensor_inferior_nivel):

    tanque_vazio = True

    #desativa a alimentacao dos vasos
    gpio.output(pino_rele_vaso_1, LOW)
    gpio.output(pino_rele_vaso_2, LOW)
    gpio.output(pino_rele_vaso_3, LOW)
    gpio.output(pino_rele_vaso_4, LOW)
    gpio.output(pino_rele_vaso_5, LOW)
    gpio.output(pino_rele_vaso_6, LOW)
    gpio.output(pino_rele_vaso_7, LOW)
    gpio.output(pino_rele_vaso_8, LOW)
    gpio.output(pino_rele_vaso_9, LOW)

    #ativa solenoide da agua
    gpio.output(pino_solenoide, HIGH)


gpio.add_event_detect(pino_sensor_inferior_nivel, gpio.FALLING, bouncetime=300)
gpio.add_event_callback(pino_sensor_inferior_nivel, callback_tanque_vazio)

gpio.add_event_detect(pino_sensor_superior_nivel, gpio.RISING, bouncetime=300)
gpio.add_event_callback(pino_sensor_superior_nivel, callback_tanque_cheio)


while True:
    try:
        tds_list, umidade_list, tanque_tds, tanque_pH = get_sensor_data()
        fila = atualiza_fila_de_alimentacao(umidade_list)
        week = get_current_week()
        alimenta(fila, week)
        sleep(60*10)
    except:
        continue