import matplotlib.pyplot as plt
import numpy as np

plt.figure(figsize=(14,10))

def show_frequency(x, y, i):
  plt.subplot(3, 1, i)
  plt.stem(x, y, 'r', use_line_collection=True)
  plt.plot(x, y)
  plt.xlabel("time")
  plt.ylabel("amplitude")
  plt.grid()

frequency = 7
samples = 100
x = np.arange(samples)
y1 = np.sin(2*np.pi*frequency*(x/samples))

frequency2 = 3
y2 = frequency2 * np.sin(2*np.pi*frequency2*(x/samples))

# compose a new curve
ys = y1 + y2

show_frequency(x, y1, 1)
show_frequency(x, y2, 2)
show_frequency(x, ys, 3)

plt.show()