#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import pdb

class Getters:
# Provides growcharts as dataframes and information from them

    def get_chart_by_feeding_regime(self, feeding_regime):
    # Returns a dataframe containing the complete growchart. Needs the type of the feeding regime as input ("agressive", "medium", or "light", as strings) or else will raise ValueError

        try:
            growchart = pd.read_pickle("agressive_feed_growchart.pkl") #test if one of dfs exist
        except IOError:
            from greenutils import gh_micro_grow_chart_raw_data_to_df #creates the dataframes if exception is raised

        if feeding_regime == "agressive":
            return pd.read_pickle("agressive_feed_growchart.pkl")
        if feeding_regime == "medium":
            return pd.read_pickle("medium_feed_growchart.pkl")
        if feeding_regime == "light":
            return pd.read_pickle("light_feed_growchart.pkl")
        else:
            raise ValueError

    def get_nutrient_parameters_by_week_and_feeding_regime(self, week, feeding_regime):
    # Based on the given week ("a" to "d" for the vegetative stage, "1" to "9" for flowering stage) and feeding regime ("agressive", "medium", or "light", as strings) returns a dictionary containing all parameters related to the nutrients needed (except light measuements)
        try:
            data = Getters.get_chart_by_feeding_regime(self, feeding_regime)[week]
        except:
            return None
        quantities = {"Growth stage" : data[0], "Photoperiod (h)" : data[1], "Total Nitrogen (ppm)" : data[2], "EC range (mS/cm)" : data[3], "PPM range (500 scale)" : data[4], "FloraMicro (ml/l)" : data[5], "FloraGro (ml/l)" : data[6], "FloraBloom (ml/l)" : data[7]}

        return quantities

    def adjust_solution_quantities_based_on_tank_capacity(self, quantities, tank_capacity):
    # Receives a list of float quantities (ml/l needed for each nutrient) and the tank capacity (float) and provides back a list with the adjusted quantities of nutrient solution needed

        adjusted_quantities = quantities.copy()
        floramicro = adjusted_quantities["FloraMicro (ml/l)"]*tank_capacity
        floragro = adjusted_quantities["FloraGro (ml/l)"]*tank_capacity
        florabloom = adjusted_quantities["FloraBloom (ml/l)"]*tank_capacity

        adjusted_quantities["FloraMicro (ml/l)"] = floramicro
        adjusted_quantities["FloraGro (ml/l)"] = floragro
        adjusted_quantities["FloraBloom (ml/l)"] = florabloom

        adjusted_quantities["FloraMicro"] = adjusted_quantities.pop("FloraMicro (ml/l)")
        adjusted_quantities["FloraGro"] = adjusted_quantities.pop("FloraGro (ml/l)")
        adjusted_quantities["FloraBloom"] = adjusted_quantities.pop("FloraBloom (ml/l)")
        return adjusted_quantities
