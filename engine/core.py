from engine.games import load_games
from engine.launcher import launch_program
from engine.config import load_identity
from engine.system_info import (
    get_cpu_name,
    get_memory_gb,
    get_storage_info,
    get_os_name,
)


class J29Engine:
    def get_games(self):
        return load_games()

    def launch_game(self, program_path):
        return launch_program(program_path)

    def get_system_info(self):
        storage = get_storage_info()

        return {
            "cpu": get_cpu_name(),
            "memory_gb": get_memory_gb(),
            "os_name": get_os_name(),
            "system_drive": storage["system_drive"],
            "total_gb": storage["total_gb"],
            "free_gb": storage["free_gb"],
        }

    def get_identity(self):
        return load_identity()