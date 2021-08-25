# -*- coding: utf-8 -*-
"""
# Created on Wed Apr 28 15:01:00 2021
# @title : Projet PROFIL
# @author: Xiaohua LU (Stagiaire Céréma - INSA GM5)
"""


# =============================================================================
# Dependencies
# =============================================================================
import sys
import os
import pandas as pd
import numpy as np

# QT dependencies
import qtawesome
import pyqtgraph as pg
from PyQt5 import QtCore,QtGui,QtWidgets
from PyQt5.QtWidgets import QMessageBox, QScrollArea
from PyQt5.QtGui import *
# from PyQt5.QtCore.Qt import KeepAspectRatio
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer, QMediaPlaylist
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.Qt import QUrl
from pyqtgraph import PlotWidget, plot
from moviepy.video.compositing.concatenate import concatenate_videoclips
from PyQt5 import uic

# Scripts
from treatData import *
from video2 import *
from detect import *


# =============================================================================
# Software UI
# =============================================================================
class MainUi(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.showMaximized()
        self.setWindowTitle('PROFIL v1')
        self.init_ui()

    def click_window1(self):
        if self.stacked_layout.currentIndex() != 1:
            self.stacked_layout.setCurrentIndex(1)
                
    def click_window2(self):
        if self.stacked_layout.currentIndex() != 2:
            self.stacked_layout.setCurrentIndex(2)
            
    def click_window3(self):
        if self.stacked_layout.currentIndex() != 3:
            self.stacked_layout.setCurrentIndex(3)
            
    def click_window4(self):
        if self.stacked_layout.currentIndex() != 4:
            self.stacked_layout.setCurrentIndex(4)
    
    def click_window5(self):
        if self.stacked_layout.currentIndex() != 5:
            self.stacked_layout.setCurrentIndex(5)
            
    def closeEvent(self, event):
        '''
        override, le méssage affiché lors de quitter le logiciel
        '''
        reply = QtWidgets.QMessageBox.question(self, 'Message', "Voulez vous vraiment quitter?",  QtWidgets.QMessageBox.Yes,  QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
 
    def mousePressEvent(self, event):
        '''
        la position de souris lors de la clique
        '''
        self.pressX = event.x()
        self.pressY = event.y()

    def mouseMoveEvent(self, event):
        '''
        la position de souris lors du deplacement
        '''
        x = event.x()
        y = event.y()
        # la distance déplacée
        moveX = x-self.pressX
        moveY = y-self.pressY
        # la position de fenêtre après le déplacement
        positionX = self.frameGeometry().x() + moveX
        positionY = self.frameGeometry().y() + moveY
        self.move(positionX, positionY)
    
    def wheelEvent(self, event):
        angle = event.angleDelta()
        y = angle.y()
        self.hSb.setValue(self.hSb.value() - y)
        
        
    # =============================================================================
    # Interface 4 : DETECTION
    # =============================================================================
    def displayPlayedTime4(self, ms):
        '''
        afficher le temps écoulé

        Parameters
        ----------
        ms : 
            temps écoulé en micro-seconde
        '''
        minutes = int(ms/60000)
        seconds = int((ms-minutes*60000)/1000)
        self.lab_duration42.setText('\t{}:{}'.format(minutes, seconds))
        
    def getDuration4(self, d):
        '''
        retourner la duration de la vidéo

        Parameters
        ----------
        d : 
            duration de la vidéo
        '''
        self.slider4.setRange(0, d)
        self.slider4.setEnabled(True)
        
        self.displayPlayedTime4(self.slider4.maximum()-d)
        self.displayTime4(d)
        
    def getPosition4(self, p):
        '''
        retourner la poisition de la vidéo
        '''
        self.slider4.setValue(p)
        self.displayPlayedTime4(p)
        self.displayTime4(self.slider4.maximum()-p)
        
    def displayTime4(self, ms):
        '''
        retourner le temps restant de la vidéo
        '''
        minutes = int(ms/60000)
        seconds = int((ms-minutes*60000)/1000)
        self.lab_duration4.setText('{}:{}'.format(minutes, seconds))
        
    def updatePosition4(self, v):
        '''
        mise à jour de la position de la barre de progression
        '''
        self.player4.setPosition(v)
        self.displayPlayedTime4(v)
        self.displayTime4(self.slider4.maximum()-v)
        
    def updatePosition_video4(self, v):
        '''
        mise à jour de la position de la barre de progression
        '''
        self.player4.setPosition(v)
        self.displayPlayedTime4(v)
        self.displayTime4(self.slider4.maximum()-v)
        
    def win4_PlayPause(self):
        '''
        lecture vidéo et pause
        '''
        if self.start4.isChecked():
            if self.player4.state()!=1:
                self.player4.play()
        else:
            if self.player4.state()==1:
                self.player4.pause()

    def win4_fileVideoIn(self):
        '''
        lecture du fichier vidéo
        '''
        self.video_fileName4, filetype = QtWidgets.QFileDialog.getOpenFileName(self, 'File Explorer', '', 'Fichier Media (*.mp4;*.avi)')
        if len(self.video_fileName4) == 0:
            print("Cancel choosing...")
            self.video_btn2.setChecked(False)
            return
        else:
            print('le chemin du csv courrant:' + self.video_fileName4)
            
    def win4_GenererVideo(self):
        '''
        générer la vidéo selon les donn2es et la vidéo
        '''
        self.right_label_451.setText("En cours de générer les detections. Merci d'attendre...")
        self.right_label_451.repaint()
        
        self.save_video_name4, filetype = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File Explorer', '', 'Fichier Media (*.avi)')
        if len(self.save_video_name4) == 0:
            print("Cancel choosing...")
            self.genVideo3.setChecked(False)
            return
        else:
            detectionYolo(self.video_fileName4, self.save_video_name4)
            self.player4 = QMediaPlayer()
            # Widget pour afficher
            self.play_video4 = QVideoWidget()
            self.play_video4.setFixedWidth(int(self.screen.width()*0.6))
            self.play_video4.setFixedHeight(int(self.screen.width()*0.4))
            # Widget pour exporter
            self.playlist_courbes3 = QMediaPlaylist()
            self.player4.setVideoOutput(self.play_video4)
            # Ajouter une vidéo
            self.playlist_courbes3.addMedia(QMediaContent(QUrl.fromLocalFile(self.save_video_name4)))
            self.player4.setPlaylist(self.playlist_courbes3)
            # Interactions
            self.right_label_451.setText("La detection est faite. Cliquez pour regarder les vidéos.")
            self.right_label_451.repaint()
            self.player4.durationChanged.connect(self.getDuration4)
            self.player4.positionChanged.connect(self.getPosition4)
            self.slider4.sliderMoved.connect(self.updatePosition4)
            self.right_layout45.addWidget(self.play_video4,0,0)
            
            
    # =============================================================================
    # Interface 3 : SIMULATION
    # =============================================================================
    def displayPlayedTime2(self, ms):
        '''
        afficher le temps écoulé
        '''
        minutes = int(ms/60000)
        seconds = int((ms-minutes*60000)/1000)
        self.lab_duration22.setText('\t{}:{}'.format(minutes, seconds))
        
    def getDuration2(self, d):
        '''
        retourner la duration de la vidéo
        '''
        self.slider2.setRange(0, d)
        self.slider2.setEnabled(True)
        self.displayPlayedTime2(self.slider2.maximum()-d)
        self.displayTime2(d)
        
    def getPosition2(self, p):
        '''
        retourner la poisition de la vidéo
        '''
        self.slider2.setValue(p)
        
        self.displayPlayedTime2(p)
        self.displayTime2(self.slider2.maximum()-p)
        
    def displayTime2(self, ms):
        '''
        retourner le temps restant de la vidéo
        '''
        minutes = int(ms/60000)
        seconds = int((ms-minutes*60000)/1000)
        self.lab_duration2.setText('{}:{}'.format(minutes, seconds))
        
    def updatePosition2(self, v):
        '''
        mise à jour de la position de la barre de progression
        '''
        self.player2.setPosition(v)
        self.displayPlayedTime2(v)
        self.displayTime2(self.slider2.maximum()-v)
        
    def updatePosition_video2(self, v):
        '''
        mise à jour de la position de la barre de progression
        '''
        self.player3.setPosition(v)
        self.displayPlayedTime2(v)
        self.displayTime2(self.slider2.maximum()-v)
        
    def win3_PlayPause(self):
        '''
        lecture vidéo et pause
        '''
        if self.start2.isChecked():
            try:
                if self.player2.state()!=1 and self.player3.state()!=1:
                    self.player2.play()
                    self.player3.play()
            except:
                if self.player3.state()!=1:
                    self.player3.play()
        else:
            try:
                if self.player2.state()==1 and self.player3.state()==1:
                    self.player2.pause()
                    self.player3.pause()
            except:
                if self.player3.state()==1:
                    self.player3.pause()
        
    def win3_GenererVideo(self):
        '''
        générer la vidéo selon les données et la vidéo
        '''
        if not self.cb31.isChecked() and not self.cb32.isChecked() and not self.cb33.isChecked() and not self.cb34.isChecked():
            QtWidgets.QMessageBox.information(self,'Error Message',"Veuillez choisir au moins une façon pour traiter Lidar!" )
            self.genVideo2.setChecked(False)
            return
        else:
            self.right_label_351.setText("En cours de générer les courbes. Merci d'attendre...")
            self.right_label_351.repaint()
            
            self.save_video_name2, filetype = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File Explorer', '', 'Fichier Media (*.avi)')
            if len(self.save_video_name2) == 0:
                print("Cancel choosing...")
                self.genVideo2.setChecked(False)
                return
            
            dirs = './temp/'
            if not os.path.exists(dirs):
                os.makedirs(dirs)
            
            all_dossiers = os.listdir(dirs)
            
            for dos in all_dossiers:
                if dos.endswith('.avi'):
                    filePath = dirs+dos
                    os.remove(filePath)
                elif dos.endswith('.gif'):
                    filePath = dirs+dos
                    os.remove(filePath)
                
            if not self.cb31.isChecked() and not self.cb32.isChecked() and self.cb33.isChecked() and not self.cb34.isChecked():
                fps_courbe = 1  #5
                interval_origin = 40
                interval = 1000 #200
                
                for i in range(0,20):
                    save_name_gif = dirs+'lidar' + str(i) + '.gif'
                    save_name_mp4 = dirs+'lidar' + str(i) + '.avi'
                    
                    begin = 0
                    rows = 20000
                    skip = rows*i
                    
                    try:
                        text = 'Read files: %d - %d...'%(skip, skip+rows)
                        self.right_label_351.setText(text)
                        self.right_label_351.repaint()
                        
                        scan_csv = pd.read_csv(self.lidar_fileName, sep=';', nrows=rows, skiprows=skip, header=None)
                        points = len(np.arange(0, len(scan_csv.loc[0].values[1:])))
                        scan_dt = scan_csv.loc[begin:rows].values
                        scanxy_per_second = polair2cartesien(rows, begin, points, scan_dt, interval_origin, interval)
                        
                        data_final = scanxy_per_second
                        lidar_video(save_name_gif, save_name_mp4, data_final, interval, fps_courbe)
                    except:
                        # print("Read last files.")
                        self.right_label_351.setText("Read last files.")
                        self.right_label_351.repaint()
                        
                        scan_csv = pd.read_csv(self.lidar_fileName, sep=';', skiprows=skip, header=None)
                        rows = len(scan_csv)
                        points = len(np.arange(0, len(scan_csv.loc[0].values[1:])))
                        scan_dt = scan_csv.loc[begin:rows].values
                        scanxy_per_second = polair2cartesien(rows, begin, points, scan_dt, interval_origin, interval)
                        
                        data_final = scanxy_per_second
                        lidar_video(save_name_gif, save_name_mp4, data_final, interval, fps_courbe)
                        print('Break the iteration.')
                        break
                    
                all_dossiers = os.listdir(dirs)
                save_all_mp4 = self.save_video_name2
                all_mp4 = []
                for dos in all_dossiers:
                    print(dos)
                    if dos.endswith('.avi'):
                        filePath = dirs+dos
                        video = VideoFileClip(filePath)
                        all_mp4.append(video)
                    elif dos.endswith('.gif'):
                        filePath = dirs+dos
                        os.remove(filePath)
                        
                final_clip = concatenate_videoclips(all_mp4)
                final_clip.to_videofile(save_all_mp4, remove_temp=False, fps=fps_courbe, codec='libx264')
            ##########
            
            elif self.cb31.isChecked() and not self.cb32.isChecked() and not self.cb33.isChecked() and not self.cb34.isChecked():
                fps_courbe = 1  #5
                interval_origin = 40
                interval = 1000 #200
                
                for i in range(0,20):
                    save_name_gif = dirs+'lidar' + str(i) + '.gif'
                    save_name_mp4 = dirs+'lidar' + str(i) + '.avi'
                    
                    begin = 0
                    rows = 20000
                    skip = rows*i
                    
                    try:
                        text = 'Read files: %d - %d...'%(skip, skip+rows)
                        self.right_label_351.setText(text)
                        self.right_label_351.repaint()
                        
                        scan_csv = pd.read_csv(self.lidar_fileName, sep=';', nrows=rows, skiprows=skip, header=None)
                        points = len(np.arange(0, len(scan_csv.loc[0].values[1:])))
                        scan_dt = scan_csv.loc[begin:rows].values
                        scanxy_per_second = polair2cartesien(rows, begin, points, scan_dt, interval_origin, interval)
                        
                        data_final = scanxy_per_second
                        lidar_video_brut(save_name_gif, save_name_mp4, data_final, interval, fps_courbe)
                    except:
                        # print("Read last files.")
                        self.right_label_351.setText("Read last files.")
                        self.right_label_351.repaint()
                        
                        scan_csv = pd.read_csv(self.lidar_fileName, sep=';', skiprows=skip, header=None)
                        rows = len(scan_csv)
                        points = len(np.arange(0, len(scan_csv.loc[0].values[1:])))
                        scan_dt = scan_csv.loc[begin:rows].values
                        scanxy_per_second = polair2cartesien(rows, begin, points, scan_dt, interval_origin, interval)
                        
                        data_final = scanxy_per_second
                        lidar_video_brut(save_name_gif, save_name_mp4, data_final, interval, fps_courbe)
                        print('Break the iteration.')
                        break
                    
                save_all_mp4 = self.save_video_name2
                all_mp4 = []
                for dos in all_dossiers:
                    if dos.endswith('.avi'):
                        filePath = dirs+dos
                        video = VideoFileClip(filePath)
                        all_mp4.append(video)
                    elif dos.endswith('.gif'):
                        filePath = dirs+dos
                        os.remove(filePath)
                        
                final_clip = concatenate_videoclips(all_mp4)
                final_clip.to_videofile(save_all_mp4, remove_temp=False, fps=fps_courbe, codec='libx264')
            ##########
            
            elif not self.cb31.isChecked() and self.cb32.isChecked() and not self.cb33.isChecked() and not self.cb34.isChecked():
                fps_courbe = 1  #5
                interval_origin = 40
                interval = 1000 #200
                
                for i in range(0,20):
                    save_name_gif = dirs+'lidar' + str(i) + '.gif'
                    save_name_mp4 = dirs+'lidar' + str(i) + '.avi'
                    
                    begin = 0
                    rows = 20000
                    skip = rows*i
                    
                    try:
                        text = 'Read files: %d - %d...'%(skip, skip+rows)
                        self.right_label_351.setText(text)
                        self.right_label_351.repaint()
                        
                        alpha_list = np.arange(0.3, 1, 0.7/8)
                        scan_csv = pd.read_csv(self.lidar_fileName, sep=';', nrows=rows, skiprows=skip, header=None)
                        remission_csv = pd.read_csv(self.remission_fileName, sep=';', nrows=rows, skiprows=skip, header=None)
                        
                        points = len(np.arange(0, len(scan_csv.loc[0].values[1:])))
                        scan_dt = scan_csv.loc[begin:rows].values
                        
                        scanxy_per_second = polair2cartesien(rows, begin, points, scan_dt, interval_origin, interval)
                        light_per_second = remissionTreatment(rows, begin, points, remission_csv, interval_origin, interval)
                        data_final = scanxy_per_second
                        light_final = light_per_second
                        lidar_video_brut_remis(save_name_gif, save_name_mp4, data_final, light_final, alpha_list, interval, fps_courbe)
                    except:
                        # print("Read last files.")
                        self.right_label_351.setText("Read last files.")
                        self.right_label_351.repaint()
                        
                        alpha_list = np.arange(0.3, 1, 0.7/8)
                        scan_csv = pd.read_csv(self.lidar_fileName, sep=';', skiprows=skip, header=None)
                        remission_csv = pd.read_csv(self.remission_fileName, sep=';', skiprows=skip, header=None)
                        
                        rows = len(scan_csv)
                        points = len(np.arange(0, len(scan_csv.loc[0].values[1:])))
                        scan_dt = scan_csv.loc[begin:rows].values
                        
                        scanxy_per_second = polair2cartesien(rows, begin, points, scan_dt, interval_origin, interval)
                        light_per_second = remissionTreatment(rows, begin, points, remission_csv, interval_origin, interval)
                        
                        data_final = scanxy_per_second
                        light_final = light_per_second
                        lidar_video_brut_remis(save_name_gif, save_name_mp4, data_final, light_final, alpha_list, interval, fps_courbe)
                        print('Break the iteration.')
                        break
                    
                
                save_all_mp4 = self.save_video_name2
                all_dossiers = os.listdir(dirs)
                all_mp4 = []
                for dos in all_dossiers:
                    if dos.endswith('.avi'):
                        filePath = dirs+dos
                        video = VideoFileClip(filePath)
                        all_mp4.append(video)
                    elif dos.endswith('.gif'):
                        filePath = dirs+dos
                        os.remove(filePath)
                        
                final_clip = concatenate_videoclips(all_mp4)
                final_clip.to_videofile(save_all_mp4, remove_temp=False, fps=fps_courbe, codec='libx264')
            ##########
            
            self.player2 = QMediaPlayer()
            # Widget pour afficher
            self.play_video2 = QVideoWidget()
            self.play_video2.setFixedWidth(int(self.screen.width()*0.25))
            self.play_video2.setFixedHeight(int(self.screen.width()*0.3))
            # Widget pour exporter            
            self.playlist_courbes2 = QMediaPlaylist()
            self.player2.setVideoOutput(self.play_video2)
            self.playlist_courbes2.addMedia(QMediaContent(QUrl.fromLocalFile(self.save_video_name2)))
            self.player2.setPlaylist(self.playlist_courbes2)
            # Interactions
            self.right_label_351.setText("Le nuage des points est faite. Cliquez pour regarder les vidéos.")
            self.right_label_351.repaint()
            self.player2.durationChanged.connect(self.getDuration2)
            self.player2.positionChanged.connect(self.getPosition2)
            self.slider2.sliderMoved.connect(self.updatePosition2)
            self.right_layout35.addWidget(self.play_video2,1,8)
            
    def win3_fileLidarIn(self):
        '''
        lecture du fichier Lidar
        '''
        self.lidar_fileName, filetype = QtWidgets.QFileDialog.getOpenFileName(self, 'File Explorer', '', 'Fichier CSV (*.csv)')
        if len(self.lidar_fileName) == 0:
            print("Cancel choosing...")
            self.lidar_btn.setChecked(False)
            return
        else:
            print('le chemin du csv courrant:' + self.lidar_fileName)
            
    def win3_fileRemisIn(self):
        '''
        lecture du fichier Remission
        '''
        self.remission_fileName, filetype = QtWidgets.QFileDialog.getOpenFileName(self, 'File Explorer', '', 'Fichier CSV (*.csv)')
        if len(self.remission_fileName) == 0:
            print("Cancel choosing...")
            self.remis_btn.setChecked(False)
            return
        else:
            print('le chemin du csv courrant:' + self.remission_fileName)
            
    def win3_fileVideoIn(self):
        '''
        lecture du fichier vidéo
        '''
        self.video_fileName3, filetype = QtWidgets.QFileDialog.getOpenFileName(self, 'File Explorer', '', 'Fichier Media (*.mp4;*.avi)')
        if len(self.video_fileName3) == 0:
            print("Cancel choosing...")
            self.video_btn1.setChecked(False)
            return
        else:
            print('le chemin du csv courrant:' + self.video_fileName3)
            # Widget pour afficher
            self.player3 = QMediaPlayer()
            self.play_video3 = QVideoWidget()
            self.play_video3.setFixedWidth(int(self.screen.width()*0.32))
            self.play_video3.setFixedHeight(int(self.screen.width()*0.3))
            # Widget pour exporter
            self.player3.setVideoOutput(self.play_video3)
            self.player3.setMedia(QMediaContent(QUrl.fromLocalFile(self.video_fileName3)))  
            self.play_video3.setStyleSheet("background-color: black")
            # Interactions
            self.player3.durationChanged.connect(self.getDuration2)
            self.player3.positionChanged.connect(self.getPosition2)
            self.slider2.sliderMoved.connect(self.updatePosition_video2)
            self.right_layout35.addWidget(self.play_video3,1,0)
        
    def win3_refreshCourbes(self):
        '''
        mise à jour des courbes
        '''
        reply = QMessageBox.question(self, 'Message', "Voulez vous refaire le nuqge des points ?",  QMessageBox.Yes,  QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.genVideo2.setChecked(False)
            self.cb31.setChecked(False)
            self.cb32.setChecked(False)
            self.cb33.setChecked(False)
            self.cb34.setChecked(False)
            
            self.save_video_name2 = ""
            self.right_label_351.setText("Veillez choisir la nouvelle type.")
            self.playlist_courbes2.clear()
            self.player3.stop()
            self.refresh2.setChecked(False)
            self.play_video3.setStyleSheet("background-color: white")
            
    def win3_combineAvi(self):
        '''
        merger les vidéos
        '''
        fps_output = 7
        self.right_label_351.setText("En cour de combiner deux vidéos... ça prend du temps !")
        self.right_label_351.repaint()
        
        self.save_video_name32, filetype = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File Explorer', '', 'Fichier Media (*.mp4)')
        if len(self.save_video_name32) == 0:
            print("Cancel choosing...")
            self.right_label_351.setText("")
            self.export2.setChecked(False)
            return
        else:
            combine_all_avi(self.video_fileName3, self.save_video_name32, fps_output, self.save_video_name2)
            self.right_label_251.setText(self.save_video_name32+" est bien enregistré.")
    
    def changecb3(self):
        '''
        retourne de message lors d'erreux en raison de séléction
        '''
        if self.cb31.isChecked() and self.cb32.isChecked() :
            QtWidgets.QMessageBox.information(self,'Error Message','Vous ne pouvez pas générer les deux en même temps!')
            self.cb31.setCheckState(QtCore.Qt.Unchecked)
            self.cb32.setCheckState(QtCore.Qt.Unchecked)
            self.cb33.setCheckState(QtCore.Qt.Unchecked)
        elif self.cb31.isChecked() and self.cb33.isChecked():
            QtWidgets.QMessageBox.information(self,'Error Message','Vous ne pouvez pas générer les deux en même temps!')
            self.cb31.setCheckState(QtCore.Qt.Unchecked)
            self.cb32.setCheckState(QtCore.Qt.Unchecked)
            self.cb33.setCheckState(QtCore.Qt.Unchecked)
        elif self.cb32.isChecked() and self.cb33.isChecked():
            QtWidgets.QMessageBox.information(self,'Error Message','Vous ne pouvez pas générer les deux en même temps!')
            self.cb31.setCheckState(QtCore.Qt.Unchecked)
            self.cb32.setCheckState(QtCore.Qt.Unchecked)
            self.cb33.setCheckState(QtCore.Qt.Unchecked)
        elif self.cb31.isChecked() and self.cb32.isChecked() and self.cb33.isChecked():
            QtWidgets.QMessageBox.information(self,'Error Message','Vous ne pouvez pas générer les trois en même temps!')
            self.cb31.setCheckState(QtCore.Qt.Unchecked)
            self.cb32.setCheckState(QtCore.Qt.Unchecked)
            self.cb33.setCheckState(QtCore.Qt.Unchecked)


    # =============================================================================
    # Interface 2 : COURBE
    # =============================================================================
    def getDuration(self, d):
        '''
        retourner la duration de la vidéo
        '''
        self.slider1.setRange(0, d)
        self.slider1.setEnabled(True)
        
        self.displayPlayedTime(self.slider1.maximum()-d)
        self.displayTime(d)
        
    def getPosition(self, p):
        '''
        retourner la poisition de la vidéo
        '''
        self.slider1.setValue(p)
        self.displayPlayedTime(p)
        self.displayTime(self.slider1.maximum()-p)
    
    def displayPlayedTime(self, ms):
        '''
        afficher le temps écoulé
        '''
        minutes = int(ms/60000)
        seconds = int((ms-minutes*60000)/1000)
        self.lab_duration12.setText('\t{}:{}'.format(minutes, seconds))
        
    def displayTime(self, ms):
        '''
        retourner le temps restant de la vidéo
        '''
        minutes = int(ms/60000)
        seconds = int((ms-minutes*60000)/1000)
        self.lab_duration1.setText('- {}:{}'.format(minutes, seconds))
        
    def updatePosition(self, v):
        '''
        mise à jour de la position de la barre de progression
        '''
        self.player1.setPosition(v)
        self.displayPlayedTime(v)
        self.displayTime(self.slider1.maximum()-v)

    def updatePosition_video(self, v):
        '''
        mise à jour de la position de la barre de progression
        '''
        self.player.setPosition(v)
        self.displayPlayedTime(v)
        self.displayTime(self.slider1.maximum()-v)
    
    def win2_PlayPause(self):
        '''
        lecture vidéo et pause
        '''
        if self.start1.isChecked():
            try:
                if self.player1.state()!=1 and self.player.state()!=1:
                    self.player.play()
                    self.player1.play()
            except:
                if self.player.state()!=1:
                    self.player.play()
        else:
            try:
                if self.player1.state()==1 and self.player.state()==1:
                    self.player.pause()
                    self.player1.pause()
            except:
                if self.player.state()==1:
                    self.player.pause()
                
        
    def win2_GenererVideo(self):
        '''
        générer la vidéo selon les données et la vidéo d'entrée
        '''
        if not self.cb21.isChecked() and not self.cb22.isChecked() and not self.cb23.isChecked() and not self.cb24.isChecked():
            QtWidgets.QMessageBox.information(self,'Error Message',"Veuillez d'abord choisir au moins une courbe à ajouter!" )
            self.genVideo1.setChecked(False)
            return
        else:
            self.save_video_name1, filetype = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File Explorer', '', 'Fichier Media (*.avi)')
            if len(self.save_video_name1) == 0:
                print("Cancel choosing...")
                self.genVideo1.setChecked(False)
                return
            
            self.right_label_251.setText("En cours de générer les courbes. Merci d'attendre...")
            self.right_label_251.repaint()
            
            if self.cb21.isChecked() and not self.cb22.isChecked() and not self.cb23.isChecked() and not self.cb24.isChecked():
                self.nb_courbe = 1
                X = [self.can_csv['delta_t'].values]
                Y = [self.can_csv['Odo_distance'].values]
                ## unifier unité temporelle de CAN à 1s
                step1 = 1/0.04
                index1 = [int(i*step1) for i in range(int(len(X[0])/step1))]
                X_new = [X[0][index1]]
                Y_new = [Y[0][index1]]
                fps_output = 7
                ori_video_len = get_video_times(self.video_fileName)
                fps_origin = 30
                fps_courbe = 1
                ## Mise à jour de courbe avec une fréquence de 1 fois par seconde
                l = 10
                interval_ori = 1000/fps_origin # micro-seconde
                interval_courbe = 1000/fps_courbe
                frames_courbe = ori_video_len/interval_courbe*1000 # should be 2018 frames
                X_final, Y_final = padding_XY_can(l, X_new, Y_new, ran=1)
                gather_all_can_video(self.video_fileName, self.save_video_name1, fps_courbe, fps_output, interval_courbe, X_final, Y_final, l, [2])
                #####
                
            elif not self.cb21.isChecked() and self.cb22.isChecked() and not self.cb23.isChecked() and not self.cb24.isChecked():
                self.nb_courbe = 1
                X = [self.can_csv['delta_t'].values]
                Y = [self.can_csv['VehicleSpeed'].values/3.6]
                ## unifier unité temporelle de CAN à 1s
                step1 = 1/0.04
                index1 = [int(i*step1) for i in range(int(len(X[0])/step1))]
                X_new = [X[0][index1]]
                Y_new = [Y[0][index1]]
                fps_output = 7
                ori_video_len = get_video_times(self.video_fileName)
                fps_origin = 30
                fps_courbe = 1
                ## Mise à jour de courbe avec une fréquence de 1 fois par seconde
                l = 10
                interval_ori = 1000/fps_origin
                interval_courbe = 1000/fps_courbe
                frames_courbe = ori_video_len/interval_courbe*1000
                X_final, Y_final = padding_XY_can(l, X_new, Y_new, ran=1)
                gather_all_can_video(self.video_fileName, self.save_video_name1, fps_courbe, fps_output, interval_courbe, X_final, Y_final, l, [0])
                #####
                
            elif not self.cb21.isChecked() and not self.cb22.isChecked() and self.cb23.isChecked() and not self.cb24.isChecked():
                self.nb_courbe = 1
                X = [self.can_csv['delta_t'].values]
                Y = [self.can_csv['acc'].values]
                ## unifier unité temporelle de CAN à 1s
                step1 = 1/0.04
                index1 = [int(i*step1) for i in range(int(len(X[0])/step1))]
                X_new = [X[0][index1]]
                Y_new = [Y[0][index1]]
                fps_output = 7
                ori_video_len = get_video_times(self.video_fileName)
                fps_origin = 30
                fps_courbe = 1
                ## Mise à jour de courbe avec une fréquence de 1 fois par seconde
                l = 10
                interval_ori = 1000/fps_origin
                interval_courbe = 1000/fps_courbe
                frames_courbe = ori_video_len/interval_courbe*1000 
                X_final, Y_final = padding_XY_can(l, X_new, Y_new, ran=1)
                gather_all_can_video(self.video_fileName, self.save_video_name1, fps_courbe, fps_output, interval_courbe, X_final, Y_final, l, [1])
                #####
                
            elif not self.cb21.isChecked() and not self.cb22.isChecked() and not self.cb23.isChecked() and self.cb24.isChecked():
                self.nb_courbe = 1
                X = [self.ci_csv['delta_t'].values]
                Y = [[self.ci_csv['Acceleration_vector_X'].values, self.ci_csv['Acceleration_vector_Y'].values, self.ci_csv['Acceleration_vector_Z'].values]]
                ## unifier unité temporelle de CI à 1s
                step2 = 1/0.01
                index2 = [int(i*step2) for i in range(int(len(X[0])/step2))]
                X_new = [X[0][index2]]
                Y_new = [[Y[0][0][index2], Y[0][1][index2], Y[0][2][index2]]]
                fps_output = 7
                ori_video_len = get_video_times(self.video_fileName)
                fps_origin = 30
                fps_courbe = 1
                ## Mise à jour de courbe avec une fréquence de 1 fois par seconde
                l = 10
                interval_ori = 1000/fps_origin
                interval_courbe = 1000/fps_courbe
                frames_courbe = ori_video_len/interval_courbe*1000
                X_final, Y_final = padding_XY_ci(l, X_new, Y_new)
                gather_ci_video(self.video_fileName, self.save_video_name1, fps_courbe, fps_output, interval_courbe, X_final, Y_final, l)
                #####
                
            elif self.cb21.isChecked() and self.cb22.isChecked() and not self.cb23.isChecked() and not self.cb24.isChecked():
                self.nb_courbe = 2
                X = [self.can_csv['delta_t'].values, self.can_csv['delta_t'].values]
                Y = [self.can_csv['Odo_distance'].values, self.can_csv['VehicleSpeed'].values/3.6]
                ## unifier unité temporelle de CAN à 1s
                step1 = 1/0.04
                index1 = [int(i*step1) for i in range(int(len(X[0])/step1))]
                X_new = [X[0][index1], X[1][index1]]
                Y_new = [Y[0][index1], Y[1][index1]]
                fps_output = 7
                ori_video_len = get_video_times(self.video_fileName)
                fps_origin = 30
                fps_courbe = 1
                ## Mise à jour de courbe avec une fréquence de 1 fois par seconde
                l = 10
                interval_ori = 1000/fps_origin
                interval_courbe = 1000/fps_courbe
                frames_courbe = ori_video_len/interval_courbe*1000 
                X_final, Y_final = padding_XY_can(l, X_new, Y_new, ran=2)
                gather_all_can_video(self.video_fileName, self.save_video_name1, fps_courbe, fps_output, interval_courbe, X_final, Y_final, l, [2,0])
                #####
                
            elif self.cb21.isChecked() and not self.cb22.isChecked() and self.cb23.isChecked() and not self.cb24.isChecked():
                self.nb_courbe = 2
                X = [self.can_csv['delta_t'].values, self.can_csv['delta_t'].values]
                Y = [self.can_csv['Odo_distance'].values, self.can_csv['acc'].values]
                ## unifier unité temporelle de CAN à 1s
                step1 = 1/0.04
                index1 = [int(i*step1) for i in range(int(len(X[0])/step1))]
                X_new = [X[0][index1], X[1][index1]]
                Y_new = [Y[0][index1], Y[1][index1]]
                fps_output = 7
                ori_video_len = get_video_times(self.video_fileName)
                fps_origin = 30
                fps_courbe = 1
                ## Mise à jour de courbe avec une fréquence de 1 fois par seconde
                l = 10
                interval_ori = 1000/fps_origin
                interval_courbe = 1000/fps_courbe
                frames_courbe = ori_video_len/interval_courbe*1000
                X_final, Y_final = padding_XY_can(l, X_new, Y_new, ran=2)
                gather_all_can_video(self.video_fileName, self.save_video_name1, fps_courbe, fps_output, interval_courbe, X_final, Y_final, l, [2,1])
                #####
                
            elif not self.cb21.isChecked() and self.cb22.isChecked() and self.cb23.isChecked() and not self.cb24.isChecked():
                self.nb_courbe = 2
                X = [self.can_csv['delta_t'].values, self.can_csv['delta_t'].values]
                Y = [self.can_csv['VehicleSpeed'].values/3.6, self.can_csv['acc'].values]
                ## unifier unité temporelle de CAN à 1s
                step1 = 1/0.04
                index1 = [int(i*step1) for i in range(int(len(X[0])/step1))]
                X_new = [X[0][index1], X[1][index1]]
                Y_new = [Y[0][index1], Y[1][index1]]
                fps_output = 7
                ori_video_len = get_video_times(self.video_fileName)
                fps_origin = 30
                fps_courbe = 1
                ## Mise à jour de courbe avec une fréquence de 1 fois par seconde
                l = 10
                interval_ori = 1000/fps_origin
                interval_courbe = 1000/fps_courbe
                frames_courbe = ori_video_len/interval_courbe*1000
                X_final, Y_final = padding_XY_can(l, X_new, Y_new, ran=2)
                gather_all_can_video(self.video_fileName, self.save_video_name1, fps_courbe, fps_output, interval_courbe, X_final, Y_final, l, [0,1])
                #####
                
            elif self.cb21.isChecked() and not self.cb22.isChecked() and not self.cb23.isChecked() and self.cb24.isChecked():
                self.nb_courbe = 2
                X = [self.can_csv['delta_t'].values, self.ci_csv['delta_t'].values]
                Y = [self.can_csv['Odo_distance'].values, [self.ci_csv['Acceleration_vector_X'].values, self.ci_csv['Acceleration_vector_Y'].values, self.ci_csv['Acceleration_vector_Z'].values]]
                ## unifier unité temporelle de CAN à 1s
                step1 = 1/0.04
                index1 = [int(i*step1) for i in range(int(len(X[0])/step1))]
                ## unifier unité temporelle de CI à 1s
                step2 = 1/0.01
                index2 = [int(i*step2) for i in range(int(len(X[0])/step2))]
                ## unifier le temps total de CAN et CI 
                diff = len(index1)-len(index2)

                if diff < 0:
                    X_new = [X[0][index1], X[1][index2[:diff]]]
                    Y_new = [Y[0][index1], [Y[1][0][index2[:diff]],Y[1][1][index2[:diff]],Y[1][2][index2[:diff]]]]
                else:
                    diff = -diff
                    X_new = [X[0][index1[:diff]], X[1][index2]]
                    Y_new = [Y[0][index1[:diff]], [Y[1][0][index2],Y[1][1][index2],Y[1][2][index2]]]
                    
                fps_output = 7
                ori_video_len = get_video_times(self.video_fileName)
                fps_origin = 30
                fps_courbe = 1
                ## Mise à jour de courbe avec une fréquence de 1 fois par seconde
                l = 10
                interval_ori = 1000/fps_origin
                interval_courbe = 1000/fps_courbe
                frames_courbe = ori_video_len/interval_courbe*1000
                X_final, Y_final = padding_XY(l, X_new, Y_new, ran=2)
                gather_all_video(self.video_fileName, self.save_video_name1, fps_courbe, fps_output, interval_courbe, X_final, Y_final, l, [2,3])
                #####
            
            elif not self.cb21.isChecked() and self.cb22.isChecked() and not self.cb23.isChecked() and self.cb24.isChecked():
                self.nb_courbe = 2
                X = [self.can_csv['delta_t'].values, self.ci_csv['delta_t'].values]
                Y = [self.can_csv['VehicleSpeed'].values/3.6, [self.ci_csv['Acceleration_vector_X'].values, self.ci_csv['Acceleration_vector_Y'].values, self.ci_csv['Acceleration_vector_Z'].values]]
                ## unifier unité temporelle de CAN à 1s
                step1 = 1/0.04
                index1 = [int(i*step1) for i in range(int(len(X[0])/step1))]
                ## unifier unité temporelle de CI à 1s
                step2 = 1/0.01
                index2 = [int(i*step2) for i in range(int(len(X[0])/step2))]
                ## unifier le temps total de CAN et CI 
                diff = len(index1)-len(index2)
                if diff < 0:
                    X_new = [X[0][index1], X[1][index2[:diff]]]
                    Y_new = [Y[0][index1], [Y[1][0][index2[:diff]],Y[1][1][index2[:diff]],Y[1][2][index2[:diff]]]]
                else:
                    diff = -diff
                    X_new = [X[0][index1[:diff]], X[1][index2]]
                    Y_new = [Y[0][index1[:diff]], [Y[1][0][index2],Y[1][1][index2],Y[1][2][index2]]]
                
                fps_output = 7
                ori_video_len = get_video_times(self.video_fileName)
                fps_origin = 30
                fps_courbe = 1
                ## Mise à jour de courbe avec une fréquence de 1 fois par seconde
                l = 10
                interval_ori = 1000/fps_origin
                interval_courbe = 1000/fps_courbe
                frames_courbe = ori_video_len/interval_courbe*1000
                X_final, Y_final = padding_XY(l, X_new, Y_new, ran=2)
                gather_all_video(self.video_fileName, self.save_video_name1, fps_courbe, fps_output, interval_courbe, X_final, Y_final, l, [0,3])
                #####
            
            elif not self.cb21.isChecked() and not self.cb22.isChecked() and self.cb23.isChecked() and self.cb24.isChecked():
                self.nb_courbe = 2
                X = [self.can_csv['delta_t'].values, self.ci_csv['delta_t'].values]
                Y = [self.can_csv['acc'].values, [self.ci_csv['Acceleration_vector_X'].values, self.ci_csv['Acceleration_vector_Y'].values, self.ci_csv['Acceleration_vector_Z'].values]]
                ## unifier unité temporelle de CAN à 1s
                step1 = 1/0.04
                index1 = [int(i*step1) for i in range(int(len(X[0])/step1))]
                ## unifier unité temporelle de CI à 1s
                step2 = 1/0.01
                index2 = [int(i*step2) for i in range(int(len(X[0])/step2))]
                ## unifier le temps total de CAN et CI 
                diff = len(index1)-len(index2)
                if diff < 0:
                    X_new = [X[0][index1], X[1][index2[:diff]]]
                    Y_new = [Y[0][index1], [Y[1][0][index2[:diff]],Y[1][1][index2[:diff]],Y[1][2][index2[:diff]]]]
                else:
                    diff = -diff
                    X_new = [X[0][index1[:diff]], X[1][index2]]
                    Y_new = [Y[0][index1[:diff]], [Y[1][0][index2],Y[1][1][index2],Y[1][2][index2]]]
                #self.save_video_name1 = 'concate_courbes.avi'
                fps_output = 7
                ori_video_len = get_video_times(self.video_fileName)
                fps_origin = 30
                fps_courbe = 1
                ## Mise à jour de courbe avec une fréquence de 1 fois par seconde
                l = 10
                interval_ori = 1000/fps_origin
                interval_courbe = 1000/fps_courbe
                frames_courbe = ori_video_len/interval_courbe*1000
                X_final, Y_final = padding_XY(l, X_new, Y_new, ran=2)
                gather_all_video(self.video_fileName, self.save_video_name1, fps_courbe, fps_output, interval_courbe, X_final, Y_final, l, [1,3])
                #####
                
            elif self.cb21.isChecked() and self.cb22.isChecked() and self.cb23.isChecked() and not self.cb24.isChecked():
                self.nb_courbe = 3
                X = [self.can_csv['delta_t'].values, self.can_csv['delta_t'].values, self.can_csv['delta_t'].values]
                Y = [self.can_csv['Odo_distance'].values, self.can_csv['VehicleSpeed'].values/3.6, self.can_csv['acc'].values]
                ## unifier unité temporelle de CAN à 1s
                step1 = 1/0.04
                index1 = [int(i*step1) for i in range(int(len(X[0])/step1))]
                X_new = [X[0][index1], X[1][index1], X[2][index1]]
                Y_new = [Y[0][index1], Y[1][index1], Y[2][index1]]
                fps_output = 7
                ori_video_len = get_video_times(self.video_fileName)
                fps_origin = 30
                fps_courbe = 1
                ## Mise à jour de courbe avec une fréquence de 1 fois par seconde
                l = 10
                interval_ori = 1000/fps_origin
                interval_courbe = 1000/fps_courbe
                frames_courbe = ori_video_len/interval_courbe*1000
                X_final, Y_final = padding_XY_can(l, X_new, Y_new, ran=3)
                gather_all_can_video(self.video_fileName, self.save_video_name1, fps_courbe, fps_output, interval_courbe, X_final, Y_final, l, [2,0,1])
            
            elif self.cb21.isChecked() and not self.cb22.isChecked() and self.cb23.isChecked() and self.cb24.isChecked():
                self.nb_courbe = 3
                X = [self.can_csv['delta_t'].values, self.can_csv['delta_t'].values, self.ci_csv['delta_t'].values]
                Y = [self.can_csv['Odo_distance'].values, self.can_csv['acc'].values, [self.ci_csv['Acceleration_vector_X'].values, self.ci_csv['Acceleration_vector_Y'].values, self.ci_csv['Acceleration_vector_Z'].values]]
                ## unifier unité temporelle de CAN à 1s
                step1 = 1/0.04
                index1 = [int(i*step1) for i in range(int(len(X[0])/step1))]
                ## unifier unité temporelle de CI à 1s
                step2 = 1/0.01
                index2 = [int(i*step2) for i in range(int(len(X[0])/step2))]
                ## unifier le temps total de CAN et CI 
                diff = len(index1)-len(index2)
                if diff < 0:
                    X_new = [X[0][index1], X[1][index1], X[2][index2[:diff]]]
                    Y_new = [Y[0][index1], Y[1][index1], [Y[2][0][index2[:diff]],Y[2][1][index2[:diff]],Y[2][2][index2[:diff]]]]
                else:
                    diff = -diff
                    X_new = [X[0][index1[:diff]], X[1][index1[:diff]], X[2][index2]]
                    Y_new = [Y[0][index1[:diff]], Y[1][index1[:diff]], [Y[2][0][index2],Y[2][1][index2],Y[2][2][index2]]]
                fps_output = 7
                ori_video_len = get_video_times(self.video_fileName)
                fps_origin = 30
                fps_courbe = 1
                ## Mise à jour de courbe avec une fréquence de 1 fois par seconde
                l = 10
                interval_ori = 1000/fps_origin
                interval_courbe = 1000/fps_courbe
                frames_courbe = ori_video_len/interval_courbe*1000 
                X_final, Y_final = padding_XY(l, X_new, Y_new, ran=3)
                gather_all_video(self.video_fileName, self.save_video_name1, fps_courbe, fps_output, interval_courbe, X_final, Y_final, l, [2, 1,3])
                #####
                
            elif self.cb21.isChecked() and self.cb22.isChecked() and not self.cb23.isChecked() and self.cb24.isChecked():
                self.nb_courbe = 3
                X = [self.can_csv['delta_t'].values, self.can_csv['delta_t'].values, self.ci_csv['delta_t'].values]
                Y = [self.can_csv['Odo_distance'].values, self.can_csv['VehicleSpeed'].values/3.6, [self.ci_csv['Acceleration_vector_X'].values, self.ci_csv['Acceleration_vector_Y'].values, self.ci_csv['Acceleration_vector_Z'].values]]
                ## unifier unité temporelle de CAN à 1s
                step1 = 1/0.04
                index1 = [int(i*step1) for i in range(int(len(X[0])/step1))]
                ## unifier unité temporelle de CI à 1s
                step2 = 1/0.01
                index2 = [int(i*step2) for i in range(int(len(X[0])/step2))]
                ## unifier le temps total de CAN et CI 
                diff = len(index1)-len(index2)
                
                if diff < 0:
                    X_new = [X[0][index1], X[1][index1], X[2][index2[:diff]]]
                    Y_new = [Y[0][index1], Y[1][index1], [Y[2][0][index2[:diff]],Y[2][1][index2[:diff]],Y[2][2][index2[:diff]]]]
                else:
                    diff = -diff
                    X_new = [X[0][index1[:diff]], X[1][index1[:diff]], X[2][index2]]
                    Y_new = [Y[0][index1[:diff]], Y[1][index1[:diff]], [Y[2][0][index2],Y[2][1][index2],Y[2][2][index2]]]

                fps_output = 7
                ori_video_len = get_video_times(self.video_fileName)
                fps_origin = 30
                fps_courbe = 1
                ## Mise à jour de courbe avec une fréquence de 1 fois par seconde                
                l = 10
                interval_ori = 1000/fps_origin
                interval_courbe = 1000/fps_courbe
                frames_courbe = ori_video_len/interval_courbe*1000
                X_final, Y_final = padding_XY(l, X_new, Y_new, ran=3)
                gather_all_video(self.video_fileName, self.save_video_name1, fps_courbe, fps_output, interval_courbe, X_final, Y_final, l, [2,0,3])
                #####
            
            elif not self.cb21.isChecked() and self.cb22.isChecked() and self.cb23.isChecked() and self.cb24.isChecked():
                self.nb_courbe = 3
                X = [self.can_csv['delta_t'].values, self.can_csv['delta_t'].values, self.ci_csv['delta_t'].values]
                Y = [self.can_csv['VehicleSpeed'].values/3.6, self.can_csv['acc'].values, [self.ci_csv['Acceleration_vector_X'].values, self.ci_csv['Acceleration_vector_Y'].values, self.ci_csv['Acceleration_vector_Z'].values]]
                ## unifier unité temporelle de CAN à 1s
                step1 = 1/0.04
                index1 = [int(i*step1) for i in range(int(len(X[0])/step1))]
                ## unifier unité temporelle de CI à 1s
                step2 = 1/0.01
                index2 = [int(i*step2) for i in range(int(len(X[0])/step2))]
                ## unifier le temps total de CAN et CI 
                diff = len(index1)-len(index2)
                
                if diff < 0:
                    X_new = [X[0][index1], X[1][index1], X[2][index2[:diff]]]
                    Y_new = [Y[0][index1], Y[1][index1], [Y[2][0][index2[:diff]],Y[2][1][index2[:diff]],Y[2][2][index2[:diff]]]]
                else:
                    diff = -diff
                    X_new = [X[0][index1[:diff]], X[1][index1[:diff]], X[2][index2]]
                    Y_new = [Y[0][index1[:diff]], Y[1][index1[:diff]], [Y[2][0][index2],Y[2][1][index2],Y[2][2][index2]]]
                    
                fps_output = 7
                ori_video_len = get_video_times(self.video_fileName)
                fps_origin = 30
                fps_courbe = 1
                ## Mise à jour de courbe avec une fréquence de 1 fois par seconde
                l = 10
                interval_ori = 1000/fps_origin
                interval_courbe = 1000/fps_courbe
                frames_courbe = ori_video_len/interval_courbe*1000
                X_final, Y_final = padding_XY(l, X_new, Y_new, ran=3)
                gather_all_video(self.video_fileName, self.save_video_name1, fps_courbe, fps_output, interval_courbe, X_final, Y_final, l, [0,1,3])
                #####
            
            if self.nb_courbe == 1:
                # Widget pour afficher
                self.player1 = QMediaPlayer()
                self.play_video1 = QVideoWidget()
                self.play_video1.setFixedWidth(int(self.screen.width()*0.24))
                self.play_video1.setFixedHeight(int(self.screen.width()*0.2))
                
            elif self.nb_courbe == 2:
                # Widget pour afficher
                self.player1 = QMediaPlayer()
                self.play_video1 = QVideoWidget()
                self.play_video1.setFixedWidth(int(self.screen.width()*0.26))
                self.play_video1.setFixedHeight(int(self.screen.width()*0.3))
            
            elif self.nb_courbe == 3:
                # Widget pour afficher
                self.player1 = QMediaPlayer()
                self.play_video1 = QVideoWidget()
                self.play_video1.setFixedWidth(int(self.screen.width()*0.26))
                self.play_video1.setFixedHeight(int(self.screen.width()*0.3))
            
            self.playlist_courbes = QMediaPlaylist()
            # Widget pour exporter
            self.player1.setVideoOutput(self.play_video1)
            self.playlist_courbes.addMedia(QMediaContent(QUrl.fromLocalFile(self.save_video_name1)))
            self.player1.setPlaylist(self.playlist_courbes)
            # Interactions
            self.right_label_251.setText("Les courbes sont faites. Cliquez pour regarder les vidéos.")
            self.right_label_251.repaint()
            self.player1.durationChanged.connect(self.getDuration)
            self.player1.positionChanged.connect(self.getPosition)
            self.slider1.sliderMoved.connect(self.updatePosition)
            self.right_layout25.addWidget(self.play_video1,1,8)
    
    def win2_combineAvi(self):
        '''
        merger les vidéos
        '''
        fps_output = 7
        self.right_label_251.setText("En cour de combiner deux vidéos... ça prend du temps, n'hésitez pas à prendre un café !")
        self.right_label_251.repaint()

        self.save_video_name12, filetype = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File Explorer', '', 'Fichier Media (*.mp4)')
        if len(self.save_video_name12) == 0:
            print("Cancel choosing...")
            self.right_label_251.setText("")
            self.export1.setChecked(False)
            return
        else:
            combine_all_avi(self.video_fileName, self.save_video_name12, fps_output, self.save_video_name1)
            self.right_label_251.setText(self.save_video_name12+" est bien enregistré.")
    
    def win2_refreshCourbes(self):
        '''
        mise à jour des courbes
        '''
        reply = QMessageBox.question(self, 'Message', "Voulez vous refaire les courbes ?",  QMessageBox.Yes,  QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.genVideo1.setChecked(False)
            self.cb21.setChecked(False)
            self.cb22.setChecked(False)
            self.cb23.setChecked(False)
            self.cb24.setChecked(False)
            
            self.save_video_name1 = ""
            self.right_label_251.setText("Veillez choisir les nouvelles courbes.")
            self.playlist_courbes.clear()
            self.player.stop()
            self.refresh1.setChecked(False)
            self.play_video.setStyleSheet("background-color: white")
            
    def win2_fileVideoIn(self):
        '''
        mise à jour des courbes
        '''
        self.video_fileName, filetype = QtWidgets.QFileDialog.getOpenFileName(self, 'File Explorer', '', 'Fichier Media (*.mp4;*.avi)')
        if len(self.video_fileName) == 0:
            print("Cancel choosing...")
            self.video_btn.setChecked(False)
            return
        else:
            print('le chemin du csv courrant:' + self.video_fileName)
            self.player = QMediaPlayer()
            # Widget pour afficher
            self.play_video = QVideoWidget()
            self.play_video.setFixedWidth(int(self.screen.width()*0.32))
            self.play_video.setFixedHeight(int(self.screen.width()*0.28))
            # Widget pour exporter
            self.player.setVideoOutput(self.play_video) 
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(self.video_fileName)))
            # Interactions
            self.play_video.setStyleSheet("background-color: black;")
            self.player.durationChanged.connect(self.getDuration)
            self.player.positionChanged.connect(self.getPosition)
            self.slider1.sliderMoved.connect(self.updatePosition_video)
            self.right_layout25.addWidget(self.play_video,1,0)
            
            
    # =============================================================================
    # Interface 1 : ANALYSE
    # =============================================================================
    def win1_fileGPSIn(self):
        '''
        lecture de fichier GPS
        '''
        self.gps_fileName, filetype = QtWidgets.QFileDialog.getOpenFileName(self, 'File Explorer', '', 'Fichier CSV (*.csv)')
        if len(self.gps_fileName) == 0:
            print("Cancel choosing...")
            self.gps_btn.setChecked(False)
            return
        else:
            print('le chemin du csv courrant:' + self.gps_fileName)
            self.gps_csv = pd.read_csv(self.gps_fileName, sep=';')
            timestamp_init = split_time_eu(self.gps_csv['timestamp'][0])
            self.gps_csv['delta_t'] = self.gps_csv['timestamp'].apply(lambda x: time_diff(timestamp_init, split_time_eu(x)))
            self.gps_csv = temps_consecu(self.gps_csv)
            self.gps_duree = round(time_diff(split_time_eu(self.gps_csv['timestamp'].values[0]), split_time_eu(self.gps_csv['timestamp'].values[-1])))
            text = "\n\t"+self.gps_csv['timestamp'].values[0][:10]+'\t'+self.gps_csv['timestamp'].values[0][11:19]+' - '+self.gps_csv['timestamp'].values[-1][11:19]+'\t'+ str(self.gps_duree) + ' s'
            self.right_label_131.setText(text)
            # 3. GPS ## 
            self.gps_csv = gps_distance(self.gps_csv)
            # 2. GPS: v ## 
            self.gps_csv = gps_distance(self.gps_csv)
            self.gps_csv = calcul_vit(self.gps_csv)
            
    def win1_fileCIIn(self):
        '''
        lecture de fichier CI
        '''
        self.ci_fileName, filetype = QtWidgets.QFileDialog.getOpenFileName(self, 'File Explorer', '', 'Fichier CSV (*.csv)')
        if len(self.ci_fileName) == 0:
            print("Cancel choosing...")
            self.ci_btn.setChecked(False)
            return
        else:
            print('le chemin du csv courrant:' + self.ci_fileName)
            self.ci_csv = pd.read_csv(self.ci_fileName, sep=';')
            timestamp_init = split_time_eu(self.ci_csv['timestamp'][0])
            self.ci_csv['delta_t'] = self.ci_csv['timestamp'].apply(lambda x: time_diff(timestamp_init, split_time_eu(x)))
            self.ci_csv = temps_consecu(self.ci_csv)
            self.ci_duree = round(time_diff(split_time_eu(self.ci_csv['timestamp'].values[0]), split_time_eu(self.ci_csv['timestamp'].values[-1])))
            text = "\n\t"+self.ci_csv['timestamp'].values[0][:10]+'\t'+self.ci_csv['timestamp'].values[0][11:19]+' - '+self.ci_csv['timestamp'].values[-1][11:19]+'\t'+ str(self.ci_duree) + ' s'
            self.right_label_132.setText(text)
            
    def win1_fileCANIn(self):
        '''
        lecture de fichier CAN
        '''
        self.can_fileName, filetype = QtWidgets.QFileDialog.getOpenFileName(self, 'File Explorer', '', 'Fichier CSV (*.csv)')
        if len(self.can_fileName) == 0:
            print("Cancel choosing...")
            self.bus_btn.setChecked(False)
            return
        else:
            print('le chemin du csv courrant:' + self.can_fileName)
            self.can_csv = pd.read_csv(self.can_fileName, sep=';')
            timestamp_init = split_time_eu(self.can_csv['timestamp'][0])
            self.can_csv['delta_t'] = self.can_csv['timestamp'].apply(lambda x: time_diff(timestamp_init, split_time_eu(x)))
            self.can_csv = temps_consecu(self.can_csv)
            self.can_duree = round(time_diff(split_time_eu(self.can_csv['timestamp'].values[0]), split_time_eu(self.can_csv['timestamp'].values[-1])))
            text = "\n\t"+self.can_csv['timestamp'].values[0][:10]+'\t'+self.can_csv['timestamp'].values[0][11:19]+' - '+self.can_csv['timestamp'].values[-1][11:19]+'\t'+ str(self.can_duree) + ' s'
            self.right_label_133.setText(text)
            ## 1.odomètre dans CAN ##
            self.can_csv = traiter_odo(self.can_csv) 
            ## 2.can_csv: S = v*t ##
            vitesses = self.can_csv['VehicleSpeed']/(3.6*1000) #from km/h to km/s
            intervals_consecu = self.can_csv['delta_t_consecu']
            trajets = np.array(vitesses*intervals_consecu)
            self.can_csv['Distance'] = trajets
            ## 3.can_csv:acc ##
            self.can_csv = calcul_acc(self.can_csv)
            
    def analyse_go(self):
        if self.cb11.isChecked():
            if self.can_fileName != "" and self.gps_fileName != "":
                # ## 1.odomètre dans CAN ##
                # self.can_csv = traiter_odo(self.can_csv) 
                # ## 2.can_csv: S = v*t ##
                # vitesses = self.can_csv['VehicleSpeed']/(3.6*1000) #from km/h to km/s
                # intervals_consecu = self.can_csv['delta_t_consecu']
                # trajets = np.array(vitesses*intervals_consecu)
                # self.can_csv['Distance'] = trajets
                # # 3. GPS ## 
                # self.gps_csv = gps_distance(self.gps_csv)
                
                hour1 = self.can_csv['delta_t']
                temperature1 = self.can_csv['Odo_distance']
                hour2 = hour1
                temperature2 = np.cumsum(self.can_csv['Distance'])
                hour3 = self.gps_csv['delta_t']
                temperature3 = np.cumsum(self.gps_csv['Distance'])
                self.graphWidget.setTitle("Distance", color="#808080", size="16pt")
                styles = {'color':'#A9A9A9', 'font-size':'17px'}
                self.graphWidget.setLabel('left', 'Distance (km)', **styles)
                self.graphWidget.setLabel('bottom', 'Temps (s)\n\n\n', **styles)
                pen1 = pg.mkPen(color=(255,228,181),width=5)
                pen2 = pg.mkPen(color=(144,238,144),width=5)
                pen3 = pg.mkPen(color=(173,216,230),width=5)
                self.graphWidget.plot(hour1, temperature1, pen=pen1, name = "CAN-ODO")
                self.graphWidget.plot(hour2, temperature2, pen=pen2, name = "CAN-v*t")
                self.graphWidget.plot(hour3, temperature3, pen=pen3, name = "GPS-lat/lon")
            else:
                QtWidgets.QMessageBox.information(self,'Error Message',"Veuillez importer au moins le fichier de GPS et de CAN !" )
                self.bt11.setChecked(False)
                self.cb12.setChecked(False)
                self.cb11.setChecked(False)
                
        elif self.cb12.isChecked():
            ## 1.can_csv: v ##
            hour1 = self.can_csv['delta_t']
            temperature1 = self.can_csv['VehicleSpeed']
            # 2. GPS: v ## 
            # self.gps_csv = gps_distance(self.gps_csv)
            # self.gps_csv = calcul_vit(self.gps_csv)
            # hour2 = self.gps_csv['delta_t']
            # temperature2 = self.gps_csv['Vitesse']
            hour2 = self.can_csv['delta_t']
            temperature2 = self.can_csv['Displayed_Speed']
            self.graphWidget.setTitle("Vitesse", color="#808080", size="16pt")
            styles = {'color':'#A9A9A9', 'font-size':'17px'}
            self.graphWidget.setLabel('left', 'Vitesse (km/h)', **styles)
            self.graphWidget.setLabel('bottom', 'Temps (s)\n\n\n', **styles)
            pen1 = pg.mkPen(color=(255,228,181),width=5)
            pen2 = pg.mkPen(color=(144,238,144),width=5)
            self.graphWidget.plot(hour1, temperature1, pen=pen1, name = "CAN-vitesse")
            self.graphWidget.plot(hour2, temperature2, pen=pen2, name = "GPS-vitesse")

        elif self.cb13.isChecked():
            self.graphWidget.clear()
            QtWidgets.QMessageBox.information(self,'Error Message',"Veuillez d'abord choisir soit la distance soit la vitesse!" )
        else:
            QtWidgets.QMessageBox.information(self,'Error Message',"Veuillez d'abord choisir soit la distance soit la vitesse!" )
            self.bt11.setChecked(False)
            
    def changecb1(self):
        if self.cb13.checkState() == QtCore.Qt.Checked:
            self.cb12.setChecked(False)
            self.cb11.setChecked(False)
            self.bt11.setChecked(False)
            self.graphWidget.clear()
        
    def changecb2(self):
        if self.cb12.isChecked() and self.cb11.isChecked() :
            QtWidgets.QMessageBox.information(self,'Error Message','Vous ne pouvez pas générer la distance et la vitesse en même temps!')
            self.cb13.setCheckState(QtCore.Qt.Unchecked)
            self.cb11.setCheckState(QtCore.Qt.Unchecked)
            self.cb12.setCheckState(QtCore.Qt.Unchecked)
        elif self.cb12.isChecked():
            self.cb11.setCheckState(QtCore.Qt.Unchecked)
            self.cb13.setCheckState(QtCore.Qt.Unchecked)
        elif self.cb11.isChecked():
            self.cb12.setCheckState(QtCore.Qt.Unchecked)
            self.cb13.setCheckState(QtCore.Qt.Unchecked)


    def init_ui(self):
        self.screen = QtWidgets.QDesktopWidget().screenGeometry()
        self.gps_fileName = ""
        self.ci_fileName = ""
        self.can_fileName = ""
        self.lidar_fileName = ""
        self.remission_fileName = ""
        
        self.video_fileName = "" # nom dela vidéo d'interface 2
        self.save_video_name1 = "" # nom dela vidéo sauvegardé d'interface 2
        self.save_video_name12 = "" # nom dela vidéo mergé d'interface 2
        self.video_fileName3 = "" # nom dela vidéo d'interface 1
        
        self.gps_duree = 0
        self.ci_duree = 0
        self.can_duree = 0
        self.video_duree = 0
        
        # changer flexiblement de la hauteur des boutons
        self.buttonheight = int(self.screen.height()/25)
        self.buttonwidth = int(self.screen.width()*0.05)
        
        
        # =============================================================================
        # Déclaration de la disposition
        # =============================================================================
        # Widget Principal
        self.main_widget = QtWidgets.QWidget()  # créer le widget principal
        self.main_layout = QtWidgets.QGridLayout()  # une disposition en grille du widget principal
        self.main_widget.setLayout(self.main_layout)  # définir la disposition du widget principal de la fenêtre sur la disposition en grille
        self.main_layout.setSpacing(0)
        # Widget à gauche
        self.left_widget = QtWidgets.QWidget()  
        self.left_widget.setObjectName('left_widget')
        self.left_layout = QtWidgets.QGridLayout()
        self.left_widget.setLayout(self.left_layout)  
        # Widget en haut à gauche
        self.left_widget1 = QtWidgets.QWidget()
        self.left_widget1.setObjectName('left_widget1')
        self.left_layout1 = QtWidgets.QGridLayout()
        self.left_widget1.setLayout(self.left_layout1)  
        # Widget au milieu gauche
        self.left_widget2 = QtWidgets.QWidget()
        self.left_widget2.setObjectName('left_widget2')
        self.left_layout2 = QtWidgets.QGridLayout()
        self.left_widget2.setLayout(self.left_layout2)  
        # Widget en bas à gauche
        self.left_widget3 = QtWidgets.QWidget() 
        self.left_widget3.setObjectName('left_widget3')
        self.left_layout3 = QtWidgets.QGridLayout()
        self.left_widget3.setLayout(self.left_layout3)  
        
        
        # =============================================================================
        # Configurer la disposition
        # =============================================================================
        # Widget en bas à droite
        self.right_widget = QtWidgets.QWidget()
        self.right_widget.setObjectName('right_widget')
        self.right_layout = QtWidgets.QGridLayout()
        # configurer la disposition de la grille
        self.right_widget.setLayout(self.right_layout)
        self.right_widget.setFixedWidth(int(self.screen.width()*0.77))
        self.right_widget.setFixedHeight(int(self.screen.height()))
        # Widgets à gauche
        self.left_layout.addWidget(self.left_widget1,0,0,3,3) # rang 0 col 0, taille 3 * 3
        self.left_layout.addWidget(self.left_widget2,3,0,6,3) # rang 3 col 0, taille 6 * 3
        self.left_layout.addWidget(self.left_widget3,9,0,2,3) # rang 9 col 0, taille 2 * 3
        # Widgets principaux
        self.main_layout.addWidget(self.left_widget,0,0,24,3) # taille 24 * 3
        self.main_layout.addWidget(self.right_widget,1,3,24,9) # taille 24 * 9
        self.setCentralWidget(self.main_widget)

        self.left_layout.setVerticalSpacing(0);
        self.left_layout.setSpacing(0)
        self.left_layout2.setSpacing(0)
        self.left_layout3.setSpacing(0)
        self.left_out = QtWidgets.QPushButton(qtawesome.icon('fa.sign-out',color='#ffffff'),"Exit")
        self.left_out.setObjectName('left_out')
        self.left_out.clicked.connect(self.close) # button pour quitter

        # lignes d'information
        self.left_username = QtWidgets.QLabel("PROFIL Vers 1.0")
        self.left_username.setObjectName('username')

        # boutons dans la barre de menu de gauche
        self.left_button_1 = QtWidgets.QToolButton()
        self.left_button_1.setText("   A N A L Y S E") # définir le texte du bouton
        self.left_button_1.setIcon(qtawesome.icon('fa.bar-chart',color='#2c3a45')) # définir l'icône du bouton
        self.left_button_1.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.left_button_1.setCheckable(True)
        self.left_button_1.clicked.connect(self.click_window1)
        self.left_button_1.setAutoRaise(True)
        
        self.left_button_2 = QtWidgets.QToolButton()
        self.left_button_2.setText("   C O U R B E") # définir le texte du bouton
        self.left_button_2.setIcon(qtawesome.icon('fa.tags',color='#2c3a45')) # définir l'icône du bouton
        self.left_button_2.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.left_button_2.setCheckable(True)
        self.left_button_2.clicked.connect(self.click_window2)
        self.left_button_2.setAutoRaise(True)
        
        self.left_button_3 = QtWidgets.QToolButton()
        self.left_button_3.setText( "   S I M U L A T I O N") # définir le texte du bouton
        self.left_button_3.setIcon(qtawesome.icon('fa.globe',color='#2c3a45')) # définir l'icône du bouton
        self.left_button_3.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.left_button_3.setCheckable(True)
        self.left_button_3.clicked.connect(self.click_window3)
        self.left_button_3.setAutoRaise(True)
        
        self.left_button_4 = QtWidgets.QToolButton()
        self.left_button_4.setText("   D E T E C T I O N") # définir le texte du bouton
        self.left_button_4.setIcon(qtawesome.icon('fa.car',color='#2c3a45')) # définir l'icône du bouton
        self.left_button_4.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.left_button_4.setCheckable(True)
        self.left_button_4.clicked.connect(self.click_window4)
        self.left_button_4.setAutoRaise(True)
        
        self.left_button_5 = QtWidgets.QToolButton()
        self.left_button_5.setText("   A I D E") # définir le texte du bouton
        self.left_button_5.setIcon(qtawesome.icon('fa.search',color='#2c3a45')) # définir l'icône du bouton
        self.left_button_5.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.left_button_5.setCheckable(True)
        self.left_button_5.clicked.connect(self.click_window5)
        self.left_button_5.setAutoRaise(True)
        
        # groupes de bouton
        self.btn_group = QtWidgets.QButtonGroup(self.left_widget)
        self.btn_group.addButton(self.left_button_1, 1)
        self.btn_group.addButton(self.left_button_2, 2)
        self.btn_group.addButton(self.left_button_3, 3)
        self.btn_group.addButton(self.left_button_4, 4)
        self.btn_group.addButton(self.left_button_5, 5)

        # icône
        pix = QtGui.QPixmap('.\\logo-3.png')
        re_pix = pix.scaled(int(self.screen.width()/5), int(self.screen.height()/5), QtCore.Qt.KeepAspectRatio)
        self.left_img_1 = QtWidgets.QLabel()
        self.left_img_1.setPixmap(re_pix)
        self.left_img_1.setObjectName('left_img')
        self.left_img_1.setFixedHeight(int(self.screen.height()/4))
        
        # disposition stackée
        self.stacked_layout = QtWidgets.QStackedLayout(self.main_widget)

                
        # =============================================================================
        # la disposition de l'interface initiale
        # =============================================================================
        self.right_widget0 = QtWidgets.QWidget()
        self.right_widget0.setObjectName('right_widget0')
        self.right_layout0 = QtWidgets.QGridLayout()
        self.right_widget0.setLayout(self.right_layout0)
        self.right_widget0.setFixedWidth(int(self.screen.width()*0.8))
        self.right_widget0.setFixedHeight(int(self.screen.height()*0.9))
        
        
        self.right_label_0 = QtWidgets.QLabel()
        pix0 = QtGui.QPixmap('.\\fenetre0.png')
        re_pix0 = pix0.scaled(int(self.screen.width()*0.8), int(self.screen.height()), QtCore.Qt.KeepAspectRatio)
        self.right_label_0.setPixmap(re_pix0)
        self.right_label_0.setObjectName('right_labe0')
        self.right_label_0.setFixedWidth(int(self.screen.width()*0.7))
        self.right_label_0.setFixedHeight(int(self.screen.height()*0.9))
        self.right_layout0.addWidget(self.right_label_0,0,0)
        
                
        # =============================================================================
        # la disposition de l'interface 1 : ANALYSE
        # =============================================================================
        # widgets à droite
        self.right_widget1 = QtWidgets.QWidget()
        self.right_widget1.setObjectName('right_widget1')
        self.right_layout1 = QtWidgets.QGridLayout()
        self.right_widget1.setLayout(self.right_layout1)
        self.right_widget1.setFixedWidth(int(self.screen.width()/3*2))
        self.right_widget1.setFixedHeight(int(self.screen.height()*0.93))
        # titre à droite
        self.right_widget11 = QtWidgets.QWidget()  
        self.right_widget11.setObjectName('right_widget11')
        self.right_layout11 = QtWidgets.QGridLayout()
        self.right_widget11.setLayout(self.right_layout11)
        self.right_label_11 = QtWidgets.QLabel("A N A L Y S E R    C S V")
        self.right_label_11.setObjectName('right_label11')
        # séléction de fichier à droite
        self.right_widget12 = QtWidgets.QWidget()
        self.right_widget12.setObjectName('right_widget12')
        self.right_layout12 = QtWidgets.QGridLayout()
        self.right_widget12.setLayout(self.right_layout12)

        # Button de GPS
        self.gps_btn = QtWidgets.QPushButton(qtawesome.icon('fa.file-text',color='#A9A9A9'),"GPS Fichier")
        self.gps_btn.setObjectName('gps')
        self.gps_btn.setCheckable(True)
        self.gps_btn.clicked.connect(self.win1_fileGPSIn)
        # Button de CI
        self.ci_btn = QtWidgets.QPushButton(qtawesome.icon('fa.file-text',color='#A9A9A9'),"CI Fichier")
        self.ci_btn.setObjectName('ci')
        self.ci_btn.setCheckable(True)
        self.ci_btn.clicked.connect(self.win1_fileCIIn)
        # Button de BUS CAN
        self.bus_btn = QtWidgets.QPushButton(qtawesome.icon('fa.file-text',color='#A9A9A9'),"CAN BUS Fichier")
        self.bus_btn.setObjectName('can')
        self.bus_btn.setCheckable(True)
        self.bus_btn.clicked.connect(self.win1_fileCANIn)
        
        # résultats affiché à droite
        self.right_widget13 = QtWidgets.QWidget()
        self.right_widget13.setObjectName('right_widget13')
        self.right_layout13 = QtWidgets.QGridLayout()
        self.right_widget13.setLayout(self.right_layout13)
        self.right_label_13 = QtWidgets.QLabel()
        self.right_label_13.setObjectName('right_label13')
        pix2 = QtGui.QPixmap('.\\CONT1.png')
        self.right_label_13.setPixmap(pix2)
        self.right_label_13.setScaledContents(True)
        self.right_label_131 = QtWidgets.QLabel("\n \t No file imported...")
        self.right_label_131.setObjectName('right_label131')
        self.right_label_132 = QtWidgets.QLabel("\n \t No file imported...")
        self.right_label_132.setObjectName('right_label132')
        self.right_label_133 = QtWidgets.QLabel("\n \t No file imported...")
        self.right_label_133.setObjectName('right_label133')
        self.right_label_131.setStyleSheet("text-align:centre;font-size:20px;font-family:'Calibri';color:#808080")
        self.right_label_132.setStyleSheet("text-align:centre;font-size:20px;font-family:'Calibri';color:#808080")
        self.right_label_133.setStyleSheet("text-align:centre;font-size:20px;font-family:'Calibri';color:#808080")
        
        # le checkbox à droite
        self.right_widget14 = QtWidgets.QWidget()
        self.right_widget14.setObjectName('right_widget14')
        self.right_layout14 = QtWidgets.QGridLayout()
        self.right_widget14.setLayout(self.right_layout14)
        self.cb11 = QtWidgets.QCheckBox('Distance',self)
        self.cb11.setObjectName('checkbox11')
        self.cb12 = QtWidgets.QCheckBox('Vitesse',self)
        self.cb12.setObjectName('checkbox12')
        self.cb13 = QtWidgets.QCheckBox('Clear',self)
        self.cb13.setObjectName('checkbox13')
        
        # les buttons
        self.bt11 = QtWidgets.QPushButton('Analyser les données',self) 
        self.bt11.setObjectName('bt11')
        self.cb11.stateChanged.connect(self.changecb2)
        self.cb12.stateChanged.connect(self.changecb2)
        self.cb13.stateChanged.connect(self.changecb1)
        self.bt11.clicked.connect(self.analyse_go)
        self.bt11.setCheckable(True)
        
        # le graph à droite
        self.right_widget15 = QtWidgets.QWidget()  
        self.right_widget15.setObjectName('right_widget15')
        self.right_layout15 = QtWidgets.QGridLayout()
        self.right_widget15.setLayout(self.right_layout15)
        self.right_label_15 = QtWidgets.QLabel()
        self.right_label_15.setObjectName('right_label15')
        self.graphWidget = pg.PlotWidget()
        self.graphWidget.setBackground('#fafafa')
        self.graphWidget.showGrid(x=True, y=True)
        self.graphWidget.addLegend()
        
        # la disposition à droite
        self.right_layout11.addWidget(self.right_label_11,1,0,3,8)
        self.right_layout12.addWidget(self.gps_btn,0,1,2,2)
        self.right_layout12.addWidget(self.ci_btn,0,4,2,2)
        self.right_layout12.addWidget(self.bus_btn,0,7,2,2)
        self.right_layout12.setSpacing(15)
        self.right_layout13.addWidget(self.right_label_13,0,0,7,9)
        self.right_layout13.addWidget(self.right_label_131,0,2,2,7)
        self.right_layout13.addWidget(self.right_label_132,2,2,2,7)
        self.right_layout13.addWidget(self.right_label_133,4,2,2,7)
        self.right_layout14.addWidget(self.cb11,0,0,1,1)
        self.right_layout14.addWidget(self.cb12,0,1,1,1)
        self.right_layout14.addWidget(self.cb13,0,2,1,1)
        self.right_layout14.addWidget(self.bt11,0,3,1,1)
        self.right_layout14.setSpacing(15)
        self.right_layout15.addWidget(self.graphWidget,0,0)
        self.right_layout1.addWidget(self.right_widget11,1,0,3,9)
        self.right_layout1.addWidget(self.right_widget12,4,2,1,9)
        self.right_layout1.addWidget(self.right_widget13,6,2,3,9) 
        self.right_layout1.addWidget(self.right_widget14,9,2,3,9) 
        self.right_layout1.addWidget(self.right_widget15,12,2,10,9) 
        
                
        # =============================================================================
        # la disposition de l'interface 2 : COURBE
        # =============================================================================
        # la partie texte et graph à droite
        self.right_widget2 = QtWidgets.QWidget()
        self.right_widget2.setObjectName('right_widget2')
        self.right_layout2 = QtWidgets.QGridLayout()
        self.right_widget2.setLayout(self.right_layout2)
        self.right_widget2.setFixedWidth(int(self.screen.width()/3*2))
        self.right_widget2.setFixedHeight(int(self.screen.height()*0.93))
        # le titre et graph à droite
        self.right_widget21 = QtWidgets.QWidget()  
        self.right_widget21.setObjectName('right_widget21')
        self.right_layout21 = QtWidgets.QGridLayout()
        self.right_widget21.setLayout(self.right_layout21)
        self.right_label_21 = QtWidgets.QLabel("G E N E R E R   D E S   C O U R B E S")
        self.right_label_21.setObjectName('right_label21')
        # la lecture de fichier à droite
        self.right_widget22 = QtWidgets.QWidget()
        self.right_widget22.setObjectName('right_widget22')
        self.right_layout22 = QtWidgets.QGridLayout()
        self.right_widget22.setLayout(self.right_layout22)
        # le button pour vidéo
        self.video_btn = QtWidgets.QPushButton(qtawesome.icon('fa.video-camera',color='#A9A9A9'),"\tChoisir Vidéo")
        self.video_btn.setObjectName('video')
        self.video_btn.setCheckable(True)
        self.video_btn.clicked.connect(self.win2_fileVideoIn)
        # le button pour commencer à générer la vidéo
        self.genVideo1 = QtWidgets.QPushButton(qtawesome.icon('fa.plus-square',color='#A9A9A9'),"\tGénérer Courbes")
        self.genVideo1.setObjectName('genVideo1')
        self.genVideo1.setCheckable(True)
        self.genVideo1.clicked.connect(self.win2_GenererVideo)
        # l'afficahge de résultat à droite
        self.right_widget23 = QtWidgets.QWidget()
        self.right_widget23.setObjectName('right_widget23')
        self.right_layout23 = QtWidgets.QGridLayout()
        self.right_widget23.setLayout(self.right_layout23)
        self.right_label_23 = QtWidgets.QLabel()
        self.cb21 = QtWidgets.QCheckBox('Distance',self)
        self.cb21.setObjectName('checkbox21')
        self.cb22 = QtWidgets.QCheckBox('Vitesse',self)
        self.cb22.setObjectName('checkbox22')
        self.cb23 = QtWidgets.QCheckBox('Accélération',self)
        self.cb23.setObjectName('checkbox23')
        self.cb24 = QtWidgets.QCheckBox('Acc Latérale',self)
        self.cb24.setObjectName('checkbox24')
        # le joueur à droite
        self.right_widget24 = QtWidgets.QWidget()
        self.right_widget24.setObjectName('right_widget24')
        self.right_layout24 = QtWidgets.QGridLayout()
        self.right_widget24.setLayout(self.right_layout24)
        
        # le button 'start'
        self.start1 = QtWidgets.QPushButton(qtawesome.icon('fa.play',color='#A9A9A9'),"")
        self.start1.setObjectName('start1')
        self.start1.setCheckable(True)
        self.start1.clicked.connect(self.win2_PlayPause)
        # le button 'refresh'        
        self.refresh1 = QtWidgets.QPushButton(qtawesome.icon('fa.refresh',color='#A9A9A9'),"")
        self.refresh1.setObjectName('refresh1')
        self.refresh1.setCheckable(True)
        self.refresh1.clicked.connect(self.win2_refreshCourbes)
        # le button 'export'
        self.export1 = QtWidgets.QPushButton(qtawesome.icon('fa.download',color='#A9A9A9'),"")
        self.export1.setObjectName('export1')
        self.export1.setCheckable(True)
        self.export1.clicked.connect(self.win2_combineAvi)
        # l'info de duration
        self.lab_duration12 = QtWidgets.QLabel("\t00 : 00")
        self.slider1 = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.lab_duration1 = QtWidgets.QLabel("-- : --")
        # l'affichage de vidéo à droite
        self.right_widget25 = QtWidgets.QWidget()
        self.right_widget25.setObjectName('right_widget25')
        self.right_layout25 = QtWidgets.QGridLayout()
        self.right_widget25.setLayout(self.right_layout25)
        self.right_label_25 = QtWidgets.QLabel()
        self.right_label_25.setObjectName('right_label25')
        self.right_label_251 = QtWidgets.QLabel()
        
        # ranger et activer les layout
        self.right_layout21.addWidget(self.right_label_21,1,0,3,8)
        self.right_layout22.addWidget(self.video_btn,0,1,2,2)
        self.right_layout22.addWidget(self.genVideo1,0,7,2,2)
        self.right_layout22.setSpacing(25)
        # 
        self.right_layout23.addWidget(self.cb21,0,0,1,1)
        self.right_layout23.addWidget(self.cb22,0,1,1,1)
        self.right_layout23.addWidget(self.cb23,0,2,1,1)
        self.right_layout23.addWidget(self.cb24,0,3,1,1)
        self.right_layout23.setSpacing(15)
        # 
        self.right_layout24.addWidget(self.lab_duration12,0,0,1,1)
        self.right_layout24.addWidget(self.slider1,0,1,1,9)
        self.right_layout24.addWidget(self.lab_duration1,0,10,1,1)
        self.right_layout24.addWidget(self.start1,0,11,1,1)
        self.right_layout24.addWidget(self.refresh1,0,12,1,1)
        self.right_layout24.addWidget(self.export1,0,13,1,1)
        self.right_layout24.addWidget(self.right_label_251,3,4,1,9)
        self.right_layout24.setSpacing(15)
        # 
        self.right_layout25.addWidget(self.right_label_25,3,0,3,9)
        # 
        self.right_layout2.addWidget(self.right_widget21,1,0,2,9)
        self.right_layout2.addWidget(self.right_widget23,4,1,1,9)
        self.right_layout2.addWidget(self.right_widget22,6,1,2,9)
        self.right_layout2.addWidget(self.right_widget25,9,1,10,9)
        self.right_layout2.addWidget(self.right_widget24,22,1,1,9)
                

        # =============================================================================
        # la disposition de l'interface 3 : SIMULATION
        # =============================================================================
        self.right_widget3 = QtWidgets.QWidget()
        self.right_widget3.setObjectName('right_widget3')
        self.right_layout3 = QtWidgets.QGridLayout()
        self.right_widget3.setLayout(self.right_layout3)
        self.right_widget3.setFixedWidth(int(self.screen.width()/3*2))
        self.right_widget3.setFixedHeight(int(self.screen.height()*0.93))
        # le titre à droite
        self.right_widget31 = QtWidgets.QWidget()
        self.right_widget31.setObjectName('right_widget31')
        self.right_layout31 = QtWidgets.QGridLayout()
        self.right_widget31.setLayout(self.right_layout31)
        self.right_label_31 = QtWidgets.QLabel("S I M U L A T I O N   L I D A R")
        self.right_label_31.setObjectName('right_label31')
        
        # le button pour la lecture de fichier 
        self.right_widget32 = QtWidgets.QWidget()
        self.right_widget32.setObjectName('right_widget32')
        self.right_layout32 = QtWidgets.QGridLayout()
        self.right_widget32.setLayout(self.right_layout32)
        
        # le button pour le fichier Lidar 
        self.lidar_btn = QtWidgets.QPushButton(qtawesome.icon('fa.file-text',color='#A9A9A9'),"Scan Fichier")
        self.lidar_btn.setObjectName('lidar')
        self.lidar_btn.setCheckable(True)
        self.lidar_btn.clicked.connect(self.win3_fileLidarIn)
        # le button pour le fichier remission 
        self.remis_btn = QtWidgets.QPushButton(qtawesome.icon('fa.file-text',color='#A9A9A9'),"Remission Fichier")
        self.remis_btn.setObjectName('remis')
        self.remis_btn.setCheckable(True)
        self.remis_btn.clicked.connect(self.win3_fileRemisIn)
        # le button pour le fichier vidéo
        self.video_btn1 = QtWidgets.QPushButton(qtawesome.icon('fa.video-camera',color='#A9A9A9'),"\tChoisir Vidéo")
        self.video_btn1.setObjectName('video1')
        self.video_btn1.setCheckable(True)
        self.video_btn1.clicked.connect(self.win3_fileVideoIn)
        # le button pour commencer à générer la vidéo
        self.genVideo2 = QtWidgets.QPushButton(qtawesome.icon('fa.download',color='#A9A9A9'),"Générer Vidéo")
        self.genVideo2.setObjectName('genVideo2')
        self.genVideo2.setCheckable(True)
        self.genVideo2.clicked.connect(self.win3_GenererVideo)
        
        # l'affichage de résultats à droite
        self.right_widget33 = QtWidgets.QWidget()  
        self.right_widget33.setObjectName('right_widget33')
        self.right_layout33 = QtWidgets.QGridLayout()
        self.right_widget33.setLayout(self.right_layout33)
        self.right_label_33 = QtWidgets.QLabel()
        self.cb31 = QtWidgets.QCheckBox('Nuage des points',self)
        self.cb31.setObjectName('checkbox31')
        self.cb32 = QtWidgets.QCheckBox('Nuage + Luminosité',self)
        self.cb32.setObjectName('checkbox32')
        self.cb33 = QtWidgets.QCheckBox('Nettoyage LBP',self)
        self.cb33.setObjectName('checkbox33')
        self.cb34 = QtWidgets.QCheckBox('OTHER',self)
        self.cb34.setObjectName('checkbox34')
        self.cb31.stateChanged.connect(self.changecb3)
        self.cb32.stateChanged.connect(self.changecb3)
        self.cb33.stateChanged.connect(self.changecb3)
        ## 3: le joueur dela vidéo
        self.right_widget34 = QtWidgets.QWidget()
        self.right_widget34.setObjectName('right_widget34')
        self.right_layout34 = QtWidgets.QGridLayout()
        self.right_widget34.setLayout(self.right_layout34)
        ## 3: le button start
        self.start2 = QtWidgets.QPushButton(qtawesome.icon('fa.play',color='#A9A9A9'),"")
        self.start2.setObjectName('start2')
        self.start2.setCheckable(True)
        self.start2.clicked.connect(self.win3_PlayPause)
        ## 3: le button refresh       
        self.refresh2 = QtWidgets.QPushButton(qtawesome.icon('fa.refresh',color='#A9A9A9'),"")
        self.refresh2.setObjectName('refresh2')
        self.refresh2.setCheckable(True)
        self.refresh2.clicked.connect(self.win3_refreshCourbes)
        ## 3: le button export        
        self.export2 = QtWidgets.QPushButton(qtawesome.icon('fa.download',color='#A9A9A9'),"")
        self.export2.setObjectName('export2')
        self.export2.setCheckable(True)
        self.export2.clicked.connect(self.win3_combineAvi)
        ## 3: le bar    
        self.lab_duration22 = QtWidgets.QLabel("\t00 : 00")
        self.slider2 = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.lab_duration2 = QtWidgets.QLabel("-- : --")
        ## 3: la disposition dela vidéo
        self.right_widget35 = QtWidgets.QWidget()
        self.right_widget35.setObjectName('right_widget35')
        self.right_layout35 = QtWidgets.QGridLayout()
        self.right_widget35.setLayout(self.right_layout35)
        self.right_label_35 = QtWidgets.QLabel()
        self.right_label_35.setObjectName('right_label35')
        self.right_label_351 = QtWidgets.QLabel()
        
        # ranger et activer les layout
        self.right_layout31.addWidget(self.right_label_31,1,0,3,8)
        # 
        self.right_layout32.addWidget(self.video_btn1,0,1,2,2)
        self.right_layout32.addWidget(self.lidar_btn,0,4,2,2)
        self.right_layout32.addWidget(self.remis_btn,0,7,2,2)
        self.right_layout32.addWidget(self.genVideo2,0,9,2,2)
        self.right_layout32.setSpacing(25)
        # 
        self.right_layout33.addWidget(self.cb31,0,0,1,1)
        self.right_layout33.addWidget(self.cb32,0,1,1,1)
        self.right_layout33.addWidget(self.cb33,0,2,1,1)
        self.right_layout33.addWidget(self.cb34,0,3,1,1)
        self.right_layout33.setSpacing(15)
        # 
        self.right_layout34.addWidget(self.lab_duration22,0,0,1,1)
        self.right_layout34.addWidget(self.slider2,0,1,1,9)
        self.right_layout34.addWidget(self.lab_duration2,0,10,1,1)
        self.right_layout34.addWidget(self.start2,0,11,1,1)
        self.right_layout34.addWidget(self.refresh2,0,12,1,1)
        self.right_layout34.addWidget(self.export2,0,13,1,1)
        self.right_layout34.addWidget(self.right_label_351,3,4,1,4)
        self.right_layout34.setSpacing(15)
        # 
        self.right_layout35.addWidget(self.right_label_35,0,0,3,9)
        # 
        self.right_layout3.addWidget(self.right_widget31,1,0,2,9)
        self.right_layout3.addWidget(self.right_widget33,4,1,1,9)
        self.right_layout3.addWidget(self.right_widget32,6,1,2,9)
        self.right_layout3.addWidget(self.right_widget35,9,1,10,9)
        self.right_layout3.addWidget(self.right_widget34,22,1,1,9)
        
        
        # =============================================================================
        # la disposition de l'interface 4 : DETECTION
        # =============================================================================
        self.right_widget4 = QtWidgets.QWidget()
        self.right_widget4.setObjectName('right_widget4')
        self.right_layout4 = QtWidgets.QGridLayout()
        self.right_widget4.setLayout(self.right_layout4)
        self.right_widget4.setFixedWidth(int(self.screen.width()/3*2))
        self.right_widget4.setFixedHeight(int(self.screen.height()*0.93))
        
        # le titre à droite
        self.right_widget41 = QtWidgets.QWidget()
        self.right_widget41.setObjectName('right_widget41')
        self.right_layout41 = QtWidgets.QGridLayout()
        self.right_widget41.setLayout(self.right_layout41)
        self.right_label_41 = QtWidgets.QLabel("D E T E C T I O N   P A R   Y O L O")
        self.right_label_41.setObjectName('right_label41')
        # le button pour la lecture de fichier 
        self.right_widget42 = QtWidgets.QWidget()
        self.right_widget42.setObjectName('right_widget42')
        self.right_layout42 = QtWidgets.QGridLayout()
        self.right_widget42.setLayout(self.right_layout42)
        # le button pour choisir la vidéo
        self.video_btn2 = QtWidgets.QPushButton(qtawesome.icon('fa.video-camera',color='#A9A9A9'),"\tChoisir Vidéo")
        self.video_btn2.setObjectName('video1')
        self.video_btn2.setCheckable(True)
        self.video_btn2.clicked.connect(self.win4_fileVideoIn)
        # le button pour commencer la génération
        self.genVideo3 = QtWidgets.QPushButton(qtawesome.icon('fa.download',color='#A9A9A9'),"Générer et Enregistrer Vidéo")
        self.genVideo3.setObjectName('genVideo3')
        self.genVideo3.setCheckable(True)
        self.genVideo3.clicked.connect(self.win4_GenererVideo)
        
        # le joueuer de la vidéo à droite
        self.right_widget44 = QtWidgets.QWidget()
        self.right_widget44.setObjectName('right_widget44')
        self.right_layout44 = QtWidgets.QGridLayout()
        self.right_widget44.setLayout(self.right_layout44)
        # le button start
        self.start4 = QtWidgets.QPushButton(qtawesome.icon('fa.play',color='#A9A9A9'),"")
        self.start4.setObjectName('start4')
        self.start4.setCheckable(True)
        self.start4.clicked.connect(self.win4_PlayPause)
        # le bar
        self.lab_duration42 = QtWidgets.QLabel("\t00 : 00")
        self.slider4 = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.lab_duration4 = QtWidgets.QLabel("-- : --")
        # la disposition dela vidéo à droite
        self.right_widget45 = QtWidgets.QWidget()
        self.right_widget45.setObjectName('right_widget45')
        self.right_layout45 = QtWidgets.QGridLayout()
        self.right_widget45.setLayout(self.right_layout45)
        self.right_label_45 = QtWidgets.QLabel()
        self.right_label_45.setObjectName('right_label45')
        self.right_label_451 = QtWidgets.QLabel()

        # ranger et activer les layout
        self.right_layout41.addWidget(self.right_label_41,1,0,3,8)
        # 
        self.right_layout42.addWidget(self.video_btn2,0,1,2,2)
        self.right_layout42.addWidget(self.genVideo3,0,9,2,2)
        self.right_layout42.setSpacing(25)
        self.right_layout44.addWidget(self.lab_duration42,0,0,1,1)
        self.right_layout44.addWidget(self.slider4,0,1,1,9)
        self.right_layout44.addWidget(self.lab_duration4,0,10,1,1)
        self.right_layout44.addWidget(self.start4,0,11,1,1)
        self.right_layout44.addWidget(self.right_label_451,3,4,1,4)
        self.right_layout44.setSpacing(15)
        # 
        self.right_layout45.addWidget(self.right_label_45,0,0,3,9)
        # 
        self.right_layout4.addWidget(self.right_widget41,1,0,2,9)
        self.right_layout4.addWidget(self.right_widget42,4,1,1,9)
        self.right_layout4.addWidget(self.right_widget45,9,1,10,9)
        self.right_layout4.addWidget(self.right_widget44,22,1,1,9)
        
                
        # =============================================================================
        # la disposition de l'interface 5 : AIDE
        # =============================================================================
        self.right_widget5 = QtWidgets.QWidget()
        self.right_widget5.setObjectName('right_widget5')
        self.right_widget5.setFixedWidth(int(self.screen.width()*0.65))
        self.right_widget5.setFixedHeight(int(self.screen.height()*0.96))
        self.right_widget55 = QtWidgets.QWidget()
        self.right_widget55.setObjectName('right_widget55')
        self.right_widget55.setMinimumSize(int(self.screen.width()*0.5), int(self.screen.width()*0.5*1.4)*12) 
        self.right_label_55 = QtWidgets.QLabel()
        self.right_label_55.setObjectName('right_label55')
        self.right_label_55.setAlignment(QtCore.Qt.AlignCenter)
        self.right_label_55.setStyleSheet("padding-left:130px;")
        self.right_label_55.setScaledContents(True)
        pixmap = QtGui.QPixmap('doc_0610.png')
        self.right_label_55.setScaledContents(True)
        self.right_label_55.setPixmap(pixmap)
        
        ## créer un scroll
        self.scroll = QScrollArea()
        self.scroll.setWidget(self.right_widget55)
        self.scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.hSb = self.scroll.verticalScrollBar()
        ## ajouter layout pour right_widget55
        self.vbox1 = QtWidgets.QVBoxLayout()
        self.vbox1.addWidget(self.right_label_55)
        self.right_widget55.setLayout(self.vbox1)
        ## configurer le layout de right_widget55 pour scroll
        self.vbox2 = QtWidgets.QVBoxLayout()
        self.vbox2.addWidget(self.right_widget55)
        self.scroll.setLayout(self.vbox2)
        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.addWidget(self.scroll)
        self.right_widget5.setLayout(self.vbox)
        

        # =============================================================================
        # arranger toutes les dispositions
        # =============================================================================
        self.right_layout.addWidget(self.right_widget0,0,0,24,9) 
        self.right_layout.addWidget(self.right_widget1,0,0,24,9) 
        self.right_layout.addWidget(self.right_widget2,0,0,24,9) 
        self.right_layout.addWidget(self.right_widget3,0,0,24,9) 
        self.right_layout.addWidget(self.right_widget4,0,0,24,9) 
        self.right_layout.addWidget(self.right_widget5,0,0,24,9) 
        
        self.stacked_layout.addWidget(self.right_widget0)
        self.stacked_layout.addWidget(self.right_widget1)
        self.stacked_layout.addWidget(self.right_widget2)
        self.stacked_layout.addWidget(self.right_widget3)
        self.stacked_layout.addWidget(self.right_widget4)
        self.stacked_layout.addWidget(self.right_widget5)
        
        
        # =============================================================================
        # la disposition pour les buttons à gauche
        # =============================================================================
        self.left_layout1.addWidget(self.left_img_1,1,0,1,3)
        self.left_layout2.addWidget(self.left_button_1,0,0,1,3)
        self.left_layout2.addWidget(self.left_button_2,2,0,1,3)
        self.left_layout2.addWidget(self.left_button_3,3,0,1,3)
        self.left_layout2.addWidget(self.left_button_4,4,0,1,3)
        self.left_layout2.addWidget(self.left_button_5,5,0,1,3)

        self.main_layout.setContentsMargins(0,0,0,0);
        self.left_layout.setContentsMargins(0,0,0,0);
        self.left_layout1.setContentsMargins(0,0,0,0);
        self.left_layout2.setContentsMargins(0,0,0,0);
        self.left_layout3.setContentsMargins(0,0,0,0);
        self.right_layout.setContentsMargins(0,0,0,0);
        # self.setWindowFlag(QtCore.Qt.FramelessWindowHint) # pour cacher le cadre
        
        
        # =============================================================================
        # changer la style de disposition
        # =============================================================================
        # ## 5: titre à droite
        # self.right_widget51.setStyleSheet(
        # '''
        # QLabel{
        # border:none;
        # font-size:32px;
        # font-weight:600;
        # letter-spacing:big;
        # word-spacing:big;
        # color:#2F4F4F;
        # font-family:'Calibri';
        # padding-left:70px;}
        # ''')
        
        ## 4: la disposition dela vidéo
        self.right_widget45.setStyleSheet(
        ''' 
        background-color:#fafafa;
        border-style:none;
       ''')
       

        ## 4: la disposition du joueuer
        self.right_widget44.setStyleSheet(
        '''
         QPushButton{
         background-color:#fafafa;
         border-style:none;
         
         padding:5px;
         min-height:30px;
         border-radius:20px;
         
         text-align:centre;
         font-weight:400px;
         font-size:20px;
         font-family:'Calibri';
         color:#A52A2A;}
         QPushButton:checked{background-color:#FFE4E1;border:3px solid #FF7F50;}
        ''')        


        ## 4: 2 buttons pour les vidéos
        # background-color:#B6C29A; #E0E5DF;
        self.right_widget42.setStyleSheet(
        '''
        QPushButton{
        color:#808080;
        background-color:#fafafa;
        border-style:none;
        border:0px solid #3f3f3f; 
        
        padding:5px;
        min-height:20px;
        border-radius:20px;
        
        text-align:centre; 
        height:30px;
        width:60px;
        font-size:16px;
        font-weight:400;
        font-family:'Calibri';}
        QPushButton:hover{background:rgb(112,173,71,55);}
        QPushButton:checked{border:3px solid #B6C29A;}''')
                            
                            
        ## 4: titre à droite
        self.right_widget41.setStyleSheet(
        '''
        QLabel{
        border:none;
        font-size:32px;
        font-weight:600;
        letter-spacing:big;
        word-spacing:big;
        color:#2F4F4F;
        font-family:'Calibri';
        padding-left:70px;}
        
        ''')
        
        
        ## 3: la disposition du joueur
        self.right_widget34.setStyleSheet(
        '''
         QPushButton{
         background-color:#fafafa;
         border-style:none;
         
         padding:5px;
         min-height:25px;
         border-radius:15px;
         
         text-align:centre;
         font-weight:400px;
         font-size:15px;
         font-family:'Calibri';
         color:#A52A2A;}
         QPushButton:checked{background-color:#FFE4E1;border:3px solid #FF7F50;}
        ''')
        
        ## 3: la disposition dela vidéo
        self.right_widget35.setStyleSheet(
        ''' 
        background-color:#fafafa;
        border-style:none;

       ''')
       ## 3: le style de checkbox
        self.right_widget33.setStyleSheet(
        '''
        QCheckBox{background-color:#fafafa;
          padding:5px; 
          min-height:30px;
          border-radius:20px;
          font-size:15px;
          font-family:'Calibri';
          color:#808080;
          padding-left:40px; 
          }
         QCheckBox:indicator{width:13px;height:13px;color:#808080;}
         
         QPushButton{
         background-color:#fafafa;
         border-style:none;
         
         padding:5px;
         min-height:30px;
         border-radius:20px;
         
         text-align:centre;
         font-weight:400px;
         font-size:15px;
         font-family:'Calibri';
         color:#A52A2A;}
         QPushButton:checked{background-color:#FFE4E1;border:3px solid #FF7F50;}
        ''')

        ## 3: button pour les 3 vidéos
        # background-color:#B6C29A; #E0E5DF;
        self.right_widget32.setStyleSheet(
        '''
        QPushButton{
        color:#808080;
        background-color:#fafafa;
        border-style:none;
        border:0px solid #3f3f3f; 
        
        padding:5px;
        min-height:20px;
        border-radius:20px;
        
        text-align:centre; 
        height:30px;
        width:60px;
        font-size:15px;
        font-weight:400;
        font-family:'Calibri';}
        QPushButton:hover{background:rgb(112,173,71,55);}
        QPushButton:checked{border:3px solid #B6C29A;}''')

        ## 3: titre à droite
        self.right_widget31.setStyleSheet(
        '''
        QLabel{
        border:none;
        font-size:32px;
        font-weight:600;
        letter-spacing:big;
        word-spacing:big;
        color:#2F4F4F;
        font-family:'Calibri';
        padding-left:70px;}
        
        ''')
        
        ## 2: la disposition du joueur
        self.right_widget24.setStyleSheet(
        '''
         QPushButton{
         background-color:#fafafa;
         border-style:none;
         
         padding:5px;
         min-height:25px;
         border-radius:15px;
         
         text-align:centre;
         font-weight:400px;
         font-size:20px;
         font-family:'Calibri';
         color:#A52A2A;}
         QPushButton:checked{background-color:#FFE4E1;border:3px solid #FF7F50;}
        ''')
        
        ## 2: la disposition dela vidéo
        self.right_widget25.setStyleSheet(
        ''' 
        background-color:#fafafa;
        border-style:none;

       ''')
       ## 2: le style de checkbox
        self.right_widget23.setStyleSheet(
        '''
        QCheckBox{background-color:#fafafa;
          padding:5px; 
          min-height:30px;
          border-radius:20px;
          font-size:16px;
          font-family:'Calibri';
          color:#808080;
          padding-left:60px; 
          }
         QCheckBox:indicator{width:13px;height:13px;color:#808080;}
         
         QPushButton{
         background-color:#fafafa;
         border-style:none;
         
         padding:5px;
         min-height:30px;
         border-radius:20px;
         
         text-align:centre;
         font-weight:400px;
         font-size:18px;
         font-family:'Calibri';
         color:#A52A2A;}
         QPushButton:checked{background-color:#FFE4E1;border:3px solid #FF7F50;}
        ''')
        ## 2: label pour montrer le temps
        self.right_label_23.setStyleSheet(
        '''
        QLabel{
        background-color:#fafafa;
        border-style:none;
        border:0px solid #3f3f3f; 
        
        padding:5px;
        min-height:20px;
        border-radius:20px;
        
        text-align:centre; 
        height:100px;
        font-size:15px;
        font-weight:400;
        font-family:'Calibri';}
        '''
        )
        
        ## 2: button pour les 3 vidéos
        # background-color:#B6C29A; #E0E5DF;
        self.right_widget22.setStyleSheet(
        '''
        QPushButton{
        color:#808080;
        background-color:#fafafa;
        border-style:none;
        border:0px solid #3f3f3f; 
        
        padding:5px;
        min-height:20px;
        border-radius:20px;
        
        text-align:centre; 
        height:30px;
        width:60px;
        font-size:16px;
        font-weight:400;
        font-family:'Calibri';}
        QPushButton:hover{background:rgb(112,173,71,55);}
        QPushButton:checked{border:3px solid #B6C29A;}''')

        ## 2: titre à droite
        self.right_widget21.setStyleSheet(
        '''
        QLabel{
        border:none;
        font-size:32px;
        font-weight:600;
        letter-spacing:big;
        word-spacing:big;
        color:#2F4F4F;
        font-family:'Calibri';
        padding-left:70px;}
        
        ''')
        
        self.right_widget0.setStyleSheet(
        '''
        QLabel{
        color:#C0C0C0;
        font-size:40px;
        font-weight:900;
        font-family:'Arial Black';}
        ''')
        
        ## 1: la disposition des courbes
        self.right_widget15.setStyleSheet(
        ''' 
        background-color:#fafafa;
        border-style:none;

       ''')
       
        ## 1: le label pour les courbes
        self.right_label_15.setStyleSheet(
        '''
        QLabel{
        background-color:#fafafa;
        border-style:none;
        border:0px solid #3f3f3f; 
        
        padding:5px;
        min-height:20px;
        border-radius:20px;
        
        text-align:centre; 
        height:230px;
        font-size:15px;
        font-weight:400;
        font-family:'Calibri';}
        '''
        )
        
        ## 1: le style de checkbox
        self.right_widget14.setStyleSheet(
        '''
        QCheckBox{background-color:#fafafa;
          padding:5px; 
          min-height:30px;
          border-radius:20px;
          font-size:16px;
          font-family:'Calibri';
          color:#808080;
          padding-left:60px; 
          }
         QCheckBox:indicator{width:13px;height:13px;color:#808080;}
         
         QPushButton{
         background-color:#fafafa;
         border-style:none;
         
         padding:5px;
         min-height:30px;
         border-radius:20px;
         
         text-align:centre;
         font-weight:400px;
         font-size:18px;
         font-family:'Calibri';
         color:#A52A2A;}
         QPushButton:checked{background-color:#FFE4E1;border:3px solid #FF7F50;}
        ''')
        
        ## 1: label pour montrer le temps
        self.right_label_13.setStyleSheet(
        '''
        QLabel{
        background-color:#fafafa;
        border-style:none;
        border:0px solid #3f3f3f; 
        
        padding:5px;
        min-height:20px;
        border-radius:20px;
        
        text-align:centre; 
        height:180px;
        font-size:15px;
        font-weight:400;
        font-family:'Calibri';}
        '''
        )
        
        ## 1: button pour entrer 3 fichiers
        # background-color:#B6C29A; #E0E5DF;
        self.right_widget12.setStyleSheet(
        '''
        QPushButton{
        color:#808080;
        background-color:#fafafa;
        border-style:none;
        border:0px solid #3f3f3f; 
        
        padding:5px;
        min-height:20px;
        border-radius:20px;
        
        text-align:centre; 
        height:30px;
        width:60px;
        font-size:16px;
        font-weight:400;
        font-family:'Calibri';}
        QPushButton:hover{background:rgb(112,173,71,55);}
        QPushButton:checked{border:3px solid #B6C29A;}''')

        ## 1: titre à droite
        self.right_widget11.setStyleSheet(
        '''
        QLabel{
        border:none;
        font-size:32px;
        font-weight:600;
        letter-spacing:big;
        word-spacing:big;
        color:#2F4F4F;
        font-family:'Calibri';
        padding-left:70px;}
        
        ''')
        
        ## 1: font pour le lofo ##
        self.left_widget1.setStyleSheet( 
        '''
        QLabel{
        color:#8895a5;
        border:none;
        padding-left:5px;
        font-weight:500;
        font-size:15px;
        font-family:'Calibri';
        }
        ''')

        
        # self.top_widget.setStyleSheet(
        # '''
        # *{background-color:#303030;}
        # QLabel{
        # color:#ffffff;
        # border:none;
        # font-weight:600;
        # font-size:17px;
        # font-family:'Calibri';
        #  }
        # QPushButton{
        # text-align:right;
        # padding-right:30px;
        # color:#ffffff;
        # font-weight:400;
        # border:none;
        # font-size:14px;
        # font-family:'Calibri';}
        # ''')

        ## couleurs du boutons à gauche #B0C4DE
        ## couleurs du boutons lors de 'hover' #e6e6e6 #B6C29A #E0E5DF
        self.left_widget.setStyleSheet(
        '''
        *{background-color:#fafafa;} 
          QToolButton{border:none;font-size:16px;text-align:left; 
                      font-weight:400;padding-left:55px;height:70px;
                      font-family:"DIN";width:400px;}
          QToolButton:hover{background:rgb(112,173,71,55);}
          QToolButton:checked{background-color:rgb(112,173,71,120);} ''')
        
        
def main():
    app = QtWidgets.QApplication(sys.argv)
    gui = MainUi()
    gui.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()