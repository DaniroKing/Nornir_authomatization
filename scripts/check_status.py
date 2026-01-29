#!/usr/bin/env python3

# Скрипт для проверки состояния устройств

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from nornir import InitNornir
from nornir_utils.plugins.functions import print_result

from tasks.status import check_connectivity, check_basic_info
from utils.helpers import print_separator
from utils.reports import generate_status_report

def main():
    """Checking device status"""
    print_separator("CHECKING DEVICE STATUS")
    
    try:
        # Инициализация Nornir
        nr = InitNornir(config_file="config/nornir_config.yaml")
        
        print(f"Checking it out {len(nr.inventory.hosts)} devices")
        
        # Проверка доступности
        print("\n1. Checking availability...")
        connectivity_results = nr.run(task=check_connectivity)
        print_result(connectivity_results)
        
        # проверяем только доступные устройства
        available_devices = nr.filter(lambda host: not connectivity_results[host.name].failed)
        
        if len(available_devices.inventory.hosts) > 0:
            print("\n2. Getting basic information")
            info_results = available_devices.run(task=check_basic_info)
            print_result(info_results)
        else:
            info_results = {}
        
        # Создание отчета
        report_file = generate_status_report(connectivity_results, info_results)
        
        # Резюме
        total = len(nr.inventory.hosts)
        available = len(available_devices.inventory.hosts)
        
        print_separator("AUDIT RESULTS")
        print(f"Total devices: {total}")
        print(f"Доступно: {available}")
        print(f"Unavailable: {total - available}")
        print(f"Report: {report_file}")
        
        return 0
        
    except Exception as error:
        print(f"ОVerification error: {str(error)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())