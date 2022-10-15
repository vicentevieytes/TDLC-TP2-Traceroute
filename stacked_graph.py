import matplotlib.pyplot as plt
import numpy


labels = ['India','Australia','Sudáfrica', 'Qatar']
ttls = [[293.62, 1.26, 2.57, 0.07],
[29.88, 0.1, 28.14, 4.63],
[104.94, 20.5, 24.34, 0.14],
[15.06, 106.12, 0.84, 250.21],
[0.46, 9.67, 107.31, 7.93],
[221.175, 27.84, 8.93, 95.13],
[2.865, 8.63, 300.62, 2.2],
[10.23, 1.66, 0, 24.81],
 [0, 12.04, 0, 0],
 [0, 0.53, 0, 0],
 [0, 194.5, 0, 0],
 [0, 0.52, 0, 0],
 [0, 98.09, 0, 0],
 [0, 7.195, 0, 0]]

width = 0.35       # the width of the bars: can also be len(x) sequence

fig, ax = plt.subplots()
bottom = [0,0,0,0]
i = 1
for ttl in ttls:
    ax.bar(labels, ttl, width, bottom=bottom, label=('TTL = ' + str(i)))
    bottom = numpy.add(bottom, ttl)
    i+=1

ax.set_ylabel('RTT en ms')
ax.set_title('Comparativa de RTTs')
ax.legend()

plt.show()