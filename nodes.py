from .martinodes.MediaSlicer import MediaSlicer
from .martinodes.AudioResampler import AudioResampler

NODE_CLASS_MAPPINGS = {
    "MARMediaSlicer": MediaSlicer,
    "MARAudioResampler": AudioResampler
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MARMediaSlicer": "Video head or tail",
    "MARAudioResampler": "Resample audio"
}