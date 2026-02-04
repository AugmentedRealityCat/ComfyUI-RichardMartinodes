from .shared import CATEGORY, resample_audio

class AudioResampler:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "audio": ("AUDIO", {}),
                "samplerate" : ("INT", { "default" : 24000 }),
                "channels" : ("INT", { "default" : 1 })
            },
        }

    RETURN_TYPES = ("AUDIO",)
    RETURN_NAMES = ("audio",)

    SEARCH_ALIASES = ["resample audio"]

    FUNCTION = "run"
    CATEGORY = CATEGORY
    DESCRIPTION = "Resamples audio to the target samplerate and channels. Useful when concatenating audios from different sources."

    def run(self,  **kwargs):

        samplerate = kwargs.get("samplerate", 24000)
        channels = kwargs.get("channels", 1) 
        if channels < 1 or channels > 2:
             raise Exception("Only 1 or 2 channels are supported.")
       
        # ComfyUI AUDIO structure: {"waveform": tensor(batch, channels, samples), "sample_rate": int}
        audio = kwargs.get("audio", None)

        if audio is None:
             raise Exception("No audio provided to resample.")

        out_audio = resample_audio(audio, samplerate, channels)

        return (out_audio,)
