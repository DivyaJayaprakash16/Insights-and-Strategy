# -*- coding: utf-8 -*-

"""
Project: Airline Data Challenge
Module: Data Analysis
File: Flights.csv, Tickets.csv,Airport_Codes.csv
Author: Capital One - Data Analysis Team
Date: 02/14/2024
Version: 1.0
"""

import Routes as rt

print("Question #1")
routes_inscope = rt.routes_inscope
busiest_round_trip_routes = routes_inscope[['ROUTE', 'ISO_COUNTRY','POINT_A', 'POINT_A_NAME', 'POINT_A_IATA_TYPE','POINT_A_CITY_NAME',
                                                    'POINT_B', 'POINT_B_NAME', 'POINT_B_IATA_TYPE','POINT_B_CITY_NAME','ROUNDTRIP_FLIGHTS']]
busiest_round_trip_routes = busiest_round_trip_routes.sort_values(['ROUNDTRIP_FLIGHTS'], ascending=[False])
busiest_round_trip_routes = busiest_round_trip_routes.head(10)
print(busiest_round_trip_routes)
busiest_round_trip_routes.to_excel("Busiest RoundTrip Routes.xlsx") 
#*************************************************************************************************************************************
print("Question #2")
routes_inscope = routes_inscope.sort_values(['TOTAL_PROFIT'], ascending=[False])
profitable_round_trip_routes = routes_inscope[['ROUTE', 'ISO_COUNTRY','POINT_A', 'POINT_A_NAME', 'POINT_A_IATA_TYPE','POINT_A_CITY_NAME',
                                                       'POINT_B', 'POINT_B_NAME', 'POINT_B_IATA_TYPE','POINT_B_CITY_NAME',
                                                       'TOTAL_PROFIT','TOTAL_REVENUE','TOTAL_COST','ROUNDTRIP_FLIGHTS','ROUNDTRIP_PASSENGERS',
                                                       'BREAKEVEN_FLIGHTS','PROFIT_COST_RATIO']].head(10)
print(profitable_round_trip_routes)
profitable_round_trip_routes.to_excel("Profitable Roundtrip Routes.xlsx") 
#*************************************************************************************************************************************
print("Question #3")
options = ['SLC-TWF', 'MDT-PHL', 'CLT-FLO', 'JFK-LAX', 'LAX-SFO']
recommended_routes = routes_inscope[['ROUTE', 'ISO_COUNTRY','POINT_A', 'POINT_A_NAME', 'POINT_A_IATA_TYPE','POINT_A_CITY_NAME',
                                                       'POINT_B', 'POINT_B_NAME', 'POINT_B_IATA_TYPE','POINT_B_CITY_NAME',
                                                       'BREAKEVEN_FLIGHTS','ROUTE_DISTANCE','AVG_OCCUPANCY_RATE_A_TO_B','AVG_OCCUPANCY_RATE_B_TO_A',
                                                       'PROFIT_COST_RATIO','TOTAL_PROFIT','ROUNDTRIP_FLIGHTS','ROUNDTRIP_PASSENGERS']][routes_inscope['ROUTE'].isin(options)]

recommended_routes.insert(0,"RATIONALE_FOR_RECOMMENDATION","",True)
recommended_routes["RATIONALE_FOR_RECOMMENDATION"][recommended_routes['ROUTE']=='SLC-TWF'] = 'QUICK BREAKEVEN ROUTE'
recommended_routes["RATIONALE_FOR_RECOMMENDATION"][recommended_routes['ROUTE']=='MDT-PHL'] = 'SHORT DISTANCE FLIGHT WITH HIGH OCCUPANCY,HIGH PROFIT TO COST RATIO AND QUICK BREAKEVEN'
recommended_routes["RATIONALE_FOR_RECOMMENDATION"][recommended_routes['ROUTE']=='CLT-FLO'] = 'HIGH PROFIT TO COST RATIO ROUTE'
recommended_routes["RATIONALE_FOR_RECOMMENDATION"][recommended_routes['ROUTE']=='JFK-LAX'] = 'HIGH PROFIT PER QUARTER ROUTE'
recommended_routes["RATIONALE_FOR_RECOMMENDATION"][recommended_routes['ROUTE']=='LAX-SFO'] = 'BUSIEST ROUTE'
print(recommended_routes)
recommended_routes.to_excel("Recommended Routes.xlsx") 
#*************************************************************************************************************************************
print("Question #4")
options = ['SLC-TWF', 'MDT-PHL', 'CLT-FLO', 'JFK-LAX', 'LAX-SFO']
recommended_routes = routes_inscope[['ROUTE', 'ISO_COUNTRY','POINT_A', 'POINT_A_NAME', 'POINT_A_IATA_TYPE','POINT_A_CITY_NAME',
                                                       'POINT_B', 'POINT_B_NAME', 'POINT_B_IATA_TYPE','POINT_B_CITY_NAME',
                                                       'BREAKEVEN_FLIGHTS','ROUTE_DISTANCE','AVG_OCCUPANCY_RATE_A_TO_B','AVG_OCCUPANCY_RATE_B_TO_A',
                                                       'PROFIT_COST_RATIO','TOTAL_PROFIT','ROUNDTRIP_FLIGHTS','ROUNDTRIP_PASSENGERS','TOTAL_REVENUE','TOTAL_COST']][routes_inscope['ROUTE'].isin(options)]
recommended_routes.insert(0,"RATIONALE_FOR_RECOMMENDATION","",True)
recommended_routes["RATIONALE_FOR_RECOMMENDATION"][recommended_routes['ROUTE']=='SLC-TWF'] = 'QUICK BREAKEVEN ROUTE'
recommended_routes["RATIONALE_FOR_RECOMMENDATION"][recommended_routes['ROUTE']=='MDT-PHL'] = 'SHORT DISTANCE FLIGHT WITH HIGH OCCUPANCY,HIGH PROFIT TO COST RATIO AND QUICK BREAKEVEN'
recommended_routes["RATIONALE_FOR_RECOMMENDATION"][recommended_routes['ROUTE']=='CLT-FLO'] = 'HIGH PROFIT TO COST RATIO ROUTE'
recommended_routes["RATIONALE_FOR_RECOMMENDATION"][recommended_routes['ROUTE']=='JFK-LAX'] = 'HIGH PROFIT PER QUARTER ROUTE'
recommended_routes["RATIONALE_FOR_RECOMMENDATION"][recommended_routes['ROUTE']=='LAX-SFO'] = 'BUSIEST ROUTE'
print(recommended_routes)
recommended_routes.to_excel("Recommended Routes.xlsx") 
#*************************************************************************************************************************************
print("Question #5")
options = ['SLC-TWF', 'MDT-PHL', 'CLT-FLO', 'JFK-LAX', 'LAX-SFO']
# Below list of KPIs shall be tracked on a weekly basis
key_performance_indicators = routes_inscope[['ROUTE', 'ISO_COUNTRY','POINT_A', 'POINT_A_NAME', 'POINT_A_IATA_TYPE','POINT_A_CITY_NAME',
                                                       'POINT_B', 'POINT_B_NAME', 'POINT_B_IATA_TYPE','POINT_B_CITY_NAME',
                                                       'BREAKEVEN_FLIGHTS','AVG_OCCUPANCY_RATE_A_TO_B','AVG_OCCUPANCY_RATE_B_TO_A',
                                                       'PROFIT_COST_RATIO','TOTAL_PROFIT','ROUNDTRIP_PASSENGERS','TOTAL_REVENUE','TOTAL_COST',
                                                       'ROUNDTRIP_FLIGHTS','ROUNDTRIP_CAN_FLIGHTS','TOTAL_ROUTE_DELAY','AVG_DELAY_LEG_A_TO_B',
                                                       'AVG_DELAY_LEG_B_TO_A']][routes_inscope['ROUTE'].isin(options)]
key_performance_indicators.insert(0,"RATIONALE_FOR_RECOMMENDATION","",True)
key_performance_indicators["RATIONALE_FOR_RECOMMENDATION"][key_performance_indicators['ROUTE']=='SLC-TWF'] = 'QUICK BREAKEVEN ROUTE'
key_performance_indicators["RATIONALE_FOR_RECOMMENDATION"][key_performance_indicators['ROUTE']=='MDT-PHL'] = 'SHORT DISTANCE FLIGHT WITH HIGH OCCUPANCY,HIGH PROFIT TO COST RATIO AND QUICK BREAKEVEN'
key_performance_indicators["RATIONALE_FOR_RECOMMENDATION"][key_performance_indicators['ROUTE']=='CLT-FLO'] = 'HIGH PROFIT TO COST RATIO ROUTE'
key_performance_indicators["RATIONALE_FOR_RECOMMENDATION"][key_performance_indicators['ROUTE']=='JFK-LAX'] = 'HIGH PROFIT PER QUARTER ROUTE'
key_performance_indicators["RATIONALE_FOR_RECOMMENDATION"][key_performance_indicators['ROUTE']=='LAX-SFO'] = 'BUSIEST ROUTE'
print(key_performance_indicators)
key_performance_indicators.to_excel("Key Performance Indicators.xlsx") 





