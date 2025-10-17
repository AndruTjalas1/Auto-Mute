Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "C:\Auto-Mute\.venv\Scripts\pythonw.exe C:\Auto-Mute\auto_mute.py --tray", 0, False
Set WshShell = Nothing
