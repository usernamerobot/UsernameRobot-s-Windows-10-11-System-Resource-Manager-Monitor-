╔═════════════════════════════════════════════════════════════════════════════════╗
║                                                                                 ║
║  _   _                                                    _           _   _     ║
║ | | | |___  ___ _ __ _ __   __ _ _ __ ___   ___ _ __ ___ | |__   ___ | |_( )___ ║
║ | | | / __|/ _ \ '__| '_ \ / _` | '_ ` _ \ / _ \ '__/ _ \| '_ \ / _ \| __|// __|║
║ | |_| \__ \  __/ |  | | | | (_| | | | | | |  __/ | | (_) | |_) | (_) | |_  \__ \║
║  \___/|___/\___|_|  |_| |_|\__,_|_| |_| |_|\___|_|  \___/|_.__/ \___/ \__| |___/║
║                                                                                 ║
║                   SYSTEM RESOURCE MANAGER for Windows 10/11  (Python)                   ║
║                                                                                 ║
╚═════════════════════════════════════════════════════════════════════════════════╝

----------------------------------------------

Simple command-line system monitor and manager for Windows 10 and 11.
Built with Python. Runs in a terminal.

Monitors system resources in real time and provides basic process
and service management tools :)

--------------------------------------------------
FEATURES
--------------------------------------------------

[Monitoring]
- Real-time CPU, memory, and disk usage
- Disk read/write stats
- Network activity monitoring
- CPU/GPU temperature (if supported)
- Battery info (laptops only)

[Processes]
- List running processes
- Search processes by name
- Detailed process info (priority, threads, status, start time)
- Top 5 memory-consuming processes
- Memory cleanup (non-critical apps only)

[System]
- Startup program manager
- Windows service manager
- Scheduled automatic cleanup
- Export system report to CSV

--------------------------------------------------
REQUIREMENTS
--------------------------------------------------

- Windows 10 or Windows 11
- Python 3.6+
- psutil
- electricity

Install dependency:

    pip install psutil

Run program:

    python win_resource_manager.py

--------------------------------------------------
MAIN MENU
--------------------------------------------------

1  - Basic System Info
2  - Real-Time Monitoring
3  - Search Process
4  - Network Monitoring
5  - Temperature Monitoring
6  - Startup Programs
7  - Detailed Process Info
8  - Custom Memory Cleanup
9  - Running Processes
10 - Top Resource Hogs
11 - Disk I/O Statistics
12 - Battery Info
13 - Service Manager
14 - Scheduled Cleanup
15 - Export Report
16 - Exit

--------------------------------------------------
EXAMPLES
--------------------------------------------------

Real Time Monitoring:
    Select option 2
    Press Ctrl+C to stop

Search Process:
    Select option 3
    Enter process name (example: chrome)

Memory Cleanup:
    Select option 8
    Set memory threshold (default: 100 MB)
    Only non-critical apps are terminated

Export Report:
    Select option 15
    Enter filename
    CSV file will be generated

--------------------------------------------------
NOTES
--------------------------------------------------

- Some features require Administrator privileges.
- Temperature monitoring depends on hardware support I don't really know I have not tested the program on enough devices yet.
- Battery info only works on laptops or custom desktops with laptop batteries?
- Use cleanup features carefully I have crashed my pc with it so proceed with caution when using the feature.

--------------------------------------------------
LICENSE
--------------------------------------------------

MIT License 

Author: UsernameRobot 




