#!/usr/bin/python3
#-*- coding: utf-8 -*-


import RPi.GPIO as gpio
from time import sleep
from datetime import datetime
import json
from greenutils import GHMicroGrowChart as GHMicro
from greenutils import GHFloraNovaGrowChart as GHFloraNova
import serial
import sys
from unqlite import UnQLite
import smbus

print("starting setup")
db = UnQLite("greenutils/db.log")
print("db set")
print("fetching config file")
config = open('config.json',mode='r')
config = json.load(config)
init_date = config['init_date']
irrigation_events = int(config['irrigation_events'])
nute_type = config['nute_type'] #"floranova" or "micro"
ideal_ph = float(config['ideal_ph'])
min_ph = float(config['min_ph'])
max_ph = float(config['max_ph'])
tank_capacity = float(config['tank_capacity'])
init_date = datetime.strptime(init_date, '%b %d %Y %I:%M%p')
minimum_moisture = int(config['minimum_moisture'])
peristaltic_flow = 0.666 # 0.666 ml/s
print("config file read")

print("setting pins up - or down xD")
gpio.setmode(gpio.BOARD)

# SETUP DO PINO DO SENSOR SUPERIOR DE NIVEL DO TANQUE
superior_level_sensor_pin = 24
gpio.setup(superior_level_sensor_pin, gpio.IN, pull_up_down = gpio.PUD_DOWN)

# SETUP DO PINO DO SENSOR INFERIOR DE NIVEL DO TANQUE
inferior_level_sensor_pin = 26
gpio.setup(inferior_level_sensor_pin, gpio.IN, pull_up_down = gpio.PUD_DOWN)

# SETUP DO PINO DO SENSOR INFERIOR DE NIVEL DO TANQUE (FAILSAFE)
inferior_level_sensor_failsafe_pin = 23
gpio.setup(inferior_level_sensor_failsafe_pin, gpio.IN, pull_up_down = gpio.PUD_DOWN)


# SETUP DO RELE DA SOLENOIDE DA AGUA
solenoid_pin = 38
gpio.setup(solenoid_pin, gpio.OUT)

# SETUP DO RELE DA BOMBA DE DRENAGEM

drainage_relay_pin = 19
gpio.setup(drainage_relay_pin, gpio.OUT)

# SETUP DOS PINOS DOS RELES DE BOMBAS DE AGUA DE ALIMENTACAO
vase_1_relay_pin = 33
gpio.setup(vase_1_relay_pin, gpio.OUT)
vase_2_relay_pin = 35
gpio.setup(vase_2_relay_pin, gpio.OUT)
vase_3_relay_pin = 37
gpio.setup(vase_3_relay_pin, gpio.OUT)
vase_4_relay_pin = 12
gpio.setup(vase_4_relay_pin, gpio.OUT)
vase_5_relay_pin = 16
gpio.setup(vase_5_relay_pin, gpio.OUT)
vase_6_relay_pin = 18
gpio.setup(vase_6_relay_pin, gpio.OUT)
vase_7_relay_pin = 22
gpio.setup(vase_7_relay_pin, gpio.OUT)
vase_8_relay_pin = 32
gpio.setup(vase_8_relay_pin, gpio.OUT)
vase_9_relay_pin = 36
gpio.setup(vase_9_relay_pin, gpio.OUT)

# SETUP DOS PINOS DOS RELES DA BOMBA DE AGUA DO SHAKER
shaker_relay_pin = 31
gpio.setup(shaker_relay_pin, gpio.OUT)

# SETUP DOS PINOS DAS BOMBAS PERISTALTICAS

##### IMPORTANTE #####
# Quando usando floranova, utilizar a peristaltica bloom para ambos os nutes nomeados bloom
# o pino 11, que seria da peristaltica gro no esquema micro é reutilizado para criar o dreno ativo quando usando floranova
##### IMPORTANTE #####

bloom_peristaltic_relay_pin = 7
gpio.setup(bloom_peristaltic_relay_pin, gpio.OUT)
gro_peristaltic_relay_pin = 11
gpio.setup(gro_peristaltic_relay_pin, gpio.OUT)
micro_peristaltic_relay_pin = 13
gpio.setup(micro_peristaltic_relay_pin, gpio.OUT)
phup_peristaltic_relay_pin = 15
gpio.setup(phup_peristaltic_relay_pin, gpio.OUT)
phdown_peristaltic_relay_pin = 29
gpio.setup(phdown_peristaltic_relay_pin, gpio.OUT)
print("pins set up")
print("setup done")

print("setting serial")

ser0 = serial.Serial('/dev/ttyUSB0', 115200, timeout=0.1)
ser1 = serial.Serial('/dev/ttyUSB1', 115200, timeout=0.1)
ser2 = serial.Serial('/dev/ttyUSB2', 115200, timeout=0.1)

print("serial set")

def get_sensor_data():

    print("obtaining sensor data")
    full_json = ""
    ser0.reset_input_buffer()
    sleep(1.5)
    #ser2.reset_input_buffer();sleep(1);
    #import pdb; pdb.set_trace()
    line0 = ser0.readall().decode('utf-8')
    if line0.find("1-") != -1:
        start_index_line0 = line0.find("1-")+2
        order_of_line0_in_json = 1
    if line0.find("2-") != -1:
        start_index_line0 = line0.find("2-")+2
        order_of_line0_in_json = 2
    if line0.find("3-") != -1:
        start_index_line0 = line0.find("3-")+2
        order_of_line0_in_json = 3
    end_index_line0 = line0.find("fim", start_index_line0)
    line0 = line0[start_index_line0:end_index_line0]
    #print("serial 1 response: ", line0)


    ser1.reset_input_buffer()
    sleep(1.5)
    line1 = ser1.readall().decode('utf-8')
    if line1.find("1-") != -1:
        start_index_line1 = line1.find("1-")+2
        order_of_line1_in_json = 1
    if line1.find("2-") != -1:
        start_index_line1 = line1.find("2-")+2
        order_of_line1_in_json = 2
    if line1.find("3-") != -1:
        start_index_line1 = line1.find("3-")+2
        order_of_line1_in_json = 3
    end_index_line1 = line1.find("fim", start_index_line1)
    line1 = line1[start_index_line1:end_index_line1]
    #print("serial 2 response: ", line1)

    ser2.reset_input_buffer()
    sleep(1.5)
    line2 = ser2.readall().decode('utf-8')

    if line2.find("1-") != -1:
        start_index_line2 = line2.find("1-")+2
        order_of_line2_in_json = 1
    if line2.find("2-") != -1:
        start_index_line2 = line2.find("2-")+2
        order_of_line2_in_json = 2
    if line2.find("3-") != -1:
        start_index_line2 = line2.find("3-")+2
        order_of_line2_in_json = 3
    end_index_line2 = line2.find("fim", start_index_line2)
    line2 = line2[start_index_line2:end_index_line2]
    #print("serial 3 response: ", line2)



    if order_of_line0_in_json == 1:
        full_json = full_json+line0
    if order_of_line1_in_json == 1:
        full_json = full_json+line1
    if order_of_line2_in_json == 1:
        full_json = full_json+line2

    if order_of_line0_in_json == 2:
        full_json = full_json+line0
    if order_of_line1_in_json == 2:
        full_json = full_json+line1
    if order_of_line2_in_json == 2:
        full_json = full_json+line2


    if order_of_line0_in_json == 3:
        full_json = full_json+line0
    if order_of_line1_in_json == 3:
        full_json = full_json+line1
    if order_of_line2_in_json == 3:
        full_json = full_json+line2

    temp_string = """, "datetime":" """
    temp_string = temp_string[:-1]
    date_now = str(datetime.now())
    temp_string2 = """ "} """
    temp_string2 = temp_string2[1:]
    temp_string2 = temp_string2[:-1]
    full_json = full_json[:-1]+temp_string+date_now+temp_string2
    print("full response in json format: " , full_json)
    #import pdb; pdb.set_trace()

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

    moisture_list = []
    moisture_list.append(full_json["vaso_1"]["umidade"])
    moisture_list.append(full_json["vaso_2"]["umidade"])
    moisture_list.append(full_json["vaso_3"]["umidade"])
    moisture_list.append(full_json["vaso_4"]["umidade"])
    moisture_list.append(full_json["vaso_5"]["umidade"])
    moisture_list.append(full_json["vaso_6"]["umidade"])
    moisture_list.append(full_json["vaso_7"]["umidade"])
    moisture_list.append(full_json["vaso_8"]["umidade"])
    moisture_list.append(full_json["vaso_9"]["umidade"])

    tank_tds = full_json["tanque"]["tds"]
    tank_ph = full_json["tanque"]["pH"]

    print("get_sensors results: ",
          tds_list, moisture_list, tank_tds, tank_ph)

    #LOG SENSOR DATA

    collection = db.collection("sensor_data")
    collection.create()
    collection.store(full_json)

    return tds_list, moisture_list, tank_tds, float(tank_ph)


def update_feeding_queue(moisture_list):
    print("updating feeding queue")
    i = 0
    queue = []
    while i<len(moisture_list):
        if int(moisture_list[i])>minimum_moisture:
            queue.append(i)
        i = i + 1
    print("queue: ", queue)
    print("queue updated")

    #LOG THIS
    return queue


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


def feed(queue, week):

    tds = 0
    tank_capacity = 7 #7 litros
    print("getting growchart")

    if nute_type == "micro":

        growchart_getter = GHMicro.Getters()
        todays_nutes = growchart_getter.get_nutrient_parameters_by_week_and_feeding_regime(week, "medium")
        todays_tds = (float(todays_nutes["PPM range (500 scale)"].split('-')[0])+float(todays_nutes["PPM range (500 scale)"].split('-')[1]))/2
        print("today's nutes calculated")

    if nute_type == "floranova":

        growchart_getter = GHFloraNova.Getters()
        todays_nutes = growchart_getter.get_nutrient_parameters_by_week(week)
        todays_tds = (float(todays_nutes["max PPM"]))
        print("todays nutes calculated")

    global superior_level_sensor_pin
    global inferior_level_sensor_pin
    global inferior_level_sensor_failsafe_pin

    global solenoid_pin
    global vase_1_relay_pin
    global vase_2_relay_pin
    global vase_3_relay_pin
    global vase_4_relay_pin
    global vase_5_relay_pin
    global vase_6_relay_pin
    global vase_7_relay_pin
    global vase_8_relay_pin
    global vase_9_relay_pin

# SETUP DOS PINOS DOS RELES DA BOMBA DE AGUA DO SHAKER
    global shaker_relay_pin

# SETUP DOS PINOS DAS BOMBAS PERISTALTICAS
    global bloom_peristaltic_relay_pin
    global gro_peristaltic_relay_pin
    global micro_peristaltic_relay_pin
    global phup_peristaltic_relay_pin
    global phdown_peristaltic_relay_pin

    for vase in queue:

        sleep_time = 10
        counter = 0
        global irrigation_events # of sleep_time duration each

        print("tds: ", float(tds))
        print("minimum tds: ", todays_tds-10)
        print("maximum tds: ", todays_tds+10)

        #tds comeca maior pois ha nutrientes ainda na terra antiga provavelmente
        while counter < irrigation_events:
        #while (todays_tds-10 <= float(tds) <= todays_tds+10) == False:

            tds_list, moisture_list, tank_tds, tank_ph = get_sensor_data()
            turn_drainage_on()
            turn_shaker_on()

            print("irrigation event number: ", str(counter+1))
            print("total irrigation events needed: ", str(irrigation_events))

            if vase == 0:
                if not gpio.input(inferior_level_sensor_pin) and not gpio.input(inferior_level_sensor_failsafe_pin):
                    gpio.output(vase_1_relay_pin, gpio.LOW)
                    create_nutritive_solution(todays_nutes)
                    #LOG THIS

                start_time = datetime.now()
                log_data = {"start_time":str(start_time), "vase":"1"}
                collection = db.collection("feed_data")
                collection.create()
                collection.store(log_data)

                print("feeding vase 1")
                gpio.output(vase_1_relay_pin, gpio.HIGH)
                sleep(sleep_time)
                gpio.output(vase_1_relay_pin, gpio.LOW)

                end_time = datetime.now()
                log_data = {"end_time":str(end_time), "vase":"1"}
                collection = db.collection("feed_data")
                collection.create()
                collection.store(log_data)

                tds = tds_list[0]
                counter = counter +1

            if vase == 1:
                if not gpio.input(inferior_level_sensor_pin) and not gpio.input(inferior_level_sensor_failsafe_pin):
                    gpio.output(vase_2_relay_pin, gpio.LOW)
                    create_nutritive_solution(todays_nutes)

                start_time = datetime.now()
                log_data = {"start_time":str(start_time), "vase":"2"}
                collection = db.collection("feed_data")
                collection.create()
                collection.store(log_data)

                print("feeding vase 2")
                gpio.output(vase_2_relay_pin, gpio.HIGH)
                sleep(sleep_time)
                gpio.output(vase_2_relay_pin, gpio.LOW)

                end_time = datetime.now()
                log_data = {"end_time":str(end_time), "vase":"2"}
                collection = db.collection("feed_data")
                collection.create()
                collection.store(log_data)

                tds = tds_list[1]
                counter = counter +1


            if vase == 2:
                if not gpio.input(inferior_level_sensor_pin) and not gpio.input(inferior_level_sensor_failsafe_pin):
                    gpio.output(vase_3_relay_pin, gpio.LOW)
                    create_nutritive_solution(todays_nutes)

                start_time = datetime.now()
                log_data = {"start_time":str(start_time), "vase":"3"}
                collection = db.collection("feed_data")
                collection.create()
                collection.store(log_data)

                print("feeding vase 3")
                gpio.output(vase_3_relay_pin, gpio.HIGH)
                sleep(sleep_time)
                gpio.output(vase_3_relay_pin, gpio.LOW)

                end_time = datetime.now()
                log_data = {"end_time":str(end_time), "vase":"3"}
                collection = db.collection("feed_data")
                collection.create()
                collection.store(log_data)

                tds = tds_list[2]
                counter = counter +1


            if vase == 3:
                if not gpio.input(inferior_level_sensor_pin) and not gpio.input(inferior_level_sensor_failsafe_pin):
                    gpio.output(vase_4_relay_pin, gpio.LOW)
                    create_nutritive_solution(todays_nutes)

                start_time = datetime.now()
                log_data = {"start_time":str(start_time), "vase":"4"}
                collection = db.collection("feed_data")
                collection.create()
                collection.store(log_data)

                print("feeding vase 4")
                gpio.output(vase_4_relay_pin, gpio.HIGH)
                sleep(sleep_time)
                gpio.output(vase_4_relay_pin, gpio.LOW)

                end_time = datetime.now()
                log_data = {"end_time":str(end_time), "vase":"4"}
                collection = db.collection("feed_data")
                collection.create()
                collection.store(log_data)

                tds = tds_list[3]
                counter = counter +1


            if vase == 4:
                if not gpio.input(inferior_level_sensor_pin) and not gpio.input(inferior_level_sensor_failsafe_pin):
                    gpio.output(vase_5_relay_pin, gpio.LOW)
                    create_nutritive_solution(todays_nutes)

                start_time = datetime.now()
                log_data = {"start_time":str(start_time), "vase":"5"}
                collection = db.collection("feed_data")
                collection.create()
                collection.store(log_data)

                print("feeding vase 5")
                gpio.output(vase_5_relay_pin, gpio.HIGH)
                sleep(sleep_time)
                gpio.output(vase_5_relay_pin, gpio.LOW)

                end_time = datetime.now()
                log_data = {"end_time":str(end_time), "vase":"5"}
                collection = db.collection("feed_data")
                collection.create()
                collection.store(log_data)

                tds = tds_list[4]
                counter = counter +1


            if vase == 5:
                if not gpio.input(inferior_level_sensor_pin) and not gpio.input(inferior_level_sensor_failsafe_pin):
                    gpio.output(vase_6_relay_pin, gpio.LOW)
                    create_nutritive_solution(todays_nutes)

                start_time = datetime.now()
                log_data = {"start_time":str(start_time), "vase":"6"}
                collection = db.collection("feed_data")
                collection.create()
                collection.store(log_data)

                print("feeding vase 6")
                gpio.output(vase_6_relay_pin, gpio.HIGH)
                sleep(sleep_time)
                gpio.output(vase_6_relay_pin, gpio.LOW)

                end_time = datetime.now()
                log_data = {"end_time":str(end_time), "vase":"6"}
                collection = db.collection("feed_data")
                collection.create()
                collection.store(log_data)

                tds = tds_list[5]
                counter = counter +1


            if vase == 6:
                if not gpio.input(inferior_level_sensor_pin) and not gpio.input(inferior_level_sensor_failsafe_pin):
                    gpio.output(vase_7_relay_pin, gpio.LOW)
                    create_nutritive_solution(todays_nutes)

                start_time = datetime.now()
                log_data = {"start_time":str(start_time), "vase":"7"}
                collection = db.collection("feed_data")
                collection.create()
                collection.store(log_data)

                print("feeding vase 7")
                gpio.output(vase_7_relay_pin, gpio.HIGH)
                sleep(sleep_time)
                gpio.output(vase_7_relay_pin, gpio.LOW)

                end_time = datetime.now()
                log_data = {"end_time":str(end_time), "vase":"7"}
                collection = db.collection("feed_data")
                collection.create()
                collection.store(log_data)

                tds = tds_list[6]
                counter = counter +1


            if vase == 7:
                if not gpio.input(inferior_level_sensor_pin) and not gpio.input(inferior_level_sensor_failsafe_pin):
                    gpio.output(vase_8_relay_pin, gpio.LOW)
                    create_nutritive_solution(todays_nutes)

                start_time = datetime.now()
                log_data = {"start_time":str(start_time), "vase":"8"}
                collection = db.collection("feed_data")
                collection.create()
                collection.store(log_data)

                print("feeding vase 8")
                gpio.output(vase_8_relay_pin, gpio.HIGH)
                sleep(sleep_time)
                gpio.output(vase_8_relay_pin, gpio.LOW)

                end_time = datetime.now()
                log_data = {"end_time":str(end_time), "vase":"8"}
                collection = db.collection("feed_data")
                collection.create()
                collection.store(log_data)

                tds = tds_list[7]
                counter = counter +1

            if vase == 8:
                if not gpio.input(inferior_level_sensor_pin) and not gpio.input(inferior_level_sensor_failsafe_pin):
                    gpio.output(vase_9_relay_pin, gpio.LOW)
                    create_nutritive_solution(todays_nutes)

                start_time = datetime.now()
                log_data = {"start_time":str(start_time), "vase":"9"}
                collection = db.collection("feed_data")
                collection.create()
                collection.store(log_data)

                print("feeding vase 9")
                gpio.output(vase_9_relay_pin, gpio.HIGH)
                sleep(sleep_time)
                gpio.output(vase_9_relay_pin, gpio.LOW)

                end_time = datetime.now()
                log_data = {"end_time":str(end_time), "vase":"9"}
                collection = db.collection("feed_data")
                collection.create()
                collection.store(log_data)

                tds = tds_list[8]
                counter = counter +1

        else:
            if vase == 0:
                print("finished feeding vase 1")
                gpio.output(vase_1_relay_pin, gpio.LOW)
            if vase == 1:
                print("finished feeding vase 2")
                gpio.output(vase_2_relay_pin, gpio.LOW)
            if vase == 2:
                print("finished feeding vase 3")
                gpio.output(vase_3_relay_pin, gpio.LOW)
            if vase == 3:
                print("finished feeding vase 4")
                gpio.output(vase_4_relay_pin, gpio.LOW)
            if vase == 4:
                print("finished feeding vase 5")
                gpio.output(vase_5_relay_pin, gpio.LOW)
            if vase == 5:
                print("finished feeding vase 6")
                gpio.output(vase_6_relay_pin, gpio.LOW)
            if vase == 6:
                print("finished feeding vase 7")
                gpio.output(vase_7_relay_pin, gpio.LOW)
            if vase == 7:
                print("finished feeding vase 8")
                gpio.output(vase_8_relay_pin, gpio.LOW)
            if vase == 8:
                print("finished feeding vase 9")
                gpio.output(vase_9_relay_pin, gpio.LOW)
            sleep(20)
            turn_drainage_off()
        turn_shaker_off()



def adjust_ph(expected_ph):

    turn_shaker_on()
    tds_list, moisture_list, tank_tds, tank_ph = get_sensor_data()

    while (max_ph <= tank_ph <= min_ph) == False:

        print("adjusting ph")
        print("tank ph: " , tank_ph)
        print("ideal ph: " , ideal_ph)


        if tank_ph < ideal_ph:
            print("increasing ph")
            gpio.output(phup_peristaltic_relay_pin, gpio.HIGH)
            sleep(2)
            gpio.output(phup_peristaltic_relay_pin, gpio.LOW)

        if tank_ph > ideal_ph:
            print("decreasing ph")
            gpio.output(phdown_peristaltic_relay_pin, gpio.HIGH)
            sleep(2)
            gpio.output(phdown_peristaltic_relay_pin, gpio.LOW)

        print("sleepping 60s at:", datetime.now())
        sleep(60)
        print("waking up")
        tds_list, moisture_list, tank_tds, tank_ph = get_sensor_data()

    turn_shaker_off()
    return 1


def create_nutritive_solution(todays_nutes):

    #import pdb; pdb.set_trace()
    print("empty tank, preparing nutritive solution")

    while gpio.input(superior_level_sensor_pin) == 0:
        gpio.output(solenoid_pin, gpio.HIGH)
        sleep(0.1)
        if gpio.input(superior_level_sensor_pin) == 0:
            continue

    gpio.output(solenoid_pin, gpio.LOW)
    #faz solucao nutritiva
    global tank_capacity

    if nute_type == "micro":
        growchart_getter = GHMicro.Getters()
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


    if nute_type == "floranova":
        todays_tds = float(todays_nutes["max PPM"])
        todays_minimum_tds, todays_maximum_tds = todays_tds-30, todays_tds+30

    print("turning the shaker on and sleeping 30 secs")
    turn_shaker_on()
    sleep(30)
    tds_list, moisture_list, tank_tds, tank_ph = get_sensor_data()

    # as bombas peristalticas tem vazao de 40ml/min com 12v -> 0.666ml/s
    while (float(todays_minimum_tds) <= float(tank_tds) <= float(todays_maximum_tds)) == False:

        print("adding nutes until the sensor hits correct week tds")
        print("tank tds: " , tank_tds)
        print("minimum tds for today: " , todays_minimum_tds)

        if nute_type == "micro":

            print("adding bloom")
            gpio.output(bloom_peristaltic_relay_pin, gpio.HIGH)
            sleep(proportion_bloom*0.6)
            gpio.output(bloom_peristaltic_relay_pin, gpio.LOW)

            print("adding gro")
            gpio.output(gro_peristaltic_relay_pin, gpio.HIGH)
            sleep(proportion_gro*0.6)
            gpio.output(gro_peristaltic_relay_pin, gpio.LOW)

            print("adding micro")
            gpio.output(micro_peristaltic_relay_pin, gpio.HIGH)
            sleep(proportion_micro*0.6)
            gpio.output(micro_peristaltic_relay_pin, gpio.LOW)

        if nute_type == "floranova":

            print("adding floranova bloom")
            gpio.output(bloom_peristaltic_relay_pin, gpio.HIGH)
            sleep(0.5)
            gpio.output(bloom_peristaltic_relay_pin, gpio.LOW)


        tds_list, moisture_list, tank_tds, tank_ph = get_sensor_data()

    print("nutes ready")
    adjust_ph(ideal_ph)
    turn_shaker_off()
    print("tank refueled and ready!")

    return 1


def turn_drainage_on():
    print("turning drainage on")
    gpio.output(drainage_relay_pin, gpio.HIGH)


def turn_drainage_off():
    print("turning drainage off")
    gpio.output(drainage_relay_pin, gpio.LOW)


def turn_shaker_on():
    print("turning shaker on")
    gpio.output(shaker_relay_pin, gpio.HIGH)


def turn_shaker_off():
    print("turning shaker off")
    gpio.output(shaker_relay_pin, gpio.LOW)


def log_event_on_database(event, caller):
    return 0


while True:
    #import pdb;pdb.set_trace()
    print("000- checking sensors to see if plants need nutes")
    tds_list, moisture_list, tank_tds, tank_ph = get_sensor_data()
    print("000- updating feeding queue")
    queue = update_feeding_queue(moisture_list)
    print("000- queue : ", queue)
    week = get_current_week(init_date)
    print("000- current week: ", week)
    feed(queue, week)
    print("000- taking a nap")
    sleep(60*10)