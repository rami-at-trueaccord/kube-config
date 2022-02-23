from colorama import Fore


def get(phrase, color):
    match str(color).upper():
        case 'RED':
            return f"{Fore.RED}{phrase}{Fore.RESET}"
        case 'GREEN':
            return f"{Fore.GREEN}{phrase}{Fore.RESET}"
        case 'BLUE':
            return f"{Fore.BLUE}{phrase}{Fore.RESET}"
        case 'WHITE':
            return f"{Fore.WHITE}{phrase}{Fore.RESET}"
        case 'YELLOW':
            return f"{Fore.YELLOW}{phrase}{Fore.RESET}"

    print(f"Color '{color}' invalid; phrase not styled.")
    return phrase
