import os
from distutils.extension import Extension


def _get_bool(key: str, default: bool = False) -> bool:
    value = os.getenv(key)
    if value is not None:
        return value.lower() in ["true", "1", "t"]
    return default


def _get_extensions():
    return [
        Extension(
            "audiomatch.popcount._popcount",
            sources=["src/audiomatch/popcount/_popcount.c"],
        )
    ]


def build(setup_kwargs):
    """This function is mandatory in order to build the extensions."""
    use_extensions = not _get_bool("AUDIOMATCH_NO_EXTENSIONS", default=False)

    if use_extensions:
        setup_kwargs.update({"ext_modules": _get_extensions()})
