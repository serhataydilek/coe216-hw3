import argparse
from pathlib import Path
import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt

def read_wav(path):
    fs, x = wavfile.read(path)
    if x.ndim == 2:
        x = x.mean(axis=1)
    x = x.astype(np.float64)
    if np.max(np.abs(x)) > 0:
        x = x / np.max(np.abs(x))
    return fs, x

def frame_signal(x, frame_len, hop):
    n_frames = 1 + max(0, (len(x) - frame_len) // hop)
    frames = np.zeros((n_frames, frame_len))
    for i in range(n_frames):
        start = i * hop
        frames[i] = x[start:start + frame_len]
    return frames

def zcr(frame):
    return np.sum(np.abs(np.diff(np.sign(frame)))) / (2 * len(frame))

def overlap_add(frames, hop):
    n_frames, frame_len = frames.shape
    out = np.zeros((n_frames - 1) * hop + frame_len)
    weight = np.zeros_like(out)
    for i in range(n_frames):
        start = i * hop
        out[start:start + frame_len] += frames[i]
        weight[start:start + frame_len] += 1.0
    weight[weight == 0] = 1.0
    return out / weight

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("wav_path", help="Input wav path")
    parser.add_argument("--alpha", type=float, default=3.0, help="Noise threshold multiplier")
    parser.add_argument("--tz", type=float, default=0.12, help="ZCR threshold")
    args = parser.parse_args()

    wav_path = Path(args.wav_path)
    fs, x = read_wav(wav_path)

    frame_len = int(0.02 * fs)
    hop = int(0.01 * fs)
    frames = frame_signal(x, frame_len, hop)
    win = np.hamming(frame_len)
    wframes = frames * win

    energy = np.sum(wframes ** 2, axis=1)
    zcr_vals = np.array([zcr(fr) for fr in wframes])

    n_noise = max(1, int(0.2 / 0.01))
    noise_e = energy[:n_noise]
    T_energy = noise_e.mean() + args.alpha * noise_e.std()
    speech = (energy > T_energy).astype(int)

    for i in range(3, len(speech)):
        if speech[i] == 0 and speech[i - 3:i].sum() >= 2:
            speech[i] = 1

    voiced = np.zeros_like(speech)
    med_energy = np.median(energy[speech == 1]) if np.any(speech == 1) else 0.0
    voiced[(speech == 1) & (zcr_vals < args.tz) & (energy > med_energy * 0.6)] = 1
    speech_frames = wframes[speech == 1]
    speech_only = overlap_add(speech_frames, hop) if len(speech_frames) else np.array([], dtype=float)

    out_dir = wav_path.parent
    if len(speech_only):
        wavfile.write(out_dir / "speech_only.wav", fs, np.int16(np.clip(speech_only, -1, 1) * 32767))

    original_duration = len(x) / fs
    speech_duration = len(speech_only) / fs if len(speech_only) else 0.0
    removed = original_duration - speech_duration
    compression = 100.0 * removed / original_duration if original_duration > 0 else 0.0

    times = (np.arange(len(energy)) * hop + frame_len / 2) / fs
    t = np.arange(len(x)) / fs

    plt.figure(figsize=(10, 6))
    ax1 = plt.subplot(311)
    ax1.plot(t, x, linewidth=0.7)
    for i in range(len(times)):
        if speech[i]:
            c = "green" if voiced[i] else "gold"
            ax1.axvspan(times[i] - 0.01, times[i] + 0.01, color=c, alpha=0.25)
    ax1.set_title("Original waveform with VAD/V-UV mask")
    ax1.set_ylabel("Amplitude")

    ax2 = plt.subplot(312, sharex=ax1)
    ax2.plot(times, energy, linewidth=0.9)
    ax2.axhline(T_energy, linestyle="--", linewidth=0.8)
    ax2.set_ylabel("Energy")

    ax3 = plt.subplot(313, sharex=ax1)
    ax3.plot(times, zcr_vals, linewidth=0.9)
    ax3.axhline(args.tz, linestyle="--", linewidth=0.8)
    ax3.set_ylabel("ZCR")
    ax3.set_xlabel("Time (s)")
    plt.tight_layout()
    plt.savefig(out_dir / "analysis_plot.png", dpi=220)

    with open(out_dir / "summary.txt", "w", encoding="utf-8") as f:
        f.write(f"Sampling rate: {fs}\n")
        f.write(f"Original duration (s): {original_duration:.3f}\n")
        f.write(f"Shortened duration (s): {speech_duration:.3f}\n")
        f.write(f"Removed duration (s): {removed:.3f}\n")
        f.write(f"Compression ratio (%): {compression:.2f}\n")
        f.write(f"Energy threshold: {T_energy:.6f}\n")
        f.write(f"ZCR threshold: {args.tz:.4f}\n")

if __name__ == "__main__":
    main()
