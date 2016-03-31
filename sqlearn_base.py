from __future__ import print_function
import fileinput
from glob import glob
import pickle
import sys
import time

from sklearn.metrics import accuracy_score
import numpy as np
import sklearn

label_to_index={
        'C1_TOP_PLAYER_FOREHAND_SERVE':0,
        'C2_TOP_PLAYER_BACKHAND_SERVE':1,
        'C3_BOTTOM_PLAYER_FOREHAND_SERVE':2,
        'C4_BOTTOM_PLAYER_BACKHAND_SERVE':3,
        'C5_TOP_PLAYER_FOREHAND_LOOP':4,
        'C6_TOP_PLAYER_BACKHAND_LOOP':5,
        'C7_BOTTOM_PLAYER_FOREHAND_LOOP':6,
        'C8_BOTTOM_PLAYER_BACKHAND_LOOP':7,
        'C9_TOP_PLAYER_FOREHAND_BLOCK':8,
        'C10_TOP_PLAYER_BACKHAND_BLOCK':9,
        'C11_BOTTOM_PLAYER_FOREHAND_BLOCK':10,
        'C12_BOTTOM_PLAYER_BACKHAND_BLOCK':11,
        'C13_TOP_PLAYER_FOREHAND_FLIP':12,
        'C14_TOP_PLAYER_BACKHAND_FLIP':13,
        'C15_BOTTOM_PLAYER_FOREHAND_FLIP':14,
        'C16_BOTTOM_PLAYER_BACKHAND_FLIP':15,
        'C17_TOP_PLAYER_FOREHAND_CHOP':16,
        'C18_TOP_PLAYER_BACKHAND_CHOP':17,
        'C19_BOTTOM_PLAYER_FOREHAND_CHOP':18,
        'C20_BOTTOM_PLAYER_BACKHAND_CHOP':19,
        'C21_TOP_PLAYER_UNDER_NET':20,
        'C22_TOP_PLAYER_HIT_OUT':21,
        'C23_TOP_PLAYER_FOREHAND_MISS_HIT':22,
        'C24_TOP_PLAYER_BACKHAND_MISS_HIT':23,
        'C25_BOTTOM_PLAYER_UNDER_NET':24,
        'C26_BOTTOM_PLAYER_HIT_OUT':25,
        'C27_BOTTOM_PLAYER_FOREHAND_MISS_HIT':26,
        'C28_BOTTOM_PLAYER_BACKHAND_MISS_HIT':27,
        'C29_TOP_PLAYER_BACKHAND_LOB':28,
        'C30_BOTTOM_PLAYER_BACKHAND_LOB':29}
index_to_label={
        0:'C1_TOP_PLAYER_FOREHAND_SERVE',
        1:'C2_TOP_PLAYER_BACKHAND_SERVE',
        2:'C3_BOTTOM_PLAYER_FOREHAND_SERVE',
        3:'C4_BOTTOM_PLAYER_BACKHAND_SERVE',
        4:'C5_TOP_PLAYER_FOREHAND_LOOP',
        5:'C6_TOP_PLAYER_BACKHAND_LOOP',
        6:'C7_BOTTOM_PLAYER_FOREHAND_LOOP',
        7:'C8_BOTTOM_PLAYER_BACKHAND_LOOP',
        8:'C9_TOP_PLAYER_FOREHAND_BLOCK',
        9:'C10_TOP_PLAYER_BACKHAND_BLOCK',
        10:'C11_BOTTOM_PLAYER_FOREHAND_BLOCK',
        11:'C12_BOTTOM_PLAYER_BACKHAND_BLOCK',
        12:'C13_TOP_PLAYER_FOREHAND_FLIP',
        13:'C14_TOP_PLAYER_BACKHAND_FLIP',
        14:'C15_BOTTOM_PLAYER_FOREHAND_FLIP',
        15:'C16_BOTTOM_PLAYER_BACKHAND_FLIP',
        16:'C17_TOP_PLAYER_FOREHAND_CHOP',
        17:'C18_TOP_PLAYER_BACKHAND_CHOP',
        18:'C19_BOTTOM_PLAYER_FOREHAND_CHOP',
        19:'C20_BOTTOM_PLAYER_BACKHAND_CHOP',
        20:'C21_TOP_PLAYER_UNDER_NET',
        21:'C22_TOP_PLAYER_HIT_OUT',
        22:'C23_TOP_PLAYER_FOREHAND_MISS_HIT',
        23:'C24_TOP_PLAYER_BACKHAND_MISS_HIT',
        24:'C25_BOTTOM_PLAYER_UNDER_NET',
        25:'C26_BOTTOM_PLAYER_HIT_OUT',
        26:'C27_BOTTOM_PLAYER_FOREHAND_MISS_HIT',
        27:'C28_BOTTOM_PLAYER_BACKHAND_MISS_HIT',
        28:'C29_TOP_PLAYER_BACKHAND_LOB',
        29:'C30_BOTTOM_PLAYER_BACKHAND_LOB'}

def load_data():
    # files = glob('./seq_data/point_00125.dat')
    files = glob('./seq_data_fc6_normalized_testset/point_*.dat')
    pairwise_potential = [[0 for _ in xrange(30)] for _ in xrange(30)]

    test_data = []
    test_label = []
    num_of_pairs = 0
    # print("Loading test data...", end=" ")
    for dat_file in files:
        test_data_pt = []
        test_label_pt = []
        prev_label = None
        with open(dat_file) as f:
            for line in f:
                line = line.strip().split()
                test_label_pt.append(line[-1])
                test_data_pt.append(line[:-1])
                if prev_label != None:
                    pairwise_potential[label_to_index[prev_label]][label_to_index[line[-1]]]+=1
                    num_of_pairs += 1
                prev_label = line[-1]
        test_data.append(test_data_pt)
        test_label.append(test_label_pt)
    for i,_ in enumerate(pairwise_potential):
        for j,_ in enumerate(pairwise_potential[i]):
            pairwise_potential[i][j] = 1.0*pairwise_potential[i][j]/num_of_pairs

    print('PAIRWISE_POTENTIALS:'+str(pairwise_potential))
    print(sum(map(sum, pairwise_potential)))

    return test_data, test_label, pairwise_potential


if __name__ == "__main__":
    start_time = time.time()
    test_data, test_label, pairwise_potential = load_data()
    clf = pickle.load(open( "./fc6_normalized_lr_clf_6videos.pickle", "rb" ))

    numCorrectPred = 0
    accuracies = []
    for i,_ in enumerate(test_data):
        numCorrectPred = 0
        for j,_ in enumerate(test_data[i]):
            min_ind = max(0, j-4)
            max_ind = min(len(test_data[i]), j+5)
            sum_dat = np.array(test_data[i][min_ind], dtype=np.float64)
            for k in xrange(min_ind+1, max_ind):
                sum_dat += np.array(test_data[i][k], dtype=np.float64)

            # dat = np.array(test_data[i][j], dtype=np.float64)
            dat = sum_dat / 9
            y_pred = clf.predict(dat)[0].replace('_selected', '')
            # predict_probability = clf.predict_proba(dat)
            if y_pred == test_label[i][j]:
                numCorrectPred += 1
            # print("Index: %d; Predict: %s; Actual: %s"%(j, y_pred, test_label[i][j]))
        accuracies.append(100.0*numCorrectPred/len(test_data[i]))
        print("Accuracy: %.3f" % (accuracies[-1]))

    print("Overall Accuracy: %.3f" % (sum(accuracies)/len(accuracies)))
    print("Total time: %d"%(time.time()-start_time))
    # print("Accuracy: %.3f" % (100 * accuracy_score(y_test, y_pred)))
