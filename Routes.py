# -*- coding: utf-8 -*-
"""
Project: Airline Data Challenge
Module: Data Analysis
File: Flights.csv, Tickets.csv,Airport_Codes.csv
Author: Capital One - Data Analysis Team
Date: 02/14/2024
Version: 1.0
"""
import pandas as pd
import numpy as np
import Tickets as tk
import Flights as fl

#Remove Duplicates
routes_inscope = pd.DataFrame()
tickets_inscope = tk.tickets_inscope
print(len(tickets_inscope[['ORIGIN_COUNTRY','ROUTE','CHK_ORI_IATA_TYPE','CHK_DEST_IATA_TYPE','CHK_ORI_NAME','CHK_DEST_NAME']].drop_duplicates()))
print(len(tickets_inscope[['ORIGIN_COUNTRY','ROUTE']].drop_duplicates()))

#Derive Routes dataset
routes_inscope = tickets_inscope[['ORIGIN_COUNTRY','ROUTE','CHK_ORI_IATA_TYPE','CHK_DEST_IATA_TYPE','CHK_ORI_NAME','CHK_DEST_NAME','MEAN_ITIN_FARE']].drop_duplicates()
routes_inscope.insert(0,"DUPLICATE_ID",routes_inscope.duplicated(subset=['ROUTE']),True)
routes_inscope = routes_inscope[routes_inscope.DUPLICATE_ID == False]
print(len(routes_inscope))

#Add column
routes_inscope[['POINT_A', 'POINT_B']] = routes_inscope["ROUTE"].str.split('-', expand=True)
routes_inscope.insert(4,"POINT_A_TO_B",routes_inscope.POINT_A+'-'+routes_inscope.POINT_B,True)
routes_inscope.insert(5,"POINT_B_TO_A",routes_inscope.POINT_B+'-'+routes_inscope.POINT_A,True)
mapping = {"ORIGIN_COUNTRY" : "ISO_COUNTRY" , "CHK_ORI_IATA_TYPE" : "POINT_A_IATA_TYPE","CHK_DEST_IATA_TYPE" : "POINT_B_IATA_TYPE","CHK_ORI_NAME" : "POINT_A_NAME","CHK_DEST_NAME" : "POINT_B_NAME"}
routes_inscope.rename(columns = mapping, inplace = True)

flights_inscope = pd.DataFrame()
flights_inscope = fl.operated_flights

#JOIN: Flights & Routes
#Add column
city_flights = flights_inscope[['ROUTE','ORIGIN_CITY_NAME','DEST_CITY_NAME']]
mapping = {"ORIGIN_CITY_NAME" : "POINT_A_CITY_NAME","DEST_CITY_NAME" : "POINT_B_CITY_NAME"}
city_flights.rename(columns = mapping, inplace = True)
city_flights.insert(0,"DUPLICATE_ID",city_flights.duplicated(subset=['ROUTE']),True)
city_flights = city_flights[city_flights.DUPLICATE_ID == False]
routes_inscope = pd.merge(routes_inscope,city_flights, on ='ROUTE',  how ='left')

#Add column
cnt_flights = flights_inscope[['ROUTE','ID']]
mapping = {"ROUTE" : "POINT_A_TO_B","ID" : "CNT_FLIGHTS_A_TO_B"}
cnt_flights.rename(columns = mapping, inplace = True)
cnt_flights = cnt_flights.groupby(['POINT_A_TO_B'])['CNT_FLIGHTS_A_TO_B'].count()
routes_inscope = pd.merge(routes_inscope,cnt_flights, on ='POINT_A_TO_B',  how ='left')
routes_inscope['CNT_FLIGHTS_A_TO_B'] = routes_inscope['CNT_FLIGHTS_A_TO_B'].replace(np.nan, (0)).astype(int)

#Add column
cnt_flights = flights_inscope[['ROUTE','ID']]
mapping = {"ROUTE" : "POINT_B_TO_A","ID" : "CNT_FLIGHTS_B_TO_A"}
cnt_flights.rename(columns = mapping, inplace = True)
cnt_flights = cnt_flights.groupby(['POINT_B_TO_A'])['CNT_FLIGHTS_B_TO_A'].count()
routes_inscope = pd.merge(routes_inscope,cnt_flights, on ='POINT_B_TO_A',  how ='left')
routes_inscope['CNT_FLIGHTS_B_TO_A'] = routes_inscope['CNT_FLIGHTS_B_TO_A'].replace(np.nan, (0)).astype(int)

#Add column
#JOIN: Flights & Routes
flights_outscope = pd.DataFrame()
flights_outscope = fl.cancelled_flights

cnt_can_flights = flights_outscope[['ROUTE','ID']]
mapping = {"ROUTE" : "POINT_A_TO_B","ID" : "CNT_CAN_FLIGHTS_A_TO_B"}
cnt_can_flights.rename(columns = mapping, inplace = True)
cnt_can_flights = cnt_can_flights.groupby(['POINT_A_TO_B'])['CNT_CAN_FLIGHTS_A_TO_B'].count()
routes_inscope = pd.merge(routes_inscope,cnt_can_flights, on ='POINT_A_TO_B',  how ='left')
routes_inscope['CNT_CAN_FLIGHTS_A_TO_B'] = routes_inscope['CNT_CAN_FLIGHTS_A_TO_B'].replace(np.nan, (0)).astype(int)

#Add column
cnt_can_flights = flights_outscope[['ROUTE','ID']]
mapping = {"ROUTE" : "POINT_B_TO_A","ID" : "CNT_CAN_FLIGHTS_B_TO_A"}
cnt_can_flights.rename(columns = mapping, inplace = True)
cnt_can_flights = cnt_can_flights.groupby(['POINT_B_TO_A'])['CNT_CAN_FLIGHTS_B_TO_A'].count()
routes_inscope = pd.merge(routes_inscope,cnt_can_flights, on ='POINT_B_TO_A',  how ='left')
routes_inscope['CNT_CAN_FLIGHTS_B_TO_A'] = routes_inscope['CNT_CAN_FLIGHTS_B_TO_A'].replace(np.nan, (0)).astype(int)

print(fl.join_op_flights_mean_air_time.dtypes)

#Add column
flights_inscope.insert(20,"FOMC_COST",round(flights_inscope.DISTANCE.astype(float)*8),True)                      
flights_inscope.insert(21,"DIO_COST",round(flights_inscope.DISTANCE.astype(float)*1.18),True)

cost_flights = flights_inscope[['ROUTE','FOMC_COST']]
mapping = {"FOMC_COST" : "FOMC_COST_A_TO_B"}
cost_flights.rename(columns = mapping, inplace = True)
cost_flights = cost_flights.groupby(['ROUTE'])['FOMC_COST_A_TO_B'].sum().astype(int)
routes_inscope = pd.merge(routes_inscope,cost_flights, left_on ='POINT_A_TO_B', right_on = 'ROUTE', how ='left')
routes_inscope['FOMC_COST_A_TO_B'] = routes_inscope['FOMC_COST_A_TO_B'].replace(np.nan, (0)).astype(int)

#Add column
cost_flights = flights_inscope[['ROUTE','FOMC_COST']]
mapping = {'FOMC_COST': 'FOMC_COST_B_TO_A'}
cost_flights.rename(columns = mapping, inplace = True) 
cost_flights = cost_flights.groupby(['ROUTE'])['FOMC_COST_B_TO_A'].sum().astype(int)
routes_inscope = pd.merge(routes_inscope,cost_flights, left_on ='POINT_B_TO_A', right_on = 'ROUTE', how ='left')
routes_inscope['FOMC_COST_B_TO_A'] = routes_inscope['FOMC_COST_B_TO_A'].replace(np.nan, (0)).astype(int)

#Add column
cost_flights = flights_inscope[['ROUTE','DIO_COST']]
mapping = {"DIO_COST" : "DIO_COST_A_TO_B"}
cost_flights.rename(columns = mapping, inplace = True)
cost_flights = cost_flights.groupby(['ROUTE'])['DIO_COST_A_TO_B'].sum().astype(int)
routes_inscope = pd.merge(routes_inscope,cost_flights, left_on ='POINT_A_TO_B', right_on = 'ROUTE', how ='left')
routes_inscope['DIO_COST_A_TO_B'] = routes_inscope['DIO_COST_A_TO_B'].replace(np.nan, (0)).astype(int)

#Add column
cost_flights = flights_inscope[['ROUTE','DIO_COST']]
mapping = {'DIO_COST': 'DIO_COST_B_TO_A'}
cost_flights.rename(columns = mapping, inplace = True) 
cost_flights = cost_flights.groupby(['ROUTE'])['DIO_COST_B_TO_A'].sum().astype(int)
routes_inscope = pd.merge(routes_inscope,cost_flights, left_on ='POINT_B_TO_A', right_on = 'ROUTE', how ='left')
routes_inscope['DIO_COST_B_TO_A'] = routes_inscope['DIO_COST_B_TO_A'].replace(np.nan, (0)).astype(int)

#Add column
routes_inscope['TOTAL_FOMC_COST'] = routes_inscope['FOMC_COST_A_TO_B'] + routes_inscope['FOMC_COST_B_TO_A']
routes_inscope['TOTAL_DIO_COST'] = routes_inscope['DIO_COST_A_TO_B'] + routes_inscope['DIO_COST_B_TO_A']

routes_inscope['POINT_A_IATA_TYPE'] = routes_inscope['POINT_A_IATA_TYPE'].replace(np.nan, ('???')).astype(str)
routes_inscope['POINT_B_IATA_TYPE'] = routes_inscope['POINT_B_IATA_TYPE'].replace(np.nan, ('???')).astype(str)

#1)	Function to determine airport operations cost 
def get_airport_ops_cost(airport_type):
    if airport_type == 'large_airport':
        return 10000
    elif airport_type == 'medium_airport':
        return 5000
    else:
        return 0
    
routes_inscope['POINT_A_AIRPORT_OPS_COST'] = routes_inscope['POINT_A_IATA_TYPE'].apply(get_airport_ops_cost)
routes_inscope['POINT_B_AIRPORT_OPS_COST'] = routes_inscope['POINT_B_IATA_TYPE'].apply(get_airport_ops_cost)
routes_inscope['TOTAL_AIRPORT_OPS_COST'] = routes_inscope['POINT_A_AIRPORT_OPS_COST'] + routes_inscope['POINT_B_AIRPORT_OPS_COST']

#2)	Function to determine costing delay 
def get_leg_delay(delay):
   if (delay>15):
       return (delay-15)
   else:
       return 0

flights_inscope.insert(22,"COSTING_DEP_DELAY",flights_inscope['DEP_DELAY'].apply(get_leg_delay),True)
flights_inscope.insert(23,"COSTING_ARR_DELAY",flights_inscope['ARR_DELAY'].apply(get_leg_delay),True)
flights_inscope['LEG_COSTING_DELAY'] = flights_inscope['COSTING_DEP_DELAY'] + flights_inscope['COSTING_ARR_DELAY']

#Add column
cost_flights = flights_inscope[['ROUTE','LEG_COSTING_DELAY']]
mapping = {"LEG_COSTING_DELAY" : "LEG_DELAY_A_TO_B"}
cost_flights.rename(columns = mapping, inplace = True)
cost_flights = cost_flights.groupby(['ROUTE'])['LEG_DELAY_A_TO_B'].sum().astype(int)
routes_inscope = pd.merge(routes_inscope,cost_flights, left_on ='POINT_A_TO_B', right_on = 'ROUTE', how ='left')
routes_inscope['LEG_DELAY_A_TO_B'] = routes_inscope['LEG_DELAY_A_TO_B'].replace(np.nan, (0)).astype(int)

#Add column
cost_flights = flights_inscope[['ROUTE','LEG_COSTING_DELAY']]
mapping = {"LEG_COSTING_DELAY" : "LEG_DELAY_B_TO_A"}
cost_flights.rename(columns = mapping, inplace = True)
cost_flights = cost_flights.groupby(['ROUTE'])['LEG_DELAY_B_TO_A'].sum().astype(int)
routes_inscope = pd.merge(routes_inscope,cost_flights, left_on ='POINT_B_TO_A', right_on = 'ROUTE', how ='left')
routes_inscope['LEG_DELAY_B_TO_A'] = routes_inscope['LEG_DELAY_B_TO_A'].replace(np.nan, (0)).astype(int)

#Add column
cost_flights = flights_inscope[['ROUTE','LEG_COSTING_DELAY']]
mapping = {"LEG_COSTING_DELAY" : "AVG_DELAY_LEG_A_TO_B"}
cost_flights.rename(columns = mapping, inplace = True)
cost_flights = round(cost_flights.groupby(['ROUTE'])['AVG_DELAY_LEG_A_TO_B'].mean().astype(float),2)
routes_inscope = pd.merge(routes_inscope,cost_flights, left_on ='POINT_A_TO_B', right_on = 'ROUTE', how ='left')
routes_inscope['AVG_DELAY_LEG_A_TO_B'] = routes_inscope['AVG_DELAY_LEG_A_TO_B'].replace(np.nan, (0)).astype(int)

#Add column
cost_flights = flights_inscope[['ROUTE','LEG_COSTING_DELAY']]
mapping = {"LEG_COSTING_DELAY" : "AVG_DELAY_LEG_B_TO_A"}
cost_flights.rename(columns = mapping, inplace = True)
cost_flights = round(cost_flights.groupby(['ROUTE'])['AVG_DELAY_LEG_B_TO_A'].mean().astype(float),2)
routes_inscope = pd.merge(routes_inscope,cost_flights, left_on ='POINT_B_TO_A', right_on = 'ROUTE', how ='left')
routes_inscope['AVG_DELAY_LEG_B_TO_A'] = routes_inscope['AVG_DELAY_LEG_B_TO_A'].replace(np.nan, (0)).astype(int)

#Add column
routes_inscope['TOTAL_ROUTE_DELAY'] = routes_inscope['LEG_DELAY_A_TO_B'] + routes_inscope['LEG_DELAY_B_TO_A']
routes_inscope['TOTAL_DELAY_OPS_COST'] = (routes_inscope['TOTAL_ROUTE_DELAY']*75).astype(int)
routes_inscope['TOTAL_COST'] = routes_inscope['TOTAL_FOMC_COST']+routes_inscope['TOTAL_DIO_COST']+routes_inscope['TOTAL_AIRPORT_OPS_COST']+routes_inscope['TOTAL_DELAY_OPS_COST']
    
#Add column
flights_inscope.insert(24,"OCCUPANCY",round(flights_inscope.OCCUPANCY_RATE.astype(float)*200),True)
occ_flights = flights_inscope[['ROUTE','OCCUPANCY']]
mapping = {"OCCUPANCY" : "OCCUPANCY_A_TO_B"}
occ_flights.rename(columns = mapping, inplace = True)
occ_flights = occ_flights.groupby(['ROUTE'])['OCCUPANCY_A_TO_B'].sum().astype(int)
routes_inscope = pd.merge(routes_inscope,occ_flights, left_on ='POINT_A_TO_B', right_on = 'ROUTE', how ='left')
routes_inscope['OCCUPANCY_A_TO_B'] = routes_inscope['OCCUPANCY_A_TO_B'].replace(np.nan, (0)).astype(int)

#Add column
occ_flights = flights_inscope[['ROUTE','OCCUPANCY']]
mapping = {"OCCUPANCY" : "OCCUPANCY_B_TO_A"}
occ_flights.rename(columns = mapping, inplace = True)
occ_flights = occ_flights.groupby(['ROUTE'])['OCCUPANCY_B_TO_A'].sum().astype(int)
routes_inscope = pd.merge(routes_inscope,occ_flights, left_on ='POINT_B_TO_A', right_on = 'ROUTE', how ='left')
routes_inscope['OCCUPANCY_B_TO_A'] = routes_inscope['OCCUPANCY_B_TO_A'].replace(np.nan, (0)).astype(int)

#Add column
routes_inscope['ROUNDTRIP_PASSENGERS'] = np.where(routes_inscope['OCCUPANCY_A_TO_B']<routes_inscope['OCCUPANCY_B_TO_A'], routes_inscope['OCCUPANCY_A_TO_B'],routes_inscope['OCCUPANCY_B_TO_A'])
routes_inscope['ROUNDTRIP_FLIGHTS'] = np.where(routes_inscope['CNT_FLIGHTS_A_TO_B']<routes_inscope['CNT_FLIGHTS_B_TO_A'], routes_inscope['CNT_FLIGHTS_A_TO_B'],routes_inscope['CNT_FLIGHTS_B_TO_A'])
routes_inscope['ROUNDTRIP_CAN_FLIGHTS'] = np.where(routes_inscope['CNT_CAN_FLIGHTS_A_TO_B']<routes_inscope['CNT_CAN_FLIGHTS_B_TO_A'], routes_inscope['CNT_CAN_FLIGHTS_A_TO_B'],routes_inscope['CNT_CAN_FLIGHTS_B_TO_A'])
print(routes_inscope.dtypes)
print(routes_inscope['MEAN_ITIN_FARE'])

#Add column
routes_inscope['TICKET_REVENUE'] = (routes_inscope['ROUNDTRIP_PASSENGERS'] * routes_inscope['MEAN_ITIN_FARE']).astype(float)
routes_inscope['BAGGAGE_PASSENGERS'] = (routes_inscope['ROUNDTRIP_PASSENGERS']/2)
routes_inscope['BAGGAGE_REVENUE'] = (routes_inscope['BAGGAGE_PASSENGERS']*70).astype(float)
routes_inscope['TOTAL_REVENUE'] = (routes_inscope['TICKET_REVENUE'] + routes_inscope['BAGGAGE_REVENUE']).astype(float)
routes_inscope['TOTAL_PROFIT'] = (routes_inscope['TOTAL_REVENUE'] - routes_inscope['TOTAL_COST']).astype(float)
routes_inscope = routes_inscope[routes_inscope.ROUNDTRIP_FLIGHTS != 0]
routes_inscope = routes_inscope[routes_inscope.ROUNDTRIP_PASSENGERS != 0]
routes_inscope = routes_inscope[routes_inscope.MEAN_ITIN_FARE != 0]
routes_inscope = routes_inscope.sort_values(['TOTAL_PROFIT','CNT_FLIGHTS_A_TO_B', 'CNT_FLIGHTS_B_TO_A'], ascending=[False, False, False])
routes_inscope['BREAKEVEN_FLIGHTS'] = ((90000000/routes_inscope['TOTAL_PROFIT'])*routes_inscope['ROUNDTRIP_FLIGHTS']).astype(int)
routes_inscope['PROFIT_COST_RATIO'] = round((routes_inscope['TOTAL_PROFIT']/routes_inscope['TOTAL_COST']).astype(float),2)

#Add column
occ_flights = flights_inscope[['ROUTE','OCCUPANCY_RATE']]
mapping = {"OCCUPANCY_RATE" : "AVG_OCCUPANCY_RATE_A_TO_B"}
occ_flights.rename(columns = mapping, inplace = True)
occ_flights = occ_flights.groupby(['ROUTE'])['AVG_OCCUPANCY_RATE_A_TO_B'].mean().astype(float)
routes_inscope = pd.merge(routes_inscope,occ_flights, left_on ='POINT_A_TO_B', right_on = 'ROUTE', how ='left')
routes_inscope['AVG_OCCUPANCY_RATE_A_TO_B'] = round(routes_inscope['AVG_OCCUPANCY_RATE_A_TO_B'].replace(np.nan, (0)).astype(float),2)

#Add column
occ_flights = flights_inscope[['ROUTE','OCCUPANCY_RATE']]
mapping = {"OCCUPANCY_RATE" : "AVG_OCCUPANCY_RATE_B_TO_A"}
occ_flights.rename(columns = mapping, inplace = True)
occ_flights = occ_flights.groupby(['ROUTE'])['AVG_OCCUPANCY_RATE_B_TO_A'].mean().astype(float)
routes_inscope = pd.merge(routes_inscope,occ_flights, left_on ='POINT_B_TO_A', right_on = 'ROUTE', how ='left')
routes_inscope['AVG_OCCUPANCY_RATE_B_TO_A'] = round(routes_inscope['AVG_OCCUPANCY_RATE_B_TO_A'].replace(np.nan, (0)).astype(float),2)

#Add column
dist_flights = flights_inscope[['ROUTE','DISTANCE']]
dist_flights['DISTANCE'] = round(dist_flights['DISTANCE'].astype(float),2)
mapping = {"DISTANCE" : "AVG_DISTANCE_A_TO_B"}
dist_flights.rename(columns = mapping, inplace = True)
dist_flights = dist_flights.groupby(['ROUTE'])['AVG_DISTANCE_A_TO_B'].mean().astype(float)
routes_inscope = pd.merge(routes_inscope,dist_flights, left_on ='POINT_A_TO_B', right_on = 'ROUTE', how ='left')
routes_inscope['AVG_DISTANCE_A_TO_B'] = round(routes_inscope['AVG_DISTANCE_A_TO_B'].replace(np.nan, (0)).astype(float),2)

#Add column
dist_flights = flights_inscope[['ROUTE','DISTANCE']]
dist_flights['DISTANCE'] = round(dist_flights['DISTANCE'].astype(float),2)
mapping = {"DISTANCE" : "AVG_DISTANCE_B_TO_A"}
dist_flights.rename(columns = mapping, inplace = True)
dist_flights = dist_flights.groupby(['ROUTE'])['AVG_DISTANCE_B_TO_A'].mean().astype(float)
routes_inscope = pd.merge(routes_inscope,dist_flights, left_on ='POINT_B_TO_A', right_on = 'ROUTE', how ='left')
routes_inscope['AVG_DISTANCE_B_TO_A'] = round(routes_inscope['AVG_DISTANCE_B_TO_A'].replace(np.nan, (0)).astype(float),2)

#Data type conversion
routes_inscope['ROUTE_DISTANCE'] = routes_inscope['AVG_DISTANCE_A_TO_B'] + routes_inscope['AVG_DISTANCE_B_TO_A']  
routes_inscope = routes_inscope[routes_inscope.TOTAL_PROFIT > 0]
routes_inscope['TICKET_REVENUE'] = routes_inscope['TICKET_REVENUE'].astype(int , errors='ignore')
routes_inscope['BAGGAGE_PASSENGERS'] = routes_inscope['BAGGAGE_PASSENGERS'].astype(int , errors='ignore')
routes_inscope['BAGGAGE_REVENUE'] = routes_inscope['BAGGAGE_REVENUE'].astype(int , errors='ignore')
routes_inscope['TOTAL_REVENUE'] = routes_inscope['TOTAL_REVENUE'].astype(int , errors='ignore')
routes_inscope['TOTAL_PROFIT'] = routes_inscope['TOTAL_PROFIT'].astype(int , errors='ignore')

routes_inscope = routes_inscope[['ROUTE', 'ISO_COUNTRY', 'MEAN_ITIN_FARE','POINT_A', 'POINT_A_NAME', 'POINT_A_IATA_TYPE','POINT_A_CITY_NAME', 
                                 'POINT_B', 'POINT_B_NAME', 'POINT_B_IATA_TYPE','POINT_B_CITY_NAME', 
                                 'POINT_A_TO_B','CNT_FLIGHTS_A_TO_B','CNT_CAN_FLIGHTS_A_TO_B','FOMC_COST_A_TO_B', 'DIO_COST_A_TO_B','AVG_DISTANCE_A_TO_B',
                                 'POINT_B_TO_A','CNT_FLIGHTS_B_TO_A','CNT_CAN_FLIGHTS_B_TO_A','FOMC_COST_B_TO_A','DIO_COST_B_TO_A','AVG_DISTANCE_B_TO_A',
                                 'ROUNDTRIP_FLIGHTS','ROUNDTRIP_CAN_FLIGHTS','TOTAL_FOMC_COST','TOTAL_DIO_COST','ROUTE_DISTANCE',
                                 'POINT_A_AIRPORT_OPS_COST','POINT_B_AIRPORT_OPS_COST','TOTAL_AIRPORT_OPS_COST',
                                 'LEG_DELAY_A_TO_B','LEG_DELAY_B_TO_A','TOTAL_ROUTE_DELAY','TOTAL_DELAY_OPS_COST','TOTAL_COST',
                                 'OCCUPANCY_A_TO_B', 'OCCUPANCY_B_TO_A', 'ROUNDTRIP_PASSENGERS','TICKET_REVENUE',
                                 'AVG_OCCUPANCY_RATE_A_TO_B','AVG_OCCUPANCY_RATE_B_TO_A','AVG_DELAY_LEG_A_TO_B','AVG_DELAY_LEG_B_TO_A',
                                 'BAGGAGE_PASSENGERS','BAGGAGE_REVENUE','TOTAL_REVENUE','TOTAL_PROFIT','BREAKEVEN_FLIGHTS',
                                 'PROFIT_COST_RATIO']]

