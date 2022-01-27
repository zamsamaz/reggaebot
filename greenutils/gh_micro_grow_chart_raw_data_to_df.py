#!/usr/bin/env python
# -*- coding: utf-8 -*-

#source https://edge.generalhydroponics.com/www/uploads/20210121184300/FloraSeries-Basic-Feed-Charts.pdf


#Create one dataframe for each "feeding regime": "agressive", "medium", "light"

import pandas as pd

##############################################################################
####################### AGRESSIVE FEED CHART #################################

agressive_feed_data = {'Week': ['Growth stage', 'Photoperiod (h)', 'Total Nitrogen (ppm)', 'EC range (mS/cm)', 'PPM range (500 scale)', 'FloraMicro (ml/gal)', 'FloraGro (ml/gal)', 'FloraBloom (ml/gal)'],

'a': ['Seedling/Clone', '18', '60', '0.6-0.8', '300-400', '2.5', '2.5', '2.5'],

'b': ['Early Growth', '18', '135', '1.3-1.5', '600-800', '5.2', '4.8', '3.7'],


'c': ['Early Growth', '18', '180', '1.7-2.1', '850-1050', '7.0', '6.5', '4.8'],


'd': ['Late Growth', '18', '210', '2.0-2.5', '1050-1250', '8.5', '8.0', '6.0'],


'1': ['Early bloom', '12', '180', '2.0-2.4', '1000-1200', '7.6', '6.6', '8.5'],


'2': ['Early bloom', '12', '180', '2.0-2.4', '1000-1200', '7.6', '6.6', '8.5'],


'3': ['Mid bloom', '12', '160', '1.9-2.4', '950-1200', '6.6', '6.6', '9.5'],


'4': ['Mid bloom', '12', '160', '1.9-2.4', '950-1200', '6.6', '6.6', '9.5'],

'5': ['Mid bloom', '12', '160', '1.9-2.4', '950-1200', '6.6', '6.6', '9.5'],

'6': ['Late bloom', '12', '115', '1.3-1.6', '650-800', '4.7', '4.7', '5.7'],

'7': ['Late bloom', '12', '115', '1.3-1.6', '650-800', '4.7', '4.7', '5.7'],

'8': ['Ripen', '12', '85', '0.9-1.1', '450-500', '2.8', '2.8', '4.5'],

'9': ['Flush', '12', '0', '0', '0', '0', '0', '0']}

agressive_feed_df = pd.DataFrame(agressive_feed_data,columns=['Week', 'a', 'b', 'c', 'd', '1',  '2',  '3',  '4',  '5',  '6',  '7',  '8',  '9'])


##############################################################################
######################### MEDIUM FEED CHART ##################################


medium_feed_data = {'Week': ['Growth stage', 'Photoperiod (h)', 'Total Nitrogen (ppm)', 'EC range (mS/cm)', 'PPM range (500 scale)', 'FloraMicro (ml/gal)', 'FloraGro (ml/gal)', 'FloraBloom (ml/gal)'],

'a': ['Seedling/Clone', '18', '50', '0.5-0.6', '250-350', '2.0', '2.0', '2.0'],

'b': ['Early Growth', '18', '110', '1.0-1.2', '500-650', '4.2', '3.8', '3.0'],


'c': ['Early Growth', '18', '145', '1.3-1.6', '650-850', '5.6', '5.2', '3.8'],


'd': ['Late Growth', '18', '170', '1.6-2.0', '800-1000', '6.8', '6.4', '4.8'],


'1': ['Early bloom', '12', '145', '1.6-1.9', '800-1000', '6.1', '5.3', '6.8'],


'2': ['Early bloom', '12', '145', '1.6-1.9', '800-1000', '6.1', '5.3', '6.8'],


'3': ['Mid bloom', '12', '130', '1.6-1.9', '800-1000', '5.3', '5.3', '7.6'],


'4': ['Mid bloom', '12', '130', '1.6-1.9', '800-1000', '5.3', '5.3', '7.6'],

'5': ['Mid bloom', '12', '130', '1.6-1.9', '800-1000', '5.3', '5.3', '7.6'],

'6': ['Late bloom', '12', '90', '1.0-1.3', '500-650', '3.8', '3.8', '4.5'],

'7': ['Late bloom', '12', '90', '1.0-1.3', '500-650', '3.8', '3.8', '4.6'],

'8': ['Ripen', '12', '70', '0.7-0.9', '350-450', '2.3', '2.3', '3.6'],

'9': ['Flush', '12', '0', '0', '0', '0', '0', '0']}

medium_feed_df = pd.DataFrame(medium_feed_data,columns=['Week', 'a', 'b', 'c', 'd', '1',  '2',  '3',  '4',  '5',  '6',  '7',  '8',  '9'])


##############################################################################
########################## LIGHT FEED CHART ##################################


light_feed_data = {'Week': ['Growth stage', 'Photoperiod (h)', 'Total Nitrogen (ppm)', 'EC range (mS/cm)', 'PPM range (500 scale)', 'FloraMicro (ml/gal)', 'FloraGro (ml/gal)', 'FloraBloom (ml/gal)'],

'a': ['Seedling/Clone', '18', '45', '0.4-0.5', '200-3500', '1.8', '1.8', '1.8'],

'b': ['Early Growth', '18', '95', '0.9-1.1', '400-550', '3.6', '3.4', '2.6'],


'c': ['Early Growth', '18', '125', '1.2-1.4', '550-750', '4.9', '4.6', '3.4'],


'd': ['Late Growth', '18', '150', '1.4-1.7', '700-900', '6.0', '5.6', '4.2'],


'1': ['Early bloom', '12', '125', '1.4-1.7', '700-850', '5.3', '4.6', '6.0'],


'2': ['Early bloom', '12', '125', '1.4-1.7', '700-850', '5.3', '4.6', '6.0'],


'3': ['Mid bloom', '12', '115', '1.4-1.7', '700-850', '4.6', '4.6', '6.6'],


'4': ['Mid bloom', '12', '115', '1.4-1.7', '700-850', '4.6', '4.6', '6.6'],

'5': ['Mid bloom', '12', '115', '1.4-1.7', '700-850', '4.6', '4.6', '6.6'],

'6': ['Late bloom', '12', '80', '0.9-1.1', '450-600', '3.3', '3.3', '4.0'],

'7': ['Late bloom', '12', '80', '0.9-1.1', '450-600', '3.3', '3.3', '4.0'],

'8': ['Ripen', '12', '60', '0.6-0.8', '300-400', '2.0', '2.0', '3.2'],

'9': ['Flush', '12', '0', '0', '0', '0', '0', '0']}

light_feed_df = pd.DataFrame(light_feed_data,columns=['Week', 'a', 'b', 'c', 'd', '1',  '2',  '3',  '4',  '5',  '6',  '7',  '8',  '9'])



##############################################################################
################### OPERAÇÕES DE CONVERSÃO DE UNIDADES #######################

#Converte FloraMicro
floramicro = agressive_feed_df.iloc[5][1:] #original em ml/gallon
label = [agressive_feed_df.iloc[5][0][:-4]+"l)"] #converte unidade da label
floramicro = [float(quantity)/3.785 for quantity in floramicro] #divide cada valor por 3.785 para obter ml/l
agressive_feed_df.iloc[5] = label+floramicro #reinsere valores convertidos no dataframe

floramicro = medium_feed_df.iloc[5][1:]
label = [medium_feed_df.iloc[5][0][:-4]+"l)"]
floramicro = [float(quantity)/3.785 for quantity in floramicro]
medium_feed_df.iloc[5] = label+floramicro

floramicro = light_feed_df.iloc[5][1:]
label = [light_feed_df.iloc[5][0][:-4]+"l)"]
floramicro = [float(quantity)/3.785 for quantity in floramicro]
light_feed_df.iloc[5] = label+floramicro

#Converte FloraGro
floragro = agressive_feed_df.iloc[6][1:]
label = [agressive_feed_df.iloc[6][0][:-4]+"l)"]
floragro = [float(quantity)/3.785 for quantity in floragro]
agressive_feed_df.iloc[6] = label+floragro

floragro = medium_feed_df.iloc[6][1:]
label = [medium_feed_df.iloc[6][0][:-4]+"l)"]
floragro = [float(quantity)/3.785 for quantity in floragro]
medium_feed_df.iloc[6] = label+floragro

floragro = light_feed_df.iloc[6][1:]
label = [light_feed_df.iloc[6][0][:-4]+"l)"]
floragro = [float(quantity)/3.785 for quantity in floragro]
light_feed_df.iloc[6] = label+floragro

#Converte FloraBloom
florabloom = agressive_feed_df.iloc[7][1:]
label = [agressive_feed_df.iloc[7][0][:-4]+"l)"]
florabloom = [float(quantity)/3.785 for quantity in florabloom]
agressive_feed_df.iloc[7] = label+florabloom

florabloom = medium_feed_df.iloc[7][1:]
label = [medium_feed_df.iloc[7][0][:-4]+"l)"]
florabloom = [float(quantity)/3.785 for quantity in florabloom]
medium_feed_df.iloc[7] = label+florabloom

florabloom = light_feed_df.iloc[7][1:]
label = [light_feed_df.iloc[7][0][:-4]+"l)"]
florabloom = [float(quantity)/3.785 for quantity in florabloom]
light_feed_df.iloc[7] = label+florabloom

agressive_feed_df.to_pickle("greenutils/agressive_feed_growchart.pkl")
medium_feed_df.to_pickle("greenutils/medium_feed_growchart.pkl")
light_feed_df.to_pickle("greenutils/light_feed_growchart.pkl")

print("Done!")
