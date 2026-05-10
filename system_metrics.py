import psutil

def get_sys_metrics():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/') 

    return {
        "cpu_percent": cpu_usage,
        "ram_percent": memory.percent,
        "disk_percent": disk.percent
    }