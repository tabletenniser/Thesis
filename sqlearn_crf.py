import numpy as np
import fileinput
from glob import glob
import pickle
import sys
import time

label_to_index_pt_end={
        'C21_TOP_PLAYER_UNDER_NET':0,
        'C22_TOP_PLAYER_HIT_OUT':1,
        'C23_TOP_PLAYER_FOREHAND_MISS_HIT':2,
        'C24_TOP_PLAYER_BACKHAND_MISS_HIT':3,
        'C25_BOTTOM_PLAYER_UNDER_NET':4,
        'C26_BOTTOM_PLAYER_HIT_OUT':5,
        'C27_BOTTOM_PLAYER_FOREHAND_MISS_HIT':6,
        'C28_BOTTOM_PLAYER_BACKHAND_MISS_HIT':7}

index_to_label_pt_end={
        0:'C21_TOP_PLAYER_UNDER_NET',
        1:'C22_TOP_PLAYER_HIT_OUT',
        2:'C23_TOP_PLAYER_FOREHAND_MISS_HIT',
        3:'C24_TOP_PLAYER_BACKHAND_MISS_HIT',
        4:'C25_BOTTOM_PLAYER_UNDER_NET',
        5:'C26_BOTTOM_PLAYER_HIT_OUT',
        6:'C27_BOTTOM_PLAYER_FOREHAND_MISS_HIT',
        7:'C28_BOTTOM_PLAYER_BACKHAND_MISS_HIT'}

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
        'C20_BOTTOM_PLAYER_BACKHAND_CHOP':11,
        # 'C2_TOP_PLAYER_BACKHAND_SERVE':11,
        'C30_BOTTOM_PLAYER_BACKHAND_LOB':12,
        'C3_BOTTOM_PLAYER_FOREHAND_SERVE':13,
        # 'C4_BOTTOM_PLAYER_BACKHAND_SERVE':14,
        'C5_TOP_PLAYER_FOREHAND_LOOP':14,
        'C6_TOP_PLAYER_BACKHAND_LOOP':15,
        'C7_BOTTOM_PLAYER_FOREHAND_LOOP':16,
        'C8_BOTTOM_PLAYER_BACKHAND_LOOP':17,
        'C9_TOP_PLAYER_FOREHAND_BLOCK':18,
        'C21_TOP_PLAYER_UNDER_NET':19,
        'C22_TOP_PLAYER_HIT_OUT':20,
        'C23_TOP_PLAYER_FOREHAND_MISS_HIT':21,
        'C24_TOP_PLAYER_BACKHAND_MISS_HIT':22,
        'C25_BOTTOM_PLAYER_UNDER_NET':23,
        'C26_BOTTOM_PLAYER_HIT_OUT':24,
        'C27_BOTTOM_PLAYER_FOREHAND_MISS_HIT':25,
        'C28_BOTTOM_PLAYER_BACKHAND_MISS_HIT':26}

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
        11:'C20_BOTTOM_PLAYER_BACKHAND_CHOP',
        # 11:'C2_TOP_PLAYER_BACKHAND_SERVE',
        12:'C30_BOTTOM_PLAYER_BACKHAND_LOB',
        13:'C3_BOTTOM_PLAYER_FOREHAND_SERVE',
        # 14:'C4_BOTTOM_PLAYER_BACKHAND_SERVE',
        14:'C5_TOP_PLAYER_FOREHAND_LOOP',
        15:'C6_TOP_PLAYER_BACKHAND_LOOP',
        16:'C7_BOTTOM_PLAYER_FOREHAND_LOOP',
        17:'C8_BOTTOM_PLAYER_BACKHAND_LOOP',
        18:'C9_TOP_PLAYER_FOREHAND_BLOCK',
        19:'C21_TOP_PLAYER_UNDER_NET',
        20:'C22_TOP_PLAYER_HIT_OUT',
        21:'C23_TOP_PLAYER_FOREHAND_MISS_HIT',
        22:'C24_TOP_PLAYER_BACKHAND_MISS_HIT',
        23:'C25_BOTTOM_PLAYER_UNDER_NET',
        24:'C26_BOTTOM_PLAYER_HIT_OUT',
        25:'C27_BOTTOM_PLAYER_FOREHAND_MISS_HIT',
        26:'C28_BOTTOM_PLAYER_BACKHAND_MISS_HIT'}


def load_data(files, end_pt_only=False, skip_end_pt=False):
    test_data = []
    test_label = []
    # print("Loading test data...", end=" ")
    for dat_file in files:
        test_data_pt = []
        test_label_pt = []
        prev_label = None
        with open(dat_file) as f:
            for line in f:
                line = line.strip().split()
                if end_pt_only and label_to_index[line[-1]] < 19:
                    continue
                if skip_end_pt and label_to_index[line[-1]] >= 19:
                    continue
                if end_pt_only:
                    test_label_pt.append(label_to_index_pt_end[line[-1]])
                else:
                    test_label_pt.append(label_to_index[line[-1]])
                data_val = map(float, line[:-1])
                test_data_pt.append(data_val)
        if len(test_data_pt) > 0:
            test_data.append(np.asarray(test_data_pt,dtype=np.float32))
            test_label.append(np.asarray(test_label_pt))
    return np.array(test_data), np.array(test_label)
    # return (test_data), (test_label)

# This function inputs a pre-processed training/testing data and output its running
# average over 9 consecutive frames.
def running_window_average(preData):
    Data = np.copy(preData)
    for i,_ in enumerate(preData):
        numCorrectPred = 0
        for j,_ in enumerate(preData[i]):
            min_ind = max(0, j-4)
            max_ind = min(len(preData[i]), j+5)
            sum_dat = np.array(preData[i][min_ind], dtype=np.float64)
            for k in xrange(min_ind+1, max_ind):
                sum_dat += np.array(preData[i][k], dtype=np.float64)
            dat = sum_dat / 9
            Data[i][j] = dat
    return Data


training_files = glob('./seq_data_fc6_normalized_8videos_trainingset_2000iter/point_0*.dat')
# testing_files = glob('./seq_data_fc6_normalized_8videos_testset/point_00*.dat')
testing_files = glob('./seq_data_fc6_normalized_8videos_testset_2000iter/point_0*.dat')

X_train_pre_stroke_cls, y_train_stroke_cls = load_data(training_files, skip_end_pt=True)
X_train_pre_end_pt, y_train_end_pt = load_data(training_files, end_pt_only=True)
X_test_pre_stroke_cls, y_test_stroke_cls = load_data(testing_files, skip_end_pt=True)
X_test_pre_end_pt, y_test_end_pt = load_data(testing_files, end_pt_only=True)

X_train_stroke_cls = running_window_average(X_train_pre_stroke_cls)
X_train_end_pt = running_window_average(X_train_pre_end_pt)
X_test_stroke_cls = running_window_average(X_test_pre_stroke_cls)
X_test_end_pt = running_window_average(X_test_pre_end_pt)

# letters = load_letters()
# X, y, folds = letters['data'], letters['labels'], letters['folds']
# X, y = np.array(X), np.array(y)
# X_train, X_test = X[folds != 1], X[folds == 1]
# y_train, y_test = y[folds != 1], y[folds == 1]

from pystruct.models import ChainCRF
from pystruct.learners import FrankWolfeSSVM
from pystruct.learners import SubgradientSSVM
import cPickle as pickle

model = ChainCRF(directed=True)
# ssvm_stroke_cls = SubgradientSSVM(model=model, C=.1, max_iter=200)
ssvm_stroke_cls = FrankWolfeSSVM(model=model, C=1000, max_iter=300, verbose=3, show_loss_every=1)
ssvm_stroke_cls.fit(X_train_stroke_cls, y_train_stroke_cls) 
pickle.dump(ssvm_stroke_cls, open( "crf_ssvm_player_stroke_cls.pickle", "wb" ) )

model_end_pt = ChainCRF(directed=True)
# ssvm_end_pt = SubgradientSSVM(model=model_end_pt, C=.1, max_iter=200)
ssvm_end_pt = FrankWolfeSSVM(model=model_end_pt, C=1000, max_iter=300, verbose=3, show_loss_every=1)
ssvm_end_pt.fit(X_train_end_pt, y_train_end_pt) 
pickle.dump(ssvm_end_pt, open( "crf_ssvm_player_end_pt.pickle", "wb" ) )

ssvm_stroke_cls = pickle.load(open("crf_ssvm_player_stroke_cls.pickle", "rb" ) )
ssvm_end_pt = pickle.load(open("crf_ssvm_player_end_pt.pickle", "rb" ) )
y_pred_stroke_cls = np.array(ssvm_stroke_cls.predict(X_test_stroke_cls))
y_pred_end_pt = np.array(ssvm_end_pt.predict(X_test_end_pt))
# print ssvm.score(X_test, y_test) 



stroke_accuracies = []
ending_accuracies = []
accuracies = []
for i,_ in enumerate(y_test_stroke_cls):
    # print 'Point #%d'%(i)
    # SECTION #1: Player stroke class identification.
    num_of_correct_strokes = 0
    for j,_ in enumerate(y_test_stroke_cls[i]):
        print 'Predict:%s;Actual:%s'%(index_to_label[y_pred_stroke_cls[i][j]], index_to_label[y_test_stroke_cls[i][j]])
        if y_pred_stroke_cls[i][j] == y_test_stroke_cls[i][j]:
            num_of_correct_strokes += 1

    # SECTION #2: End of a point classification.
    num_of_correct_ending = 0
    for j,_ in enumerate(y_test_end_pt[i]):
        print 'Predict:%s;Actual:%s'%(index_to_label_pt_end[y_pred_end_pt[i][j]], index_to_label_pt_end[y_test_end_pt[i][j]])
        if y_pred_end_pt[i][j] == y_test_end_pt[i][j]:
            num_of_correct_ending += 1
    stroke_accuracies.append((num_of_correct_strokes)*100.0/len(y_test_stroke_cls[i]))
    ending_accuracies.append((num_of_correct_ending)*100.0/len(y_test_end_pt[i]))
    accuracies.append((num_of_correct_strokes+num_of_correct_ending)*100.0/(len(y_test_stroke_cls[i])+len(y_test_end_pt[i])))
    # print "Stroke accuracy: %.3f"%(stroke_accuracies[-1])
    # print "End of point accuracy: %.3f"%(ending_accuracies[-1])
    print "Accuracy: %.3f"%(accuracies[-1])

# print "Overall Stroke Classification Accuracy: %.3f"%(sum(stroke_accuracies)/len(stroke_accuracies))
# print "Overall Ending of Point Accuracy: %.3f"%(sum(ending_accuracies)/len(ending_accuracies))
print "Overall Accuracy: %.3f"%(sum(accuracies)/len(accuracies))

