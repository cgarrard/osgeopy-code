# Function to stretch and scale data.

import numpy as np

def stretch_data(data, num_stddev):
    """Returns the data with a standard deviation stretch applied.

    data       - array containing data to stretch
    num_stddev - number of standard deviations to use
    """
    mean = np.mean(data)
    std_range = np.std(data) * 2
    new_min = max(mean - std_range, np.min(data))
    new_max = min(mean + std_range, np.max(data))
    clipped_data = np.clip(data, new_min, new_max)
    return clipped_data / (new_max - new_min)
