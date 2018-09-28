#!/usr/bin/python3
import matplotlib as mpl
mpl.use('Agg')

from matplotlib.ticker import FormatStrFormatter
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np

# Beautiful colors
default_color = "#478DCB"
grey_color = "#D0D0D0"
colors = ["#CF3D1E", "#F15623", "#F68B1F", "#FFC60B", "#DFCE21",
  "#BCD631", "#95C93D", "#48B85C", "#00833D", "#00B48D", 
  "#60C4B1", "#27C4F4", "#3E67B1", "#4251A3", "#59449B", 
  "#6E3F7C", "#6A246D", "#8A4873", "#EB0080", "#EF58A0", "#C05A89"]

# Some default parameters for the figure
scale = 4
plotscale = 2.5

# # Dashed line for sensors
# plt.plot(
#   [a for a in range(1, 256)],
#   [a for a in range(1, 256)],
#   '--',
#   color=grey_color
# )

ntox = {0:'X', 1:'Y', 2:'Z'}

def sensor_oddity(hit, print_even, print_odd):
  if print_even and print_odd:
    return True
  elif print_even and hit.sensor_number%2 == 0:
    return True
  elif print_odd and hit.sensor_number%2 == 1:
    return True
  return False

def print_event_2d(event,
  tracks=[],
  x=2,
  y=0,
  track_color=0,
  filename="visual",
  print_tracks=True,
  print_even=True,
  print_odd=True):
  fig = plt.figure(figsize=(16*plotscale, 9*plotscale))
  ax = plt.axes()

  # Limits of the sensors
  limits = [(-20, 50), (-50, 20)]
  shift = 0.4
  if print_even:
    for s in event.sensors[::2]:
      plt.plot(
        [s.z+shift, s.z+shift],
        [limits[0][0], limits[0][1]],
        color=grey_color,
        alpha=0.4,
        linewidth=4
      )

  if print_odd:
    for s in event.sensors[1::2]:
      plt.plot(
        [s.z+shift, s.z+shift],
        [limits[1][0], limits[1][1]],
        color=grey_color,
        alpha=0.4,
        linewidth=4
      )

  plt.scatter(
    [h[x] for h in event.hits if sensor_oddity(h, print_even, print_odd)],
    [h[y] for h in event.hits if sensor_oddity(h, print_even, print_odd)],
    color=default_color,
    s=2*scale
  )

  if print_tracks:
    for t in tracks:
      plt.plot(
        [h[x] for h in t.hits],
        [h[y] for h in t.hits],
        color=colors[track_color],
        linewidth=1
      )

  plt.tick_params(axis='both', which='major', labelsize=4*scale)
  plt.xlabel(ntox[x], fontdict={'fontsize': 4*scale})
  plt.ylabel(ntox[y], fontdict={'fontsize': 4*scale}, rotation='horizontal')

  plt.savefig("output/" + filename + ".png", bbox_inches='tight', pad_inches=0.2)
  plt.savefig("output/" + filename + ".pdf", bbox_inches='tight', pad_inches=0.2, transparent=True)

  plt.close()