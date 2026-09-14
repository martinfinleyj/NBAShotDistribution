#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 13 21:19:45 2026

@author: finleymartin
"""

#must input player name in Playerdata:mapping.py first

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns

fig, ax = plt.subplots(figsize=(10,8))


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
        (22, 3.7), 6, 0,
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
        (25, 5.25), width = 47.3, height = 47.3,
        fill=False,
        linewidth=2,
        theta1 = 21.5,
        theta2 = 158.5
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
        (25, 5.25), 1.5,
        fill=False,
        linewidth=2
    )
)

#line left 2
ax.add_patch(
    patches.Rectangle(
        (0, 28), 3, 0, 
        fill=False,
        linewidth=2
    )
)

#line right 2
ax.add_patch(
    patches.Rectangle(
        (47, 28), 50, 0, 
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
plt.suptitle(f"3PT %: {threeppct}")
plt.axis('off')
plt.show()


# percent of total shots made and shots within an area made
# better graphics
# 2 get all years csvs- put into one large clean dataset and be able to pick year and player
# 1 create 3pt percent made by adjusting x if higher than 14 and y greater than 23.75 or x less than 14 y greater than 22