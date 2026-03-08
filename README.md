# coe216-hw3

Simple Python implementation for the COE216 homework.

- Voice Activity Detection (VAD): adaptive short-time energy thresholding with hangover smoothing.
- Voiced/Unvoiced Classification: frame-based decision using zero-crossing rate and energy.

## Steps to Run Locally

Run in the terminal:

```bash
pip install numpy scipy matplotlib
python src/vad_voiced_unvoiced.py assets/audio/your_recording.wav --out-dir outputs
```

Optional parameters:

```bash
python src/vad_voiced_unvoiced.py assets/audio/your_recording.wav --alpha 3.0 --tz 0.12 --out-dir outputs
```

To fill the report table automatically from the generated `summary.txt`:

```bash
python src/fill_report_from_summary.py docs/COE216-HW3-REPORT.docx outputs/summary.txt
```

Generated outputs are written to `outputs/`: `speech_only.wav`, `analysis_plot.png`, and `summary.txt`.

Final report files are in `docs/`:

- `docs/COE216-HW3-REPORT.docx`
- `docs/COE216-HW3-REPORT.pdf`
