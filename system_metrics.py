import psutil

def get_system_metrics():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/') 

    return {
        "cpu_percent": cpu_usage,
        "ram_percent": memory.percent,
        "disk_percent": disk.percent
    }

def print_sys_metrics():
    metrics = get_system_metrics()
    print(f"CPU: {metrics['cpu_percent']}%")
    print(f"RAM: {metrics['ram_percent']}%")
    print(f"Disk: {metrics['disk_percent']}%")