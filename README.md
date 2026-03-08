# coe216-hw3

Simple Python implementation for the COE216 homework.

- Voice Activity Detection (VAD): adaptive short-time energy thresholding with hangover smoothing.
- Voiced/Unvoiced Classification: frame-based decision using zero-crossing rate and energy.

## Steps to Run Locally

Run in the terminal:

```bash
pip install numpy scipy matplotlib
python vad_voiced_unvoiced.py your_recording.wav
```

Optional parameters:

```bash
python vad_voiced_unvoiced.py your_recording.wav --alpha 3.0 --tz 0.12
```

To fill the report table automatically from the generated `summary.txt`:

```bash
python fill_report_from_summary.py HW3_Complete_Report.docx summary.txt
```

Generated outputs are written next to the input WAV file: `speech_only.wav`, `analysis_plot.png`, and `summary.txt`.
