# Function to get slices of any size from an array.

import numpy as np

def make_slices(data, win_size):
    """Return a list of slices given a window size.

    data     - two-dimensional array to get slices from
    win_size - tuple of (rows, columns) for the moving window
    """
    # Calculate the slice size
    rows = data.shape[0] - win_size[0] + 1
    cols = data.shape[1] - win_size[1] + 1
    slices = []

    # Loop through the rows and columns in the provided window size and
    # create each slice.
    for i in range(win_size[0]):
        for j in range(win_size[1]):
            slices.append(data[i:rows+i, j:cols+j])
    return slices
