#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyb import Pin
import json
import machine
from datetime import datetime, timedelta

config = open('config.json',mode='r')
config = json.load(config)
maximum_moisture = config['maximum_moisture']
maximum_tds = get_maximum_tds()
unit_list = [1,2,3,4,5,6,7,8,9]

def search_unit_pump_pin (unit):
    search_string = "pump_pin_"+str(unit)
    pin_number = config[search_string]
    return pin_number

def search_unit_moisture_pin (unit):
    search_string = "moisture_pin_"+str(unit)
    pin_number = config[search_string]
    return pin_number

def search_unit_tds_pin (unit):
    search_string = "tds_pin_"+str(unit)
    pin_number = config[search_string]
    return pin_number

def get_moisture_by_unit(unit):
    moisture_pin = search_unit_moisture_pin(unit)
    analog_digital_conversion = machine.ADC(moisture_pin)   # create an ADC object acting on a pin
    moisture_value = analog_digital_conversion.read_u16()
    return moisture_value

def get_tds_by_unit(unit):
    tds_pin = search_unit_tds_pin(unit)
    analog_digital_conversion = machine.ADC(moisture_pin)
    sensor_value = analog_digital_conversion.read_u16()
    voltage = sensor_value*5/1024.0
    tds_value=(133.42/voltage*voltage*voltage-255.86*voltage*voltage+857.39*voltage)*0.5 #Convert voltage value to TDS value
    return tds_value

def pump_switch (unit, state):
    pump_pin = search_unit_pump_pin(unit)
    p_out = Pin(pump_pin, Pin.OUT_PP)
    if state == 1:
        p_out.high()
        return 1
    if state == 0:
        p_out.low()
        return 1

def feed(unit):
    tds = get_tds_by_unit(unit)
    ####### CHECAR NIVEL DO TANQUE
    ####### CHECAR NIVEL DO TANQUE
    ####### CHECAR NIVEL DO TANQUE
    while tds < maximum_tds:
        tds = get_tds_by_unit(unit)
        pump_switch(unit, 1)
    else:
        pump_switch(unit, 0)
    return 1

def unit_moist_mon(unit_list, maximum_tds):
    i = 0
    while i < len(unit_list):
        moisture = get_moisture_by_unit(unit_list[i])
        if moisture <  maximum_moisture:
            feed(unit_list[i], maximum_tds)

def get_week_by_date(date_now):
    initial_date = config["initial_date"]
    delta = date_now = initial_date
    return delta


def main ():
    try:
        # ve se o software não rodou antes
        open("flag")
    except IOError:
        salva_data_inicial

        while 1:
            date_now = datetime.now()
            week = check_week_by_date(date_now)
            week_tds = tdsget_week_tds
            unit_moist_mon(unit_list, week_tds)



def get_maximum_tds(week):
    getters.gh etc


def prepare_solution():
    # SOLTA UNS MLS
    # SHAKE
    # MEDE TDS
    # SOLTA MLS
    # MEDE tds
    # SE TDS ESTA BOM
    # CHECA PH
    # AJUSTA PH
    # RETORNA A
