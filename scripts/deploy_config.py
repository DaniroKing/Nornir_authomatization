#!/usr/bin/env python3

# Скрипт для настройки устройств


import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from nornir import InitNornir
from nornir_utils.plugins.functions import print_result

from tasks.config import deploy_commands
from utils.helpers import print_separator
from utils.reports import generate_backup_report

def main():
    """Configuring devices"""
    print_separator("Configuring devices")
    
    # Команды для настройки
    config_commands = [
        "interface loopback100",
        "description Test interface from Nornir",
        "ip address 192.168.100.1 255.255.255.255"
    ]
    
    try:
        # Инициализация Nornir
        nr = InitNornir(config_file="config/nornir_config.yaml")
        
        print(f"Devices will be configured: {len(nr.inventory.hosts)}")
        print(f"Commands: {config_commands}")
        
        # Подтверждение
        confirm = input("\n Continue? (y/n): ")
        if confirm.lower() != 'y':
            print("Cancelled by the user")
            return 0
        
        # Запуск программы настройки
        results = nr.run(task=deploy_commands, commands=config_commands)
        
        # Отображение результатов
        print_result(results)
        
        # Создание отчета
        report_file = generate_backup_report(results, "deployment")
        
        print_separator("SETUP IS COMPLETED")
        print(f"Report: {report_file}")
        
        return 0
        
    except Exception as error:
        print(f"Configuration error: {str(error)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())