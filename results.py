import numpy as np

class Results:
    def __init__(self):
        self.MinTime = None
        self.SredTime = None
        self.MaxTime = None
        self.SredTimeRestore = None
        self.CoefReady = None
        self.HistogramFailure = None
        self.HistogramRestore = None
        self.bars = 100

    def CalcMinTime(self, data):
        self.MinTime = np.min(data)

    def CalcSredTime(self, data):
        self.SredTime = np.average(data)

    def CalcMaxTime(self, data):
        self.MaxTime = np.max(data)

    def CalcSredTimeRestore(self, data):
        self.SredTimeRestore = np.average(data)

    def CalcCoefReady(self):
        self.CoefReady = self.SredTime / (self.SredTime + self.SredTimeRestore)

    def CalcHistogram(self, data, mindata = None, maxdata = None, internal = True, restore = False):
        if internal:
            min = np.min(data)
            max = np.max(data)
        else:
            min = mindata
            max = maxdata
        if restore:
            self.HistogramRestore = np.histogram(data, self.bars, (min, max), density=False)
        else:
            self.HistogramFailure = np.histogram(data, self.bars, (min, max), density=False)

    def get_data_result(self):
        return [self.MinTime, self.MaxTime, self.SredTime, self.SredTimeRestore, self.CoefReady]

    def get_histogram_failure(self):
        return self.HistogramFailure

    def get_histogram_restore(self):
        return self.HistogramRestore

    @staticmethod
    def CalcProbGraph(list_data):
        common_multiply = 1.0
        for probability in list_data[1]:
            object_probability = np.subtract(1, np.exp(np.multiply(-probability, list_data[0])))
            common_multiply = np.multiply(common_multiply, object_probability)
        common_probability = np.subtract(1, common_multiply)
        return common_probability

    def Prob(self, data):
        common_list = []
        probability_list = []
        x = np.linspace(0, self.MaxTime / 90, 100)
        common_list.append(x)
        for item in data:
            sum_prob = 0
            for obj in item:
                sum_prob = sum_prob + obj[1]
            probability_list.append(sum_prob)
        common_list.append(probability_list)
        result = self.CalcProbGraph(common_list)
        return [result, x]