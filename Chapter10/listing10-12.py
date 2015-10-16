# Script to run a map classificatin using a classification tree.

import csv
import os
import numpy as np
from sklearn import tree
from osgeo import gdal
import ospybook as pb

folder = r'D:\osgeopy-data\Landsat\Utah'
raster_fns = ['LE70380322000181EDC02_60m.tif',
              'LE70380322000181EDC02_TIR_60m.tif']
out_fn = 'tree_prediction60.tif'
train_fn = r'D:\osgeopy-data\Utah\training_data.csv'
gap_fn = r'D:\osgeopy-data\Utah\landcover60.tif'

os.chdir(folder)

# Read the coordinates and actual classification from the csv.
# This is the training data.
xys = []
classes = []
with open(train_fn) as fp:
    reader = csv.reader(fp)
    next(reader)
    for row in reader:
        xys.append([float(n) for n in row[:2]])
        classes.append(int(row[2]))

# Calculate the pixel offsets for the coordinates obtained from
# the csv.
ds = gdal.Open(raster_fns[0])
pixel_trans = gdal.Transformer(ds, None, [])
offset, ok = pixel_trans.TransformPoints(True, xys)
cols, rows, z = zip(*offset)

# Get the satellite data.
data = pb.stack_bands(raster_fns)

# Sample the satellite data at the coordinates from the csv.
sample = data[rows, cols, :]

# Fit the classification tree.
clf = tree.DecisionTreeClassifier(max_depth=5)
clf = clf.fit(sample, classes)

# Apply the new classification tree model to the satellite data.
rows, cols, bands = data.shape
data2d = np.reshape(data, (rows * cols, bands))
prediction = clf.predict(data2d)
prediction = np.reshape(prediction, (rows, cols))

# Set the pixels with no valid satellite data to 0.
prediction[np.sum(data, 2) == 0] = 0

# Save the output.
predict_ds = pb.make_raster(ds, out_fn, prediction, gdal.GDT_Byte, 0)
predict_ds.FlushCache()
levels = pb.compute_overview_levels(predict_ds.GetRasterBand(1))
predict_ds.BuildOverviews('NEAREST', levels)

# Apply the color table from the SWReGAP landcover raster.
gap_ds = gdal.Open(gap_fn)
colors = gap_ds.GetRasterBand(1).GetRasterColorTable()
predict_ds.GetRasterBand(1).SetRasterColorTable(colors)

del ds
