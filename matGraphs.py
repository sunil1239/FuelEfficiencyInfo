import matplotlib.pyplot as plt
import json, datetime
class showGraph:
    def displayGraph(self):
        with open("fuelInfo.json") as fd:
            data = json.load(fd)
        dates = []
        rates = []
        for keys, values in data['DailyRate'].items():
            dates.append(keys)

        dates.sort()
        for each in dates:
            rates.append(data['DailyRate'][each])
        x = dates
        y = rates
        plt.plot(x,y)
        plt.xlabel("Somethin X")
        plt.ylabel("Something Y")

        plt.show()

if __name__ == '__main__':
    showGraph().displayGraph()