import torch
import comfy.nested_tensor
from .shared import CATEGORY, MINIMAX_H3_PARAMS


class LatentAVInfo:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "av_latent": ("LATENT", {}),
            },
        }

    RETURN_TYPES = ("LATENT", "INT", "STRING", "INT", "INT")
    RETURN_NAMES = ("av_latent", "frames", "video_resolution", "video_tokens", "audio_tokens")

    SEARCH_ALIASES = ["av latent info", "latent info", "video audio latent info"]

    FUNCTION = "run"
    CATEGORY = CATEGORY
    DESCRIPTION = "Displays basic info for a combined AV latent: frame count, video resolution, and token counts."

    def run(self, **kwargs):
        av_latent = kwargs.get("av_latent", None)
        if av_latent is None:
            raise Exception("No av_latent provided.")

        samples = av_latent.get("samples", None)
        if samples is None:
            raise Exception("av_latent is missing samples.")

        if isinstance(samples, comfy.nested_tensor.NestedTensor) or getattr(samples, "is_nested", False):
            tensors = list(samples.unbind())
        elif isinstance(samples, (list, tuple)):
            tensors = list(samples)
        elif isinstance(samples, torch.Tensor):
            tensors = [samples]
        else:
            tensors = [samples]

        if len(tensors) < 2:
            raise Exception("av_latent does not contain both video and audio samples.")

        video_tensor = tensors[0]
        audio_tensor = tensors[1]

        dims_v = len(video_tensor.shape)
        t_dim_v = 2 if dims_v >= 3 else 0
        video_tokens = int(video_tensor.shape[t_dim_v])
        audio_tokens = int(audio_tensor.shape[-1])

        latent_h = int(video_tensor.shape[-2])
        latent_w = int(video_tensor.shape[-1])
        video_resolution = f"{latent_w}x{latent_h}"

        # Inverse of the token snapping rule used by MiniMax H3 latent nodes.
        frame_multi = float(MINIMAX_H3_PARAMS["frame_multi"])
        frame_offset = float(MINIMAX_H3_PARAMS["frame_offset"])
        min_latent_temporal_tokens = float(MINIMAX_H3_PARAMS["min_latent_temporal_tokens"])

        if video_tokens <= min_latent_temporal_tokens:
            frames = int(round(frame_offset))
        else:
            k = (float(video_tokens) - min_latent_temporal_tokens) / frame_offset
            frames = int(round(k * frame_multi + frame_offset))

        return (av_latent, frames, video_resolution, video_tokens, audio_tokens)