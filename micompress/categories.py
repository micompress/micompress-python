"""File extension -> MiCompress category routing.

Authoritative source on the server: services/formatDetector.js + routes/category.js.
"""

EXT_CATEGORY = {
    # image
    "jpg": "image", "jpeg": "image", "png": "image", "webp": "image", "gif": "image",
    "bmp": "image", "tiff": "image", "tif": "image", "avif": "image", "svg": "image",
    "heic": "image", "heif": "image", "ico": "image", "psd": "image", "dng": "image",
    "raw": "image", "cr2": "image", "arw": "image", "nef": "image",
    # video
    "mp4": "video", "mov": "video", "avi": "video", "mkv": "video", "webm": "video",
    "mpeg": "video", "mpg": "video", "m4v": "video", "wmv": "video", "flv": "video", "3gp": "video",
    # audio
    "mp3": "audio", "wav": "audio", "flac": "audio", "ogg": "audio", "m4a": "audio",
    "aac": "audio", "wma": "audio", "opus": "audio",
    # pdf (dedicated /pdf-compressors path)
    "pdf": "pdf",
    # document
    "csv": "document", "json": "document", "xml": "document", "md": "document",
    "odt": "document", "ods": "document", "docx": "document", "doc": "document",
    "ppt": "document", "pptx": "document", "xls": "document", "xlsx": "document",
    "epub": "document", "html": "document", "htm": "document", "hwp": "document",
    "txt": "document", "rtf": "document",
    # archive
    "zip": "archive", "7z": "archive", "tar": "archive", "gz": "archive",
    "tgz": "archive", "rar": "archive",
}

CATEGORY_PATH = {
    "image": "image-compressors",
    "video": "video-compressors",
    "audio": "audio-compressors",
    "document": "document-compressors",
    "pdf": "pdf-compressors",
    "archive": "archive-compressors",
}


def ext_of(filename):
    name = filename.rsplit("/", 1)[-1]
    if "." not in name:
        return ""
    return name.rsplit(".", 1)[-1].lower()


def category_for(filename):
    return EXT_CATEGORY.get(ext_of(filename))


def endpoint_path(category):
    return CATEGORY_PATH.get(category)
