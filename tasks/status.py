# Tasks for checking device status

from nornir.core.task import Task, Result

def check_connectivity(task: Task) -> Result:
    # проверяем доступность устройства
    try:
        conn = task.host.get_connection("netmiko")
        
        if conn.is_alive():
            # пытаемся выполнить простую команду
            conn.send_command("show version", read_timeout=30)
            return Result(
                host=task.host,
                result="The device is available",
                changed=False
            )
        else:
            return Result(
                host=task.host,
                result="The device is unavailable",
                failed=True
            )
            
    except Exception as e:
        return Result(
            host=task.host,
            result=f"Connection error: {str(e)}",
            failed=True
        )

def check_basic_info(task: Task) -> Result:
    # Проверяем основную информацию об устройстве
    try:
        conn = task.host.get_connection("netmiko")
        
        if task.host.platform == "cisco_ios":
            # Получение версии для iOS
            version_output = conn.send_command("show version", use_textfsm=True)
            
            # Получение информации об интерфейсах
            interfaces_output = conn.send_command("show ip interface brief", use_textfsm=True)
            
            result_info = {
                "platform": "Cisco IOS",
                "version": str(version_output)[:100] if version_output else "N/A",
                "interfaces_count": len(interfaces_output) if interfaces_output else 0
            }
            
        else:
            result_info = {
                "platform": task.host.platform,
                "status": "Basic checks passed"
            }
        
        return Result(
            host=task.host,
            result=result_info,
            changed=False
        )
        
    except Exception as e:
        return Result(
            host=task.host,
            result=f"Verification error: {str(e)}",
            failed=True
        )