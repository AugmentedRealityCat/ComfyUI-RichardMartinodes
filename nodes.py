from .martinodes.MediaSlicer import MediaSlicer
from .martinodes.AudioResampler import AudioResampler
from .martinodes.AudioTrimExtender import AudioTrimExtender
from .martinodes.AudioInfo import AudioInfo
from .martinodes.MediaTrimmer import MediaTrimmer
from .martinodes.MediaOverlappingConcatenator import MediaOverlappingConcatenator
from .martinodes.LatentAVTailMaskedExtender import LatentAVTailMaskedExtender
from .martinodes.LatentAVLoadSave import SaveAVLatent, LoadAVLatent

NODE_CLASS_MAPPINGS = {
    "MARMediaSlicer": MediaSlicer,
    "MARAudioResampler": AudioResampler,
    "MARAudioTrimExtender": AudioTrimExtender,
    "MARMediaTrimmer": MediaTrimmer,
    "MARAudioInfo": AudioInfo,
    "MARMediaOverlappingConcatenator": MediaOverlappingConcatenator,
    "LatentAVTailMaskedExtender": LatentAVTailMaskedExtender,
    "SaveAVLatent": SaveAVLatent,
    "LoadAVLatent": LoadAVLatent
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MARMediaSlicer": "Media head or tail",
    "MARAudioInfo": "Audio info",
    "MARAudioResampler": "Resample audio",
    "MARMediaTrimmer": "Trim media",
    "MARAudioTrimExtender": "Ensure audio duration",
    "MARMediaOverlappingConcatenator": "Concatenate media",
    "LatentAVTailMaskedExtender": "Extend video from latent tail",
    "SaveAVLatent": "Save video+audio latent",
    "LoadAVLatent": "Load video+audio latent"
}