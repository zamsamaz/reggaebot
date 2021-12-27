#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd


class Getters:
# Provides growcharts as dataframes and information from them

    def get_chart(self):
    # Returns a dataframe containing the complete growchart.

        try:
            growchart = pd.read_pickle("floranova_growchart.pkl") #test if one of dfs exist
        except IOError:
            import gh_floranova_grow_chart_raw_data_to_df #creates the dataframes if exception is raised
        return pd.read_pickle("floranova_growchart.pkl")

    def get_nutrient_parameters_by_week(self, week):
    # Based on the given week ("1" to "9" for flowering stage) returns a dictionary containing all parameters related to the nutrients needed (except light measurements)

        try:
            data = Getters.get_chart(self)[week]
        except:
            return None
        quantities = {"Growth stage" : data[0], "Photoperiod (h)" : data[1], "min PPM" : data[2], 'max PPM' : data[3], "FloraNova (ml/l)" : data[4]}
        return quantities

    def adjust_solution_quantities_based_on_tank_capacity(self, quantities, tank_capacity):
    # Receives a list of float quantities (ml/l needed for each nutrient) and the tank capacity (float) and provides back a list with the adjusted quantities of nutrient solution needed

        adjusted_quantities = quantities.copy()
        floranova = adjusted_quantities["FloraNova (ml/l)"]*tank_capacity
        adjusted_quantities["FloraNova (ml/l)"] = floranova
        adjusted_quantities["FloraNova (ml/"+str(tank_capacity)+"l)"] = adjusted_quantities.pop("FloraNova (ml/l)")
        return adjusted_quantities
