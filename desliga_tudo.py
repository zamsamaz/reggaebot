import RPi.GPIO as gpio
gpio.setmode(gpio.BOARD)
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
print("desligando todos reles")
gpio.output(pino_rele_shaker, gpio.LOW)
gpio.output(pino_solenoide, gpio.LOW)
gpio.output(pino_rele_vaso_1, gpio.LOW)
gpio.output(pino_rele_vaso_2, gpio.LOW)
gpio.output(pino_rele_vaso_3, gpio.LOW)
gpio.output(pino_rele_vaso_4, gpio.LOW)
gpio.output(pino_rele_vaso_5, gpio.LOW)
gpio.output(pino_rele_vaso_6, gpio.LOW)
gpio.output(pino_rele_vaso_7, gpio.LOW)
gpio.output(pino_rele_vaso_8, gpio.LOW)
gpio.output(pino_rele_vaso_9, gpio.LOW)
gpio.output(pino_rele_peristaltica_bloom, gpio.LOW)
gpio.output(pino_rele_peristaltica_micro, gpio.LOW)
gpio.output(pino_rele_peristaltica_gro, gpio.LOW)
gpio.output(pino_rele_peristaltica_phup, gpio.LOW)
gpio.output(pino_rele_peristaltica_phdown, gpio.LOW)

import pdb;pdb.set_trace()
gpio.output(pino_rele_vaso_9, gpio.LOW)