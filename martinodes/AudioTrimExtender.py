from .shared import CATEGORY
import torch

class AudioTrimExtender:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "audio": ("AUDIO", {}),
                "duration_seconds" : ("FLOAT", { "default" : 0.0 }),
                "pad" : (["start", "end"], { "default" : "end" }),
                "crop" : (["start", "end"], { "default" : "end" }),
            },
        }

    RETURN_TYPES = ("AUDIO",)
    RETURN_NAMES = ("audio",)

    SEARCH_ALIASES = ["pad audio", "crop audio"]

    FUNCTION = "run"
    CATEGORY = CATEGORY
    DESCRIPTION = "Makes audio to have the specified duration, cropping or padding as needed."

    def run(self,  **kwargs):
        duration_seconds = kwargs.get("duration_seconds", 0.0)
        pad = kwargs.get("pad", "end")
        crop = kwargs.get("crop", "end")

        # ComfyUI AUDIO structure: {"waveform": tensor(batch, channels, samples), "sample_rate": int}
        audio = kwargs.get("audio", None)

        if audio is None:
             raise Exception("No audio provided to process.")

        waveform = audio["waveform"]
        sr = audio["sample_rate"]
        device = waveform.device

        batch_size = waveform.shape[0]
        processed_batch = []

        target_samples = int(duration_seconds * sr)

        for b in range(batch_size):
            item = waveform[b]
            current_samples = item.shape[-1]

            if current_samples == target_samples:
                processed_batch.append(item)
                continue

            if current_samples > target_samples:
                if crop == "start":
                    processed = item[..., current_samples - target_samples:]
                else:
                    processed = item[..., :target_samples]
            else:
                pad_amount = target_samples - current_samples
                silence = torch.zeros((item.shape[0], pad_amount), device=device, dtype=item.dtype)
                if pad == "start":
                    processed = torch.cat((silence, item), dim=-1)
                else:
                    processed = torch.cat((item, silence), dim=-1)

            processed_batch.append(processed)

        # Stack back into a batch tensor
        out_tensor = torch.stack(processed_batch).to(device)

        out_audio = {
            "waveform": out_tensor,
            "sample_rate": sr
        }

        return (out_audio,)
