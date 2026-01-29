# Tasks for device backups

import os
from datetime import datetime
from nornir.core.task import Task, Result

def backup_running_config(task: Task, backup_dir: str = "backups") -> Result:

    # Создание папки для резервных копий
    os.makedirs(backup_dir, exist_ok=True)
    
    try:
        # Подключение к устройству
        conn = task.host.get_connection("netmiko")
        
        # Мы получаем конфигурацию в зависимости от платформы
        if task.host.platform == "cisco_ios":
            config = conn.send_command("show running-config")
        elif task.host.platform == "juniper_junos":
            config = conn.send_command("show configuration | display set")
        else:
            config = conn.send_command("show running-config")
        
        # Сохраните его в файл
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{backup_dir}/{task.host.name}_{timestamp}.cfg"
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(config)
        
        return Result(
            host=task.host,
            result=f"Backup saved: {filename}",
            changed=False
        )
        
    except Exception as e:
        return Result(
            host=task.host,
            result=f"Backup error: {str(e)}",
            failed=True
        )

def backup_startup_config(task: Task, backup_dir: str = "backups") -> Result:
    
    try:
        conn = task.host.get_connection("netmiko")
        
        # Получение конфигурации запуска
        if task.host.platform == "cisco_ios":
            config = conn.send_command("show startup-config")
        elif task.host.platform == "juniper_junos":
            config = conn.send_command("show configuration")
        else:
            config = conn.send_command("show startup-config")
        
        # Сохраняем его в файл
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{backup_dir}/{task.host.name}_startup_{timestamp}.cfg"
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(config)
        
        return Result(
            host=task.host,
            result=f"Startup backup saved: {filename}",
            changed=False
        )
        
    except Exception as e:
        return Result(
            host=task.host,
            result=f"Startup backup error: {str(e)}",
            failed=True
        )