from .martinodes.MediaSlicer import MediaSlicer
from .martinodes.AudioResampler import AudioResampler
from .martinodes.AudioTrimExtender import AudioTrimExtender
from .martinodes.AudioInfo import AudioInfo
from .martinodes.MediaTrimmer import MediaTrimmer
from .martinodes.MediaOverlappingConcatenator import MediaOverlappingConcatenator

NODE_CLASS_MAPPINGS = {
    "MARMediaSlicer": MediaSlicer,
    "MARAudioResampler": AudioResampler,
    "MARAudioTrimExtender": AudioTrimExtender,
    "MARMediaTrimmer": MediaTrimmer,
    "MARAudioInfo": AudioInfo,
    "MARMediaOverlappingConcatenator": MediaOverlappingConcatenator
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MARMediaSlicer": "Media head or tail",
    "MARAudioInfo": "Audio info",
    "MARAudioResampler": "Resample audio",
    "MARMediaTrimmer": "Trim media",
    "MARAudioTrimExtender": "Ensure audio duration",
    "MARMediaOverlappingConcatenator": "Concatenate media"
}