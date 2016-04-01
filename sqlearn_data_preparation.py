# coding: utf-8

# In[1]:

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn import svm, cross_validation
import pylab as pl
from PIL import Image
import numpy as np
import os


# In[2]:

# Make sure that caffe is on the python path:
caffe_root = '/u/zexuan/caffe/caffe/'  # this file is expected to be in {caffe_root}/examples
caffe_real_root = '/pkgs/caffe/'
thesis_root = '/ais/gobi2/pingpong/thesis/'
#!ls /pkgs/caffe
import sys
sys.path.insert(0, caffe_real_root + 'python')
import caffe

plt.rcParams['figure.figsize'] = (10, 10)
plt.rcParams['image.interpolation'] = 'nearest'
plt.rcParams['image.cmap'] = 'gray'

if not os.path.isfile('~/caffe/caffe/models/bvlc_reference_caffenet/bvlc_reference_caffenet.caffemodel'):
    print("Downloading pre-trained CaffeNet model...")
    os.system(u'~/caffe/caffe/scripts/download_model_binary.py ~/caffe/caffe/models/bvlc_reference_caffenet')


# In[3]:

caffe.set_device(0)
caffe.set_mode_gpu()


# In[4]:

import skimage
import skimage.io
import time

# container_path = 'output_labeled_img_dir_5videos_for_pt/'
# container_path = './output_labeled_img_dir_6videos_for_pt/'
container_path = './output_labeled_img_dir_8videos_for_pt_testset/'

pt_folders = [f for f in sorted(os.listdir(container_path)) if os.path.isdir(os.path.join(container_path, f))]

def write_to_data_file(pt_num):
    global container_path
    global pt_folders
    global caffe_root
    global caffe_real_root
    global thesis_root

    start_time = time.time()
    training_set = {}
    training_set['data'] = []
    training_set['target'] = []
    pt_folder = pt_folders[pt_num]
    pt_folder_path = os.path.join(container_path, pt_folder)
    documents = [os.path.join(pt_folder_path, d) for d in sorted(os.listdir(pt_folder_path))]
    pt_data = []
    pt_target = []
    frame_class_tuple = []
    #print documents
    for pic in documents:
        pic_basename_lower = os.path.basename(pic).lower()
        if not pic_basename_lower.endswith('png'):
            if pic_basename_lower == 'a_label.txt':
                with open(pic) as f:
                    for line in f:
                        line = line.strip()
                        if len(line) == 0 or line[0] == "#":
                            continue
                        frames = line.split(':')
                        assert(len(frames)==3)
                        frames[0] = int(frames[0])
                        frames[1] = int(frames[1])
                        output_class = frames[2]
                        frame_class_tuple.append((frames[0], frames[1], output_class))
            continue

        img = skimage.img_as_float(skimage.io.imread(pic)).astype(np.float32)
        frame_num = int(pic_basename_lower[pic_basename_lower.find('_')+1: pic_basename_lower.find('.')])
        for tup in frame_class_tuple:
            if frame_num >= tup[0] and frame_num < tup[1]:
                frame_target = tup[2]
                break
        pt_data.append(img)
        pt_target.append(frame_target)
    training_set['data'].append(pt_data)
    training_set['target'].append(pt_target)

    print 'Total time loading training data: ', time.time()-start_time, ' seconds'

    # In[6]:

    # MODEL_FILE = caffe_root +'models/bvlc_reference_caffenet/deploy.prototxt'
    # PRETRAINED = caffe_root +'models/bvlc_reference_caffenet/bvlc_reference_caffenet.caffemodel'
    # caffe.set_mode_cpu()
    # net = caffe.Classifier(MODEL_FILE, PRETRAINED,
    #                        mean=np.load(caffe_root + 'python/caffe/imagenet/ilsvrc_2012_mean.npy').mean(1).mean(1),
    #                        channel_swap=(2,1,0),
    #                        raw_scale=255,
    #                        image_dims=(600, 600))
    # print net.blobs['data'].data.shape
    # [(k, v.data.shape) for k, v in net.blobs.items()]


    # caffe.set_mode_cpu()
    print caffe_root + 'models/bvlc_reference_caffenet/deploy.prototxt'
    #!ls caffe_root+'models/bvlc_reference_caffenet/deploy.prototxt'
    net = caffe.Net(caffe_root + 'models/bvlc_reference_caffenet/deploy.prototxt',
                    caffe_root + 'models/bvlc_reference_caffenet/bvlc_reference_caffenet.caffemodel',
                    caffe.TEST)

    # input preprocessing: 'data' is the name of the input blob == net.inputs[0]
    transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
    transformer.set_transpose('data', (2,0,1))
    transformer.set_mean('data', np.load(caffe_root + 'python/caffe/imagenet/ilsvrc_2012_mean.npy').mean(1).mean(1)) # mean pixel
    transformer.set_raw_scale('data', 255)  # the reference model operates on images in [0,255] range instead of [0,1]
    transformer.set_channel_swap('data', (2,1,0))  # the reference model has channels in BGR order instead of RGB
    print net.blobs['data'].data.shape
    [(k, v.data.shape) for k, v in net.blobs.items()]


    # In[7]:
    print 'number of points: ', len(training_set['data'])
    print 'number of frames in point[0]: ', len(training_set['data'][0])
    print 'dimensionality of each image: ', training_set['data'][0][0].shape


    # In[8]:

    # print caffe.io.load_image(thesis_root + 'labeled_image_selected/bottom_player_winning_selected/point_00001_frame_00033.png').shape
    # print caffe.io.load_image(thesis_root + 'labeled_image_selected/bottom_player_winning_selected/point_00001_frame_00033.png')[0][0]
    # print training_set['data'][0][0][0]
    start_time = time.time()

    result = []
    for pt_index in xrange(len(training_set['data'])):
    #for pt_index in xrange(2):
        pt_result = []
        for frame_index in xrange(len(training_set['data'][pt_index])):
        #for frame_index in xrange(5):
            net.blobs['data'].data[...] = transformer.preprocess('data', training_set['data'][pt_index][frame_index])
            #net.blobs['data'].data[...] = map(lambda x: transformer.preprocess('data', x), training_set['data'][i:i+10])
            out = net.forward()
            #print net.blobs['fc7'].data.shape
            pt_result.append(np.mean(net.blobs['fc6'].data, axis=0))
        result.append(pt_result)

    print 'Number of pts in result: ', len(result), 'Number of frame labels in result[0]', len(result[0])
    print 'result[0][0]: ', result[0][0]

    print 'Total time for neural net: ', time.time()-start_time, ' seconds'
    print transformer.deprocess('data', net.blobs['data'].data[0]).shape
    print 'Sample image from the training set'
    # plt.imshow(transformer.deprocess('data', net.blobs['data'].data[4]))

    # In[10]:
    normalized_result = []
    #normalized_result = normalize(result)
    for r in result:
        normalized_result.append((r-np.mean(r))/np.std(r))
    result = normalized_result

    output_file = './seq_data_fc6_normalized_8videos_testset/point_%05d.dat'%(pt_num+1)
    with open(output_file, 'w+') as f:
        for i in xrange(len(result[0])):
            result_lst = [str(elem) for elem in result[0][i]]
            f.write(' '.join(result_lst))
            f.write(' '+training_set['target'][0][i])
            f.write('\n')
    print 'SAVE LABEL TO '+output_file


for pt_num,_ in enumerate(pt_folders):
    write_to_data_file(pt_num)
