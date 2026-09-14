#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 13 21:19:45 2026

@author: finleymartin
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd
import seaborn as sns

fig, ax = plt.subplots(figsize=(10,8))

pbp_25 = pd.read_csv("pbp2025.csv")
shots = pbp_25.loc[:, ["playerid", "player", "x", "y","dist", "type", "subtype"]]
shots = shots[shots["type"].isin(["Made Shot", "Missed Shot"])]
shots["made"] = (shots["type"] == "Made Shot").astype('int')

print("enter player name: F. Last:")
name = input()

shots['court_x'] = shots['x']/10 + 25
shots['court_y'] = shots['y']/10 + 5.25

shots_player = shots.query('player == @name')


sns.kdeplot(shots_player.loc[shots['made'] == 1],
            x = 'court_x',
            y = 'court_y',
            fill = True,
            cmap = "Reds",
            levels = 4)


ax.scatter(
    shots_player.loc[shots['made'] == 1, "court_x"],
    shots_player.loc[shots['made'] == 1, "court_y"],
    alpha=1,
    s=20,
    color = 'green',
    marker = 'o'
)

ax.scatter(
    shots_player.loc[shots['made'] == 0, "court_x"],
    shots_player.loc[shots['made'] == 0, "court_y"],
    alpha=0.5,
    s=20,
    color = 'red',
    marker = 'x'
)

#half court size
ax.add_patch(
    patches.Rectangle(
        (0, 0), 50, 47,
        fill=False,
        linewidth=2
    )
)

#right line
ax.add_patch(
    patches.Rectangle(
        (47, 0), 0, 14,
        fill=False,
        linewidth=2
    )
)

#backboard
ax.add_patch(
    patches.Rectangle(
        (22, 3.3), 6, 0,
        fill=False,
        linewidth=2
    )
)

#left line
ax.add_patch(
    patches.Rectangle(
        (3, 0), 0, 14,
        fill=False,
        linewidth=2
    )
)

#arc
ax.add_patch(
    patches.Arc(
        (25, 14), 44, 29,
        fill=False,
        linewidth=2,
        theta2 = 180
    )
)
#paint
ax.add_patch(
    patches.Rectangle(
        (17, 0), 16, 19,
        fill=False,
        linewidth=2
    )
)

#midcourt circle
ax.add_patch(
    patches.Circle(
        (25, 47), 6,
        fill=False,
        linewidth=2
    )
)

#hoop
ax.add_patch(
    patches.Circle(
        (25, 5.25), 2,
        fill=False,
        linewidth=2
    )
)

#midcourt circle
ax.add_patch(
    patches.Circle(
        (25, 19), 6,
        fill=False,
        linewidth=2
    )
)


ax.set_xlim(0, 50)
ax.set_ylim(0, 47)


ax.set_aspect('equal')

plt.title(f"{name} 2024-2025 Shot Distribution", loc = 'center')
plt.axis('off')
plt.show()


#*** MAKE GIT REPO WITH UPDATES STARTING FROM JUST THE COURT PLOT***

# percent of total shots made and shots within an area made
# better graphics
# get all years csvs- put into one large clean dataset and be able to pick year and player
# create 3pt percent made by adjusting x if higher than 14 and y greater than 23.75 or x less than 14 y greater than 22
# create another box boundry inverse of arc and outside of lines that is the 3pt area and shot is 3pt if in that area