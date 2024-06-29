import os


class CscopeCLI(object):
    """Cscope CLI class"""

    cscope_path: str

    def __init__(self, path: str):
        """
        Initialize CscopeCLI class

        Args:
            path (str): Path to cscope executable
        """

        # Check if the path exists
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")

        if not os.access(path, os.X_OK):
            raise Exception(f"File not executable: {path}")

        self.cscope_path = path
