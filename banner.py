import os
import platform
import subprocess
import sys

def show_banner():
        # Enable VT100 escape sequences in Windows terminals
        if platform.system() == 'Windows':
            os.system('')  # This enables VT100 escape sequences in Windows terminals
    
        # ASCII art for the banner
        banner_lines = [
            "   ░█████╗░██████╗░████████╗██╗  ░█████╗░██████╗░░█████╗░░██╗░░░░░░░██╗██╗░░░░░",
            "   ██╔══██╗██╔══██╗╚══██╔══╝██║  ██╔══██╗██╔══██╗██╔══██╗░██║░░██╗░░██║██║░░░░░",
            "   ██║░░██║██████╔╝░░░██║░░░██║  ██║░░╚═╝██████╔╝███████║░╚██╗████╗██╔╝██║░░░░░",
            "   ██║░░██║██╔═══╝░░░░██║░░░██║  ██║░░██╗██╔══██╗██╔══██║░░████╔═████║░██║░░░░░",
            "   ╚█████╔╝██║░░░░░░░░██║░░░██║  ╚█████╔╝██║░░██║██║░░██║░░╚██╔╝░╚██╔╝░███████╗",
            "   ░╚════╝░╚═╝░░░░░░░░╚═╝░░░╚═╝  ░╚════╝░╚═╝░░╚═╝╚═╝░░╚═╝░░░╚═╝░░░╚═╝░░╚══════╝",
            "                         The 🔥 Hottest Scraper in Town"
    ]

        # Check if we're in PowerShell
        is_powershell = False
        if platform.system() == 'Windows':
            # Check if we're in PowerShell by looking at parent process name
            try:
                import subprocess
                parent_process = subprocess.check_output(['powershell', '-Command', 
                                                        '(Get-Process -Id $PID).Parent.ProcessName']).decode().strip()
                is_powershell = 'powershell' in parent_process.lower()
            except:
                # If we can't check, assume standard terminal
                pass
    
        if is_powershell:
            # PowerShell-specific way to output colored text
            import subprocess
            for line in banner_lines:
                ps_cmd = f'Write-Host "{line}" -ForegroundColor Red'
                subprocess.run(['powershell', '-Command', ps_cmd])
        else:
            # Standard ANSI color approach for other terminals
            red_color = '\033[31m'
            reset_color = '\033[0m'
            print(f"{red_color}")
            for line in banner_lines:
                print(line)
            print(f"{reset_color}")

    # Display the banner
show_banner()