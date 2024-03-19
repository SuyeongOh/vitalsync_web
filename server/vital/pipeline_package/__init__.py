from .pipeline import Pipeline
from .detrend import Detrend
from server.vital.pipeline_package.bandpassfilter import BandpassFilter
from server.vital.pipeline_package.hilbert_normalization import HilbertNormalization
from server.vital.pipeline_package.smooth import Smooth

preprocess_pipeline = Pipeline(steps=[
    Smooth(),
])

heartrate_pipeline = Pipeline(steps=[
    # Detrend(),
    BandpassFilter(filter_type="butterworth", fs=30, low=0.75, high=2.5),
])

lf_hf_pipeline = Pipeline(steps=[
    # Detrend(),
    BandpassFilter(filter_type="butterworth", fs=30, low=0.04, high=0.4),
    HilbertNormalization()
])
