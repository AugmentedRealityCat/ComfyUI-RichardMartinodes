from .martinodes.MediaSlicer import MediaSlicer
from .martinodes.AudioResampler import AudioResampler
from .martinodes.AudioTrimExtender import AudioTrimExtender
from .martinodes.AudioInfo import AudioInfo
from .martinodes.MediaTrimmer import MediaTrimmer
from .martinodes.MediaOverlappingConcatenator import MediaOverlappingConcatenator
from .martinodes.LatentAVMaskedExtender import LatentAVMaskedExtender
from .martinodes.LatentAVLoadSave import SaveAVLatent, LoadAVLatent
from .martinodes.LatentOverlappingConcatenator import LatentOverlappingConcatenator

NODE_CLASS_MAPPINGS = {
    "MARMediaSlicer": MediaSlicer,
    "MARAudioResampler": AudioResampler,
    "MARAudioTrimExtender": AudioTrimExtender,
    "MARMediaTrimmer": MediaTrimmer,
    "MARAudioInfo": AudioInfo,
    "MARMediaOverlappingConcatenator": MediaOverlappingConcatenator,
    "LatentAVMaskedExtender": LatentAVMaskedExtender,
    "SaveAVLatent": SaveAVLatent,
    "LoadAVLatent": LoadAVLatent,
    "LatentOverlappingConcatenator": LatentOverlappingConcatenator
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MARMediaSlicer": "Media head or tail",
    "MARAudioInfo": "Audio info",
    "MARAudioResampler": "Resample audio",
    "MARMediaTrimmer": "Trim media",
    "MARAudioTrimExtender": "Ensure audio duration",
    "MARMediaOverlappingConcatenator": "Concatenate media",
    "LatentAVMaskedExtender": "Extend video+audio latent",
    "SaveAVLatent": "Save video+audio latent",
    "LoadAVLatent": "Load video+audio latent",
    "LatentOverlappingConcatenator": "Concatenate video+audio latents"
}