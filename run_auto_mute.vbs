Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "C:\Personal\.venv\Scripts\pythonw.exe C:\Personal\auto_mute.py", 0, False
Set WshShell = Nothing
