from .martinodes.MediaSlicer import MediaSlicer
from .martinodes.AudioResampler import AudioResampler
from .martinodes.AudioTrimExtender import AudioTrimExtender
from .martinodes.AudioInfo import AudioInfo
from .martinodes.MediaOverlappingConcatenator import MediaOverlappingConcatenator

NODE_CLASS_MAPPINGS = {
    "MARMediaSlicer": MediaSlicer,
    "MARAudioResampler": AudioResampler,
    "MARAudioTrimExtender": AudioTrimExtender,
    "MARAudioInfo": AudioInfo,
    "MARMediaOverlappingConcatenator": MediaOverlappingConcatenator
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MARMediaSlicer": "Video head or tail",
    "MARAudioInfo": "Audio info",
    "MARAudioResampler": "Resample audio",
    "MARAudioTrimExtender": "Ensure audio duration",
    "MARMediaOverlappingConcatenator": "Concatenate media"
}