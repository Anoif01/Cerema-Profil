# -*- coding: utf-8 -*-
"""
# Created on Wed Apr 28 15:01:00 2021
# @title : Projet PROFIL
# @author: Xiaohua LU (Stagiaire Céréma - INSA GM5)
"""


# =============================================================================
# Dependencies
# =============================================================================
import numpy as np
import os
import seaborn as sns
import sklearn
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib
import imageio
from matplotlib.animation import FuncAnimation
import seaborn as sns
from matplotlib import animation
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.fx.resize import resize
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.compositing.concatenate import concatenate_videoclips
import cv2
from scipy.ndimage.measurements import label
from matplotlib.path import Path
import time


# =============================================================================
# Functions pour l'alignement et le remplissage des blancs
# =============================================================================
def padding_XY(l, X_final, Y_final, ran=3):
    '''
    Remplir X et Y en fonction de l.
    '''
    ## on clacul la différence pour padding la longueur de courbe à une longeur qui est mutiplicateur de 10
    ajout = l - len(X_final[0]) % l
    X_fin = []
    Y_fin = []
    for ind in range(ran):
        if ind != ran-1:
            y = Y_final[ind][-1]
            x = len(X_final[ind])
            Y_fin.append(np.append(Y_final[ind], [y for ind in range(ajout)]))
            X_fin.append(np.append(X_final[ind], [x+ind for ind in range(ajout)]))
        else:
            y1 = Y_final[ind][0][-1]
            y2 = Y_final[ind][1][-1]
            y3 = Y_final[ind][2][-1]
            x = len(X_final[ind])
            # Concatener les arrays
            Y_fin1 = (np.append(Y_final[ind][0], [y1 for ind in range(ajout)]))
            Y_fin2 = (np.append(Y_final[ind][1], [y2 for ind in range(ajout)]))
            Y_fin3 = (np.append(Y_final[ind][2], [y3 for ind in range(ajout)]))
            X_fin.append(np.append(X_final[ind], [x+ind for ind in range(ajout)]))
            Y_fin.append([Y_fin1,Y_fin2,Y_fin3])
    return X_fin, Y_fin


def padding_XY_can(l, X_final, Y_final, ran=3):
    '''
    Remplir X et Y en fonction de l pour les données de CAN
    '''
    ## on clacul la différence pour padding la longueur de courbe à une longeur qui est mutiplicateur de 10
    ajout = l - len(X_final[0]) % l
    X_fin = []
    Y_fin = []
    for ind in range(ran):
        y = Y_final[ind][-1]
        x = len(X_final[ind])
        Y_fin.append(np.append(Y_final[ind], [y for ind in range(ajout)]))
        X_fin.append(np.append(X_final[ind], [x+ind for ind in range(ajout)]))
    return X_fin, Y_fin


def padding_XY_ci(l, X_final, Y_final):
    '''
    Remplir X et Y en fonction de l pour les données de CI
    '''
    ## on clacul la différence pour padding la longueur de courbe à une longeur qui est mutiplicateur de 10
    ajout = l - len(X_final[0]) % l
    Y_fin = []
    X_fin = []
    print(len(Y_final))
    print(len(Y_final[0]))
    print(len(Y_final[0][0]))
    y1 = Y_final[0][0][-1]
    y2 = Y_final[0][1][-1]
    y3 = Y_final[0][2][-1]
    x = len(X_final[0])
    # Concatener les arrays
    Y_fin1 = (np.append(Y_final[0][0], [y1 for ind in range(ajout)]))
    Y_fin2 = (np.append(Y_final[0][1], [y2 for ind in range(ajout)]))
    Y_fin3 = (np.append(Y_final[0][2], [y3 for ind in range(ajout)]))
    X_fin.append(np.append(X_final[0], [x+ind for ind in range(ajout)]))
    Y_fin.append([Y_fin1,Y_fin2,Y_fin3])
    return X_fin, Y_fin


def get_video_times(video_path):
    '''
    Retourner la duration dela vidéo
    '''
    video_clip = VideoFileClip(video_path)
    durantion = video_clip.duration
    return durantion


def ajuster_minmax_axe(min_yaxe, max_yaxe):
    '''
    Ajouster les axes sur le champs d'affichage
    '''
    if (min_yaxe == 0 and max_yaxe == 0):
        min_yaxe = -5+min_yaxe
        max_yaxe = 5+max_yaxe
    elif(min_yaxe == 0 and max_yaxe != 0):
        min_yaxe = -5+min_yaxe
        if (max_yaxe > 0):
            max_yaxe = 1.5*max_yaxe
        elif(max_yaxe < 0 ):
            max_yaxe = max_yaxe - 0.5*max_yaxe
    elif(min_yaxe != 0 and max_yaxe == 0):
        max_yaxe = 5+max_yaxe
        if (min_yaxe < 0 ):
            min_yaxe = 1.5*min_yaxe
        elif(min_yaxe > 0 ):
            min_yaxe = min_yaxe - 0.5*min_yaxe
    else:
        if (max_yaxe > 0):
            max_yaxe = 1.5*max_yaxe
        elif(max_yaxe < 0 ):
            max_yaxe = max_yaxe - 0.5*max_yaxe
        if (min_yaxe < 0 ):
            min_yaxe = 1.5*min_yaxe
        elif(min_yaxe > 0 ):
            min_yaxe = min_yaxe - 0.5*min_yaxe
    return min_yaxe, max_yaxe


# =============================================================================
# Traiter les données de CAN
# =============================================================================
def courbe_can_avi(X, Y, save_names, save_video, frames_num, fps_courbe, interval, l = 10, ran=3):
    '''
    Dessiner les courbes pour le CAN et convertir en vidéo .avi
    '''
    rc = {'axes.axisbelow': True, 
            'axes.edgecolor': 'white',
            'axes.facecolor': 'white',	#fond color
            'axes.grid': True,
         }
    axe_names = [n.split(' ')[0] for n in save_names]
    save_name_gif = 'courbes.gif'
    plt.style.use('fivethirtyeight')
    sns.set_style(rc)
    
    if ran == 1:
        # create figure
        fig, ax = plt.subplots(1, 1, figsize=(6, 5))
        plt.subplots_adjust(wspace=0, hspace=0.4)
        fig.set_tight_layout(True)
        for ind in range(ran):
            ax.set_title(save_names[ind], fontsize=14, color='grey')
            ax.set_ylabel(save_names[ind], fontsize=14, color='grey')
    else:
        # create figure
        fig, ax = plt.subplots(ran,1, figsize=(int(10/3*ran), int(15/3*ran)))
        plt.subplots_adjust(wspace=0, hspace=0.4)
        fig.set_tight_layout(True)
        # labels
        for ind in range(ran):
            ax[ind].set_title(save_names[ind], fontsize=14, color='grey')
            ax[ind].set_ylabel(save_names[ind], fontsize=14, color='grey')
    # initial plots: line and scatter
    lines = []
    courbes = []
    for ind in range(ran):
        if ran == 1:
            courbe, = ax.plot(X[ind][:l], Y[ind][:l], 'darkgrey', linewidth=2)
            line, = ax.plot(X[ind][0], Y[ind][0], 'ro')
            ax.set_xticks(X[ind][:l])
            ax.set_xticklabels([str(d) for d in range(l)])
            lines.append(line)
            courbes.append(courbe)
            # le champs de figure
            max_yaxe = max(Y[ind][:l])
            min_yaxe = min(Y[ind][:l])
            min_yaxe, max_yaxe = ajuster_minmax_axe(min_yaxe, max_yaxe)
            ax.set_ylim([min_yaxe, max_yaxe])
        else:
            courbe, = ax[ind].plot(X[ind][:l], Y[ind][:l], 'darkgrey', linewidth=2)
            line, = ax[ind].plot(X[ind][0], Y[ind][0], 'ro')
            ax[ind].set_xticks(X[ind][:l])
            ax[ind].set_xticklabels([str(d) for d in range(l)])
            lines.append(line)
            courbes.append(courbe)
            # le champs de figure
            max_yaxe = max(Y[ind][:l])
            min_yaxe = min(Y[ind][:l])
            min_yaxe, max_yaxe = ajuster_minmax_axe(min_yaxe, max_yaxe)
            ax[ind].set_ylim([min_yaxe, max_yaxe])

    def update(i):
        taille = len(X[0])
        for ind in range(ran):
            if ran == 1:
                label = 'Temps: {0} s et '.format(round(i*interval/1000,2)) + axe_names[ind] + ': {0}'.format(round(Y[ind][i],2))
                print(label)
                diff = 0
                # refresh the scatter
                if (i%l == 0):
                    diff = taille-i
                    if diff>=(l-1) : 
                        courbes[ind].set_ydata(Y[ind][i:i+l])
                        x_ticks_labels = [str(i+d) for d in range(l)]
                        ax.set_xticklabels(x_ticks_labels)
                        max_yaxe = max(Y[ind][i:i+l])
                        min_yaxe = min(Y[ind][i:i+l])
                        min_yaxe, max_yaxe = ajuster_minmax_axe(min_yaxe, max_yaxe)
                        ax.set_ylim([min_yaxe, max_yaxe])
                    else :
                        ax.set_xticks(X[ind][:diff])
                        courbes[ind].set_ydata(Y[ind][i:i+diff])
                        x_ticks_labels = [str(i+d) for d in range(diff)]
                        ax.set_xticklabels(x_ticks_labels)
                        max_yaxe = max(Y[ind][i:i+diff])
                        min_yaxe = min(Y[ind][i:i+diff])
                        min_yaxe, max_yaxe = ajuster_minmax_axe(min_yaxe, max_yaxe)
                        ax.set_ylim([min_yaxe, max_yaxe])
                    lines[ind].set_xdata(X[ind][0])
                    lines[ind].set_ydata(Y[ind][i])
                else:
                    a = i%l
                    lines[ind].set_xdata(X[ind][a])
                    lines[ind].set_ydata(Y[ind][i])
                # refresh xlabel
                ax.set_xlabel(label, fontsize=18, color='darkorange')
            else:
                label = 'Temps: {0} s et '.format(round(i*interval/1000,2)) + axe_names[ind] + ': {0}'.format(round(Y[ind][i],2))
                print(label)
                diff = 0
                # refresh the scatter
                if (i%l == 0):
                    diff = taille-i
                    if diff>=(l-1) : 
                        courbes[ind].set_ydata(Y[ind][i:i+l])
                        x_ticks_labels = [str(i+d) for d in range(l)]
                        ax[ind].set_xticklabels(x_ticks_labels)
                        max_yaxe = max(Y[ind][i:i+l])
                        min_yaxe = min(Y[ind][i:i+l])
                        min_yaxe, max_yaxe = ajuster_minmax_axe(min_yaxe, max_yaxe)
                        ax[ind].set_ylim([min_yaxe, max_yaxe])
                    else :
                        ax[ind].set_xticks(X[ind][:diff])
                        courbes[ind].set_ydata(Y[ind][i:i+diff])
                        x_ticks_labels = [str(i+d) for d in range(diff)]
                        ax[ind].set_xticklabels(x_ticks_labels)
                        max_yaxe = max(Y[ind][i:i+diff])
                        min_yaxe = min(Y[ind][i:i+diff])
                        min_yaxe, max_yaxe = ajuster_minmax_axe(min_yaxe, max_yaxe)
                        ax[ind].set_ylim([min_yaxe, max_yaxe])
                    lines[ind].set_xdata(X[ind][0])
                    lines[ind].set_ydata(Y[ind][i])
                else:
                    a = i%l
                    lines[ind].set_xdata(X[ind][a])
                    lines[ind].set_ydata(Y[ind][i])
                # refresh xlabel
                ax[ind].set_xlabel(label, fontsize=18, color='darkorange')
        return line, ax

    # settings of the video to generate
    anim = FuncAnimation(fig, update, frames=np.arange(0, len(X[0])), interval=interval)
    print("Saving")
    anim.save(save_name_gif, writer='imagemagick', fps=fps_courbe)
    plt.show()
    # .gif to .mp4
    clip = VideoFileClip(save_name_gif)
    clip.write_videofile(save_video, codec='libx264')


def gather_all_can_video(video_origin, save_video_name, fps_courbe, fps_output, interval, X, Y, l, ranges):
    '''
    Concatener toutes les vidéos
    '''
    cap = cv2.VideoCapture(video_origin)
    frames_num = int(cap.get(7))
    all_save_courbe_names = ['Vitesse m/s', 'Accélération m/s2', 'Diatance km']
    save_courbe_names = [all_save_courbe_names[i] for i in ranges]
    courbe_can_avi(X, Y, save_courbe_names, save_video_name, frames_num, fps_courbe, interval, l, len(ranges))
    
    
# =============================================================================
# Traiter les données de CI
# =============================================================================
def courbe_ci_avi(X, Y, save_names, save_video, frames_num, fps_courbe, interval, l = 10):
    '''
    Dessiner les courbes pour le CI et convertir en vidéo .avi
    '''
    rc = {'axes.axisbelow': True, 
            'axes.edgecolor': 'white',
            'axes.facecolor': 'white',	#fond color
            'axes.grid': True,
         }
    axe_names = [n.split(' ')[0] for n in save_names]
    save_name_gif = 'courbes.gif'
    plt.style.use('fivethirtyeight')
    sns.set_style(rc)
    # create figure
    fig, ax = plt.subplots(1, 1, figsize=(6, 5))
    plt.subplots_adjust(wspace=0, hspace=0.4)
    fig.set_tight_layout(True)
    ax.set_title(save_names[0], fontsize=14, color='grey')
    # initial plots: line and scatter
    lines = []
    courbes = []
    ind = 0
    courbe1, = ax.plot(X[ind][:l], Y[ind][0][:l], 'darkgrey', linewidth=2)
    courbe2, = ax.plot(X[ind][:l], Y[ind][1][:l], 'darkgrey', linewidth=2)
    courbe3, = ax.plot(X[ind][:l], Y[ind][2][:l], 'darkgrey', linewidth=2)
    line1, = ax.plot(X[ind][0], Y[ind][0][0], 'ro', label='x')
    line2, = ax.plot(X[ind][0], Y[ind][1][0], 'go', label='y')
    line3, = ax.plot(X[ind][0], Y[ind][2][0], 'bo', label='z')
    ax.set_xticks(X[ind][:l])
    ax.set_xticklabels([str(d)+' s' for d in range(l)])
    ax.legend()
    lines.append([line1, line2, line3])
    courbes.append([courbe1, courbe2, courbe3])
    # le champs de figure
    max_yaxe = max(max(Y[ind][0][:l]),max(Y[ind][1][:l]),max(Y[ind][2][:l]))
    min_yaxe = min(min(Y[ind][0][:l]),min(Y[ind][1][:l]),min(Y[ind][2][:l]))
    min_yaxe, max_yaxe = ajuster_minmax_axe(min_yaxe, max_yaxe)
    ax.set_ylim([min_yaxe, max_yaxe])

    def update(i):
        taille = len(X[0])
        ind = 0
        label = 'Temps: {0} s et '.format(round(i*interval/1000,2)) + \
                'AXE X : {0} \n'.format(round(Y[ind][0][i],2)) + \
                'AXE Y : {0} '.format(round(Y[ind][1][i],2)) + \
                'AXE Z : {0} \n'.format(round(Y[ind][2][i],2))
        print(label)
        diff = 0
        # refresh the scatter
        if (i%l == 0):
            diff = taille-i
            if diff>=(l-1) : 
                courbes[ind][0].set_ydata(Y[ind][0][i:i+l])
                courbes[ind][1].set_ydata(Y[ind][1][i:i+l])
                courbes[ind][2].set_ydata(Y[ind][2][i:i+l])
                x_ticks_labels = [str(i+d) for d in range(l)]
                ax.set_xticklabels(x_ticks_labels)
                max_yaxe = max(max(Y[ind][0][i:i+l]),max(Y[ind][1][i:i+l]),max(Y[ind][2][i:i+l]))
                min_yaxe = min(min(Y[ind][0][i:i+l]),min(Y[ind][1][i:i+l]),min(Y[ind][2][i:i+l]))
                min_yaxe, max_yaxe = ajuster_minmax_axe(min_yaxe, max_yaxe)
                ax.set_ylim([min_yaxe, max_yaxe])
            else :
                ax.set_xticks(X[ind][:diff])
                courbes[ind].set_ydata(Y[ind][i:i+diff])
                x_ticks_labels = [str(i+d) for d in range(diff)]
                ax.set_xticklabels(x_ticks_labels)
                max_yaxe = max(Y[ind][i:i+diff])
                min_yaxe = min(Y[ind][i:i+diff])
                min_yaxe, max_yaxe = ajuster_minmax_axe(min_yaxe, max_yaxe)
                ax.set_ylim([min_yaxe, max_yaxe])
            lines[ind][0].set_xdata(X[ind][0])
            lines[ind][0].set_ydata(Y[ind][0][i])
            lines[ind][1].set_xdata(X[ind][0])
            lines[ind][1].set_ydata(Y[ind][1][i])
            lines[ind][2].set_xdata(X[ind][0])
            lines[ind][2].set_ydata(Y[ind][2][i])
        else:
            a = i%l
            lines[ind][0].set_xdata(X[ind][a])
            lines[ind][0].set_ydata(Y[ind][0][i])
            lines[ind][1].set_xdata(X[ind][a])
            lines[ind][1].set_ydata(Y[ind][1][i])
            lines[ind][2].set_xdata(X[ind][a])
            lines[ind][2].set_ydata(Y[ind][2][i])
        # refresh xlabel
        ax.set_xlabel(label, fontsize=18, color='darkorange')
        return lines, ax
    
    # settings of the video to generate
    anim = FuncAnimation(fig, update, frames=np.arange(0, len(X[0])), interval=interval)
    print("Saving")
    anim.save(save_name_gif, writer='imagemagick', fps=fps_courbe)
    plt.show()
    # .gif to .mp4
    # clip = mp.VideoFileClip(save_name_gif)
    clip = VideoFileClip(save_name_gif)
    clip.write_videofile(save_video, codec='libx264')


def gather_ci_video(video_origin, save_video_name, fps_courbe, fps_output, interval, X, Y, l):
    '''
    Concatener toutes les vidéos CI
    '''
    cap = cv2.VideoCapture(video_origin)
    frames_num = int(cap.get(7))
    #all_save_courbe_names = ['Vitesse m/s', 'Accélération m/s2', 'Diatance km', 'Accélération latérale m/s2']
    save_courbe_names = ['Accélération latérale m/s2']
    
    courbe_ci_avi(X, Y, save_courbe_names, save_video_name, frames_num, fps_courbe, interval, l)


def courbe_mp4(X, Y, save_names, save_video, frames_num, fps_courbe, interval, l = 10, ran=3):
    '''
    Création les courbes et convertir en vidéo .mp4 (selon besoin, car .mp4 est moins utilisé dans ce logiciel que .avi)
    '''
    rc = {'axes.axisbelow': True, 
            'axes.edgecolor': 'white',
            'axes.facecolor': 'white',	#fond color
            'axes.grid': True,
         }
    axe_names = [n.split(' ')[0] for n in save_names]
    save_name_gif = 'courbes.gif'
    #save_name_mp4 = 'courbes.mp4'
    plt.style.use('fivethirtyeight')
    sns.set_style(rc)
   # create figure
    fig, ax = plt.subplots(ran,1, figsize=(int(10/3*ran), int(15/3*ran)))
    plt.subplots_adjust(wspace=0, hspace=0.4)
    fig.set_tight_layout(True)
    for ind in range(ran):
        ax[ind].set_title(save_names[ind], fontsize=14, color='grey')
        ax[ind].set_ylabel(save_names[ind], fontsize=14, color='grey')
    # initial plots: line and scatter
    lines = []
    courbes = []
    for ind in range(ran):
        if ind != ran-1:
            courbe, = ax[ind].plot(X[ind][:l], Y[ind][:l], 'darkgrey', linewidth=2)
            line, = ax[ind].plot(X[ind][0], Y[ind][0], 'ro')
            ax[ind].set_xticks(X[ind][:l])
            ax[ind].set_xticklabels([str(d)+' s' for d in range(l)])
            lines.append(line)
            courbes.append(courbe)
            max_yaxe = max(Y[ind][:l])
            min_yaxe = min(Y[ind][:l])
            min_yaxe, max_yaxe = ajuster_minmax_axe(min_yaxe, max_yaxe)
            ax[ind].set_ylim([min_yaxe, max_yaxe])
        else:
            courbe1, = ax[ind].plot(X[ind][:l], Y[ind][0][:l], 'darkgrey', linewidth=2)
            courbe2, = ax[ind].plot(X[ind][:l], Y[ind][1][:l], 'darkgrey', linewidth=2)
            courbe3, = ax[ind].plot(X[ind][:l], Y[ind][2][:l], 'darkgrey', linewidth=2)
            line1, = ax[ind].plot(X[ind][0], Y[ind][0][0], 'ro', label='x')
            line2, = ax[ind].plot(X[ind][0], Y[ind][1][0], 'go', label='y')
            line3, = ax[ind].plot(X[ind][0], Y[ind][2][0], 'bo', label='z')
            ax[ind].set_xticks(X[ind][:l])
            ax[ind].set_xticklabels([str(d)+' s' for d in range(l)])
            ax[ind].legend()
            lines.append([line1, line2, line3])
            courbes.append([courbe1, courbe2, courbe3])
            max_yaxe = max(max(Y[ind][0][:l]),max(Y[ind][1][:l]),max(Y[ind][2][:l]))
            min_yaxe = min(min(Y[ind][0][:l]),min(Y[ind][1][:l]),min(Y[ind][2][:l]))
            min_yaxe, max_yaxe = ajuster_minmax_axe(min_yaxe, max_yaxe)
            ax[ind].set_ylim([min_yaxe, max_yaxe])

    def update(i):
        taille = len(X[0])
        for ind in range(ran):
            if ind != ran-1:
                label = 'Temps: {0} s et '.format(round(i*interval/1000,2)) + axe_names[ind] + ': {0}'.format(round(Y[ind][i],2))
                print(label)
                diff = 0
                # refresh the scatter
                if (i%l == 0):
                    diff = taille-i
                    if diff>=(l-1) : 
                        courbes[ind].set_ydata(Y[ind][i:i+l])
                        #x_ticks_labels = [str(i+d)+' s' for d in range(l)]
                        x_ticks_labels = [str(i+d) for d in range(l)]
                        ax[ind].set_xticklabels(x_ticks_labels)
                        max_yaxe = max(Y[ind][i:i+l])
                        min_yaxe = min(Y[ind][i:i+l])
                        min_yaxe, max_yaxe = ajuster_minmax_axe(min_yaxe, max_yaxe)
                        ax[ind].set_ylim([min_yaxe, max_yaxe])
                    else :
                        ax[ind].set_xticks(X[ind][:diff])
                        courbes[ind].set_ydata(Y[ind][i:i+diff])
                        # x_ticks_labels = [str(i+d)+' s' for d in range(diff)]
                        x_ticks_labels = [str(i+d) for d in range(diff)]
                        ax[ind].set_xticklabels(x_ticks_labels)
                        max_yaxe = max(Y[ind][i:i+diff])
                        min_yaxe = min(Y[ind][i:i+diff])
                        min_yaxe, max_yaxe = ajuster_minmax_axe(min_yaxe, max_yaxe)
                        ax[ind].set_ylim([min_yaxe, max_yaxe])
                    lines[ind].set_xdata(X[ind][0])
                    lines[ind].set_ydata(Y[ind][i])
                else:
                    a = i%l
                    lines[ind].set_xdata(X[ind][a])
                    lines[ind].set_ydata(Y[ind][i])
            else:
                label = 'Temps: {0} s et '.format(round(i*interval/1000,2)) + \
                        'AXE X : {0} \n'.format(round(Y[ind][0][i],2)) + \
                        'AXE Y : {0} '.format(round(Y[ind][1][i],2)) + \
                        'AXE Z : {0} \n'.format(round(Y[ind][2][i],2))
                print(label)
                diff = 0
                # refresh the scatter
                if (i%l == 0):
                    diff = taille-i
                    if diff>=(l-1) : 
                        courbes[ind][0].set_ydata(Y[ind][0][i:i+l])
                        courbes[ind][1].set_ydata(Y[ind][1][i:i+l])
                        courbes[ind][2].set_ydata(Y[ind][2][i:i+l])
                        #x_ticks_labels = [str(i+d)+' s' for d in range(l)]
                        x_ticks_labels = [str(i+d) for d in range(l)]
                        ax[ind].set_xticklabels(x_ticks_labels)
                        max_yaxe = max(max(Y[ind][0][i:i+l]),max(Y[ind][1][i:i+l]),max(Y[ind][2][i:i+l]))
                        min_yaxe = min(min(Y[ind][0][i:i+l]),min(Y[ind][1][i:i+l]),min(Y[ind][2][i:i+l]))
                        min_yaxe, max_yaxe = ajuster_minmax_axe(min_yaxe, max_yaxe)
                        ax[ind].set_ylim([min_yaxe, max_yaxe])
                    else :
                        ax[ind].set_xticks(X[ind][:diff])
                        courbes[ind].set_ydata(Y[ind][i:i+diff])
                        #x_ticks_labels = [str(i+d)+' s' for d in range(diff)]
                        x_ticks_labels = [str(i+d) for d in range(diff)]
                        ax[ind].set_xticklabels(x_ticks_labels)
                        max_yaxe = max(Y[ind][i:i+diff])
                        min_yaxe = min(Y[ind][i:i+diff])
                        min_yaxe, max_yaxe = ajuster_minmax_axe(min_yaxe, max_yaxe)
                        ax[ind].set_ylim([min_yaxe, max_yaxe])
                    lines[ind][0].set_xdata(X[ind][0])
                    lines[ind][0].set_ydata(Y[ind][0][i])
                    lines[ind][1].set_xdata(X[ind][0])
                    lines[ind][1].set_ydata(Y[ind][1][i])
                    lines[ind][2].set_xdata(X[ind][0])
                    lines[ind][2].set_ydata(Y[ind][2][i])
                else:
                    a = i%l
                    lines[ind][0].set_xdata(X[ind][a])
                    lines[ind][0].set_ydata(Y[ind][0][i])
                    lines[ind][1].set_xdata(X[ind][a])
                    lines[ind][1].set_ydata(Y[ind][1][i])
                    lines[ind][2].set_xdata(X[ind][a])
                    lines[ind][2].set_ydata(Y[ind][2][i])
            # refresh xlabel
            ax[ind].set_xlabel(label, fontsize=18, color='darkorange')
        return line, ax
    # configurer la génération dela vidéo
    anim = FuncAnimation(fig, update, frames=np.arange(0, len(X[0])), interval=interval)
    print("Saving")
    anim.save(save_name_gif, writer='imagemagick', fps=fps_courbe)
    plt.show()
    clip = VideoFileClip(save_name_gif)
    clip.write_videofile(save_video, codec='libx264')


def gather_all_video(video_origin, save_video_name, fps_courbe, fps_output, interval, X, Y, l, ranges):
    '''
    Concatener toutes les vidéos
    '''
    cap = cv2.VideoCapture(video_origin)
    frames_num = int(cap.get(7))
    all_save_courbe_names = ['Vitesse m/s', 'Accélération m/s2', 'Diatance km', 'Accélération latérale m/s2']
    save_courbe_names = [all_save_courbe_names[i] for i in ranges]
    courbe_mp4(X, Y, save_courbe_names, save_video_name, frames_num, fps_courbe, interval, l, len(ranges))


def combine_all_avi(video_origin, save_video_name, fps_output, courbes):
    '''
    Concatener toutes les vidéos et sauvegarder on .avi
    '''
    ## concaterner deux mp4 ##
    print("==== Generating concate.mp4 ====")
    clip_1 = VideoFileClip(video_origin).set_position([0, 0])
    clip_2 = VideoFileClip(courbes).set_position([clip_1.w, 0])
    tall = 0
    if clip_1.h > clip_2.h:
        tall = clip_1.h
    else:
        tall = clip_2.h
    final_clip = CompositeVideoClip([clip_1, clip_2,], size=(clip_1.w+clip_2.w, tall)) 
    final_clip = resize(final_clip, width=640, height=360)
    final_clip.to_videofile(save_video_name, fps=fps_output, remove_temp=False)
    
    
def polair2cartesien(rows, begin, points, scan_dt, interval_origin, interval):
    '''
    Convertir les positions polaires aux positions cartésienne
    '''
    vision_horz = 190 * np.pi / 180
    begin_angle = 70 * np.pi / 180
    angle = np.arange(begin_angle, vision_horz+begin_angle, vision_horz/points)
    ## axe polaire -> axe cartésienne ##
    scanxy = []
    for i in range(rows-begin):
        x = scan_dt[i][1:].astype('float64')*0.001*np.cos(angle)
        y = scan_dt[i][1:].astype('float64')*0.001*np.sin(angle)
        scanxy.append([x, y])
    ## cumuler les pts xy dans 1 second ##
    step = interval/interval_origin
    indexe = np.arange(0,rows-begin+1,step)
    scanxy_per_second = []
    for l in range(rows-begin):
        if l in indexe:
            x = np.array(scanxy[l][0])
            y = np.array(scanxy[l][1])
            scanxy_per_second.append([x, y])
    return scanxy_per_second


def get_light(array, dict_light):
    '''
    Extraire les données de lumière
    '''
    out = []
    for i in range(len(array)):
        out.append(dict_light[array[i]])
    return np.array(out)


def remissionTreatment(rows, begin, points, remission_csv, interval_origin, interval):
    '''
    Traitement des données des remissions
    '''
    alpha_list = np.arange(0.3, 1, 0.7/8)
    list_code = np.arange(0, 255)
    dict_light = {list_code[i]:alpha_list[int(i/32)] for i in range(len(list_code))}
    lumino_csv = []
    for i in range(rows):
        array = remission_csv.loc[i].values[1:].astype('int32')
        lumino_csv.append(get_light(array, dict_light))
    ## cumuler les pts xy dans 1 second ##
    step = interval/interval_origin
    indexe = np.arange(0,rows-begin+1,step)
    light_per_second = []
    for l in range(rows-begin):
        if l in indexe:
            light = np.array(lumino_csv[l])
            light_per_second.append(light)
    return light_per_second


def LBP(x0, y0):
    '''
    Fonction pour extraire les features par LBP (Motif Binaire Local)
    '''
    s = [[1,1,1],
         [1,1,1],
         [1,1,1]]
    indx0 = np.array([639, 639, 639, 639, 639, 640, 640, 640, 640, 640, 640, 640, 641,
           641, 641, 641, 641, 641, 641, 642, 642, 642, 642, 642, 642, 642,
           643, 643, 643, 643, 643, 643, 643, 644, 644, 644, 644, 644, 644,
           644, 645, 645, 645, 645, 645])
    indy0 = np.array([295, 296, 297, 298, 299, 294, 295, 296, 297, 298, 299, 300, 294,
           295, 296, 297, 298, 299, 300, 294, 295, 296, 297, 298, 299, 300,
           294, 295, 296, 297, 298, 299, 300, 294, 295, 296, 297, 298, 299,
           300, 295, 296, 297, 298, 299])
    plt.figure(figsize=(8, 10))
    plt.plot(x0, y0, 'go')
    plt.ylim([-2, 40])
    plt.xlim([-8, 8])
    plt.axis('off')
    plt.savefig('temp.jpg')
    plt.close()
    data_rgb = plt.imread('temp.jpg')
    data = data_rgb[:,:,0]
    # Binarization
    # adding threshold to extract contour without label
    threshold = .57*(np.max(data)+np.min(data))
    data_hl = np.where(data > threshold, 0, 1)
    # Labelling
    # extract contour using label function
    label_data, nb_labels = label(data_hl, structure=s)
    # count the sum of pixels for each label and sort them
    labels = np.bincount(label_data.flatten())
    labels_sorted = np.sort(labels)
    f = 120
    indexe = np.where(labels_sorted >= f)[0]
    obj_loc = np.zeros_like(label_data)
    for ind in indexe[:-1]:
        obj = labels_sorted[ind]
        obj_label = np.where(labels == obj)[0][0]
        # locate objects on original image
        obj_loc += np.where(label_data==obj_label, 1, 0)
    for i in range(len(indx0)):
        obj_loc[indx0[i], indy0[i]] = 1
    os.remove('temp.jpg')
    return obj_loc


# =============================================================================
# Traiter les données de Lidar
# =============================================================================
def lidar_video(save_name_gif, save_name_mp4, data_final, interval, fps_courbe):
    '''
    Dessiner les courbes pour le Lidar et convertir en vidéo .avi
    '''
    ## Animation pour mettre à jour l'environement ##
    rc = {'axes.axisbelow': True,
            'axes.edgecolor': 'white',
            'axes.facecolor': 'white',
            'axes.grid': True,
         }
    plt.style.use('fivethirtyeight')
    sns.set_style(rc)
    # Initialiser une figure
    fig, ax = plt.subplots(figsize=(8, 10))
    fig.set_tight_layout(False)
    ax.set_title('Environnement 2D simulé')
    ax.axis('off')
    # Dessiner une figure intiale (scatter avec une ligne initiale)
    x0 , y0 = data_final[0]
    obj_loc = LBP(-x0, y0)
    im =  ax.imshow(obj_loc, cmap='gray', animated = True)
    ax.set_ylabel('Position XY en m')

    def update(i):
        label = 'Temps: {0} s'.format(i*interval/1000)
        x0 , y0 = data_final[i]
        obj_loc = LBP(-x0, y0)
        im.set_data(obj_loc)
        print(label)
        ax.set_xlabel(label)
        return im, ax
    # configurer la génération dela vidéo
    anim = FuncAnimation(fig, update, frames=np.arange(0, len(data_final)), interval=interval)
    anim.save(save_name_gif, writer='imagemagick', fps=fps_courbe)
    clip = VideoFileClip(save_name_gif)
    clip.write_videofile(save_name_mp4, codec='libx264')


def lidar_video_brut(save_name_gif, save_name_mp4, data_final, interval, fps_courbe):
    ## Animation pour mettre à jour l'environement ##
    rc = {'axes.axisbelow': True,
            'axes.edgecolor': 'white',
            'axes.facecolor': 'white',
            'axes.grid': True,
         }
    plt.style.use('fivethirtyeight')
    sns.set_style(rc)
    # Initialiser une figure
    fig, ax = plt.subplots(figsize=(8, 10))
    fig.set_tight_layout(False)
    ax.set_title('Environnement 2D simulé')
    ax.set_ylim([-2, 40])
    ax.set_xlim([-8, 8])
    # Dessiner une figure intiale (scatter avec une ligne initiale)
    line, = ax.plot(-data_final[0][0], data_final[0][1], 'go')
    ax.set_ylabel('Position XY en m')

    def update(i):
        label = 'Temps: {0} s'.format(i*interval/1000)
        print(label)
        line.set_data(-data_final[i][0], data_final[i][1])
        ax.set_xlabel(label)
        return line, ax
    # Configurer la génération dela vidéo
    # Mise à jour l'animation
    anim = FuncAnimation(fig, update, frames=np.arange(0, len(data_final)), interval=interval)
    anim.save(save_name_gif, writer='imagemagick', fps=fps_courbe)
    clip = VideoFileClip(save_name_gif)
    clip.write_videofile(save_name_mp4, codec='libx264')
    
    
def lidar_video_brut_remis(save_name_gif, save_name_mp4, data_final, light_final, alpha_list, interval, fps_courbe):
    ## Animation pour mettre à jour l'environement ##
    rc = {'axes.axisbelow': True,
            'axes.edgecolor': 'white',
            'axes.facecolor': 'white',
            'axes.grid': True,
         }
    plt.style.use('fivethirtyeight')
    sns.set_style(rc)
    # Initialiser une figure
    fig, ax = plt.subplots(figsize=(8, 10))
    fig.set_tight_layout(False)
    ax.set_title('Environnement 2D simulé')
    ax.set_ylim([-2, 40])
    ax.set_xlim([-8, 8])
    # Dessiner une figure intiale (scatter avec une ligne initiale)
    lines = []
    for val in alpha_list:
        indexe = np.where(light_final[0] == val)[0]
        line, = ax.plot(-data_final[0][0][indexe], data_final[0][1][indexe], 'go', alpha=val)
        lines.append(line)
    ax.set_ylabel('Position XY en m')

    def update(i):
        label = 'Temps: {0} s'.format(i*interval/1000)
        print(label)
        for n, val in enumerate(alpha_list):
            indexe = np.where(light_final[i] == val)[0]
            lines[n].set_data(-data_final[i][0][indexe], data_final[i][1][indexe])
            lines[n].set_alpha(val)
        ax.set_xlabel(label)
        return line, ax
    # Configurer la génération dela vidéo
    # Mise à jour l'animation
    anim = FuncAnimation(fig, update, frames=np.arange(0, len(data_final)), interval=interval)
    anim.save(save_name_gif, writer='imagemagick', fps=fps_courbe)
    clip = VideoFileClip(save_name_gif)
    clip.write_videofile(save_name_mp4, codec='libx264')
    

# =============================================================================
# Fussioner les vidéos et les sauvegarder 
# =============================================================================
def concate_env(fps_output, video_origin, save_video_name, save_name_mp4):
    '''
    Fussioner les vidéos et les sauvegarder
    '''
    print("==== Generating concate.mp4 ====")
    clip_1 = VideoFileClip(video_origin).set_position([0, 0])
    clip_2 = VideoFileClip(save_name_mp4).set_position([clip_1.w, 0])
    tall = 0
    if clip_1.h > clip_2.h:
        tall = clip_1.h
    else:
        tall = clip_2.h
    final_clip = CompositeVideoClip([clip_1, clip_2,], size=(clip_1.w+clip_2.w, tall)) 
    final_clip = resize(final_clip, width=640, height=360)
    final_clip.to_videofile(save_video_name, fps=fps_output, remove_temp=False)