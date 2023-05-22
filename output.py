from colorama import init, Style

init()


def output_message(fore_color, message, visual_output_active):
    if visual_output_active:
        print(f"{fore_color}{message}{Style.RESET_ALL}")
