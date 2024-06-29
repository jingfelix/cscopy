import os
import subprocess


def run(
    cmds: list[str],
    capture_output: bool = True,
    check: bool = False,
    cwd: str = os.getcwd(),
) -> str:
    """
    Run a command with subprocess

    Args:
        cmds (list[str]): Command to run
        capture_output (bool, optional): Capture output. Defaults to True.
        check (bool, optional): Check return code. Defaults to False.
        cwd (str, optional): Working directory. Defaults to os.getcwd().
    Returns:
        str: Output of the command
    """
    process = subprocess.Popen(
        cmds,
        shell=False,
        stdout=subprocess.PIPE if capture_output else None,
        stderr=subprocess.PIPE if capture_output else None,
        cwd=cwd,
    )
    stdout, stderr = process.communicate()

    if check and process.returncode != 0:
        raise subprocess.CalledProcessError(
            process.returncode, cmds, output=stdout, stderr=stderr
        )

    return stdout.decode("utf-8", errors="ignore") if stdout else ""
