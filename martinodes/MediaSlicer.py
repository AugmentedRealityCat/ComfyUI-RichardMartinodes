from .shared import CATEGORY, list_head_tail

class MediaSlicer:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "optional": {
                "images": ("IMAGE", {}),
                "audio": ("AUDIO", {}),
            },
            "required" : {
                "length_seconds" : ("FLOAT", { "default" : 0.0 }),
                "video_fps" : ("FLOAT", { "default" : 24.0 }),
                "take_from" : (["start", "end"], { "default" : "end" }),
            },
        }

    RETURN_TYPES = ("IMAGE", "AUDIO")
    RETURN_NAMES = ("images", "audio")

    SEARCH_ALIASES = ["trim video", "trim audio", "slice video", "slice audio"]

    FUNCTION = "run"
    CATEGORY = CATEGORY
    DESCRIPTION = "Takes a slice with requested length from the start or the end of the loaded media. If using both audio and video, the inputs must be the same length."

    def run(self,  **kwargs):
        length_seconds = kwargs.get("length_seconds", 0.0)
        video_fps = kwargs.get("video_fps", 24.0)
        take_from = kwargs.get("take_from", "start")
        
        images = kwargs.get("images", None)
        audio = kwargs.get("audio", None)

        out_images = images
        out_audio = audio

        if length_seconds < 0.001:
            return (out_images, out_audio)

        if images is not None:
            frames_to_take = int(length_seconds * video_fps)
            out_images = list_head_tail(images, frames_to_take, take_from)


        # Process Audio
        if audio is not None:
            # ComfyUI AUDIO structure: {"waveform": tensor(batch, channels, samples), "sample_rate": int}
            waveform = audio["waveform"]
            sample_rate = audio["sample_rate"]
            
            samples_to_take = int(length_seconds * sample_rate)

            # permute the waveform to (samples, batch, channels) to slice accordingly.
            # This handles batch processing "vectorially" - by moving the time dimension to the front,
            # we can slice the time for all batch items (and channels) simultaneously without a loop.
            waveform_permuted = waveform.permute(2, 0, 1)
            
            cut_waveform = list_head_tail(waveform_permuted, samples_to_take, take_from)
            
            # Restore original shape (batch, channels, samples)
            new_waveform = cut_waveform.permute(1, 2, 0)
            
            out_audio = {
                "waveform": new_waveform,
                "sample_rate": sample_rate
            }

        return (out_images, out_audio)
