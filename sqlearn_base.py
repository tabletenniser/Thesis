from __future__ import print_function
import fileinput
from glob import glob
import pickle
import sys

from sklearn.metrics import accuracy_score
import numpy as np
import sklearn


def load_data():
    files = glob('./seq_data/point_00125.dat')

    test_data = []
    test_label = []
    # print("Loading test data...", end=" ")
    for dat_file in files:
        test_data_pt = []
        test_label_pt = []
        with open(dat_file) as f:
            for line in f:
                line = line.strip().split()
                test_label_pt.append(line[-1])
                test_data_pt.append(line[:-1])
        test_data.append(test_data_pt)
        test_label.append(test_label_pt)

    return test_data, test_label


if __name__ == "__main__":
    test_data, test_label = load_data()
    clf = pickle.load(open( "./fc7_unnormalized_clf_101pts.pickle", "rb" ))

    numCorrectPred = 0
    totalPred = 0
    for i,_ in enumerate(test_data):
        for j,_ in enumerate(test_data[i]):
            y_pred = clf.predict(test_data[i][j])[0].replace('_selected', '')
            if y_pred == test_label[i][j]:
                numCorrectPred += 1
            print("Index: %d; Predict: %s; Actual: %s"%(j, y_pred, test_label[i][j]))
            totalPred += 1

    print("Accuracy: %.3f" % (100.0 * numCorrectPred/totalPred))
    # print("Accuracy: %.3f" % (100 * accuracy_score(y_test, y_pred)))
