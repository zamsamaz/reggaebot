#-*- coding: utf-8 -*-

import RPi.GPIO as gpio
from time import sleep
from datetime import datetime
import json
from greenutils import GHMicroGrowChart as GH
import serial
import sys

print("começando o setup")
print("fetchando arquivo de config")
config = open('config.json',mode='r')
config = json.load(config)
init_date = config['init_date']
ph_ideal = float(config['ph_ideal'])
init_date = datetime.strptime(init_date, '%b %d %Y %I:%M%p')
minimum_moisture = int(config['minimum_moisture'])
vazao_peristaltica = 0.666 # 0.666 ml/s
print("config lida")
print("setando pinos")
gpio.setmode(gpio.BOARD)

# SETUP DO PINO DO SENSOR SUPERIOR DE NIVEL DO TANQUE
pino_sensor_superior_nivel = 24
gpio.setup(pino_sensor_superior_nivel, gpio.IN, pull_up_down = gpio.PUD_DOWN)

# SETUP DO PINO DO SENSOR INFERIOR DE NIVEL DO TANQUE
pino_sensor_inferior_nivel = 26
gpio.setup(pino_sensor_inferior_nivel, gpio.IN, pull_up_down = gpio.PUD_DOWN)

# SETUP DO PINO DO SENSOR INFERIOR DE NIVEL DO TANQUE (FAILSAFE)
pino_failsafe_inferior_nivel = 23
gpio.setup(pino_failsafe_inferior_nivel, gpio.IN, pull_up_down = gpio.PUD_DOWN)


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
print("pinos setados")
print("setup feito")

def get_sensor_data():

    print("obtendo dados de sensores")
    full_json = ""
    print("setando serial")

    ser0 = serial.Serial('/dev/ttyUSB0', 115200, timeout=0.1)
    ser1 = serial.Serial('/dev/ttyUSB1', 115200, timeout=0.1)
    ser2 = serial.Serial('/dev/ttyUSB2', 115200, timeout=0.1)

    print("serial setada")

    ser0.reset_input_buffer()
    ser1.reset_input_buffer()
    ser2.reset_input_buffer()

    while ser0.in_waiting == 0:
        ser0.write(b"sendit\n")
        print("enviada serial 1")
        sleep(0.5)
    else:
        line0 = ser0.readall().decode('utf-8').rstrip()
        print("resposta serial 1: ", line0)
        order_of_line0_in_json = line0[:1]
        line0 = line0[2:]


    while ser1.in_waiting == 0:
        ser1.write(b"sendit\n")
        print("enviada serial 2")
        sleep(0.5)
    else:
        line1 = ser1.readall().decode('utf-8').rstrip()
        print("resposta serial 2: ", line1)
        order_of_line1_in_json = line1[:1]
        line1 = line1[2:]


    while ser2.in_waiting == 0:
        ser2.write(b"sendit\n")
        print("enviada serial 3")
        sleep(0.5)
    else:
        line2 = ser2.readall().decode('utf-8').rstrip()
        print("resposta serial 3: ", line2)
        order_of_line2_in_json = line2[:1]
        line2 = line2[2:]

    if order_of_line0_in_json == "1":
        full_json = full_json+line0
    if order_of_line1_in_json == "1":
        full_json = full_json+line1
    if order_of_line2_in_json == "1":
        full_json = full_json+line2

    if order_of_line0_in_json == "2":
        full_json = full_json+line0
    if order_of_line1_in_json == "2":
        full_json = full_json+line1
    if order_of_line2_in_json == "2":
        full_json = full_json+line2


    if order_of_line0_in_json == "3":
        full_json = full_json+line0
    if order_of_line1_in_json == "3":
        full_json = full_json+line1
    if order_of_line2_in_json == "3":
        full_json = full_json+line2

    print("resposta completa json: " , full_json)
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
    print("resultados do get_sensors: ",
          tds_list, umidade_list, tanque_tds, tanque_pH)

    return tds_list, umidade_list, tanque_tds, tanque_pH


def atualiza_fila_de_alimentacao(umidade_list):
    print("atualizando fila de alimentacao")
    i = 0
    fila = []
    while i<len(umidade_list):
        if int(umidade_list[i])<minimum_moisture:
            fila.append(i)
        i = i + 1
    print("fila: ", fila)
    print("fila atualizada")
    return fila


def get_current_week(initial_date):

    days = (initial_date - datetime.now())
    days = abs(days.days)
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
    print("obtendo growchart")
    growchart_getter = GH.Getters()
    todays_nutes = growchart_getter.get_nutrient_parameters_by_week_and_feeding_regime(week, "medium")
    todays_tds = (float(todays_nutes["PPM range (500 scale)"].split('-')[0])+float(todays_nutes["PPM range (500 scale)"].split('-')[1]))/2
    print("nutrientes do dia calculados")

    global pino_sensor_superior_nivel
    global pino_sensor_inferior_nivel
    global pino_failsafe_inferior_nivel

    global pino_solenoide
    global pino_rele_vaso_1
    global pino_rele_vaso_2
    global pino_rele_vaso_3
    global pino_rele_vaso_4
    global pino_rele_vaso_5
    global pino_rele_vaso_6
    global pino_rele_vaso_7
    global pino_rele_vaso_8
    global pino_rele_vaso_9

# SETUP DOS PINOS DOS RELES DA BOMBA DE AGUA DO SHAKER
    global pino_rele_shaker

# SETUP DOS PINOS DAS BOMBAS PERISTALTICAS
    global pino_rele_peristaltica_bloom
    global pino_rele_peristaltica_gro
    global pino_rele_peristaltica_micro
    global pino_rele_peristaltica_phup
    global pino_rele_peristaltica_phdown

    for vaso in fila:
        print("alimentando vaso: ", vaso)
        print("tanque ainda não está vazio, ligando shaker")
        turn_shaker_on()
        sleep(120)
        turn_shaker_off()
        print("desligando o shaker pre alimentacao")
        while tds < todays_tds:
            tds_list, umidade_list, tanque_tds, tanque_pH = get_sensor_data()
            if vaso == 0:
                print("alimentando vaso 1")
                gpio.output(pino_rele_vaso_1, gpio.HIGH)
                sleep(5)
                if gpio.input(pino_sensor_inferior_nivel and pino_failsafe_inferior_nivel):
                    gpio.output(pino_rele_vaso_1, gpio.LOW)
                    cria_solucao()
                tds = tds_list[0]
            if vaso == 1:
                print("alimentando vaso 2")
                gpio.output(pino_rele_vaso_2, gpio.HIGH)
                sleep(5)
                if gpio.input(pino_sensor_inferior_nivel and pino_failsafe_inferior_nivel):
                    gpio.output(pino_rele_vaso_2, gpio.LOW)
                    cria_solucao()
                tds = tds_list[1]
            if vaso == 2:
                print("alimentando vaso 3")
                sleep(5)
                if gpio.input(pino_sensor_inferior_nivel and pino_failsafe_inferior_nivel):
                    gpio.output(pino_rele_vaso_3, gpio.LOW)
                    cria_solucao()
                gpio.output(pino_rele_vaso_3, gpio.HIGH)
                tds = tds_list[2]
            if vaso == 3:
                print("alimentando vaso 4")
                sleep(5)
                if gpio.input(pino_sensor_inferior_nivel and pino_failsafe_inferior_nivel):
                    gpio.output(pino_rele_vaso_4, gpio.LOW)
                    cria_solucao()
                gpio.output(pino_rele_vaso_4, gpio.HIGH)
                tds = tds_list[3]
            if vaso == 4:
                print("alimentando vaso 5")
                sleep(5)
                if gpio.input(pino_sensor_inferior_nivel and pino_failsafe_inferior_nivel):
                    gpio.output(pino_rele_vaso_5, gpio.LOW)
                    cria_solucao()
                gpio.output(pino_rele_vaso_5, gpio.HIGH)
                tds = tds_list[4]
            if vaso == 5:
                print("alimentando vaso 6")
                gpio.output(pino_rele_vaso_6, gpio.HIGH)
                sleep(5)
                if gpio.input(pino_sensor_inferior_nivel and pino_failsafe_inferior_nivel):
                    gpio.output(pino_rele_vaso_6, gpio.LOW)
                    cria_solucao()
                tds = tds_list[5]
            if vaso == 6:
                print("alimentando vaso 7")
                gpio.output(pino_rele_vaso_7, gpio.HIGH)
                sleep(5)
                if gpio.input(pino_sensor_inferior_nivel and pino_failsafe_inferior_nivel):
                    gpio.output(pino_rele_vaso_7, gpio.LOW)
                    cria_solucao()
                tds = tds_list[6]
            if vaso == 7:
                print("alimentando vaso 8")
                gpio.output(pino_rele_vaso_8, gpio.HIGH)
                sleep(5)
                if gpio.input(pino_sensor_inferior_nivel and pino_failsafe_inferior_nivel):
                    gpio.output(pino_rele_vaso_8, gpio.LOW)
                    cria_solucao()
                tds = tds_list[7]
            if vaso == 8:
                print("alimentando vaso 9")
                gpio.output(pino_rele_vaso_9, gpio.HIGH)
                sleep(5)
                if gpio.input(pino_sensor_inferior_nivel and pino_failsafe_inferior_nivel):
                    gpio.output(pino_rele_vaso_1, gpio.LOW)
                    cria_solucao()
                tds = tds_list[8]
        else:
            if vaso == 0:
                print("terminando alimentacao do vaso 1")
                gpio.output(pino_rele_vaso_1, gpio.LOW)
            if vaso == 1:
                print("terminando alimentacao do vaso 2")
                gpio.output(pino_rele_vaso_2, gpio.LOW)
            if vaso == 2:
                print("terminando alimentacao do vaso 3")
                gpio.output(pino_rele_vaso_3, gpio.LOW)
            if vaso == 3:
                print("terminando alimentacao do vaso 4")
                gpio.output(pino_rele_vaso_4, gpio.LOW)
            if vaso == 4:
                print("terminando alimentacao do vaso 5")
                gpio.output(pino_rele_vaso_5, gpio.LOW)
            if vaso == 5:
                print("terminando alimentacao do vaso 6")
                gpio.output(pino_rele_vaso_6, gpio.LOW)
            if vaso == 6:
                print("terminando alimentacao do vaso 7")
                gpio.output(pino_rele_vaso_7, gpio.LOW)
            if vaso == 7:
                print("terminando alimentacao do vaso 8")
                gpio.output(pino_rele_vaso_8, gpio.LOW)
            if vaso == 8:
                print("terminando alimentacao do vaso 9")
                gpio.output(pino_rele_vaso_9, gpio.LOW)


def cria_solucao():

    print("tanque vazio, preparando solução")
    while gpio.input(pino_sensor_superior_nivel) == 0:
        gpio.output(pino_solenoide, gpio.HIGH)

    gpio.output(pino_solenoide, gpio.LOW)
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
    print("turning the shaker on baby e sleeping dois minutinhos")
    turn_shaker_on()
    sleep(120)
    tds_list, umidade_list, tanque_tds, tanque_pH = get_sensor_data()

    # as bombas peristalticas tem vazao de 40ml/min com 12v -> 0.666ml/s

    while not todays_minimum_tds < tanque_tds < todays_maximum_tds:

        print("adicionando nutes até chegar no tds correto para a semana")
        print("tanque tds: " , tanque_tds)
        print("minimo tds de hoje: " , todays_minimum_tds)
        print("adding bloom")
        gpio.output(pino_rele_peristaltica_bloom, gpio.HIGH)
        sleep(proportion_bloom*0.1)
        gpio.output(pino_rele_peristaltica_bloom, gpio.LOW)

        print("adding gro")
        gpio.output(pino_rele_peristaltica_gro, gpio.HIGH)
        sleep(proportion_gro*0.1)
        gpio.output(pino_rele_peristaltica_gro, gpio.LOW)

        print("adding micro")
        gpio.output(pino_rele_peristaltica_micro, gpio.HIGH)
        sleep(proportion_micro*0.1)
        gpio.output(pino_rele_peristaltica_micro, gpio.LOW)

        tds_list, umidade_list, tanque_tds, tanque_pH = get_sensor_data()

    print("ajustados nutes")
    while not 420 < tanque_pH < 428:

        print("ajustando ph")
        print("ph do tanque: " , tanque_ph)
        print("ph ideal: " , ph_ideal)


        if tanque_pH < ph_ideal:
            gpio.output(pino_rele_peristaltica_phup, gpio.HIGH)
            sleep(0.1)
            gpio.output(pino_rele_peristaltica_phup, gpio.LOW)

        if tanque_pH > ph_ideal:
            gpio.output(pino_rele_peristaltica_phdown, gpio.HIGH)
            sleep(0.1)
            gpio.output(pino_rele_peristaltica_phdown, gpio.LOW)

        tds_list, umidade_list, tanque_tds, tanque_pH = get_sensor_data()
        sleep(400)
    turn_shaker_off()
    print("tanque cheio novamente e com nutes!")
    return 1


def turn_shaker_on():
    gpio.output(pino_rele_shaker, gpio.HIGH)


def turn_shaker_off():
    gpio.output(pino_rele_shaker, gpio.LOW)


while True:
    try:
        print("000- verificando se alguma planta precisa de alimento")
        tds_list, umidade_list, tanque_tds, tanque_pH = get_sensor_data()
        print("000- atualizando fila de alimentacao")
        fila = atualiza_fila_de_alimentacao(umidade_list)
        print("000- fila : ", fila)
        week = get_current_week(init_date)
        print("000- semana ", week)
        alimenta(fila, week)

        sleep(60*10)
        print("000- aguardando um pouco")
    except:
        print("isso aqui aconteceu: ", sys.exc_info()[0])
        import pdb; pdb.set_trace()
