import os
from datetime import datetime
from typing import List

ERROR_EMPTY_FILEPATH = "Filepath cannot be empty."
ERROR_EMPTY_BASENAME = "Filename (without extension) cannot be empty."
ERROR_EMPTY_EXT = "Extension cannot be empty."
ERROR_EXT_NOT_ALLOWED = 'Extension "{ext}" not allowed. Should be one of {allowed_ext}.'


class FilepathSchema:
    def __init__(
        self,
        filepath: str = "/tmp/file_%Y-%m-%d_%Hh%Mm%Ss",
        allowed_extensions: List[str] = ["*"],
        timestamp=None,
    ) -> None:
        self.allowed_extensions = allowed_extensions
        self.filepath_schema = filepath
        self._last_timestamp = timestamp

    @property
    def timestamp(self) -> datetime:
        """Get the last saved timestamp. If it has never been assigned, returns the current time."""
        return self._last_timestamp or datetime.now()

    @timestamp.setter
    def timestamp(self, value):
        """Set the timestamp."""
        self._last_timestamp = value

    def refresh_timestamp(self):
        """Set the timestamp at the current time."""
        self._last_timestamp = datetime.now()

    @property
    def filepath(self) -> str:
        """Get the formatted filepath according to the schema and the current timestamp."""
        return FilepathSchema.expand_filepath(self.filepath_schema, self.timestamp)

    @filepath.setter
    def filepath(self, new_filepath: str):
        """Set the filepath schema. It cannot be empty and the extension must comply with `self.allowed_extensions`."""
        FilepathSchema.expect_valid_filepath(
            new_filepath, allowed_extensions=self.allowed_extensions
        )
        self.filepath_schema = new_filepath

    @staticmethod
    def expect_allowed_extension(ext: str, allowed_extensions: List[str] = ["*"]):
        """
        Ensure the given `ext` is a valid extension according to `self.allowed_extension` or raise error.

        Args:
            ext (str): The extension to check.

        Raises:
            ValueError: If the extension is part of the allowed extensions.
        """
        if "*" in allowed_extensions:
            return
        if not ext and "" not in allowed_extensions:
            raise ValueError(ERROR_EMPTY_EXT)
        lower_ext = ext.lower()
        if not lower_ext in allowed_extensions:
            raise ValueError(
                ERROR_EXT_NOT_ALLOWED.format(
                    ext=lower_ext, allowed_ext=allowed_extensions
                )
            )

    @staticmethod
    def expect_valid_filepath(filepath: str, allowed_extensions: List[str] = ["*"]):
        if not filepath:
            raise ValueError(ERROR_EMPTY_FILEPATH)
        filename = os.path.basename(filepath)
        basename, extension = os.path.splitext(filename)
        if not basename:
            raise ValueError(ERROR_EMPTY_BASENAME)
        FilepathSchema.expect_allowed_extension(
            extension, allowed_extensions=allowed_extensions
        )

    @staticmethod
    def expand_filepath(filepath: str, timestamp: datetime = datetime.now()):
        return timestamp.strftime(filepath)

    @staticmethod
    def expand_valid_filepath(
        filepath: str,
        timestamp: datetime = datetime.now(),
        allowed_extensions: List[str] = ["*"],
    ):
        FilepathSchema.expect_valid_filepath(filepath, allowed_extensions)
        return FilepathSchema.expand_filepath(filepath, timestamp)
