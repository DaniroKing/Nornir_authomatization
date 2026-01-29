#!/usr/bin/env python3

# резервное копирование по приоритетам


import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from nornir import InitNornir
from nornir.core.filter import F
from nornir_utils.plugins.functions import print_result

from tasks.backup import backup_running_config
from utils.helpers import print_separator

def backup_by_priority(priority_level):
    """Device backup by specific priority"""
    
    nr = InitNornir(config_file="config/nornir_config.yaml")
    
    # Фильтрация устройств по приоритету
    priority_devices = nr.filter(F(data__backup_priority=priority_level))
    
    if len(priority_devices.inventory.hosts) == 0:
        print(f"There are no priority devices: {priority_level}")
        return None
    
    print_separator(f"Backup: {priority_level.upper()} priority")
    print(f"Devices: {len(priority_devices.inventory.hosts)}")
    
    # Запуск резервного копирования
    results = priority_devices.run(task=backup_running_config)
    
    # обеспечиваем результаты
    print_result(results)
    
    return results

def main():
    print_separator("Backup by priority")
    
    try:
        # ВЫСОКИЙ ПРИОРИТЕТ
        high_results = backup_by_priority("high")
        
        # СРЕДНИЙ ПРИОРИТЕТ
        medium_results = backup_by_priority("medium")
        
        # НИЗКИЙ ПРИОРИТЕТ
        low_results = backup_by_priority("low")
        
        # Статистические
        print_separator("Results:")
        
        total_success = 0
        total_failed = 0
        
        for priority, results in [("HIGH", high_results), ("MEDIUM", medium_results), ("LOW", low_results)]:
            if results:
                success = len([r for r in results.values() if not r.failed])
                failed = len([r for r in results.values() if r.failed])
                total_success += success
                total_failed += failed
                print(f" {priority}: {success} successfully, {failed} errors")
        
        print(f"\n Total: {total_success} successfully, {total_failed} errors")
        
        return 0 if total_failed == 0 else 1
        
    except Exception as error:
        print(f" Critical error: {str(error)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())