from .pipeline import Pipeline
from .detrend import Detrend
from .bandpassfilter import BandpassFilter
from .hilbert_normalization import HilbertNormalization
from .smooth import Smooth
from .visualize import Visualize

preprocess_pipeline = Pipeline(steps=[
    Smooth(),
])

postprocess_pipeline = Pipeline(steps=[
    Detrend(),
    Visualize(),
    BandpassFilter(filter_type="butterworth", fs=30, low=0.75, high=2.5),
    Visualize(),
    HilbertNormalization()
])
