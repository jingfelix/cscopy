import os
import shutil
import tempfile

from cscopy.cli import CscopeCLI
from cscopy.model import SearchType
from cscopy.utils.common import run


class CscopeWorkspace(object):
    cli: CscopeCLI
    files: list[str]
    kernel_mode: bool
    tempdir: tempfile.TemporaryDirectory
    tempdir_path: str

    def __init__(
        self,
        files: list[str],
        cli: CscopeCLI = CscopeCLI("/usr/bin/cscope"),
        use_tempfile: bool = True,
        kernel_mode: bool = True,
    ) -> None:
        self.cli = cli
        self.kernel_mode = kernel_mode

        # Check whether files exist
        for file in files:
            if not os.path.exists(file):
                raise FileNotFoundError(f"File not found: {file}")

        # copy files to a temporary directory
        if use_tempfile:
            self.tempdir = tempfile.TemporaryDirectory()
            self.tempdir_path = self.tempdir.name

            for file in files:
                shutil.copy(
                    file, self.tempdir_path
                )  # use shutil.copy to preserve file attributes

            self.files = [
                os.path.join(self.tempdir_path, os.path.basename(file))
                for file in files
            ]
        else:
            self.files = files
            self.tempdir_path = os.getcwd()

        # Generate cscope.out file
        cmds = [cli.cscope_path, "-b", *self.files]
        if kernel_mode:
            cmds.append("-k")

        output = run(
            cmds=cmds,
            capture_output=True,
            check=True,
            cwd=self.tempdir_path,
        )

        # Check if cscope.out file is generated
        if not os.path.exists(os.path.join(self.tempdir_path, "cscope.out")):
            raise FileNotFoundError("cscope.out file not found")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if hasattr(self, "tempdir"):
            self.tempdir.cleanup()

    def do_single_search(self, mode: SearchType, symbol: str):
        """
        Perform a single search

        `cscope -d -L{mode} {symbol}`

        """

        # TODO: Add kernel mode support

        output = run(
            [
                self.cli.cscope_path,
                "-d",
                f"-L{mode.value}",
                f"{symbol}",
            ],
            capture_output=True,
            check=True,
            cwd=self.tempdir_path,
        )

        return output
