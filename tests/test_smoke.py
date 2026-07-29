"""Offline smoke test — no network."""

from micompress.categories import category_for, endpoint_path, ext_of
from micompress import api, __version__


def test_ext_of():
    assert ext_of("a/b/Photo.JPG") == "jpg"
    assert ext_of("noext") == ""


def test_category_routing():
    assert category_for("photo.png") == "image"
    assert category_for("doc.pdf") == "pdf"
    assert category_for("slides.pptx") == "document"
    assert category_for("clip.mp4") == "video"
    assert category_for("song.mp3") == "audio"
    assert category_for("bundle.zip") == "archive"
    assert category_for("x.unknownext") is None


def test_endpoint_path():
    assert endpoint_path("image") == "image-compressors"
    assert endpoint_path("pdf") == "pdf-compressors"
    assert endpoint_path("archive") == "archive-compressors"


def test_exports():
    assert callable(api.compress_file)
    assert api.DEFAULT_BASE == "https://micompress.com"
    assert __version__


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
    print("ok — smoke test passed")
