import torch
from .shared import MINIMAX_H3_PARAMS


def concat_av_latents(video_fps, overlap_duration_seconds, video_overlap_resolve, audio_overlap_resolve, av_latent_1=None, av_latent_2=None):
    if av_latent_1 is None and av_latent_2 is None:
        return None
    if av_latent_1 is None:
        return av_latent_2
    if av_latent_2 is None:
        return av_latent_1

    # Convert requested overlap duration into latent token counts using the same
    # snapping rules the extender uses, so overlaps stay aligned to the model's temporal compression.
    video_overlap_tokens = 0
    audio_overlap_tokens = 0
    if overlap_duration_seconds > 0:
        audio_token_rate = MINIMAX_H3_PARAMS["audio_token_rate"]
        frame_multi = MINIMAX_H3_PARAMS["frame_multi"]
        frame_offset = MINIMAX_H3_PARAMS["frame_offset"]
        min_latent_temporal_tokens = MINIMAX_H3_PARAMS["min_latent_temporal_tokens"]

        target_frames = overlap_duration_seconds * video_fps
        k = max(0, int(round((target_frames - frame_offset) / frame_multi)))
        snapped_video_frames = int(k * frame_multi + frame_offset)

        video_overlap_tokens = int(k * frame_offset + min_latent_temporal_tokens)
        audio_overlap_tokens = int(round(snapped_video_frames * (audio_token_rate / video_fps)))

    samples_1 = av_latent_1["samples"]
    samples_2 = av_latent_2["samples"]

    video_1, audio_1 = samples_1.unbind()
    video_2, audio_2 = samples_2.unbind()

    dims_v = len(video_1.shape)
    t_dim_v = 2 if dims_v >= 3 else 0
    dims_a = len(audio_1.shape)
    t_dim_a = -1

    video_overlap_tokens = min(video_overlap_tokens, video_1.shape[t_dim_v], video_2.shape[t_dim_v])
    audio_overlap_tokens = min(audio_overlap_tokens, audio_1.shape[t_dim_a], audio_2.shape[t_dim_a])

    combined_v = _concat_with_overlap(video_1, video_2, dims_v, t_dim_v, video_overlap_tokens, video_overlap_resolve)
    combined_a = _concat_with_overlap(audio_1, audio_2, dims_a, t_dim_a, audio_overlap_tokens, audio_overlap_resolve)

    out_av = av_latent_1.copy()
    out_av["samples"] = type(samples_1)([combined_v, combined_a])
    out_av.pop("noise_mask", None)

    return out_av


def _concat_with_overlap(tensor_1, tensor_2, dims, t_dim, overlap_tokens, resolve_method):
    if overlap_tokens <= 0:
        return torch.cat((tensor_1, tensor_2), dim=t_dim)

    idx_pre = [slice(None)] * dims
    idx_pre[t_dim] = slice(None, -overlap_tokens)
    idx_post = [slice(None)] * dims
    idx_post[t_dim] = slice(overlap_tokens, None)
    idx_ov1 = [slice(None)] * dims
    idx_ov1[t_dim] = slice(-overlap_tokens, None)
    idx_ov2 = [slice(None)] * dims
    idx_ov2[t_dim] = slice(None, overlap_tokens)

    pre = tensor_1[tuple(idx_pre)]
    post = tensor_2[tuple(idx_post)]
    overlap_1 = tensor_1[tuple(idx_ov1)]
    overlap_2 = tensor_2[tuple(idx_ov2)]

    if resolve_method == "av_latent_1":
        overlap_part = overlap_1
    elif resolve_method == "av_latent_2":
        overlap_part = overlap_2
    else:  # crossfade
        alpha_shape = [1] * dims
        alpha_shape[t_dim] = overlap_tokens
        alpha = torch.linspace(0, 1, overlap_tokens, device=tensor_1.device).view(alpha_shape)
        overlap_part = overlap_1 * (1.0 - alpha) + overlap_2 * alpha

    return torch.cat((pre, overlap_part, post), dim=t_dim)
