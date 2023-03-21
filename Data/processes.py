import subprocess
import time
from Data.FetchData import DistroList
import threading
from Data.SubMenus import *


def get_default_terminal():
    try:
        command = ['gnome-terminal', '-e', 'ls']
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        if stderr:
            raise RuntimeError(f"Command {command} failed with error message: {stderr.decode().strip()}")
        process.terminate()
        return 'gnome-terminal'

    except:
        try:
            command = ['konsole', '-e', 'ls']
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            if stderr:
                raise RuntimeError(f"Command {command} failed with error message: {stderr.decode().strip()}")
            process.terminate()
            return 'konsole'
        except:
            try:
                command = ['xdg-terminal', '-e', 'ls']
                process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = process.communicate()
                if stderr:
                    raise RuntimeError(f"Command {command} failed with error message: {stderr.decode().strip()}")
                process.terminate()
                return 'xdg-terminal'
            except:
                print("cannot find terminal\ndownload gnome shell?")


terminal = get_default_terminal()
#print('\n', terminal)


def enter_distro(name):
    terminal_thread = threading.Thread(target=lambda: subprocess.run([terminal, '-e', 'distrobox', 'enter', name.strip()]))
    terminal_thread.start()
    time.sleep(1)


def remove_distro(name, id):
    dists = DistroList()
    if id in dists:
        if "up" in dists[id]["status"].lower():
            dialog = Dialog("Please stop container new before deletion", 0, 'delete' + name)
            dialog.exec_()
        else:
            dialog = Dialog('Delete this container?', 1, 'delete' + name)
            result = dialog.exec_()
            if result == QDialog.Accepted:
                subprocess.run(['distrobox', 'rm', name.strip()], input='y\n', text=True)
            else:
                print("cancelled")
    else:
        dialog = Dialog("container  doesn't exist", 0, 'delete' + name)
        dialog.exec_()


def stop_distro(name):
    subprocess.run(['distrobox', 'stop', name.strip()], input='y\n', text=True)


def create_distro():
    diag = NewDialog()
    result = diag.exec_()
    if result:
        data = diag.get_data()
        name = data["name"]
        distro = data["distro"]
        version = data["version"]
        if name == '':
            terminal_thread = threading.Thread(
                target=lambda: subprocess.run([terminal, '-e', 'distrobox', 'create', "new_container"]))
        elif distro == '':
            terminal_thread = threading.Thread(
                target=lambda: subprocess.run([terminal, '-e', 'distrobox', 'create', name.strip()]))
        else:
            if version != '':
                terminal_thread = threading.Thread(
                    target=lambda:
                    subprocess.run(
                        [terminal, '-e', 'distrobox', 'create', f"--name {name.strip()}",
                         f"--image {distro}:{version}"]))
            else:
                terminal_thread = threading.Thread(
                    target=lambda:
                    subprocess.run(
                        [terminal, '-e', 'distrobox', 'create', f"--name {name.strip()}", f"--image {distro}"]))
        terminal_thread.start()
        return terminal_thread

def InitialCheck():
    try:
        subprocess.run(["distrobox", "version"], capture_output=True, text=True)
        return 1
    except FileNotFoundError:
        return 0
