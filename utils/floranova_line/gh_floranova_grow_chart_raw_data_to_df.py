#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd

# source https://www.americanag.com/assets/FeedingSchedules/GH-FloraNova-DTW-Charts.pdf

##############################################################################
########################## MEDIUM FEED CHART #################################

feed_data = {'Week': ['Growth stage', 'Photoperiod (h)', 'min PPM', 'max PPM', 'FloraNova (ml/gal)'],

'1': ['Transition', '12', '600', '800', '2'],


'2': ['Early bloom', '12', '600', '800', '4'],


'3': ['Mid bloom', '12', '600', '800', '4'],


'4': ['Mid bloom', '12', '600', '800', '4'],

'5': ['Mid bloom', '12', '600', '800', '4'],

'6': ['Late bloom', '12', '600', '800', '4'],

'7': ['Late bloom', '12', '600', '800', '4'],

'8': ['Ripen', '12', '500', '700', '2.5'],

'9': ['Flush', '12', '0', '200', '0']}

feed_df = pd.DataFrame(feed_data,columns=['Week', '1',  '2',  '3',  '4',  '5',  '6',  '7',  '8',  '9'])

##############################################################################
################### OPERAÇÕES DE CONVERSÃO DE UNIDADES #######################

#Converts FloraNova from gallons to liters
floranova = feed_df.iloc[4][1:] #original em ml/gallon
label = [feed_df.iloc[4][0][:-4]+"l)"] #converte unidade da label
floranova = [float(quantity)/3.785 for quantity in floranova] #divide cada valor por 3.785 para obter ml/l
feed_df.iloc[4] = label+floranova #reinsere valores convertidos no dataframe

feed_df.to_pickle("floranova_growchart.pkl")

print("Done!")
