# Script to show a custom callback function

import os
import sys
from osgeo import gdal

def my_progress(complete, message, progressArg=0.02):
    '''Callback function.

    complete    - progress percentage between 0 and 1
    message     - message to show when starting
    progressArg - progress increments to print dots, between 0 and 1
    '''
    # This runs the first time only, because my_progress will get set here
    # so the attribute will always exist after the first time.
    if not hasattr(my_progress, 'last_progress'):
        sys.stdout.write(message)
        my_progress.last_progress = 0

    # Clear out the progress info if we're done.
    if complete >= 1:
        sys.stdout.write('done\n')
        del my_progress.last_progress

    # If not done, show the current progress.
    else:
        # divmod returns the quotient and remainder of
        # complete / progressArg. We're grabbing the quotient. For example,
        # if we're halfway done (complete = 0.5) and progressArg = 0.02,
        # then progress = 25. If progressArc = 0.25, then progress = 2.
        progress = divmod(complete, progressArg)[0]

        # Print dots while the last_progress counter is less than progress.
        # Since progress is a bigger number if progressArg is a small
        # number, we get more dots the smaller progressArg is.
        while my_progress.last_progress < progress:
            sys.stdout.write('.')
            sys.stdout.flush()
            my_progress.last_progress += 1


# Try it out when calculating statistics on the natural color Landsat image.
# Change the last parameter (0.05) to other values to see how it affects
# things.
# And don't forget to change folder.
os.chdir(r'D:\osgeopy-data\Landsat\Washington')
ds = gdal.Open('nat_color.tif')
for i in range(ds.RasterCount):
    ds.GetRasterBand(i + 1).ComputeStatistics(False, my_progress, 0.05)



###############################################################################

# Try out the custom progress function when we call it manually.
def process_file(fn):
    # Slow things down a bit by counting to 1,000,000 for each file.
    for i in range(1000000):
        pass # do nothing

import os
data_dir = r'D:\osgeopy-data'
list_of_files = os.listdir(os.chdir(os.path.join(data_dir, 'Landsat', 'Washington')))
for i in range(len(list_of_files)):
    process_file(list_of_files[i])
    # Uses the default progressArg value.
    my_progress(i / float(len(list_of_files)), 'Processing files')
my_progress(100, '')

# You can also change the progressArg value.
for i in range(len(list_of_files)):
    process_file(list_of_files[i])
    my_progress(i / float(len(list_of_files)), 'Processing files', 0.05)
my_progress(100, '')
