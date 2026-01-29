
# Создание отчетов
import json
import csv
from datetime import datetime
from typing import Dict, Any

def generate_backup_report(results, report_type: str = "backup") -> str:
    # Создает отчет о резервном копировании
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"logs/backup_report_{timestamp}.json"
    
    # Создание каталога для журналов
    import os
    os.makedirs("logs", exist_ok=True)
    
    report_data = {
        "timestamp": get_timestamp(),
        "type": report_type,
        "summary": {
            "total": len(results),
            "successful": len([r for r in results.values() if not r.failed]),
            "failed": len([r for r in results.values() if r.failed])
        },
        "devices": {}
    }
    
    for hostname, result in results.items():
        report_data["devices"][hostname] = {
            "success": not result.failed,
            "result": str(result.result),
            "changed": getattr(result, 'changed', False)
        }
    
    # Сохранение отчета
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report_data, f, indent=2, ensure_ascii=False)
    
    return report_file

def generate_status_report(connectivity_results, info_results) -> str:
    # Создаем отчет о состоянии устройства
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"logs/status_report_{timestamp}.json"
    
    report_data = {
        "timestamp": get_timestamp(),
        "devices": {}
    }
    
    for hostname in connectivity_results.keys():
        report_data["devices"][hostname] = {
            "connectivity": {
                "status": "OK" if not connectivity_results[hostname].failed else "FAILED",
                "result": str(connectivity_results[hostname].result)
            },
            "info": {
                "status": "OK" if hostname in info_results and not info_results[hostname].failed else "FAILED",
                "data": info_results[hostname].result if hostname in info_results else {}
            }
        }
    
    # Сохранение отчета
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report_data, f, indent=2, ensure_ascii=False)
    
    return report_file

def get_timestamp():
    # Вспомогательная функция для определения времени
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")