import numpy as np

class KnapsackProblem:
    def __init__(self, oFile):

        # initialize instance variables:
        self.items = []
        self.maxCapacity = 0

        # initialize the data:
        self.__initData(oFile)

    def __len__(self):
        """
        :return: the total number of items defined in the problem
        """
        return len(self.items)

    def __initData(self, oFile):#nhap du lieu tu file KP
        cnt = 0

        data = oFile.readlines()

        self.maxCapacity = int(data[2])

        for i in range(4, 4 + int(data[1])):
            self.items.append((cnt, int(data[i].split(" ")[1]), int(data[i].split(" ")[0])))
            cnt += 1

        oFile.close()

    def getValue(self, zeroOneList):
        """
        Calculates the value of the selected items in the list, while ignoring items that will cause the accumulating weight to exceed the maximum weight
        :param zeroOneList: a list of 0/1 values corresponding to the list of the problem's items. '1' means that item was selected.
        :return: the calculated value
        """

        totalWeight = totalValue = 0

        for i in range(len(zeroOneList)):
            item, weight, value = self.items[i]
            if totalWeight + weight <= self.maxCapacity:
                totalWeight += zeroOneList[i] * weight
                totalValue += zeroOneList[i] * value
        return totalValue

    def getSumResults(self, zeroOneList, oResFile):
        """
        Prints the selected items in the list, while ignoring items that will cause the accumulating weight to exceed the maximum weight
        :param zeroOneList: a list of 0/1 values corresponding to the list of the problem's items. '1' means that item was selected.
        """
        totalWeight = totalValue = totalItems = 0

        for i in range(len(zeroOneList)):
            item, weight, value = self.items[i]
            if totalWeight + weight <= self.maxCapacity:
                if zeroOneList[i] > 0:
                    totalItems += 1
                    totalWeight += weight
                    totalValue += value
        # print("Total packed items = {}, Total weight = {}, Total value = {}".format(totalItems, totalWeight, totalValue))
        # print("Total value =", totalValue)
        # print("Total weight =", totalWeight)
        # print("Total packed items =", totalItems)
        return totalValue, totalWeight, totalItems