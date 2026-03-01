# Synthwave Thumbnail Generator for Kleiner'82

A Python tool for generating YouTube thumbnails in two styles: a retro synthwave aesthetic and a futuristic AI/tech aesthetic.

## Requirements

- Python 3.8+
- Pillow

```
pip install Pillow
```

## Usage

### Synthwave thumbnail

Generates a retro 80s synthwave-style thumbnail with a sunset, perspective grid, mountains, and neon text.

```
python synthwave_thumbnail.py
```

### Claude Code thumbnail

Generates a futuristic tech-themed thumbnail with a background photo, glow text, and a pill badge.

```
python generate_thumbnail.py
```

Output is saved to `generated-images/<timestamp>/` with a unique folder per run.

## Configuration

Edit the constants at the top of each script to customise the output:

**`synthwave_thumbnail.py`**
```python
BAND_NAME   = "KLEINER'82"
TRACK_TITLE = "NEON SHADOWS"
SUBTITLE    = "SYNTHWAVE"
```

**`generate_thumbnail.py`** — edit the text draw calls directly (title, subtitle, badge text).

## Output

- Resolution: 1280 × 720 (standard YouTube thumbnail size)
- Format: PNG
