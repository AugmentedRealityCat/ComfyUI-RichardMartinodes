import os
import torch
import safetensors.torch
import folder_paths
import comfy.nested_tensor
from .shared import CATEGORY

class SaveAVLatent:
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()

    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
            "av_latent": ("LATENT", ),
            "filename_prefix": ("STRING", {"default": "av_latents/latent"})
        }}

    RETURN_TYPES = ()
    FUNCTION = "save"
    OUTPUT_NODE = True
    CATEGORY = CATEGORY

    def save(self, av_latent, filename_prefix):
        # Leverage ComfyUI API for standard subfolder, filename, and incrementing counter logic
        full_output_folder, filename, counter, subfolder, _ = folder_paths.get_save_image_path(
            filename_prefix, self.output_dir
        )
        
        output_filename = f"{filename}_{counter:05d}.avlatent"
        output_path = os.path.join(full_output_folder, output_filename)

        output_dict = {}
        
        samples = av_latent.get("samples")
        if samples is not None:
            if isinstance(samples, comfy.nested_tensor.NestedTensor) or getattr(samples, "is_nested", False):
                tensors = list(samples.unbind())
            elif isinstance(samples, torch.Tensor):
                tensors = [samples]
            else:
                tensors = samples if isinstance(samples, list) else [samples]
                
            output_dict["tensor_count"] = torch.tensor([len(tensors)], dtype=torch.int32)
            for i, t in enumerate(tensors):
                output_dict[f"latent_{i}"] = t.detach().contiguous()

        # Save purely as safetensors with no metadata
        safetensors.torch.save_file(output_dict, output_path)

        return {"ui": {"text": f"Saved to {output_path}"}}


# Define a sentinel value that sorts to the top of the dropdown
# and lets unselect anything
NONE_SELECTION = " [NONE]"

def get_saved_latents():
    output_dir = folder_paths.get_output_directory()
    files = [NONE_SELECTION]
    
    if not os.path.exists(output_dir):
        return files
        
    # Recursively scan the output directory for safetensors
    for root, _, filenames in os.walk(output_dir):
        for f in filenames:
            if f.endswith(".avlatent"):
                # Store paths relative to the output directory
                rel_path = os.path.relpath(os.path.join(root, f), output_dir)
                # Normalize slashes for ComfyUI cross-platform consistency
                files.append(rel_path.replace("\\", "/"))
                
    return sorted(files)


class LoadAVLatent:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
            "file_path": (get_saved_latents(), )
        }}

    RETURN_TYPES = ("LATENT", )
    RETURN_NAMES = ("av_latent", )
    FUNCTION = "load"
    CATEGORY = CATEGORY

    def load(self, file_path):
        
        # 1. Handle the explicit "None" selection or empty input
        if not file_path or file_path == NONE_SELECTION:
            return (None, )

        # 2. Reconstruct path relative to the output directory
        target_path = os.path.join(folder_paths.get_output_directory(), file_path)
        
        # 3. Fallback to absolute path if passed via converted string input widget
        if not os.path.exists(target_path) and os.path.isabs(file_path):
            target_path = file_path

        if not os.path.exists(target_path):
            print(f"LoadAVLatent: File not found at '{target_path}'. Passing None.")
            return (None, )

        try:
            data = safetensors.torch.load_file(target_path, device="cpu")
            av_latent = {}

            # Reconstruct main samples sequence
            if "tensor_count" in data:
                count = int(data["tensor_count"].item())
                tensors = [data[f"latent_{i}"].float() for i in range(count)]
                av_latent["samples"] = tensors[0] if count == 1 else comfy.nested_tensor.NestedTensor(tensors)

            return (av_latent, )

        except Exception as e:
            print(f"LoadAVLatent: Failed to load safetensors. Passing None. Error: {e}")
            return (None, )