# Auto Mute

🔇 A Python script that automatically mutes/unmutes your Windows system audio based on a customizable schedule.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

- 🔇 **Automatic muting** based on time schedules
- 📅 **Different schedules** for each day of the week
- 🌙 **Overnight ranges** supported (e.g., 22:00 to 07:00)
- 🔔 **Desktop notifications** when mute state changes
- 🔄 **Runs silently** in the background
- ⌨️ **Global Hotkey**: `Ctrl+Shift+M` to toggle auto-mute ON/OFF
- 🎨 **GUI Configuration Tool** for easy schedule setup
- 🚀 **Auto-start on Windows login**
- 🔁 **Re-mutes automatically** if you manually unmute during scheduled hours

## 🖼️ Screenshots

### GUI Configuration Tool
Easy-to-use interface for configuring your mute schedule:

![Config GUI](screenshots/config_gui.png)

## 📋 Requirements

- Windows OS
- Python 3.8 or higher
- Administrator privileges (for audio control)

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/AndruTjalas1/Auto-Mute.git
cd Auto-Mute
```

### 2. Create Virtual Environment & Install Dependencies
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 3. Configure Your Schedule

**Option A: Use the GUI (Recommended)**
```powershell
# Double-click configure_schedule.vbs
# OR run:
python config_gui.py
```

**Option B: Edit config.json manually**
```json
{
  "Monday": { "start": "22:00", "end": "07:00" },
  "Tuesday": { "start": "22:00", "end": "07:00" },
  "Wednesday": { "start": "22:00", "end": "07:00" },
  "Thursday": { "start": "22:00", "end": "07:00" },
  "Friday": { "start": "23:00", "end": "08:00" },
  "Saturday": { "start": "23:00", "end": "08:00" },
  "Sunday": { "start": "22:00", "end": "07:00" }
}
```

### 4. Run the Script

**For testing (with console output):**
```powershell
python auto_mute.py
```

**To run in background (silent mode):**
```powershell
# Double-click run_auto_mute.vbs
# OR run:
wscript run_auto_mute.vbs
```

## ⚙️ Setup Auto-Start on Windows Login

To have Auto Mute start automatically when you log in:

```powershell
# Run the setup script:
powershell -ExecutionPolicy Bypass -File setup_autostart.ps1

# Or manually: Press Win+R, type "shell:startup", and create a shortcut to run_auto_mute.vbs
```

## ⌨️ Hotkey Controls

**`Ctrl+Shift+M`** - Toggle Auto Mute ON/OFF

- ✅ **Enabled**: Schedule is enforced automatically
- ⏸️ **Paused**: Schedule temporarily disabled, manual audio control restored
- Works system-wide, even when other apps are focused

Perfect for when you need to deviate from your schedule temporarily!

## 📜 Available Scripts

| Script | Description |
|--------|-------------|
| `auto_mute.py` | Main auto-mute script |
| `config_gui.py` | GUI for configuring schedule |
| `run_auto_mute.vbs` | Run script silently in background |
| `configure_schedule.vbs` | Open configuration GUI |
| `setup_autostart.ps1` | Add to Windows startup |
| `remove_autostart.ps1` | Remove from Windows startup |
| `stop_auto_mute.ps1` | Stop running background process |
| `check_status.ps1` | Check if script is running |
| `create_desktop_shortcut.ps1` | Create desktop shortcut for GUI |

## 🛠️ How It Works

1. Script checks current time every minute
2. Compares against configured schedule for the current day
3. If current time is within mute range → mutes system
4. When time exits mute range → unmutes system
5. Notifications appear when mute state changes
6. If you manually unmute during mute hours, script re-mutes within 1 minute

## 🎯 Use Cases

- 🌙 **Quiet hours**: Prevent accidental audio during sleep hours
- 💼 **Work schedule**: Auto-mute during meetings or focus time
- 🏠 **Shared spaces**: Respect quiet hours in shared living spaces
- 🎮 **Gaming schedule**: Different schedules for weekdays vs weekends

## 📦 Dependencies

- `pycaw` - Windows audio control
- `comtypes` - COM interface support
- `plyer` - Cross-platform notifications
- `schedule` - Job scheduling
- `keyboard` - Global hotkey support

All dependencies are listed in `requirements.txt`.

## 🔧 Troubleshooting

**Notifications not appearing?**
- Enable Windows notifications for Python
- Check Windows notification settings

**Script not muting?**
- Verify time format is "HH:MM" (24-hour format)
- Check day names match exactly (e.g., "Monday", not "monday")
- Run in terminal mode to see error messages

**Can't stop background process?**
- Run `stop_auto_mute.ps1`
- Or use Task Manager to kill `pythonw.exe` process

**Hotkey not working?**
- Ensure script is running
- Check no other application is using `Ctrl+Shift+M`
- May require running as administrator

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [pycaw](https://github.com/AndreMiras/pycaw) - Windows audio control library
- [plyer](https://github.com/kivy/plyer) - Cross-platform notification support
- [schedule](https://github.com/dbader/schedule) - Job scheduling library
- [keyboard](https://github.com/boppreh/keyboard) - Global hotkey support

## 📧 Contact

Andru Tjalas - [@AndruTjalas1](https://github.com/AndruTjalas1)

Project Link: [https://github.com/AndruTjalas1/Auto-Mute](https://github.com/AndruTjalas1/Auto-Mute)

---

⭐ If you find this project useful, please consider giving it a star!
