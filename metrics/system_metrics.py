import psutil
import time

def get_sys_metrics(samples = 5):
    cpu_samples = []
    ram_samples = []
    memory_swap_samples = [] # High swap memory can indicate data being written on the disk, which has much slower access time. This is not desirable
    disk = psutil.disk_usage('/') 
    for _ in range(samples):
        cpu_samples.append(psutil.cpu_percent())
        ram_samples.append(psutil.virtual_memory().percent)
        memory_swap_samples.append(psutil.swap_memory().percent)
        time.sleep(0.2)
        
    return {
        "cpu_max": max(cpu_samples),
        "ram_max": max(ram_samples),
        "swap_memory_max": max(memory_swap_samples),
        "disk_percent": disk.percent # Keeping track of disk is also important, so that we make sure we have enough space left on our machine for more data
    }
# Information about the machine