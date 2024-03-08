from .pipeline import Pipeline
from .detrend import Detrend
from .bandpassfilter import BandpassFilter
from .hilbert_normalization import HilbertNormalization
from .smooth import Smooth

preprocess_pipeline = Pipeline(steps=[
    Smooth(),
])

heartrate_pipeline = Pipeline(steps=[
    # Detrend(),
    BandpassFilter(filter_type="butterworth", fs=30, low=0.75, high=2.5),
    HilbertNormalization()
])

lf_hf_pipeline = Pipeline(steps=[
    # Detrend(),
    BandpassFilter(filter_type="butterworth", fs=30, low=0.04, high=0.4),
    # HilbertNormalization()
])
