def print_color(color):
    match color:
        case "HEADER" : color = '\033[95m'
        case "BLUE" : color = '\033[94m'
        case "CYAN" : color = '\033[96m'
        case "GREEN" : color = '\033[92m'
        case "WARNING" : color = '\033[93m'
        case "FAIL" : color = '\033[91m'
        case "ENDC" : color = '\033[0m'
        case "BOLD" : color = '\033[1m'
        case "UNDERLINE" : color = '\033[4m'
    return color