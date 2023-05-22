import os


def clear_console():
    command = "clear"
    if os.name in ("nt", "dos"):  # If the OS is Windows
        command = "cls"
    os.system(command)
