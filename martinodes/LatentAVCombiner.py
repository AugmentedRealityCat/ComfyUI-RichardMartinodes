import comfy.nested_tensor
from .shared import CATEGORY


class LatentAVCombiner:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "video_latent": ("LATENT", ),
                "audio_latent": ("LATENT", ),
            }
        }

    RETURN_TYPES = ("LATENT", )
    RETURN_NAMES = ("av_latent", )

    SEARCH_ALIASES = ["combine latent", "combine video audio latent", "join video audio latent"]

    FUNCTION = "run"
    CATEGORY = CATEGORY
    DESCRIPTION = "Combines a separate video latent and audio latent into a single MiniMax H3 compatible av_latent."

    def run(self, video_latent, audio_latent):
        video_samples = video_latent["samples"]
        audio_samples = audio_latent["samples"]

        out_av = video_latent.copy()
        out_av["samples"] = comfy.nested_tensor.NestedTensor([video_samples, audio_samples])
        out_av.pop("noise_mask", None)

        return (out_av, )
