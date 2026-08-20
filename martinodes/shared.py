import torch
import numpy as np

try:
    # will ignore in case audio functions are never called
    import librosa
except ImportError:
    pass

CATEGORY = "martinodes"

def list_head_tail(list, take_count, start_end):

    total = list.shape[0]
    take_count = min(take_count, total)

    if start_end == "start":
        new_list = list[:take_count]
    else:
        new_list = list[-take_count:]

    return new_list

def resample_audio(audio, samplerate, channels):
 
    waveform = audio["waveform"]
    orig_sr = audio["sample_rate"]

    batch_size = waveform.shape[0]
    
    # We process things as numpy because librosa expects numpy
    # If we decide to use torchaudio later, it would be different, but prompt asked for librosa.
    
    device = waveform.device
    resampled_batch = []

    for b in range(batch_size):
        # Take specific item from batch, convert to numpy
        # Waveform shape for librosa needs to be (channels, time) or just (time) for mono
        item_np = waveform[b].cpu().numpy()
        
        # Handle Channels logic before resampling or after?
        # Librosa resample usually works on mono or multi-channel if passed correctly (axis argument)
        # but usually it's safer to resample individual channels or rely on librosa's ability.
        
        # Let's resample first to keep the speed consistent for original channels
        if orig_sr != samplerate:
            # librosa.resample takes (..., n_samples)
            item_resampled = librosa.resample(item_np, orig_sr=orig_sr, target_sr=samplerate, axis=-1)
        else:
            item_resampled = item_np
        
        # Now handle channel count adjustment
        current_channels = item_resampled.shape[0]
        if current_channels > channels:
            # if input has more channels than channels arg, just take the first one(s)
            item_resampled = item_resampled[:channels, :]
        elif current_channels < channels:
            # if input has fewer channels than channels arg, just duplicate the last one
            diff = channels - current_channels
            last_channel = item_resampled[-1:, :]
            to_concat = [item_resampled]
            for _ in range(diff):
                to_concat.append(last_channel)
            item_resampled = np.concatenate(to_concat, axis=0)

        resampled_batch.append(torch.from_numpy(item_resampled))

    # Stack back into a batch tensor
    out_tensor = torch.stack(resampled_batch).to(device)

    out_audio = {
        "waveform": out_tensor,
        "sample_rate": samplerate
    }

    return out_audio
