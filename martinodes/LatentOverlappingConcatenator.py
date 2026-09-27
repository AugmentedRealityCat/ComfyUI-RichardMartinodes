import os
import folder_paths
from .shared import CATEGORY
from .latentops import concat_av_latents
from .LatentAVLoadSave import LoadAVLatent


class LatentOverlappingConcatenator:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "optional": {
                "av_latent_1": ("LATENT", {}),
                "av_latent_2": ("LATENT", {}),
            },
            "required": {
                "video_fps": ("FLOAT", {"default": 24.0, "min": 1.0, "max": 120.0, "step": 1.0}),
                "overlap_duration_seconds": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 60.0, "step": 0.1}),
                "video_overlap_resolve": (["av_latent_1", "av_latent_2", "crossfade"], {"default": "crossfade"}),
                "audio_overlap_resolve": (["av_latent_1", "av_latent_2", "crossfade"], {"default": "crossfade"}),
            },
        }

    RETURN_TYPES = ("LATENT", )
    RETURN_NAMES = ("av_latent", )

    SEARCH_ALIASES = ["concatenate latent", "concatenate video audio latent", "join av latents"]

    FUNCTION = "run"
    CATEGORY = CATEGORY
    DESCRIPTION = "Concatenates two video+audio latents, applying overlapping logic."

    def run(self, video_fps, overlap_duration_seconds, video_overlap_resolve, audio_overlap_resolve, av_latent_1=None, av_latent_2=None):
        out_av = concat_av_latents(video_fps, overlap_duration_seconds, video_overlap_resolve, audio_overlap_resolve, av_latent_1, av_latent_2)
        return (out_av, )


class LatentFolderOverlappingConcatenator:
    # Maps UI options to the pairwise resolve names used by concat_av_latents
    RESOLVE_MAP = {"previous": "av_latent_1", "next": "av_latent_2", "crossfade": "crossfade"}

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "folder_path": ("STRING", {"default": "av_latents"}),
                "video_fps": ("FLOAT", {"default": 24.0, "min": 1.0, "max": 120.0, "step": 1.0}),
                "overlap_duration_seconds": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 60.0, "step": 0.1}),
                "video_overlap_resolve": (["previous", "next", "crossfade"], {"default": "crossfade"}),
                "audio_overlap_resolve": (["previous", "next", "crossfade"], {"default": "crossfade"}),
            },
        }

    RETURN_TYPES = ("LATENT", )
    RETURN_NAMES = ("av_latent", )

    SEARCH_ALIASES = ["concatenate latent folder", "join av latents folder", "concatenate avlatent files"]

    FUNCTION = "run"
    CATEGORY = CATEGORY
    DESCRIPTION = "Concatenates all .avlatent files in a folder (ascending name order), applying overlapping logic. Relative paths are resolved against the ComfyUI output directory."

    @classmethod
    def IS_CHANGED(s, folder_path, **kwargs):
        folder = s._resolve_folder(folder_path)
        if not os.path.isdir(folder):
            return ""
        return str([(f, os.path.getmtime(os.path.join(folder, f))) for f in s._list_files(folder)])

    @staticmethod
    def _resolve_folder(folder_path):
        folder_path = folder_path.strip()
        if os.path.isabs(folder_path):
            return folder_path
        return os.path.join(folder_paths.get_output_directory(), folder_path)

    @staticmethod
    def _list_files(folder):
        return sorted(f for f in os.listdir(folder) if f.lower().endswith(".avlatent") and os.path.isfile(os.path.join(folder, f)))


    def run(self, folder_path, video_fps, overlap_duration_seconds, video_overlap_resolve, audio_overlap_resolve):
        folder = self._resolve_folder(folder_path)
        if not os.path.isdir(folder):
            raise FileNotFoundError(f"LatentFolderOverlappingConcatenator: Folder not found: '{folder}'")

        files = self._list_files(folder)
        if not files:
            raise FileNotFoundError(f"LatentFolderOverlappingConcatenator: No .avlatent files in '{folder}'")

        video_resolve = self.RESOLVE_MAP[video_overlap_resolve]
        audio_resolve = self.RESOLVE_MAP[audio_overlap_resolve]
        loader = LoadAVLatent()

        out_av = None
        for f in files:
            (av_latent, ) = loader.load(os.path.join(folder, f))
            if av_latent is None:
                raise RuntimeError(f"LatentFolderOverlappingConcatenator: Failed to load '{f}'")
            out_av = concat_av_latents(video_fps, overlap_duration_seconds, video_resolve, audio_resolve, av_latent_1=out_av, av_latent_2=av_latent)

        return (out_av, )