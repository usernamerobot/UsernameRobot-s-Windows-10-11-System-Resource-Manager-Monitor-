import psutil
import time
import csv
from datetime import datetime
import subprocess
import threading
import os

# Global variable for scheduled cleanup be very careful with this feture it has crashed my pc before.
cleanup_thread = None
cleanup_active = False

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title):
    print("\n" + "="*50)
    print(f"  {title.center(46)}")
    print("="*50 + "\n")

def print_section(text):
    print(f"\n{'─'*50}")
    print(f"  {text}")
    print(f"{'─'*50}\n")

def print_title():
    print("""
╔═════════════════════════════════════════════════════════════════════════════════╗
║                                                                                 ║
║  _   _                                                    _           _   _     ║
║ | | | |___  ___ _ __ _ __   __ _ _ __ ___   ___ _ __ ___ | |__   ___ | |_( )___ ║
║ | | | / __|/ _ \ '__| '_ \ / _` | '_ ` _ \ / _ \ '__/ _ \| '_ \ / _ \| __|// __|║
║ | |_| \__ \  __/ |  | | | | (_| | | | | | |  __/ | | (_) | |_) | (_) | |_  \__ \║
║  \___/|___/\___|_|  |_| |_|\__,_|_| |_| |_|\___|_|  \___/|_.__/ \___/ \__| |___/║
║                                                                                 ║
║                   SYSTEM RESOURCE MANAGER for Windows 10/11                     ║
║                                                                                 ║
╚═════════════════════════════════════════════════════════════════════════════════╝
    """)

def print_menu():
    clear_screen()
    print_title()
    print("\n")
    print("╔" + "═"*48 + "╗")
    print("║" + " SYSTEM RESOURCE MANAGER".center(48) + "║")
    print("╠" + "═"*48 + "╣")
    print("║  1:  Basic System Info                         ║")
    print("║  2:  Real-Time Monitoring                      ║")
    print("║  3:  Search Process                            ║")
    print("║  4:  Network Monitoring                        ║")
    print("║  5:  Temperature Monitoring                    ║")
    print("║  6:  Startup Programs                          ║")
    print("║  7:  Detailed Process Info                     ║")
    print("║  8:  Custom Memory Cleanup                     ║")
    print("║  9:  Running Processes                         ║")
    print("║  10: Top Resource Hogs                         ║")
    print("║  11: Disk I/O Statistics                       ║")
    print("║  12: Battery Info                              ║")
    print("║  13: Service Manager                           ║")
    print("║  14: Scheduled Cleanup                         ║")
    print("║  15: Export Report                             ║")
    print("║  16: Exit                                      ║")
    print("╚" + "═"*48 + "╝\n")

def display_system_info():
    print_header("SYSTEM INFORMATION")
    
    cpu_count = psutil.cpu_count()
    mem_total = psutil.virtual_memory().total / (1024**3)
    disk_usage = psutil.disk_usage('C:').percent
    
    print(f"  [+] CPU Count:        {cpu_count} cores")
    print(f"  [+] Memory:           {mem_total:.2f} GB")
    print(f"  [+] Disk Usage (C:):  {disk_usage}%")
    
    cpu_percent = psutil.cpu_percent()
    mem = psutil.virtual_memory()
    
    print(f"\n  [+] CPU Usage:        {cpu_percent}%")
    print(f"  [+] Memory Usage:     {mem.percent}%")
    print(f"  [+] Disk Usage:       {disk_usage}%")
    
    input("\n  Press Enter to continue...")

def real_time_monitoring():
    print_header("REAL-TIME SYSTEM MONITORING")
    print("  Press Ctrl+C to stop monitoring\n")
    try:
        while True:
            cpu = psutil.cpu_percent(interval=1)
            mem = psutil.virtual_memory()
            disk = psutil.disk_usage('C:')
            
            print(f"  CPU: {cpu:>3}% | Memory: {mem.percent:>3}% ({mem.used / (1024**3):>5.2f}GB / {mem.total / (1024**3):.2f}GB) | Disk: {disk.percent:>3}%")
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n  [*] Monitoring stopped.")
        input("  Press Enter to continue...")

def search_process():
    print_header("SEARCH PROCESS")
    search_name = input("  Enter process name to search: ").lower()
    found = False
    
    print(f"\n  {'PID':<10} {'NAME':<30} {'MEMORY (MB)':<15}")
    print("  " + "─"*55)
    
    for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
        if search_name in proc.info['name'].lower():
            print(f"  {proc.info['pid']:<10} {proc.info['name']:<30} {proc.info['memory_info'].rss / (1024**2):<15.2f}")
            found = True
    
    if not found:
        print(f"\n  [-] No process found with name: {search_name}")
    
    input("\n  Press Enter to continue...")

def network_monitoring():
    print_header("NETWORK MONITORING")
    
    net_before = psutil.net_io_counters()
    print(f"  Initial - Sent: {net_before.bytes_sent / (1024**2):.2f} MB")
    print(f"  Initial - Received: {net_before.bytes_recv / (1024**2):.2f} MB\n")
    print("  Measuring for 2 seconds...")
    
    time.sleep(2)
    
    net_after = psutil.net_io_counters()
    bytes_sent = net_after.bytes_sent - net_before.bytes_sent
    bytes_recv = net_after.bytes_recv - net_before.bytes_recv
    
    print(f"\n  [+] Sent (2 sec):      {bytes_sent / (1024):.2f} KB")
    print(f"  [+] Received (2 sec):  {bytes_recv / (1024):.2f} KB")
    print(f"  [+] Active Connections: {len(psutil.net_connections())}")
    
    input("\n  Press Enter to continue...")

def temperature_monitoring():
    print_header("TEMPERATURE MONITORING")
    try:
        temps = psutil.sensors_temperatures()
        if temps:
            for name, entries in temps.items():
                print(f"  {name}:")
                for entry in entries:
                    print(f"    └─ {entry.label}: {entry.current}°C")
        else:
            print("  [-] Temperature sensors not available on this system.")
    except Exception as e:
        print(f"  [-] Error reading temperatures: {e}")
    
    input("\n  Press Enter to continue...")

def startup_programs_manager():
    print_header("STARTUP PROGRAMS MANAGER")
    try:
        result = subprocess.run(["powershell", "-Command", "Get-CimInstance Win32_StartupCommand | Select-Object Name, Command"], 
                              capture_output=True, text=True)
        print(result.stdout)
    except Exception as e:
        print(f"  [-] Error retrieving startup programs: {e}")
    
    input("\n  Press Enter to continue...")

def detailed_process_info():
    print_header("DETAILED PROCESS INFORMATION")
    search_name = input("  Enter process name for details: ").lower()
    found = False
    
    for proc in psutil.process_iter(['pid', 'name', 'memory_info', 'create_time']):
        if search_name in proc.info['name'].lower():
            try:
                p = psutil.Process(proc.info['pid'])
                create_time = datetime.fromtimestamp(proc.info['create_time']).strftime('%Y-%m-%d %H:%M:%S')
                print(f"\n  [+] PID:       {proc.info['pid']}")
                print(f"  [+] Name:      {proc.info['name']}")
                print(f"  [+] Memory:    {proc.info['memory_info'].rss / (1024**2):.2f} MB")
                print(f"  [+] Created:   {create_time}")
                print(f"  [+] Priority:  {p.nice()}")
                print(f"  [+] Status:    {p.status()}")
                print(f"  [+] Threads:   {p.num_threads()}")
                found = True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
    
    if not found:
        print(f"\n  [-] No process found with name: {search_name}")
    
    input("\n  Press Enter to continue...")

def memory_threshold_customization():
    print_header("MEMORY THRESHOLD CUSTOMIZATION")
    try:
        threshold = int(input("  Enter memory threshold in MB (default 100): "))
        return threshold
    except ValueError:
        print("  [-] Invalid input, using default 100 MB")
        return 100

def export_report():
    print_header("EXPORT SYSTEM REPORT")
    filename = input("  Enter filename (without extension): ")
    
    try:
        with open(f"{filename}.csv", 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Metric', 'Value'])
            
            mem = psutil.virtual_memory()
            disk = psutil.disk_usage('C:')
            
            writer.writerow(['CPU Usage', f"{psutil.cpu_percent()}%"])
            writer.writerow(['Memory Usage', f"{mem.percent}%"])
            writer.writerow(['Memory Used', f"{mem.used / (1024**3):.2f} GB"])
            writer.writerow(['Memory Total', f"{mem.total / (1024**3):.2f} GB"])
            writer.writerow(['Disk Usage', f"{disk.percent}%"])
            writer.writerow(['Timestamp', datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
        
        print(f"\n  [+] Report saved as {filename}.csv")
    except Exception as e:
        print(f"  [-] Error saving report: {e}")
    
    input("\n  Press Enter to continue...")

def disk_io_statistics():
    print_header("DISK I/O STATISTICS")
    
    io_before = psutil.disk_io_counters()
    print(f"  Initial - Read:  {io_before.read_bytes / (1024**3):.2f} GB")
    print(f"  Initial - Write: {io_before.write_bytes / (1024**3):.2f} GB\n")
    print("  Measuring for 2 seconds...")
    
    time.sleep(2)
    
    io_after = psutil.disk_io_counters()
    read_speed = (io_after.read_bytes - io_before.read_bytes) / (1024**2) / 2
    write_speed = (io_after.write_bytes - io_before.write_bytes) / (1024**2) / 2
    
    print(f"\n  [+] Read Speed:  {read_speed:.2f} MB/s")
    print(f"  [+] Write Speed: {write_speed:.2f} MB/s")
    
    input("\n  Press Enter to continue...")

def battery_info():
    print_header("BATTERY INFORMATION")
    try:
        battery = psutil.sensors_battery()
        if battery:
            print(f"  [+] Battery Level: {battery.percent}%")
            print(f"  [+] Plugged In: {'Yes' if battery.power_plugged else 'No'}")
            if battery.secsleft != psutil.POWER_TIME_UNLIMITED:
                hours = battery.secsleft // 3600
                minutes = (battery.secsleft % 3600) // 60
                print(f"  [+] Time Remaining: {hours}h {minutes}m")
        else:
            print("  [*] No battery detected (Desktop computer)")
    except Exception as e:
        print(f"  [-] Error reading battery: {e}")
    
    input("\n  Press Enter to continue...")

def service_manager():
    print_header("SERVICE MANAGER")
    try:
        result = subprocess.run(["powershell", "-Command", "Get-Service | Select-Object Name, Status | Head -20"], 
                              capture_output=True, text=True)
        print(result.stdout)
    except Exception as e:
        print(f"  [-] Error retrieving services: {e}")
    
    input("\n  Press Enter to continue...")

def display_running_processes():
    print_header("RUNNING PROCESSES")
    print(f"  {'PID':<10} {'NAME':<35} {'MEMORY (MB)':<15}")
    print("  " + "─"*60)
    
    for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
        print(f"  {proc.info['pid']:<10} {proc.info['name']:<35} {proc.info['memory_info'].rss / (1024**2):<15.2f}")
    
    input("\n  Press Enter to continue...")

def display_top_resource_hogs():
    print_header("TOP RESOURCE-CONSUMING APPLICATIONS")
    processes = [(proc.info['name'], proc.info['memory_info'].rss) for proc in psutil.process_iter(['name', 'memory_info'])]
    top_processes = sorted(processes, key=lambda x: x[1], reverse=True)[:5]
    
    print(f"  {'RANK':<8} {'NAME':<35} {'MEMORY (MB)':<15}")
    print("  " + "─"*60)
    
    for idx, (name, memory) in enumerate(top_processes, 1):
        print(f"  {idx:<8} {name:<35} {memory / (1024**2):<15.2f}")
    
    input("\n  Press Enter to continue...")

def scheduled_cleanup():
    global cleanup_thread, cleanup_active
    print_header("SCHEDULED CLEANUP")
    try:
        interval = int(input("  Enter cleanup interval in seconds (minimum 60): "))
        if interval < 60:
            print("  [-] Interval must be at least 60 seconds")
            input("  Press Enter to continue...")
            return
        
        cleanup_active = True
        print(f"\n  [+] Scheduled cleanup every {interval} seconds. Running in background...")
        
        def cleanup_loop():
            while cleanup_active:
                time.sleep(interval)
                if cleanup_active:
                    print("\n  [*] Running scheduled cleanup...")
                    mem_before = psutil.virtual_memory().used
                    
                    safe_processes = ['chrome.exe', 'firefox.exe', 'discord.exe', 'spotify.exe', 'vlc.exe']
                    
                    for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
                        if proc.info['memory_info'].rss > 100 * 1024 * 1024:
                            if any(safe in proc.info['name'].lower() for safe in safe_processes):
                                try:
                                    proc.terminate()
                                except (psutil.NoSuchProcess, psutil.AccessDenied):
                                    pass
                    
                    mem_after = psutil.virtual_memory().used
                    print(f"  [+] Cleanup complete. Freed: {(mem_before - mem_after) / (1024**2):.2f} MB\n")
        
        cleanup_thread = threading.Thread(target=cleanup_loop, daemon=True)
        cleanup_thread.start()
    except ValueError:
        print("  [-] Invalid input")
    
    input("  Press Enter to continue...")

def stop_scheduled_cleanup():
    global cleanup_active
    cleanup_active = False
    print_header("SCHEDULED CLEANUP")
    print("  [+] Scheduled cleanup stopped.")
    input("  Press Enter to continue...")

def clear_resources(threshold=100):
    print_header("CLEARING RESOURCES")
    print("  [!] WARNING: This will terminate processes consuming excessive memory.")
    confirm = input("\n  Are you sure you want to continue? (yes/no): ").lower()
    
    if confirm != 'yes':
        print("\n  [-] Operation cancelled.")
        input("  Press Enter to continue...")
        return
    
    mem_before = psutil.virtual_memory().used
    
    safe_processes = [
        'chrome.exe', 'msedge.exe', 'firefox.exe', 'opera.exe', 'brave.exe',
        'discord.exe', 'telegram.exe', 'whatsapp.exe', 'skype.exe', 'teams.exe', 'zoom.exe', 'slack.exe',
        'steam.exe', 'epicgameslauncher.exe', 'battle.net.exe', 'ubioftconnect.exe', 'riotclientservices.exe', 'ea desktop.exe', 'xboxappservices.exe',
        'spotify.exe', 'itunes.exe', 'netflix.exe', 'vlc.exe', 'obs64.exe',
        'onedrive.exe', 'dropbox.exe', 'googledrivefdfs.exe', 'icloudservices.exe',
        'nvidia share.exe', 'nvidia web helper.exe', 'radesnsoftware.exe', 'intelgraphicscommandcenter.exe',
        'hpprintscandoctor.exe', 'epsonstausmonitor.exe', 'logitechghub.exe', 'razersynapse.exe', 'corsair.service.exe',
        'adobegcclient.exe', 'creativecloud.exe', 'ccxprocess.exe', 'coresync.exe',
        'searchapp.exe', 'startmenuexperiencehost.exe', 'runtimebroker.exe', 'shellexperiencehost.exe', 'yourphone.exe', 'widgets.exe', 'calculator.exe', 'notepad.exe',
        'googleupdate.exe', 'microsoftedgeupdate.exe', 'adobeupdateservice.exe', 'steamservice.exe', 'discordupdate.exe'
    ]
    
    terminated_count = 0
    print("\n")
    for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
        if proc.info['memory_info'].rss > threshold * 1024 * 1024:
            if any(safe_name in proc.info['name'].lower() for safe_name in safe_processes):
                try:
                    print(f"  [X] Terminating: {proc.info['name']} (PID: {proc.info['pid']})")
                    proc.terminate()
                    terminated_count += 1
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
    
    mem_after = psutil.virtual_memory().used
    memory_freed = mem_before - mem_after
    
    print(f"\n  [+] Safely terminated {terminated_count} process(es).")
    print(f"  [+] Memory freed: {memory_freed / (1024**2):.2f} MB")
    
    input("\n  Press Enter to continue...")

def scheduled_cleanup_menu():
    while True:
        clear_screen()
        print("\n")
        print("╔" + "═"*48 + "╗")
        print("║" + "SCHEDULED CLEANUP".center(48) + "║")
        print("╠" + "═"*48 + "╣")
        print("║  1: Start Scheduled Cleanup                    ║")
        print("║  2: Stop Scheduled Cleanup                     ║")
        print("║  0: Back to Main Menu                          ║")
        print("╚" + "═"*48 + "╝\n")
        
        choice = input("  Enter your choice: ")
        
        if choice == '1':
            scheduled_cleanup()
        elif choice == '2':
            stop_scheduled_cleanup()
        elif choice == '0':
            break
        else:
            print("  [-] Invalid choice. Please try again.")
            time.sleep(1)
# that's alot of options, if you have any suggestions for more features or improvements please let me know. I have been working on this project for a while and would love to hear your feedback.
def main():
    while True:
        print_menu()
        choice = input("  Enter your choice: ")
        
        if choice == '1':
            display_system_info()
        elif choice == '2':
            real_time_monitoring()
        elif choice == '3':
            search_process()
        elif choice == '4':
            network_monitoring()
        elif choice == '5':
            temperature_monitoring()
        elif choice == '6':
            startup_programs_manager()
        elif choice == '7':
            detailed_process_info()
        elif choice == '8':
            threshold = memory_threshold_customization()
            clear_resources(threshold)
        elif choice == '9':
            display_running_processes()
        elif choice == '10':
            display_top_resource_hogs()
        elif choice == '11':
            disk_io_statistics()
        elif choice == '12':
            battery_info()
        elif choice == '13':
            service_manager()
        elif choice == '14':
            scheduled_cleanup_menu()
        elif choice == '15':
            export_report()
        elif choice == '16':
            print_header("GOODBYE")
            print("  Thank you for using System Resource Manager!")
            global cleanup_active
            cleanup_active = False
            time.sleep(1)
            break
        else:
            print("  [-] Invalid choice. Please try again.")
            time.sleep(1)

if __name__ == "__main__":
    main()