# -*- coding: utf-8 -*-
"""
# Created on Wed Apr 28 15:01:00 2021
# @title : Projet PROFIL
# @author: Xiaohua LU (Stagiaire Céréma - INSA GM5)
"""

import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn
import cv2
from datetime import timedelta
from scipy.signal import argrelextrema


def traiter_odo(csv_file):
    '''
    Traiter les données d'odometer, transformer de [0.001, 65.535] à valuer lisible

    Parameters
    ----------
    csv_file : pd.DataFrame

    Returns
    -------
    csv_file : pd.DataFrame
    '''
    odo_dis = csv_file['Odometer'].values
    max_idx = argrelextrema(odo_dis, np.greater)[0]

    step = 0
    new_odo_dis = []
    for i in range(len(odo_dis)):
        if i in max_idx:
            step += odo_dis[i]
            new_odo_dis.append(step/1000)
        else:
            new_odo_dis.append((step+odo_dis[i])/1000)
    csv_file['Odo_distance'] = new_odo_dis
    return csv_file


def split_time_eu(timestamp_eu): 
    '''
    Convertir timestamp à un objet datetime

    Parameters
    ----------
    timestamp_eu : str

    Returns
    -------
    dt : datetime.datetime
    '''
    y, m, nd = timestamp_eu.split('/')
    d, clock_eu = nd.split(' ')
    H, M, Ss = clock_eu.split(':')
    S, s = Ss.split('.')
    dt = datetime.datetime(year=int(y), month=int(m), day=int(d), hour=int(H), minute=int(M), second=int(S), microsecond=int(s))
    return dt


def time_diff(dt1, dt2):
    '''Différence entre 2 valeurs du temps'''
    return (dt2-dt1).total_seconds()


def temps_consecu(csv_file):
    '''
    Traiter les intervals temporels dela colonne delta_t
    
    Parameters
    ----------
    csv_file : pd.DataFrame

    Returns
    -------
    csv_file : pd.DataFrame
    '''
    intervals = csv_file['delta_t']
    intervals_consécu = []
    for i, interval in enumerate(intervals):
        if (i==0) or (i==1):
            intervals_consécu.append(round(interval, 4))
        else:
            intervals_consécu.append(round(interval-intervals[i-1], 4))
    csv_file['delta_t_consecu'] = intervals_consécu
    return csv_file


def deg_to_arc(deg):
    '''Convertir degré en arc'''
    return deg*np.pi/180


def to_distance(lon1, lon2, lat1, lat2):
    '''Coordonnées géographiques -> distance en mètre'''
    a1 = deg_to_arc(lat1)
    a2 = deg_to_arc(lat2)
    b1 = deg_to_arc(lon1)
    b2 = deg_to_arc(lon2)
    
    diff_lat = a1 - a2
    diff_long = b1 - b2
    racine = np.sqrt(np.sin(diff_lat/2)**2+np.cos(a1)*np.cos(a2)*np.sin(diff_long/2)**2)
    S = 2*6378.137*np.arcsin(racine)
    return S


def gps_distance(gps_csv):
    '''
    Ajouter une colonne "distance" en mètre dans gps_csv

    Parameters
    ----------
    gps_csv : pd.DataFrame

    Returns
    -------
    gps_csv : pd.DataFrame
    '''
    all_longs =  gps_csv['Longitude']
    all_lats = gps_csv['Latitude']
    distance = []
    for i, long in enumerate(all_longs):
        if i==0:
            distance.append(0)
        else:
            long1 = gps_csv['Longitude'][i]
            long2 = gps_csv['Longitude'][i-1]
            lat1 = gps_csv['Latitude'][i]
            lat2 = gps_csv['Latitude'][i-1]
            distance.append(to_distance(long1, long2, lat1, lat2))
    gps_csv['Distance'] = distance
    return gps_csv


def calcul_acc(csv_file):
    '''
    Calculer l'accélération en fonction dela vitesse
    
    Parameters
    ----------
    csv_file : pd.DataFrame

    Returns
    -------
    csv_file : pd.DataFrame
    '''
    speed = csv_file['VehicleSpeed']/3.6  # from k/h to m/s
    time = csv_file['delta_t_consecu']
    ## Traiter les intervals temporels ##
    acc = []
    for i, s in enumerate(speed):
        if (i==0):
            acc.append(round(s, 4))
        else:
            acc.append(round((s-speed[i-1])/time[i], 4))
    csv_file['acc'] = acc
    return csv_file


def calcul_vit(csv_file):
    '''
    Calculer la vitesse en fonction dela distance
    
    Parameters
    ----------
    csv_file : pd.DataFrame

    Returns
    -------
    csv_file : pd.DataFrame
    '''
    distance = csv_file['Distance']  # km
    time = csv_file['delta_t_consecu']
    ## Traiter les intervals temporels ##
    vit = []
    for i, s in enumerate(distance):
        if (i==0):
            vit.append(round(s, 4))
        else:
            vit.append(round((s-distance[i-1])/time[i], 4))
    csv_file['Vitesse'] = vit
    return csv_file