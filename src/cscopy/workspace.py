import os
import shutil
import tempfile

from cscopy.cli import CscopeCLI
from cscopy.model import SearchResult, SearchType
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
        self.files = files

        # Check whether files exist
        for file in files:
            if not os.path.exists(file):
                raise FileNotFoundError(f"File not found: {file}")

        # copy files to a temporary directory
        if use_tempfile:
            self.tempdir = tempfile.TemporaryDirectory()
            self.tempdir_path = self.tempdir.name

            file_index = 0
            target_files = []
            for file in files:
                target_file = os.path.join(self.tempdir_path, f"{file_index}")
                shutil.copy(
                    file, target_file
                )  # use shutil.copy to preserve file attributes

                target_files.append(target_file)

        else:
            target_files = files
            self.tempdir_path = os.getcwd()

        # Generate cscope.out file
        cmds = [cli.cscope_path, "-b", *target_files]
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

    def search(self, mode: SearchType, symbol: str) -> list[SearchResult]:
        """
        Perform a single search

        `cscope -d -L{mode} {symbol}`

        Args:
            mode (SearchType): Search mode, e.g. cscopy.model.SearchType.C_SYMBOL
            symbol (str): Symbol to search

        Returns:
            list[cscopy.model.SearchResult]: List of search results
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

        output_lines = output.splitlines()
        search_results = []
        for line in output_lines:
            parts = line.split(" ", 3)  # limit split to 3 parts
            if len(parts) < 4:
                raise ValueError(f"Unexpected output from cscope")

            file, parent, line_number, content = parts
            line_number = int(line_number)

            search_result = SearchResult(
                symbol=symbol,
                file=self.files[int(os.path.basename(file))],
                parent=parent,
                line=line_number,
                content=content,
            )
            search_results.append(search_result)

        return search_results

    def search_c_symbol(self, symbol: str) -> list[SearchResult]:
        return self.search(SearchType.C_SYMBOL, symbol)

    def search_global_definition(self, symbol: str) -> list[SearchResult]:
        return self.search(SearchType.GLOBAL_DEFINITION, symbol)

    def search_func_called_by(self, symbol: str) -> list[SearchResult]:
        return self.search(SearchType.FUNC_CALLED_BY, symbol)

    def search_func_calling(self, symbol: str) -> list[SearchResult]:
        return self.search(SearchType.FUNC_CALLING, symbol)

    def search_text_string(self, symbol: str) -> list[SearchResult]:
        return self.search(SearchType.TEXT_STRING, symbol)

    def search_change_text_string(self, symbol: str) -> list[SearchResult]:
        return self.search(SearchType.CHANGE_TEXT_STRING, symbol)

    def search_egrep(self, symbol: str) -> list[SearchResult]:
        return self.search(SearchType.EGREP, symbol)

    def search_file(self, symbol: str) -> list[SearchResult]:
        return self.search(SearchType.FILE, symbol)

    def search_files_including(self, symbol: str) -> list[SearchResult]:
        return self.search(SearchType.FILES_INCLUDING, symbol)

    def search_assign_to_symbol(self, symbol: str) -> list[SearchResult]:
        return self.search(SearchType.ASSIGN_TO_SYMBOL, symbol)
