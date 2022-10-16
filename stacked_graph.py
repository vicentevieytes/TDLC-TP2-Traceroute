import matplotlib.pyplot as plt
import numpy

def pad(sample, desired_length):
    for i in range(desired_length):
        if i >= len(sample):
            sample.append(0)
    return sample

def main():
    resultados_india = [293.62, 29.88, 104.94, 15.06, 0.46, 221.175, 2.865, 10.23]
    resultados_australia = [1.26, 0.1, 20.5, 106.12, 9.67, 27.84, 8.63, 1.66, 12.04, 0.53, 194.5, 0.52, 98.09, 7.195]
    resultados_sudafrica =[2.57, 28.14, 24.34, 0.84, 107.31, 8.93, 300.62]
    resultados_qatar = [0.07, 4.63, 0.14, 250.21, 7.93, 95.13, 2.2, 24.81]

    labels = ['India','Australia','Sudáfrica', 'Qatar']

    ttls = []

    max_len = max(len(resultados_india), len(resultados_australia), len(resultados_qatar), len(resultados_sudafrica))
    resultados_australia = pad(resultados_australia, max_len)
    resultados_india = pad(resultados_india, max_len)
    resultados_qatar = pad(resultados_qatar, max_len)
    resultados_sudafrica = pad(resultados_sudafrica, max_len)

    for i in range(max_len):
        ttls.append([resultados_india[i], resultados_australia[i], resultados_sudafrica[i], resultados_qatar[i]])

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

if __name__ == "__main__":
    main()
