import psutil
import platform
from datetime import datetime


def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            #return f"{bytes:.2f}{unit}{suffix}"
            # print("Bytes:" '%2f'%bytes +unit+suffix)
            # print("unit:" +unit)
            # print("suffix:" +suffix)
            return '%2f'% bytes +unit+suffix

        bytes /= factor


# to get list of process with memor details
def getListOfProcessSortedByMemory():
    '''
    Get list of running process sorted by Memory Usage
    '''
    listOfProcObjects = []
    # Iterate over the list
    for proc in psutil.process_iter():
        try:
            # Fetch process details as dict
            pinfo = proc.as_dict(attrs=['pid', 'name', 'username'])
            pinfo['vms'] = proc.memory_info().vms / (1024 * 1024)
            # Append dict to list
            listOfProcObjects.append(pinfo);
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    # Sort list of dict by key vms i.e. memory usage
    listOfProcObjects = sorted(listOfProcObjects, key=lambda procObj: procObj['vms'], reverse=True)
    return listOfProcObjects


# Iterate over all running process and print process ID & Name and to get list of top 5 processes with highest memory usage
def main():
    # Iterate over all running process
    for proc in psutil.process_iter():
        try:
            # Get process name & pid from process object.
            processName = proc.name()
            processID = proc.pid
            # print(processName , ' ::: ', processID)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    # print('*** Create a list of all running processes ***')
    listOfProcessNames = list()
    # Iterate over all running processes
    for proc in psutil.process_iter():
        # Get process detail as dictionary
        pInfoDict = proc.as_dict(attrs=['pid', 'name', 'cpu_percent'])
        # Append dict of process detail in list
        listOfProcessNames.append(pInfoDict)
    # Iterate over the list of dictionary and print each elem
    #    for elem in listOfProcessNames:
    # #       print(elem)
    print('*** Top 5 process with highest memory usage ***')
    listOfRunningProcess = getListOfProcessSortedByMemory()
    for elem in listOfRunningProcess[:5]:
        print(elem)


# System Information
def get_SystemInfo():
    print("=" * 40, "System Information", "=" * 40)
    uname = platform.uname()
   # print(f"System: {uname.system}")
    print("System: {}" .format(platform.system()))
    print("Node Name: {}" .format(platform.node()))
    print("Release:{}" .format(platform.release()))
    print("Version:{}"  .format(platform.version()))
    print("Machine:{}"  .format(platform.machine()))
    print("Processor:{}"  .format(platform.processor()))


# Date and time the computer was boosted
 # Boot Time
def get_SystemBootTime():
    print("=" * 40, "Boot Time", "=" * 40)
    boot_time_timestamp = psutil.boot_time()
    bt = datetime.fromtimestamp(boot_time_timestamp)
    #print(f"Boot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}")
    print("Boot time:  {}/{}/{} {}:{}:{}" .format(bt.year,bt.month,bt.day,bt.hour,bt.minute,bt.second) )

# gets cpu information
def cpu_info():
    print("=" * 40, "CPU Info", "=" * 40)
    # number of cores
    print("Physical cores:", psutil.cpu_count(logical=False))
    print("Total cores:", psutil.cpu_count(logical=True))
    # CPU frequencies
    cpufreq = psutil.cpu_freq()
    #print(f"Max Frequency: {cpufreq.max:.2f}Mhz")
    # print(f"Min Frequency: {cpufreq.min:.2f}Mhz")
    # print(f"Current Frequency: {cpufreq.current:.2f}Mhz")
    print("Max Frequency:{}" .format(cpufreq.max) +'Mhz')
    print("Min Frequency:{}" .format(cpufreq.min) +'Mhz')
    print("Current Frequency:{}" .format(cpufreq.current) + 'Mhz')
    # CPU usage
    # print("CPU Usage Per Core:")
    # for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
    #     print(f"Core {i}: {percentage}%")
    #print(f"Total CPU Usage: {psutil.cpu_percent()}%")
    print("Total CPU Usage:{}" .format(psutil.cpu_percent()) + '%')
    # prints at interval of 60 seconds cpu utilization and max memory utilized processes details
    while True:
        cpu = psutil.cpu_percent(interval=60)
        print(cpu)
        main()

# Memory Information
def memory_info():

    print("=" * 40, "Memory Information", "=" * 40)
    # get the memory details
    svmem = psutil.virtual_memory()
    # print(f"Total: {get_size(svmem.total)}")
    # print(f"Available: {get_size(svmem.available)}")
    # print(f"Used: {get_size(svmem.used)}")
    # print(f"Percentage: {svmem.percent}%")
    print("Total:{}" .format(get_size(svmem.total)))
    print("Available:{}" .format(get_size(svmem.available)))
    print("Used: {}" .format(get_size(svmem.used)))
    print("Percentage:{}" .format(svmem.percent))
    print("=" * 20, "SWAP", "=" * 20)
    # get the swap memory details (if exists)
    swap = psutil.swap_memory()
    print("Total: {} ".format(get_size(swap.total)))
    print("Free: {} " .format(get_size(swap.free)))
    print("Used:{}" .format(get_size(swap.used)))
    print("Percentage: {}" .format(swap.percent))


# Disk Information
def disk_info():
    print("=" * 40, "Disk Information", "=" * 40)
    print("Partitions and Usage:")
    # get all disk partitions
    partitions = psutil.disk_partitions()
    for partition in partitions:
        print("=== Device: {}" .format(partition.device) +'===')
        print("Mountpoint: {}" .format(partition.mountpoint))
        print("File system type: {}" .format(partition.fstype))
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            # this can be catched due to the disk that
            # isn't ready
            continue
        print("Total Size: {}" .format(get_size(partition_usage.total)))
        print("Used:{}" .format(get_size(partition_usage.used)))
        print("Free: {}" .format(get_size(partition_usage.free)))
        print("Percentage: {}" .format(partition_usage.percent))
    # get IO statistics since boot
    disk_io = psutil.disk_io_counters()
    print("Total read: {}".format(get_size(disk_io.read_bytes)))
    print("Total write: {}" .format(get_size(disk_io.write_bytes)))


# Network information
def network_info():
    print("=" * 40, "Network Information", "=" * 40)
    # get all network interfaces (virtual and physical)
    if_addrs = psutil.net_if_addrs()
    for interface_name, interface_addresses in if_addrs.items():
        for address in interface_addresses:
            print("=== Interface: {} === " .format(interface_name))
            if str(address.family) == 'AddressFamily.AF_INET':
                print("  IP Address: {}" .format(address.address))
                print("  Netmask:{}" .format(address.netmask))
                print("  Broadcast IP: {}" .format(address.broadcast))
            elif str(address.family) == 'AddressFamily.AF_PACKET':
                print("  MAC Address: {}" .format(address.address))
                print("  Netmask: {}" .format(address.netmask))
                print("  Broadcast MAC: {}" .format(address.broadcast))
    # get IO statistics since boot
    net_io = psutil.net_io_counters()
    print("Total Bytes Sent:{} " .format(get_size(net_io.bytes_sent)))
    print("Total Bytes Received: {} ".format(get_size(net_io.bytes_recv)))


if __name__ == "__main__":
    get_SystemInfo()
    get_SystemBootTime()
    memory_info()
    network_info()
    # disk_info()
    cpu_info()
    print("check done")
