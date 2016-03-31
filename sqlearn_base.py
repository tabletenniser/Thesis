from __future__ import print_function
import fileinput
from glob import glob
import pickle
import sys
import time

from sklearn.metrics import accuracy_score
import numpy as np
import sklearn

PAIR_WEIGHT = 0.5
# label_to_index={
#         'C1_TOP_PLAYER_FOREHAND_SERVE':0,
#         'C10_TOP_PLAYER_BACKHAND_BLOCK':1,
#         'C11_BOTTOM_PLAYER_FOREHAND_BLOCK':2,
#         'C12_BOTTOM_PLAYER_BACKHAND_BLOCK':3,
#         'C13_TOP_PLAYER_FOREHAND_FLIP':4,
#         'C14_TOP_PLAYER_BACKHAND_FLIP':5,
#         'C15_BOTTOM_PLAYER_FOREHAND_FLIP':6,
#         'C16_BOTTOM_PLAYER_BACKHAND_FLIP':7,
#         'C17_TOP_PLAYER_FOREHAND_CHOP':8,
#         'C18_TOP_PLAYER_BACKHAND_CHOP':9,
#         'C19_BOTTOM_PLAYER_FOREHAND_CHOP':10,
#         'C2_TOP_PLAYER_BACKHAND_SERVE':11,
#         'C20_BOTTOM_PLAYER_BACKHAND_CHOP':12,
#         'C21_TOP_PLAYER_UNDER_NET':13,
#         'C22_TOP_PLAYER_HIT_OUT':14,
#         'C23_TOP_PLAYER_FOREHAND_MISS_HIT':15,
#         'C24_TOP_PLAYER_BACKHAND_MISS_HIT':16,
#         'C25_BOTTOM_PLAYER_UNDER_NET':17,
#         'C26_BOTTOM_PLAYER_HIT_OUT':18,
#         'C27_BOTTOM_PLAYER_FOREHAND_MISS_HIT':19,
#         'C28_BOTTOM_PLAYER_BACKHAND_MISS_HIT':20,
#         'C29_TOP_PLAYER_BACKHAND_LOB':21,
#         'C3_BOTTOM_PLAYER_FOREHAND_SERVE':22,
#         'C30_BOTTOM_PLAYER_BACKHAND_LOB':23,
#         'C4_BOTTOM_PLAYER_BACKHAND_SERVE':24,
#         'C5_TOP_PLAYER_FOREHAND_LOOP':25,
#         'C6_TOP_PLAYER_BACKHAND_LOOP':26,
#         'C7_BOTTOM_PLAYER_FOREHAND_LOOP':27,
#         'C8_BOTTOM_PLAYER_BACKHAND_LOOP':28,
#         'C9_TOP_PLAYER_FOREHAND_BLOCK':29}
# index_to_label={
#         0:'C1_TOP_PLAYER_FOREHAND_SERVE',
#         1:'C10_TOP_PLAYER_BACKHAND_BLOCK',
#         2:'C11_BOTTOM_PLAYER_FOREHAND_BLOCK',
#         3:'C12_BOTTOM_PLAYER_BACKHAND_BLOCK',
#         4:'C13_TOP_PLAYER_FOREHAND_FLIP',
#         5:'C14_TOP_PLAYER_BACKHAND_FLIP',
#         6:'C15_BOTTOM_PLAYER_FOREHAND_FLIP',
#         7:'C16_BOTTOM_PLAYER_BACKHAND_FLIP',
#         8:'C17_TOP_PLAYER_FOREHAND_CHOP',
#         9:'C18_TOP_PLAYER_BACKHAND_CHOP',
#         10:'C19_BOTTOM_PLAYER_FOREHAND_CHOP',
#         11:'C2_TOP_PLAYER_BACKHAND_SERVE',
#         12:'C20_BOTTOM_PLAYER_BACKHAND_CHOP',
#         13:'C21_TOP_PLAYER_UNDER_NET',
#         14:'C22_TOP_PLAYER_HIT_OUT',
#         15:'C23_TOP_PLAYER_FOREHAND_MISS_HIT',
#         16:'C24_TOP_PLAYER_BACKHAND_MISS_HIT',
#         17:'C25_BOTTOM_PLAYER_UNDER_NET',
#         18:'C26_BOTTOM_PLAYER_HIT_OUT',
#         19:'C27_BOTTOM_PLAYER_FOREHAND_MISS_HIT',
#         20:'C28_BOTTOM_PLAYER_BACKHAND_MISS_HIT',
#         21:'C29_TOP_PLAYER_BACKHAND_LOB',
#         22:'C3_BOTTOM_PLAYER_FOREHAND_SERVE',
#         23:'C30_BOTTOM_PLAYER_BACKHAND_LOB',
#         24:'C4_BOTTOM_PLAYER_BACKHAND_SERVE',
#         25:'C5_TOP_PLAYER_FOREHAND_LOOP',
#         26:'C6_TOP_PLAYER_BACKHAND_LOOP',
#         27:'C7_BOTTOM_PLAYER_FOREHAND_LOOP',
#         28:'C8_BOTTOM_PLAYER_BACKHAND_LOOP',
#         29:'C9_TOP_PLAYER_FOREHAND_BLOCK'}

label_to_index={
        'C10_TOP_PLAYER_BACKHAND_BLOCK':0,
        'C11_BOTTOM_PLAYER_FOREHAND_BLOCK':1,
        'C12_BOTTOM_PLAYER_BACKHAND_BLOCK':2,
        'C13_TOP_PLAYER_FOREHAND_FLIP':3,
        'C14_TOP_PLAYER_BACKHAND_FLIP':4,
        'C15_BOTTOM_PLAYER_FOREHAND_FLIP':5,
        'C16_BOTTOM_PLAYER_BACKHAND_FLIP':6,
        'C17_TOP_PLAYER_FOREHAND_CHOP':7,
        'C18_TOP_PLAYER_BACKHAND_CHOP':8,
        'C19_BOTTOM_PLAYER_FOREHAND_CHOP':9,
        'C1_TOP_PLAYER_FOREHAND_SERVE':10,
        # 'C2_TOP_PLAYER_BACKHAND_SERVE':11,
        'C20_BOTTOM_PLAYER_BACKHAND_CHOP':11,
        'C3_BOTTOM_PLAYER_FOREHAND_SERVE':12,
        # 'C4_BOTTOM_PLAYER_BACKHAND_SERVE':14,
        'C5_TOP_PLAYER_FOREHAND_LOOP':13,
        'C6_TOP_PLAYER_BACKHAND_LOOP':14,
        'C7_BOTTOM_PLAYER_FOREHAND_LOOP':15,
        'C8_BOTTOM_PLAYER_BACKHAND_LOOP':16,
        'C9_TOP_PLAYER_FOREHAND_BLOCK':17}
index_to_label={
        0:'C10_TOP_PLAYER_BACKHAND_BLOCK',
        1:'C11_BOTTOM_PLAYER_FOREHAND_BLOCK',
        2:'C12_BOTTOM_PLAYER_BACKHAND_BLOCK',
        3:'C13_TOP_PLAYER_FOREHAND_FLIP',
        4:'C14_TOP_PLAYER_BACKHAND_FLIP',
        5:'C15_BOTTOM_PLAYER_FOREHAND_FLIP',
        6:'C16_BOTTOM_PLAYER_BACKHAND_FLIP',
        7:'C17_TOP_PLAYER_FOREHAND_CHOP',
        8:'C18_TOP_PLAYER_BACKHAND_CHOP',
        9:'C19_BOTTOM_PLAYER_FOREHAND_CHOP',
        10:'C1_TOP_PLAYER_FOREHAND_SERVE',
        # 11:'C2_TOP_PLAYER_BACKHAND_SERVE',
        11:'C20_BOTTOM_PLAYER_BACKHAND_CHOP',
        12:'C3_BOTTOM_PLAYER_FOREHAND_SERVE',
        # 14:'C4_BOTTOM_PLAYER_BACKHAND_SERVE',
        13:'C5_TOP_PLAYER_FOREHAND_LOOP',
        14:'C6_TOP_PLAYER_BACKHAND_LOOP',
        15:'C7_BOTTOM_PLAYER_FOREHAND_LOOP',
        16:'C8_BOTTOM_PLAYER_BACKHAND_LOOP',
        17:'C9_TOP_PLAYER_FOREHAND_BLOCK'}

def load_data():
    # files = glob('./seq_data/point_00125.dat')
    # files = glob('./seq_data_fc6_normalized_testset/point_00001.dat')
    files = glob('./seq_data_fc6_normalized_testset/point_00*.dat')
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
                if prev_label != None and not 'MISS_HIT' in line[-1] and not 'LOB' in line[-1] and not 'UNDER_NET' in line[-1] and not 'HIT_OUT' in line[-1]:
                    pairwise_potential[label_to_index[prev_label]][label_to_index[line[-1]]]+=1
                    num_of_pairs += 1
                prev_label = line[-1]
        test_data.append(test_data_pt)
        test_label.append(test_label_pt)
    for i,_ in enumerate(pairwise_potential):
        for j,_ in enumerate(pairwise_potential[i]):
            pairwise_potential[i][j] = 1.0*pairwise_potential[i][j]/num_of_pairs

    # print('PAIRWISE_POTENTIALS:'+str(pairwise_potential))
    # print(sum(map(sum, pairwise_potential)))

    return test_data, test_label, pairwise_potential


if __name__ == "__main__":
    start_time = time.time()
    test_data, test_label, pairwise_potential = load_data()
    clf = pickle.load(open( "./fc6_normalized_lr_clf_6videos.pickle", "rb" ))

    numCorrectPred = 0
    accuracies = []

    # for PAIR_WEIGHT in [0,0.05,0.1,0.2,0.4,0.6,0.8,0.9,0.95,1]:
    for PAIR_WEIGHT in [0]:
        for i,_ in enumerate(test_data):
            numCorrectPred = 0
            prev_pred = None
            for j,_ in enumerate(test_data[i]):
                min_ind = max(0, j-4)
                max_ind = min(len(test_data[i]), j+5)
                sum_dat = np.array(test_data[i][min_ind], dtype=np.float64)
                for k in xrange(min_ind+1, max_ind):
                    sum_dat += np.array(test_data[i][k], dtype=np.float64)
                dat = sum_dat / 9
                # y_pred = clf.predict(dat)[0].replace('_selected', '')
                predict_probability = clf.predict_proba(dat)[0]
                # print('predict_probability size:'+str(predict_probability.shape))
                # print('predict_probability'+str(predict_probability))
                final_pred_prob = []
                if prev_pred == None:
                    final_pred_prob = np.asarray(predict_probability)
                    # FORCING C1_TOP_PLAYER_FOREHAND_SERVE or C3_BOTTOM_PLAYER_FOREHAND_SERVE
                    if final_pred_prob[10] > final_pred_prob[12]:
                        prev_pred = 10
                    else:
                        prev_pred = 12
                else:
                    for l,_ in enumerate(predict_probability):
                        final_pred_prob.append(pairwise_potential[prev_pred][l]*predict_probability[l])
                        # final_pred_prob.append(PAIR_WEIGHT*pairwise_potential[prev_pred][l]+(1-PAIR_WEIGHT)*predict_probability[l])
                    final_pred_prob = np.asarray(final_pred_prob)
                    # print('final_pred_prob size:'+str(final_pred_prob.shape))
                    # print('final_pred_prob'+str(final_pred_prob))
                    prev_pred = np.argmax(final_pred_prob)
                    # print('PREDICTION:'+index_to_label[prev_pred])

                # if y_pred == test_label[i][j]:
                if index_to_label[prev_pred] == test_label[i][j]:
                    numCorrectPred += 1
                # print("Index: %d; Predict: %s; Actual: %s"%(j, y_pred, test_label[i][j]))
                # print("Index: %d; Predict: %s; Actual: %s"%(j, index_to_label[prev_pred], test_label[i][j]))
            accuracies.append(100.0*numCorrectPred/len(test_data[i]))
            print("Accuracy: %.3f" % (accuracies[-1]))

        print("Overall Accuracy: %.3f" % (sum(accuracies)/len(accuracies)))
    print("Total time: %d"%(time.time()-start_time))
    # print("Accuracy: %.3f" % (100 * accuracy_score(y_test, y_pred)))
