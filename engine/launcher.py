import subprocess


def launch_program(program_path):
    if not program_path:
        return False

    subprocess.Popen([program_path])
    return True