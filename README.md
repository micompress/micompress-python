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
| `--api-key KEY` | Personal API key from [micompress.com/account](https://micompress.com/account) (or set `MICOMPRESS_API_KEY`) |
| `--token JWT` | Legacy login token; prefer `--api-key` |
| `--api URL` | Override API base URL |
| `--json` | Machine-readable output |
| `-q, --quiet` | Only print errors |

## API key

Small files work without an account. For bigger files and a monthly allowance, use your
personal API key (`mc_…`), shown on your [account page](https://micompress.com/account) —
creating an account is free.

```bash
export MICOMPRESS_API_KEY=mc_your_key_here
micompress big-video.mp4
# or per command (the flag wins over the environment variable)
micompress big-video.mp4 --api-key mc_your_key_here
```

| Plan | Compressions per month | Notes |
|------|------------------------|-------|
| No key (anonymous) | Anonymous limits | Small files only |
| Free account | 50 via the API | Files up to 100 MB |
| Plus ($9.99/mo) | 1,000 | Shared with website usage |
| Pro ($19.99/mo) | 5,000 | Shared with website usage |

When the allowance is used up the CLI reports `API_QUOTA_REACHED` (free) or
`USAGE_LIMIT_REACHED` (paid). See [micompress.com/plans](https://micompress.com/plans).
Keep the key secret — anyone who has it can spend your quota.

## Python API

```python
from micompress import compress_file

data, meta = compress_file("photo.jpg", preset="extreme")
open("photo-min.jpg", "wb").write(data)
print(meta["savedPercent"], "% smaller")

# With an API key (sent as the X-API-Key header)
data, meta = compress_file("big.pdf", api_key="mc_your_key_here")
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
