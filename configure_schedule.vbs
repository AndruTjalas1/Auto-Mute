Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "C:\Auto-Mute\.venv\Scripts\pythonw.exe C:\Auto-Mute\config_gui.py", 1, False
Set WshShell = Nothing
