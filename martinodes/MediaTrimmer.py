from .shared import CATEGORY
import torch

class MediaTrimmer:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "optional": {
                "images": ("IMAGE", {}),
                "audio": ("AUDIO", {}),
            },
            "required": {          
                "trim_seconds" : ("FLOAT", { "default" : 0.0 }),
                "video_fps" : ("FLOAT", { "default" : 24.0 }),
                "trim_from" : (["start", "end"], { "default" : "end" }),
            },
        }

    RETURN_TYPES = ("IMAGE", "AUDIO")
    RETURN_NAMES = ("images", "audio")

    SEARCH_ALIASES = ["trim video", "trim audio"]

    FUNCTION = "run"
    CATEGORY = CATEGORY
    DESCRIPTION = "Trims video and/or audio from any end."

    def run(self,  **kwargs):
        trim_seconds = kwargs.get("trim_seconds", 0.0)
        video_fps = kwargs.get("video_fps", 24.0)
        trim_from = kwargs.get("trim_from", "end")

        audio = kwargs.get("audio", None)
        images = kwargs.get("images", None)

        out_images = images
        out_audio = audio

        if trim_seconds < 0.001:
            return (out_images, out_audio)

        if images is not None:
            frames_to_trim = int(trim_seconds * video_fps)
            total_frames = images.shape[0]
            
            if frames_to_trim == 0:
                out_images = images
            elif frames_to_trim >= total_frames:
                out_images = torch.empty((0, *images.shape[1:]), dtype=images.dtype, device=images.device)
            else:
                if trim_from == "start":
                    out_images = images[frames_to_trim:]
                else:
                    out_images = images[:-frames_to_trim]

 
        if audio is not None:            
            # ComfyUI AUDIO structure: {"waveform": tensor(batch, channels, samples), "sample_rate": int}
            waveform = audio["waveform"]
            sr = audio["sample_rate"]
            device = waveform.device

            samples_to_trim = int(trim_seconds * sr)
            total_samples = waveform.shape[-1]
            
            if samples_to_trim == 0:
                out_waveform = waveform
            elif samples_to_trim >= total_samples:
                 out_waveform = torch.empty((*waveform.shape[:-1], 0), dtype=waveform.dtype, device=device)
            else:
                if trim_from == "start":
                    out_waveform = waveform[..., samples_to_trim:]
                else:
                    out_waveform = waveform[..., :-samples_to_trim]
            
            out_audio = {"waveform": out_waveform, "sample_rate": sr}

        return (out_images, out_audio)
