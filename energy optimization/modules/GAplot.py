import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import date, timedelta

from modules import system_ as sys
from modules import getdata as data


def plot_individual(D, Gl, Gb, g, state):
    plt.figure(figsize=(20, 5))
    plt.plot(D, label='Discharge')
    

    sol = np.zeros(len(D))
    for i in range(len(D)):
        sol[i] = g[i] *sys.solar_gen(i, state)
    plt.plot(sol, label="Generated")

    
    plt.plot(state["load"], label='Total Load')

    plt.plot(Gb, label='Battery Charging')
    
    
    plt.plot(Gl, label='Grid')
    
    
    
    plt.legend()
    plt.show()



def plot_battery(D,Gb,g, state):
    check, gen, B = sys.battery_sim2(D,Gb,g, state)

    plt.figure(figsize=(20, 5))
    plt.plot(B, label='SoC')

    plt.plot(D, label='Discharge')

    plt.plot(Gb, label='G_Charge')



    plt.plot(gen/g * (np.ones(len(g)) - g), label='S_Charge')

    plt.legend()
    plt.show()


def plot_fitness(fitness_history):
    
    plt.figure()
    plt.plot(fitness_history)
    plt.xlabel("Generation")
    plt.ylabel("Best fitness")
    plt.title("GA Convergence")
    plt.grid(True)
    plt.show()


def plot_state():
    
    
    zone = "SE3"

    yesterday = date.today() - timedelta(days=1)

    spotprice = data.get_spotprice(zone)

    rows = spotprice["areas"]["SE3"]["values"]
    spotprice = pd.DataFrame(rows)
    spotprice["start"] = pd.to_datetime(spotprice["start"])
    spotprice["end"] = pd.to_datetime(spotprice["end"])

    irradiance = data.get_irradiance()
    rows = irradiance["value"]
    irradiance = pd.DataFrame(rows)
    irradiance["timestamp"] = pd.to_datetime(irradiance["date"], unit="ms", utc=True)
    irradiance["value"] = irradiance["value"].astype(float)
    irradiance = irradiance[["timestamp", "value", "quality"]]
    irradiance = irradiance[irradiance["timestamp"].dt.date == yesterday]
    
    file_name = "n_fot2025-01-10.xls" # path to file + file name

    df = pd.read_excel(file_name)

    load = df.iloc[:, 0:2].tail(24)
    load.columns = ["time", "value"]
    load["time"] = pd.to_datetime(load["time"])


    fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(20, 15))

    # Example plots
    axes[0].plot(spotprice["end"].dt.hour,spotprice["value"], '-o')
    axes[0].set_title(f"Electricity Price {spotprice["end"].dt.date.iloc[0]}")
    axes[0].set_xlabel("Hours")
    axes[0].set_ylabel("EUR/MWh")
    axes[0].set_xticks(range(24))

    axes[1].plot(irradiance["timestamp"].dt.hour,irradiance["value"], '-o')

    axes[1].set_xticks(range(25))
    axes[1].set_title(f"Irradiance {irradiance["timestamp"].dt.date.iloc[0]}")
    axes[1].set_xlabel("Hours")
    axes[1].set_ylabel("W/m^2")

    axes[2].plot(load["time"].dt.hour,-1*load["value"], '-o')
    axes[2].set_xticks(range(24))
    axes[2].set_title(f"Swedish grid load {load["time"].dt.date.iloc[0]}")
    axes[2].set_xlabel("Hours")
    axes[2].set_ylabel("MW")


    plt.tight_layout()
    plt.show()