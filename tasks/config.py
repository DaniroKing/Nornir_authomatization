#Задачи для настройки устройств

from nornir.core.task import Task, Result

def deploy_commands(task: Task, commands: list) -> Result:
    # Расширяет список команд на устройстве
    try:
        conn = task.host.get_connection("netmiko")
        
        # Для устройств Cisco
        if task.host.platform == "cisco_ios":
            #Switching to enable mode
            conn.enable()
            
            # Отправка конфигурационных команд
            output = conn.send_config_set(commands)
            
            # Сохранение конфигурации
            save_output = conn.save_config()
            
            result_output = f"{output}\n\nSave: {save_output}"
            
        # Для устройств Juniper
        elif task.host.platform == "juniper_junos":
            # Переключение в режим настройки
            conn.config_mode()
            
            # Отправка команд
            output = ""
            for command in commands:
                output += conn.send_command(command) + "\n"
            
            # Фиксация изменений
            commit_output = conn.commit()
            result_output = f"{output}\n\nCommit: {commit_output}"
            
        else:
            # Для других платформ
            result_output = conn.send_config_set(commands)
        
        return Result(
            host=task.host,
            result=result_output,
            changed=True
        )
        
    except Exception as e:
        return Result(
            host=task.host,
            result=f"Ошибка настройки: {str(e)}",
            failed=True
        )