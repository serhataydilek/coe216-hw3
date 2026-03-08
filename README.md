# COE216 HW3

Python implementation of the COE216 homework pipeline for speech processing.

## Features

- Voice Activity Detection (VAD) with adaptive short-time energy thresholding
- Voiced/Unvoiced frame classification with zero-crossing rate and energy
- Speech-only waveform export
- Analysis figure export (waveform, energy, ZCR)
- Summary report generation for document filling

## Project Structure

```text
.
|-- assets/
|   |-- audio/
|   |   |-- your_recording.m4a
|   |   `-- your_recording.wav
|   `-- plots/
|       |-- analysis_plot.png
|       |-- feature_comparison.png
|       `-- illustrative_analysis.png
|-- docs/
|   |-- COE216-HW3-REPORT.docx
|   `-- COE216-HW3-REPORT.pdf
|-- outputs/
|   |-- speech_only.wav
|   `-- summary.txt
|-- src/
|   |-- fill_report_from_summary.py
|   `-- vad_voiced_unvoiced.py
`-- README.md
```

## Requirements

- Python 3.10+
- Packages in `requirements.txt`

Install dependencies:

```bash
pip install -r requirements.txt
```

## Quick Start

Run VAD and voiced/unvoiced analysis:

```bash
python src/vad_voiced_unvoiced.py assets/audio/your_recording.wav --out-dir outputs
```

Optional thresholds:

```bash
python src/vad_voiced_unvoiced.py assets/audio/your_recording.wav --alpha 3.0 --tz 0.12 --out-dir outputs
```

This command generates:

- `outputs/speech_only.wav`
- `outputs/summary.txt`
- `outputs/analysis_plot.png`

## Fill Report Automatically

After `outputs/summary.txt` is generated, fill placeholders in the Word report:

```bash
python src/fill_report_from_summary.py docs/COE216-HW3-REPORT.docx outputs/summary.txt
```

## Notes

- If you get an "access/permission" error while editing the DOCX, close Microsoft Word completely and remove any temporary lock file like `~$*.docx`.
- Keep report files under `docs/` and generated runtime outputs under `outputs/`.
