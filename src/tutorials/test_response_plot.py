from pyrocko.plot import response_plot
from pyrocko.tutorials import get_tutorial_data

# download example data
get_tutorial_data('test_response.resp')

# read data
resps, labels = response_plot.load_response_information(
    'test_response.resp', 'resp')

# plot response and save image
response_plot.plot(
    responses=resps, labels=labels, filename='test_response.png',
    fmin=0.001, fmax=400., dpi=75.)
