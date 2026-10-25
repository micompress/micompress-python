"""micompress command-line interface."""

import argparse
import json as _json
import os
import sys

from . import __version__
from .api import compress_file, CompressError, DEFAULT_BASE, UTM


def human_size(n):
    if n is None:
        return "?"
    units = ["B", "KB", "MB", "GB"]
    i = 0
    v = float(n)
    while v >= 1024 and i < len(units) - 1:
        v /= 1024
        i += 1
    return "%d%s" % (round(v), units[i]) if i == 0 else "%.1f%s" % (v, units[i])


def out_path_for(input_path, output_dir, suffix):
    base = os.path.basename(input_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        return os.path.join(output_dir, base)
    root, ext = os.path.splitext(input_path)
    return "%s%s%s" % (root, suffix, ext)


def build_parser():
    p = argparse.ArgumentParser(
        prog="micompress",
        description="Compress images, PDFs, video, audio, documents & archives "
                    "via micompress.com.",
        epilog="Powered by micompress.com — need more formats or bigger files? "
               "%s/?%s" % (DEFAULT_BASE, UTM),
    )
    p.add_argument("files", nargs="*", help="File(s) to compress")
    p.add_argument("-o", "--output", metavar="DIR", help="Output directory")
    p.add_argument("-p", "--preset", choices=["lossless", "recommended", "extreme"],
                   default="recommended", help="Compression strength")
    p.add_argument("--max-width", type=int, metavar="PX",
                   help="Resize images down to this max width")
    p.add_argument("--api-key", metavar="KEY",
                   help="Personal API key from micompress.com/account "
                        "(default: $MICOMPRESS_API_KEY)")
    p.add_argument("--token", help="Legacy login token (JWT); prefer --api-key")
    p.add_argument("--api", default=DEFAULT_BASE, help="API base URL")
    p.add_argument("--suffix", default="-min", help='Default output suffix (default "-min")')
    p.add_argument("--json", action="store_true", help="Machine-readable JSON output")
    p.add_argument("-q", "--quiet", action="store_true", help="Only print errors")
    p.add_argument("-v", "--version", action="version", version=__version__)
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    if not args.files:
        build_parser().print_help()
        return 1

    # Flag wins over the environment variable.
    api_key = (args.api_key or os.environ.get("MICOMPRESS_API_KEY") or "").strip() or None

    results = []
    failed = 0
    total_in = 0
    total_out = 0

    for f in args.files:
        try:
            data, meta = compress_file(
                f, base_url=args.api, preset=args.preset,
                max_width=args.max_width, token=args.token,
                api_key=api_key,
            )
            dest = out_path_for(f, args.output, args.suffix)
            with open(dest, "wb") as fh:
                fh.write(data)
            total_in += meta["inputSize"] or 0
            total_out += meta["outputSize"] or 0
            results.append(dict(file=f, dest=dest, ok=True, **meta))
            if not args.quiet and not args.json:
                print("✔ %s → %s  %s → %s (-%s%%)" % (
                    f, dest, human_size(meta["inputSize"]),
                    human_size(meta["outputSize"]), meta["savedPercent"]))
        except CompressError as e:
            failed += 1
            results.append(dict(file=f, ok=False, error=str(e), code=e.code))
            if not args.json:
                sys.stderr.write("✗ %s: %s\n" % (f, e))
        except OSError as e:
            failed += 1
            results.append(dict(file=f, ok=False, error=str(e)))
            if not args.json:
                sys.stderr.write("✗ %s: %s\n" % (f, e))

    if args.json:
        print(_json.dumps(dict(results=results, totalIn=total_in,
                               totalOut=total_out, failed=failed), indent=2))
    elif not args.quiet and len(args.files) > 1:
        ok = len(args.files) - failed
        pct = round((1 - total_out / total_in) * 100) if total_in else 0
        print("\n%d/%d done — %s → %s (-%d%%)  · powered by micompress.com" % (
            ok, len(args.files), human_size(total_in), human_size(total_out), pct))

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
