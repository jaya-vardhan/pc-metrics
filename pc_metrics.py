import psutil
import subprocess
from mail import Mailer
import re
from datetime import datetime, timedelta

class PcMetrics:

    def __init__(self):
        pass

    def get_metrics(self):
        result = {}
        result['battery'] = self.get_battery_metrics()
        self.send_mail(result)
        return result

    def get_battery_metrics(self):
        battery = psutil.sensors_battery()
        _battery = self.get_battery_subprocess_metrics()
        battery_metrics = {
            'percent': battery.percent,
            'power_plugged': battery.power_plugged,
            **_battery
        }
        if battery.power_plugged:
            battery_metrics['time_to_shutdown'] = 'N/A'
        else:
            battery_metrics['time_to_shutdown'] = battery.secsleft
        return battery_metrics

    def send_mail(self, data):
        Mailer().send(data)

    def get_battery_path(self):
        result = subprocess.run(['upower', '-e'], stdout=subprocess.PIPE)
        devices = result.stdout.decode().splitlines()
        for device in devices:
            if 'battery' in device.lower():
                return device
        return None

    def get_battery_subprocess_metrics(self):
        battery_path = self.get_battery_path()
        result = {
            'full_charge_time': 'N/A'
        }
        if battery_path:
            cmd_response = subprocess.run(['upower', '-i', battery_path], stdout=subprocess.PIPE)
            output = cmd_response.stdout.decode().splitlines()
            charge_time_line = ''
            for line in output:
                line = line.strip()
                if ("time to full:" or "time to empty:") in line:
                    charge_time_line = line
            if charge_time_line:
                match = re.search(r'(\d+(\.\d+)?)', charge_time_line)
                if match:
                    minutes = float(match.group(1))
                    future_time = datetime.now() + timedelta(minutes=minutes)
                    result['full_charge_time'] = minutes
                    result['full_charge_by'] = future_time.strftime('%y-%m-%d %H:%M')
        return result
