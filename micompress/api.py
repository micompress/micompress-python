"""Thin client for the MiCompress public compression API (stdlib only)."""

import json
import os
import uuid
import urllib.request
import urllib.error

from .categories import category_for, endpoint_path, ext_of

DEFAULT_BASE = "https://micompress.com"
# Attribution so we can measure traffic driven by the Python CLI.
UTM = "utm_source=pypi&utm_medium=cli&utm_campaign=extend"
# A branded User-Agent identifies the client and avoids default urllib UA being
# blocked by the WAF (Cloudflare 403s "Python-urllib/*").
USER_AGENT = "micompress-python/0.1.0 (+https://micompress.com)"


class CompressError(Exception):
    def __init__(self, message, code=None):
        super().__init__(message)
        self.code = code


def _encode_multipart(text_fields, file_field, filename, content):
    boundary = "----MiCompress" + uuid.uuid4().hex
    crlf = b"\r\n"
    body = bytearray()
    for name, value in text_fields.items():
        if value is None:
            continue
        body += b"--" + boundary.encode() + crlf
        body += ('Content-Disposition: form-data; name="%s"' % name).encode() + crlf + crlf
        body += str(value).encode() + crlf
    body += b"--" + boundary.encode() + crlf
    body += ('Content-Disposition: form-data; name="%s"; filename="%s"'
             % (file_field, filename)).encode() + crlf
    body += b"Content-Type: application/octet-stream" + crlf + crlf
    body += content + crlf
    body += b"--" + boundary.encode() + b"--" + crlf
    return boundary, bytes(body)


def compress_file(input_path, base_url=DEFAULT_BASE, preset=None, max_width=None,
                  token=None, timeout=120):
    """Compress a single file. Returns (data_bytes, meta_dict)."""
    base_url = (base_url or DEFAULT_BASE).rstrip("/")
    filename = os.path.basename(input_path)
    category = category_for(filename)
    if not category:
        raise CompressError(
            'Unsupported file type ".%s". See %s/all-tools'
            % (ext_of(filename) or "?", base_url), "UNSUPPORTED")

    if not os.path.isfile(input_path):
        raise CompressError("File not found: %s" % input_path, "ENOENT")

    with open(input_path, "rb") as fh:
        content = fh.read()

    text_fields = {}
    if preset:
        text_fields["preset"] = preset
    if max_width:
        text_fields["maxWidth"] = int(max_width)

    boundary, body = _encode_multipart(text_fields, "file", filename, content)
    url = "%s/%s/compress" % (base_url, endpoint_path(category))
    headers = {
        "Content-Type": "multipart/form-data; boundary=%s" % boundary,
        "Accept": "application/json",
        "User-Agent": USER_AGENT,
    }
    if token:
        headers["Authorization"] = "Bearer %s" % token

    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", "replace")
        try:
            payload = json.loads(raw)
        except ValueError:
            raise CompressError("HTTP %s" % e.code, "API_ERROR")
        if e.code == 401 and payload.get("code") == "LOGIN_REQUIRED":
            raise CompressError(
                "File exceeds the anonymous size limit. Pass --token <jwt> (log in at %s) "
                "or compress it online at %s/?%s" % (base_url, base_url, UTM),
                "LOGIN_REQUIRED")
        raise CompressError(payload.get("error", "HTTP %s" % e.code),
                            payload.get("code", "API_ERROR"))
    except urllib.error.URLError as e:
        raise CompressError("Network error: %s" % e.reason, "NETWORK")

    if not payload.get("success"):
        raise CompressError(payload.get("error", "Compression failed"),
                            payload.get("code", "API_ERROR"))

    # Step 2: download the compressed bytes.
    dl_url = base_url + payload["downloadUrl"]
    dl_req = urllib.request.Request(dl_url)
    dl_req.add_header("User-Agent", USER_AGENT)
    if token:
        dl_req.add_header("Authorization", "Bearer %s" % token)
    try:
        with urllib.request.urlopen(dl_req, timeout=timeout) as resp:
            data = resp.read()
    except urllib.error.URLError as e:
        raise CompressError("Download failed: %s" % e, "DOWNLOAD")

    meta = {
        "category": category,
        "inputSize": payload.get("inputSize"),
        "outputSize": payload.get("outputSize"),
        "savedBytes": payload.get("savedBytes"),
        "savedPercent": payload.get("savedPercent"),
        "format": payload.get("format"),
        "originalName": payload.get("originalName", filename),
        "note": payload.get("note"),
    }
    return data, meta
