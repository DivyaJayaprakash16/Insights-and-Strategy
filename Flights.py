# -*- coding: utf-8 -*-
"""
Project: Airline Data Challenge
Module: Data cleaning
File: Flights.csv
Author: Capital One - Data Analysis Team
Date: 02/13/2024
Version: 1.0
"""

import pandas as pd
import numpy as np
import Airport_Codes as ac

#Import data
flights = pd.read_csv("C://Users//...//Capital One Analytics//data//Flights.csv")
print(flights.head(10))
print(len(flights))
flights = flights
print('len(flights):' , len(flights))

#Blank values found	Replaced with 0
flights['ARR_DELAY'] = flights['ARR_DELAY'].replace(np.nan, int(0)).astype(int)
print(flights['ARR_DELAY'])

#New Field created as a primary key
flights.insert(0,"ID",flights['FL_DATE']+"-"+flights['TAIL_NUM']+"-"+flights['OP_CARRIER_FL_NUM'].astype(str)+"-"+flights['ORIGIN']+"-"+flights['DESTINATION'],True)
print(flights.head(10))

#Duplicate values found	Duplicate rows removed
flights.insert(1,"DUPLICATE_ID",flights.duplicated(subset=['ID']),True)
print(flights[flights["DUPLICATE_ID"] == True])
flights = flights[flights.DUPLICATE_ID == False]

#Route field created
flights.insert(11,"ROUTE",flights['ORIGIN']+"-"+flights['DESTINATION'],True)
print(flights['ROUTE'])
print(flights.dtypes)

#Incorrect values found	Replaced
flights['AIR_TIME'] = flights['AIR_TIME'].replace('Two', (2)).astype(str)
flights['AIR_TIME'] = flights['AIR_TIME'].replace(np.nan, (0)).astype(str)
flights['AIR_TIME'] = flights['AIR_TIME'].replace('$$$', (0)).astype(str)
flights['AIR_TIME'] = flights['AIR_TIME'].astype(float)

#Incorrect values found	Replaced
flights['DISTANCE'] = flights['DISTANCE'].replace('Hundred', (100)).astype(str)
flights['DISTANCE'] = flights['DISTANCE'].replace('Twenty', (20)).astype(str)
flights['DISTANCE'] = flights['DISTANCE'].replace('****', (500)).astype(str)

#JOIN: Flights & Mean Airtime group
mean_air_time_per_route = flights.groupby('ROUTE')['AIR_TIME'].mean()
join_op_flights_mean_air_time = pd.merge(flights,mean_air_time_per_route, on ='ROUTE',  how ='left')
print(join_op_flights_mean_air_time)

#Blank values found	Replaced with MEAN_AIRTIME for the route
mapping = {"AIR_TIME_x" : "AIR_TIME", "AIR_TIME_y" : "MEAN_AIR_TIME"}
join_op_flights_mean_air_time.rename(columns = mapping, inplace = True)
print(join_op_flights_mean_air_time["MEAN_AIR_TIME"])
print(join_op_flights_mean_air_time[join_op_flights_mean_air_time["AIR_TIME"] == 0])
join_op_flights_mean_air_time.AIR_TIME[join_op_flights_mean_air_time.AIR_TIME == 0] = join_op_flights_mean_air_time.MEAN_AIR_TIME
print(join_op_flights_mean_air_time[join_op_flights_mean_air_time["AIR_TIME"] == 0])

#call variable
airport_codes = ac.airport_codes

#ORIGIN IATA Code validation
IATA = pd.DataFrame()
IATA.loc[:, 'ORIGIN'] = airport_codes.loc[:, 'IATA_CODE']
IATA.loc[:, 'CHK_ORI_IATA_VALID_CODE'] = airport_codes.loc[:, 'IATA_CODE']
IATA.loc[:, 'CHK_ORI_IATA_US'] = airport_codes.loc[:, 'ISO_COUNTRY']
IATA.loc[:, 'CHK_ORI_IATA_TYPE'] = airport_codes.loc[:, 'TYPE']
options = ['medium_airport', 'large_airport']
join_op_flights_mean_air_time = pd.merge(join_op_flights_mean_air_time,IATA, on ='ORIGIN',  how ='left')
join_op_flights_mean_air_time['CHK_ORI_IATA_VALID_CODE'] = join_op_flights_mean_air_time['CHK_ORI_IATA_VALID_CODE'].replace(np.nan, "???").astype(str)
print(join_op_flights_mean_air_time[join_op_flights_mean_air_time.CHK_ORI_IATA_VALID_CODE == "???"])
join_op_flights_mean_air_time = join_op_flights_mean_air_time[join_op_flights_mean_air_time.CHK_ORI_IATA_VALID_CODE != "???"]

join_op_flights_mean_air_time['CHK_ORI_IATA_US'] = join_op_flights_mean_air_time['CHK_ORI_IATA_US'].replace(np.nan, "???").astype(str)
print(join_op_flights_mean_air_time[join_op_flights_mean_air_time.CHK_ORI_IATA_US == "???"])
join_op_flights_mean_air_time = join_op_flights_mean_air_time[join_op_flights_mean_air_time.CHK_ORI_IATA_US == "US"]

join_op_flights_mean_air_time['CHK_ORI_IATA_TYPE'] = join_op_flights_mean_air_time['CHK_ORI_IATA_TYPE'].replace(np.nan, "???").astype(str)
print(join_op_flights_mean_air_time[join_op_flights_mean_air_time.CHK_ORI_IATA_TYPE == "???"])
join_op_flights_mean_air_time = join_op_flights_mean_air_time[join_op_flights_mean_air_time.CHK_ORI_IATA_TYPE.isin(options)]


#Destination IATA Code validation
IATA = pd.DataFrame()
IATA.loc[:, 'DESTINATION'] = airport_codes.loc[:, 'IATA_CODE']
IATA.loc[:, 'CHK_DEST_IATA_VALID_CODE'] = airport_codes.loc[:, 'IATA_CODE']
IATA.loc[:, 'CHK_DEST_IATA_US'] = airport_codes.loc[:, 'ISO_COUNTRY']
IATA.loc[:, 'CHK_DEST_IATA_TYPE'] = airport_codes.loc[:, 'TYPE']
join_op_flights_mean_air_time = pd.merge(join_op_flights_mean_air_time,IATA, on ='DESTINATION',  how ='left')
join_op_flights_mean_air_time['CHK_DEST_IATA_VALID_CODE'] = join_op_flights_mean_air_time['CHK_DEST_IATA_VALID_CODE'].replace(np.nan, "???").astype(str)
print(join_op_flights_mean_air_time[join_op_flights_mean_air_time.CHK_DEST_IATA_VALID_CODE == "???"])
join_op_flights_mean_air_time = join_op_flights_mean_air_time[join_op_flights_mean_air_time.CHK_DEST_IATA_VALID_CODE != "???"]

join_op_flights_mean_air_time['CHK_DEST_IATA_US'] = join_op_flights_mean_air_time['CHK_DEST_IATA_US'].replace(np.nan, "???").astype(str)
print(join_op_flights_mean_air_time[join_op_flights_mean_air_time.CHK_DEST_IATA_US == "???"])
join_op_flights_mean_air_time = join_op_flights_mean_air_time[join_op_flights_mean_air_time.CHK_DEST_IATA_US == "US"]

join_op_flights_mean_air_time['CHK_DEST_IATA_TYPE'] = join_op_flights_mean_air_time['CHK_DEST_IATA_TYPE'].replace(np.nan, "???").astype(str)
print(join_op_flights_mean_air_time[join_op_flights_mean_air_time.CHK_DEST_IATA_TYPE == "???"])
join_op_flights_mean_air_time = join_op_flights_mean_air_time[join_op_flights_mean_air_time.CHK_DEST_IATA_TYPE.isin(options)]
print(join_op_flights_mean_air_time.dtypes)


#Filter Cancelled flights
operated_flights = join_op_flights_mean_air_time[join_op_flights_mean_air_time["CANCELLED"] == 0]
cancelled_flights = join_op_flights_mean_air_time[join_op_flights_mean_air_time["CANCELLED"] == 1]

