import ctypes
import os
import platform
import shutil
import subprocess


def _windows_cpu_name():
    try:
        import winreg

        with winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            r"HARDWARE\DESCRIPTION\System\CentralProcessor\0",
        ) as key:
            cpu_name, _ = winreg.QueryValueEx(key, "ProcessorNameString")
            return cpu_name.strip()
    except Exception:
        return ""


def _linux_cpu_name():
    try:
        with open("/proc/cpuinfo", "r", encoding="utf-8", errors="ignore") as cpuinfo:
            for line in cpuinfo:
                if line.lower().startswith("model name"):
                    return line.split(":", 1)[1].strip()
    except Exception:
        pass
    return ""


def _macos_cpu_name():
    try:
        result = subprocess.run(
            ["sysctl", "-n", "machdep.cpu.brand_string"],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception:
        pass
    return ""


def get_cpu_name():
    system = platform.system()

    if system == "Windows":
        cpu_name = _windows_cpu_name()
    elif system == "Linux":
        cpu_name = _linux_cpu_name()
    elif system == "Darwin":
        cpu_name = _macos_cpu_name()
    else:
        cpu_name = ""

    return cpu_name or platform.processor() or platform.machine() or "Unknown CPU"


def _windows_memory_bytes():
    class MEMORYSTATUSEX(ctypes.Structure):
        _fields_ = [
            ("dwLength", ctypes.c_ulong),
            ("dwMemoryLoad", ctypes.c_ulong),
            ("ullTotalPhys", ctypes.c_ulonglong),
            ("ullAvailPhys", ctypes.c_ulonglong),
            ("ullTotalPageFile", ctypes.c_ulonglong),
            ("ullAvailPageFile", ctypes.c_ulonglong),
            ("ullTotalVirtual", ctypes.c_ulonglong),
            ("ullAvailVirtual", ctypes.c_ulonglong),
            ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
        ]

    memory_status = MEMORYSTATUSEX()
    memory_status.dwLength = ctypes.sizeof(MEMORYSTATUSEX)

    if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(memory_status)):
        return memory_status.ullTotalPhys

    return 0


def _posix_memory_bytes():
    try:
        page_size = os.sysconf("SC_PAGE_SIZE")
        physical_pages = os.sysconf("SC_PHYS_PAGES")
        return page_size * physical_pages
    except (AttributeError, OSError, ValueError):
        return 0


def get_memory_gb():
    if platform.system() == "Windows":
        total_bytes = _windows_memory_bytes()
    else:
        total_bytes = _posix_memory_bytes()

    if not total_bytes:
        return 0

    return round(total_bytes / (1024 ** 3))


def get_storage_info():
    if platform.system() == "Windows":
        system_drive = os.environ.get("SystemDrive", "C:") + "\\"
    else:
        system_drive = "/"

    total, used, free = shutil.disk_usage(system_drive)

    return {
        "system_drive": system_drive,
        "total_gb": round(total / (1024 ** 3)),
        "free_gb": round(free / (1024 ** 3)),
    }


def get_os_name():
    system = platform.system()
    release = platform.release()

    if system == "Darwin":
        mac_version = platform.mac_ver()[0]
        return f"macOS {mac_version}" if mac_version else f"macOS {release}"

    return f"{system} {release}".strip()
