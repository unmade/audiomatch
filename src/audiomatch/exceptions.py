class AudiomatchError(Exception):
    """Base class for all library-related errors"""


class NotEnoughFiles(AudiomatchError):
    """Too few input files to do any comparisson"""
