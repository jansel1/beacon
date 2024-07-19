import keyboard
import os
import shutil, time
import threading
import beaconmenu

try:
    os.chdir("./beacon.rootenv/user")
except:
    print("COULD NOT FIND ROOTENVIROMENT (BEACON.ROOTENV).")
    input("TYPE ENTER TO EXIT...")

    quit()

def shdd():
    try:
        while True:
            print("PRESS CTRL+C TO EXIT - YOU WILL GO BACK TO BEACON HOME.")
            print(f"CURRENT DRIVE: HARD_DRIVE_1.SYSM (System Memory File)")

            time.sleep(.7)
            os.system("cls")

    except KeyboardInterrupt: return

os.system("cls")
keyboard.press("f11")

default_memory = 4096

def getmem():
    with open("../reserved/HARD_DRIVE_1", "r") as f:
        return (len(f.read()))

def check_memory():
    total = 0

    for root, dirs, files in os.walk(os.getcwd()):
        for file in files:
            with open(os.path.join(root, file), 'r') as file:
                total += len(file.read())

    #print(getmem(), total)

    if total > getmem(): return -1

    return total

def update_memory():
    mem = int(check_memory())

    with open("../reserved/HARD_DRIVE_1", 'r+') as f:
        content = f.read()
        new_content = content[:-mem]
        f.seek(0)
        f.write(new_content)
        f.truncate()

def print_centered(text, end="\n", flush=False):
    columns, rows = shutil.get_terminal_size()
    start_x = (columns - len(text)) // 2

    print(' ' * start_x + text, end=end, flush=flush)


is_loading = False
after_reload = False
beacon = False
sys = False
menu_active = False
menu_done = False
cango = False

def load(skip=False):
    global cango, menu_active

    os.system("cls")
    time.sleep(0.5)

    menu_active = True

    menu = beaconmenu.menu(options=[["BOOT BEACONOS"], ["SEE HARD DRIVES"]], method=print_centered)

    menu_main = menu.print()
    cango = False

    if menu_main == 0: 
        beacon = True
        cango = True

        menu_done = True
    elif menu_main == 1: 
        shdd()

        cango = True

        menu_done = True
        beacon = True

    if menu_done: menu_active = False

    if cango:
        global is_loading

        if not skip and beacon:
            is_loading = True

            os.system("cls")
            time.sleep(0.5)

            update_memory()

            if (check_memory() == -1):
                print("No space available.")
                input("Type enter to exit...")

                quit(1)
            
            with open(f"../reserved/HARD_DRIVE_1", "w") as f:
                for i in range(default_memory):
                    f.write("0")

            print_centered("Welcome to BeaconOS")
            print_centered("Please wait while we set things up for you\n")

            loading_frames = ["⢀⠀", "⡀⠀", "⠄⠀", "⢂⠀", "⡂⠀", "⠅⠀", "⢃⠀", "⡃⠀", "⠍⠀", "⢋⠀", "⡋⠀", "⠍⠁", "⢋⠁", "⡋⠁", "⠍⠉", "⠋⠉", "⠋⠉", "⠉⠙", "⠉⠙", "⠉⠩", "⠈⢙", "⠈⡙", "⢈⠩", "⡀⢙", "⠄⡙", "⢂⠩", "⡂⢘", "⠅⡘", "⢃⠨", "⡃⢐", "⠍⡐", "⢋⠠", "⡋⢀", "⠍⡁", "⢋⠁", "⡋⠁", "⠍⠉", "⠋⠉", "⠋⠉", "⠉⠙", "⠉⠙", "⠉⠩", "⠈⢙", "⠈⡙", "⠈⠩", "⠀⢙", "⠀⡙", "⠀⠩", "⠀⢘", "⠀⡘", "⠀⠨", "⠀⢐", "⠀⡐", "⠀⠠", "⠀⢀", "⠀⡀"]

            center_loading_frames = (shutil.get_terminal_size().columns-3) // 2

            for frame in loading_frames:
                print(f'\r{" "*center_loading_frames}{frame}', end='', flush=True)
                time.sleep(0.05)

        commands = ["[CTRL+C] Exit BeaconOS", "[MEMORY] Get Memory Data.", "[TASKS] Make A Todo List/Text File", "[DIR] Lists Files", "[CLEAR] Wipes Directory", "[VIEW] <FILE> View Contents Of A File"]
        is_loading = False

        os.system("cls")

        out = ""
        cmds = 0

        for cmd in commands:
            if (cmds > 2): out += "\n";cmds=0
            out += f"{cmd}{' ':<12}"
            cmds += 1
        
        print(out+"\n")


def makefile(name, text):
    f=None

    with open(f"{os.getcwd()}/{name}", "w") as file:
        file.write(text)
        f = file.name

    if (check_memory() == -1): 
        print(f"NO MEMORY AVAILABLE TO ALLOCATE {len(text)} BYTES! PLEASE FREE SOME SPACE.")

        os.remove(f)
        return

    update_memory()
    
def main():
    global cango, menu_active

    load()

    if cango:
        bufferspace = 0
        currentbuffers = 0

        
        def _getmem(): 
            print(f"TOTAL AMOUNT OF BYTES ALLOCATED THIS SESSION (BUFFER SPACE) [{bufferspace}b]")
            return True

        def _tasks():
            out = ""

            nonlocal bufferspace

            while True:
                try:
                    while menu_active:
                        time.sleep(0.1)

                    todoBuffer = input(""); bufferspace += todoBuffer.__sizeof__()

                    line = todoBuffer.split(" ")[0]

                    out += str(line) + " " + ' '.join(str(todoBuffer.split(" ")[1:])) + "\n"

                except KeyboardInterrupt:
                    name = input("\nName of file > ")

                    makefile(name, text=out)
                    
                    print("\n")
                    break
            
            return True

        def _dir():
            m = default_memory
            cm = check_memory()

            if cm == 0: cm = 1

            print(f"\nDEF. MEMORY SIZE: {m} BYTES, {m / 1024}KB\nIN USE: {cm} BYTES, {cm / 1024}KB\nFREE: {m-cm} BYTES, {m/1024 - cm/1024}KB\n")
            
            for root, dirs, files in os.walk(os.getcwd()):
                if (len(files) == 0):
                    print("No files found.")
                    break

                for file in files:
                    title = f".{str(file.split('.')[len(file.split('.'))-1]).upper()} File"
                    size = os.path.getsize(os.path.join(root, file))

                    if file.endswith(".text"): title = "DOCUMENT FILE"
                    elif file.endswith(".todo"): title = "TODO FILE"
                    elif file.endswith(".log"): title = "SYSTEM OUTPUT FILE"

                    print(f"{file:<30} {title:<30} {size} bytes, {size/1024} kb")

            return True

        def _clear():
            amt = 0
            yn = input("ARE YOU SURE YOU WANT TO CLEAR HOME Y/N > ")

            if (yn.lower() == "y"):
                for root, dirs, files in os.walk(os.getcwd()):
                    for file in files:
                        os.remove(os.path.join(root, file))
                        amt += 1
                print(f"CLEARED {amt} FILE(s)")

        def _view():
            try: 
                input_buffer[1]
            except: 
                print("REQUIRED ARGUMENTS: <file_location> AT (InputBuffer), Argument 1")
                return

            try:
                with open(f"./{input_buffer[1]}", "r") as f:
                    for line in f.readlines():
                        print(line)
            except: print(f"COULD NOT LOCATE FILE [{input_buffer[1]}]")

        commands = [
            ["memory", _getmem],
            ["tasks", _tasks],
            ["dir", _dir],
            ["clear", _clear],
            ["view", _view]
        ]

        try:
            while menu_active == False:
                currentbuffers = bufferspace

                found = False
                input_buffer = input("\\> ").split(' '); bufferspace += input_buffer.__sizeof__()

                for command in commands:
                    if input_buffer[0].lower() == command[0]:
                        command[1]()
                        found = True

                        break

                if not found and not menu_active:
                    print(f"COULD NOT FIND COMMAND OR APPLICATION [{input_buffer[0].upper()}]")

                currentbuffers = 0
                
        except KeyboardInterrupt: pass

        time.sleep(0.1)
main()