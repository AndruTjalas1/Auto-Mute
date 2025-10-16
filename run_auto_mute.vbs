Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "C:\Personal\Auto-Mute\.venv\Scripts\pythonw.exe C:\Personal\Auto-Mute\auto_mute.py --tray", 0, False
Set WshShell = Nothing
