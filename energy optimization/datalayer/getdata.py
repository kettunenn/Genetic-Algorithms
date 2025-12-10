from pprint import pprint
from nordpool import elspot
import pandas as pd
import requests
from datetime import date, timedelta

# Initialize class for fetching the prices.
# An optional currency parameter can be provided, default is EUR.

# Fetch tomorrow's prices for Finland and print the resulting dictionary.
# If the prices are reported as None, it means that the prices fetched aren't yet available.
# The library by default tries to fetch prices for tomorrow and they're released ~13:00 Swedish time.


def get_spotprice(zone="SE3"):
    prices_spot = elspot.Prices()
    
    spotprice = prices_spot.fetch(end_date=date.today() - timedelta(days=1),areas=[zone])

    return spotprice

def get_irradiance():
    version   = "latest"
    parameter = 11 # Global Irradians (svenska stationer)	medelvärde 1 timma, varje timme	watt per kvadratmeter
    station   = 98735 #Stockholm Sol
    period    = "latest-months" 
    data      = "json"
    url =     f"https://opendata-download-metobs.smhi.se/api/version/{version}/parameter/{parameter}/station/{station}/period/{period}/data.{data}"

    r = requests.get(url)
    r.raise_for_status()

    return r.json()

def get_load():


    file_name = "n_fot2025-01-10.xls" # path to file + file name

    df = pd.read_excel(file_name)

    return df

def gen_state():

    yesterday = date.today() - timedelta(days=1)

    spotprice  = get_spotprice()
    irradiance = get_irradiance()
    load       = get_load() 


    rows = spotprice["areas"]["SE3"]["values"]
    spotprice = pd.DataFrame(rows)
    spotprice["start"] = pd.to_datetime(spotprice["start"])
    spotprice["end"] = pd.to_datetime(spotprice["end"])
    spotprice = spotprice.reset_index(drop=True)


    rows = irradiance["value"]
    irradiance = pd.DataFrame(rows)

    irradiance["timestamp"] = pd.to_datetime(irradiance["date"], unit="ms", utc=True)
    irradiance["value"] = irradiance["value"].astype(float)
    irradiance = irradiance[["timestamp", "value", "quality"]]
    irradiance = irradiance[irradiance["timestamp"].dt.date == yesterday]
    irradiance = irradiance.reset_index(drop=True)

    load = load.iloc[:, 0:2].tail(24)
    load.columns = ["time", "value"]
    load["value"] = -1*load["value"].astype(float)
    load["time"] = pd.to_datetime(load["time"])
    load = load.reset_index(drop=True)

    df = pd.concat([spotprice[["end","value"]],irradiance[["value"]]], axis=1)
    df = pd.concat([df,load[["value"]]/240], axis=1)

    
    df.columns= ["time", "spotprice", "irradiance", "load"]
    return df




