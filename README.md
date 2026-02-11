# ComfyUI-Martinodes

Collection of convenience nodes to avoid long node chains and calculations in ComfyUI when working with videos and audios. Especially useful for extending/prefixing LTX2 videos.

## Installation

You'll need a git client. Open your terminal or command window, navigate to your custom_nodes and run `git clone https://github.com/progmars/ComfyUI-Martinodes.git`

## Dependencies

Depends on librosa for audio resampling operations:

```
pip install librosa
```
or with embedded Python:

```
python -m pip install librosa
```


## Nodes

### Video head or tail (MediaSlicer)
Takes a slice with requested length from the start or the end of the loaded media. If using both audio and video, the inputs must be the same length.

- **Inputs**: `images` (optional), `audio` (optional)
- **Parameters**: 
  - `duration_seconds`: Length of the slice to take.
  - `video_fps`: Frame rate for video calculation.
  - `take_from`: "start" or "end".

### Audio info (AudioInfo)
Retrieves information about the audio, passing the audio through for convenience.

- **Inputs**: `audio`
- **Outputs**: 
  - `duration`: Duration in seconds.
  - `samplerate`: Sample rate in Hz.
  - `channels`: Number of audio channels.

### Resample audio (AudioResampler)
Resamples audio to the target samplerate and channels. Useful when concatenating audios from different sources.

- **Inputs**: `audio`
- **Parameters**: 
  - `samplerate`: Target sample rate in Hz (e.g., 24000, 44100).
  - `channels`: Target channels (1 for Mono, 2 for Stereo).

### Ensure audio duration (AudioTrimExtender)
Makes audio to have the specified duration, cropping or padding with silence as needed.

- **Inputs**: `audio`
- **Parameters**: 
  - `duration_seconds`: Target duration.
  - `pad`: Where to add silence if too short ("start" or "end").
  - `crop`: Where to cut if too long ("start" or "end").

### Concatenate media (MediaOverlappingConcatenator)
Concatenates two videos and/or audios, applying overlapping logic (crossfade or simple join).
If incoming audio channels or samplerates do not match, they will be resampled to the highest samplerate and channels of both audios.

- **Inputs**: `images_1`, `audio_1`, `images_2`, `audio_2` (all optional, but need pairs to work meaningfully)
- **Parameters**: 
  - `overlap_duration_seconds`: Duration of the overlap/crossfade.
  - `video_overlap_prefer`: How to handle video overlap ("crossfade", "images_1", "images_2").
  - `audio_overlap_prefer`: How to handle audio overlap ("crossfade", "audio_1", "audio_2").
