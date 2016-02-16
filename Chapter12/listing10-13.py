# Script to create a confusion matrix and calculate kappa.

import csv
import os
import numpy as np
from sklearn import metrics
import skll
from osgeo import gdal

folder = r'D:\osgeopy-data\Utah'
accuracy_fn = 'accuracy_data.csv'
matrix_fn = 'confusion_matrix.csv'
prediction_fn = r'D:\osgeopy-data\Landsat\Utah\tree_prediction60.tif'

os.chdir(folder)

# Collect the data needed for the accuracy assessment.
xys = []
classes = []
with open(accuracy_fn) as fp:
    reader = csv.reader(fp)
    next(reader)
    for row in reader:
        xys.append([float(n) for n in row[:2]])
        classes.append(int(row[2]))

ds = gdal.Open(prediction_fn)
pixel_trans = gdal.Transformer(ds, None, [])
offset, ok = pixel_trans.TransformPoints(True, xys)
cols, rows, z = zip(*offset)

data = ds.GetRasterBand(1).ReadAsArray()
sample = data[rows, cols]
del ds

# Compute kappa.
print('Kappa:', skll.kappa(classes, sample))

# Create the confusion matrix.
labels = np.unique(np.concatenate((classes, sample)))
matrix = metrics.confusion_matrix(classes, sample, labels)

# Add labels to the matrix and save it.
matrix = np.insert(matrix, 0, labels, 0)
matrix = np.insert(matrix, 0, np.insert(labels, 0, 0), 1)
np.savetxt(matrix_fn, matrix, fmt='%1.0f', delimiter=',')
