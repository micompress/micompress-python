# micompress

> Compress **images, PDFs, video, audio, documents & archives** from your terminal or Python.
> Powered by [**micompress.com**](https://micompress.com/?utm_source=pypi&utm_medium=cli&utm_campaign=extend).

A tiny **zero-dependency** client (standard library only) that sends your file to the
MiCompress engine and writes back the optimized result.

```bash
pip install micompress
```

## CLI usage

```bash
micompress photo.jpg                 # → photo-min.jpg
micompress *.png --preset extreme
micompress report.pdf slides.pptx -o out/
micompress big.jpg --max-width 1920 --json
```

| Option | Description |
|--------|-------------|
| `-o, --output DIR` | Write results to a directory (default: alongside input, `-min` suffix) |
| `-p, --preset` | `lossless` · `recommended` (default) · `extreme` |
| `--max-width PX` | Resize images down to a maximum width |
| `--token JWT` | Auth token for higher size limits |
| `--api URL` | Override API base URL |
| `--json` | Machine-readable output |
| `-q, --quiet` | Only print errors |

## Python API

```python
from micompress import compress_file

data, meta = compress_file("photo.jpg", preset="extreme")
open("photo-min.jpg", "wb").write(data)
print(meta["savedPercent"], "% smaller")
```

## Supported formats

Image (jpg, png, webp, gif, tiff, avif, svg, heic, psd, raw…), PDF & Office docs,
video (mp4, mov, mkv, webm…), audio (mp3, wav, flac…), archives (zip, 7z, tar, gz).
Full list: **https://micompress.com/all-tools**

## Requirements

Python **3.8+**. No third-party dependencies.

## License

MIT © [MiCompress](https://micompress.com)

---

<sub>Prefer a web UI or bigger batches? Use **[micompress.com](https://micompress.com/?utm_source=pypi&utm_medium=cli&utm_campaign=extend)**.</sub>
