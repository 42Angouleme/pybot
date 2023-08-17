import os


class FilepathTimestamp:
    last_timestamp = None
    filename_ts_suffix_format = "_%Y-%m-%d_%Hh%Mm%Ss"
    _baseFilepath = ""

    def __init__(
        self, filepath="./file.ext", use_ts_suffix=True, allowed_extensions=[]
    ) -> None:
        self.allowed_extensions = allowed_extensions
        self.use_ts_suffix = use_ts_suffix
        self.filepath = filepath

    @property
    def filepath(self):
        if not self._baseFilepath:
            raise RuntimeError(
                "Unexpected error: _baseFilepath should never be empty, this should not happen."
            )
        name, extension = os.path.splitext(self._baseFilepath)
        if (
            self.use_ts_suffix
            and self.filename_ts_suffix_format
            and self.last_timestamp is not None
        ):
            timestamp = self.last_timestamp.strftime(self.filename_ts_suffix_format)
            return f"{name}{timestamp}{extension}"
        else:
            return self._baseFilepath

    @filepath.setter
    def filepath(self, new_filepath):
        if not new_filepath:
            raise ValueError("Filepath cannot be empty.")
        filename = os.path.basename(new_filepath)
        name, extension = os.path.splitext(filename)
        if not name:
            raise ValueError("Filename (without extension) cannot be empty.")
        self._expectValidExtension(extension)
        self._baseFilepath = new_filepath

    def _expectValidExtension(self, ext: str):
        if not ext:
            raise ValueError("Extension cannot be empty")
        if self.allowed_extensions is "*":
            return
        lower_ext = ext.lower()
        if self.allowed_extensions is lower_ext:
            raise ValueError(
                f'Extension "{lower_ext}" should be {self.allowed_extensions}.'
            )
        if not lower_ext in self.allowed_extensions:
            raise ValueError(
                f"Extension \"{lower_ext}\" is not recognized. Should be one of {', '.join(self.allowed_extensions)}."
            )
