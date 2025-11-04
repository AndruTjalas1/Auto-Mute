Set WshShell = CreateObject("WScript.Shell")
' Run the watchdog batch file hidden in the background
WshShell.Run "C:\Auto-Mute\restart_watchdog.bat", 0, False
Set WshShell = Nothing
