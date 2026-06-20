
import psutil

try:
    from pynvml import (
        nvmlInit,
        nvmlDeviceGetHandleByIndex,
        nvmlDeviceGetUtilizationRates,
        nvmlDeviceGetMemoryInfo
    )
    nvmlInit()
    NVIDIA_AVAILABLE = True
except Exception:
    NVIDIA_AVAILABLE = False

class SystemUsageMonitor:
    def __init__(self):

        self.gpu_availabel = NVIDIA_AVAILABLE

    def get_usage(self):

        result_usage = {
            "cpu_percent": 0.0,
            "ram_percent": 0.0,
            "ram_used_gb": 0.0,
            "ram_total_gb": 0.0,
            "gpu_percent": None,
            "gpu_memory_percent": None,
            "gpu_memory_used_gb": None,
            "gpu_memory_total_gb": None
        }

        try:
            cpu_percent = psutil.cpu_percent()
            ram = psutil.virtual_memory()
            result_usage["cpu_percent"] = cpu_percent
            result_usage["ram_percent"] = ram.percent
            result_usage["ram_used_gb"] = ram.used / (1024 ** 3)
            result_usage["ram_total_gb"] = ram.total / (1024 ** 3)

            if self.gpu_availabel:
                handle = nvmlDeviceGetHandleByIndex(0)
                util = nvmlDeviceGetUtilizationRates(handle)
                mem = nvmlDeviceGetMemoryInfo(handle)
                result_usage["gpu_percent"] = util.gpu
                result_usage["gpu_memory_percent"] = (mem.used / mem.total) * 100
                result_usage["gpu_memory_used_gb"] = (mem.used / (1024 ** 3))
                result_usage["gpu_memory_total_gb"] = (mem.total / (1024 ** 3))
        except Exception:
            pass

        return result_usage