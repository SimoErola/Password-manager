import platform
import os
import subprocess
import string 

class DeviceTrustManager:
    def __init__(self):
        self.trust_level = 0
        
    def check_os(self):
        if platform.system() in ['Windows', 'Linux', 'Darwin']:
            self.trust_level += 1

    def check_usb_devices(self):
        usb_device_name = "PMUSB_00001"
        connected_devices = ""
        try:
            if platform.system() == 'Linux':
                connected_devices = subprocess.check_output('lsblk -o NAME,LABEL', shell=True).decode('utf-8')
            elif platform.system() == 'Windows':
                drives = [f"{d}:" for d in string.ascii_uppercase if os.path.exists(f"{d}:\\" )]
                for drive in drives:
                    drive_name = subprocess.check_output(f'vol {drive}', shell=True).decode('utf-8')
                    connected_devices += drive_name
            elif platform.system() == 'Darwin':
                connected_devices = subprocess.check_output('diskutil list', shell=True).decode('utf-8')
        except subprocess.CalledProcessError as e:
            print(f"Error occurred: {e}")
                
        if usb_device_name in connected_devices:
            self.trust_level += 1

    def check_antivirus(self):
        try:
            if platform.system() == 'Windows':
                antivirus_status = subprocess.check_output('powershell "Get-MpPreference | Select-Object -ExpandProperty DisableRealtimeMonitoring"', shell=True).decode('utf-8')
                if antivirus_status.strip() == 'False':
                    self.trust_level += 1
            elif platform.system() in ['Linux', 'Darwin']:
                self.trust_level += 1
                pass
        except subprocess.CalledProcessError as e:
            print(f"Error occurred: {e}")
            
    def assess_device_trust(self):
        self.check_os()
        self.check_usb_devices()
        self.check_antivirus()
        if self.trust_level == 3:
            return True
        else:
            return False