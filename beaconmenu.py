import keyboard
import os, time
import colorama, shutil

def print_centered(text, end="\n", flush=False):
    columns, rows = shutil.get_terminal_size()
    start_x = (columns - len(text)) // 2

    print(' ' * start_x + text, end=end, flush=flush)

class menu:
    def __init__(self, options, method):
        self.b = colorama.Back.WHITE
        self.f = colorama.Fore.BLACK

        self.options = options
        self.y = 0
        self.method = print

    def print(self):
        time.sleep(1)
        
        options = self.options
        method = self.method

        y = self.y
        b, f = self.b, self.f

        def print_menu(selected_index):
            for idx, opt in enumerate(options):
                if idx == selected_index:
                    op = str(opt[0])

                    self.method(f"{b}{f}{op} ({y}) {colorama.Style.RESET_ALL}<")

                else:
                    op = str(opt[0])
                    self.method(f"{op}")

        print_menu(y)

        while True:
            if keyboard.is_pressed("down"):
                os.system("cls")

                y = (y + 1) % len(options)
                print_menu(y)
                time.sleep(0.2)  # Debounce delay

            if keyboard.is_pressed("up"):
                os.system("cls")

                y = (y - 1) % len(options)
                print_menu(y)
                time.sleep(0.2)  # Debounce delay

            if keyboard.is_pressed("enter"):
                print(colorama.Style.RESET_ALL)

                os.system("cls")
                time.sleep(0.2)  # Debounce delay
                
                print(colorama.Style.RESET_ALL)

                return y # y is option
            