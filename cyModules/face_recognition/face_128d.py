#!/usr/bin/env python
#-- coding: utf-8 --

import pickle
import cv2
import numpy as np

#-------------------------------------------------------
#-- encoding_distance
#-- Use numpy linear algebra NORM to calculate vector distance
#-------------------------------------------------------

def get_128d_distance(a):
	distance = np.linalg.norm(a)
	return distance

def calculate_128d_distance(a, b):
	distance = np.linalg.norm(a - b)
	return distance

def load_pickle(pikfile):
	with open(pikfile, "rb") as pkf:
		face_feature = pickle.loads(pkf.read())
		pkf.close()
	return face_feature
