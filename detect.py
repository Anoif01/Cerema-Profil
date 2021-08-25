# -*- coding: utf-8 -*-
"""
# Created on Wed Apr 28 15:01:00 2021
# @title : Projet PROFIL
# @author: Xiaohua LU (Stagiaire Céréma - INSA GM5)
"""

import numpy as np
import matplotlib.pyplot as plt
import cv2
import glob
# from moviepy.editor import VideoFileClip
from moviepy.video.io.VideoFileClip import VideoFileClip
from IPython.display import HTML

# import os; os.environ['KERAS_BACKEND'] = 'theano'
import keras # broken for keras >= 2.0, use 1.2.2
from keras.models import Sequential
from keras.layers.convolutional import Convolution2D, MaxPooling2D
from keras.layers.advanced_activations import LeakyReLU
from keras.layers.core import Flatten, Dense, Activation, Reshape

from utils import load_weights, Box, yolo_net_out_to_car_boxes, draw_box


def detectionYolo(clip_name, project_video_output):
    keras.backend.set_image_dim_ordering('th')
    
    model = Sequential()
    model.add(Convolution2D(16, 3, 3,input_shape=(3,448,448),border_mode='same',subsample=(1,1)))
    model.add(LeakyReLU(alpha=0.1))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Convolution2D(32,3,3 ,border_mode='same'))
    model.add(LeakyReLU(alpha=0.1))
    model.add(MaxPooling2D(pool_size=(2, 2),border_mode='valid'))
    model.add(Convolution2D(64,3,3 ,border_mode='same'))
    model.add(LeakyReLU(alpha=0.1))
    model.add(MaxPooling2D(pool_size=(2, 2),border_mode='valid'))
    model.add(Convolution2D(128,3,3 ,border_mode='same'))
    model.add(LeakyReLU(alpha=0.1))
    model.add(MaxPooling2D(pool_size=(2, 2),border_mode='valid'))
    model.add(Convolution2D(256,3,3 ,border_mode='same'))
    model.add(LeakyReLU(alpha=0.1))
    model.add(MaxPooling2D(pool_size=(2, 2),border_mode='valid'))
    model.add(Convolution2D(512,3,3 ,border_mode='same'))
    model.add(LeakyReLU(alpha=0.1))
    model.add(MaxPooling2D(pool_size=(2, 2),border_mode='valid'))
    model.add(Convolution2D(1024,3,3 ,border_mode='same'))
    model.add(LeakyReLU(alpha=0.1))
    model.add(Convolution2D(1024,3,3 ,border_mode='same'))
    model.add(LeakyReLU(alpha=0.1))
    model.add(Convolution2D(1024,3,3 ,border_mode='same'))
    model.add(LeakyReLU(alpha=0.1))
    model.add(Flatten())
    model.add(Dense(256))
    model.add(Dense(4096))
    model.add(LeakyReLU(alpha=0.1))
    model.add(Dense(1470))
    
    load_weights(model,'./yolo-tiny.weights')
    
    def frame_func(image):
        '''Détection les objets dans chaque frame de vidéo'''
        crop = image[400:,:650,:]
        resized = cv2.resize(crop,(448,448))
        # resized = cv2.resize(image,(448,448))
        batch = np.array([resized[:,:,0],resized[:,:,1],resized[:,:,2]])
        batch = 2*(batch/255.) - 1
        batch = np.expand_dims(batch, axis=0)
        out = model.predict(batch)
        boxes = yolo_net_out_to_car_boxes(out[0], threshold = 0.2)
        # return draw_box(boxes,image,[[0,image.shape[1]],[0,image.shape[0]]])
        return draw_box(boxes,image,[[0,650],[400,image.shape[0]]])

    clip1 = VideoFileClip(clip_name)
    clip2 = clip1 #.subclip(1,40) # pour accélérer lors de la teste
    lane_clip = clip2.fl_image(frame_func) #NOTE: this function expects color images!!
    lane_clip.write_videofile(project_video_output, audio=False, threads = 8, codec='libx264')
    

# project_video_output = './detected_output.avi'
# clip_name = "D:\\01-Projet PROFIL\\01-01_Tâche_T22a_DB\\4E38P\\20161123_093137_PROFIL_record\\PROFIL_record_20161123_093137_PROFIL_quad_record_imageOut.avi"
# detectionYolo(clip_name, project_video_output)
