#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 16:18:57 2026

@author: finleymartin
"""


import pandas as pd
import numpy as np
from tkinter import Tk, mainloop, Button
from tkinter import ttk

pbp_25 = pd.read_csv("pbp2025.csv")
player_map = pd.read_csv("PlayerIndex_nba_stats.csv")
player_map = player_map.loc[:, ["PERSON_ID", "PLAYER_LAST_NAME", "PLAYER_FIRST_NAME"]]
player_map = player_map.rename(columns={"PERSON_ID": "playerid"})

result = pd.merge(pbp_25, player_map, on = "playerid")
result["Player Name"] = result["PLAYER_FIRST_NAME"] + " " + result["PLAYER_LAST_NAME"]

shots = result.loc[:, ["playerid", "Player Name","x", "y","dist", "type", "subtype", "desc"]]
shots = shots[shots["type"].isin(["Made Shot", "Missed Shot"])]
shots["made"] = (shots["type"] == "Made Shot").astype('int')
shots["3PT"] = np.where(shots["desc"].str.contains("3PT"), 1, 0)
shots["3PT_made"] = shots["3PT"] * shots["made"]

players = shots["Player Name"].unique().tolist()

master = Tk()

player_dropdown = ttk.Combobox(master, values=players)
player_dropdown.set(players[0])
player_dropdown.pack()

name = None

def ok():
    global name
    name = player_dropdown.get()

button = Button(master, text="OK", command=ok)
button.pack()

mainloop()

shots['court_x'] = shots['x']/10 + 25
shots['court_y'] = shots['y']/10 + 5.25

shots_player = shots[shots["Player Name"] == name]
threeppct = round(sum(shots_player["3PT_made"]) / sum(shots_player["3PT"]), 3)