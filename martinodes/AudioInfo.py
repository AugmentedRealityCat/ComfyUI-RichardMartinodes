from .shared import CATEGORY

class AudioInfo:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "audio": ("AUDIO", {}),
            },
        }

    RETURN_TYPES = ("AUDIO", "FLOAT", "INT", "INT")
    RETURN_NAMES = ("audio", "duration", "samplerate", "channels")

    SEARCH_ALIASES = ["audio info"]

    FUNCTION = "run"
    CATEGORY = CATEGORY
    DESCRIPTION = "Retrieves information about the audio, passing the audio through for convenience."

    def run(self,  **kwargs):
        audio = kwargs.get("audio", None)
        if audio is None:
             raise Exception("No audio provided.")

        # ComfyUI AUDIO structure: {"waveform": tensor(batch, channels, samples), "sample_rate": int}
        waveform = audio["waveform"]
        samplerate = audio["sample_rate"]

        if waveform is None:
             raise Exception("Audio waveform is missing.")
        
        # Calculate info
        # shape is (batch, channels, samples)
        # Note: ComfyUI batches are padded to the same length, so this duration applies to the entire batch tensor.
        shape = waveform.shape
        channels = shape[-2]
        sample_count = shape[-1]
        
        duration = float(sample_count) / float(samplerate)

        return (audio, duration, samplerate, channels)
