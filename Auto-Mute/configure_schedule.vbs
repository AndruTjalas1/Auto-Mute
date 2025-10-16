Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "C:\Personal\.venv\Scripts\pythonw.exe C:\Personal\config_gui.py", 1, False
Set WshShell = Nothing
