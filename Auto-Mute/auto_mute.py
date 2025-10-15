import datetime
import time
import json
import os
import schedule
import ctypes
import keyboard
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from plyer import notification

CONFIG_FILE = "config.json"
auto_mute_enabled = True  # Global flag to enable/disable auto-mute

def get_volume_mute_state():
    """Get current mute state of system volume."""
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = ctypes.cast(interface, ctypes.POINTER(IAudioEndpointVolume))
    return volume.GetMute()

def set_volume_mute(mute: bool):
    """Mute or unmute system volume."""
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = ctypes.cast(interface, ctypes.POINTER(IAudioEndpointVolume))
    volume.SetMute(mute, None)

def send_notification(title, message):
    """Send desktop notification."""
    notification.notify(
        title=title,
        message=message,
        timeout=5  # seconds
    )

def load_schedule():
    if not os.path.exists(CONFIG_FILE):
        raise FileNotFoundError(f"Config file '{CONFIG_FILE}' not found.")
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def parse_time(timestr):
    hour, minute = map(int, timestr.split(":"))
    return hour * 60 + minute

last_mute_state = None
last_notification_time = None

def toggle_auto_mute():
    """Toggle auto-mute system on/off via hotkey."""
    global auto_mute_enabled, last_mute_state
    auto_mute_enabled = not auto_mute_enabled
    
    if auto_mute_enabled:
        send_notification("✅ Auto Mute Enabled", "Schedule will be enforced again")
        print("✅ Auto Mute: ENABLED - Schedule will be enforced")
        # Reset state so it can check and enforce immediately
        last_mute_state = None
    else:
        send_notification("⏸️ Auto Mute PAUSED", "You have manual control of audio\nPress Ctrl+Shift+M to resume")
        print("⏸️ Auto Mute: PAUSED - Manual control active")
        print("   Press Ctrl+Shift+M again to resume schedule enforcement")

def check_mute_time():
    global last_mute_state, last_notification_time
    
    # Skip if auto-mute is disabled
    if not auto_mute_enabled:
        return
    
    now = datetime.datetime.now()
    weekday = now.strftime("%A")

    schedule_data = load_schedule()
    if weekday not in schedule_data:
        set_volume_mute(False)
        return

    start_str = schedule_data[weekday]["start"]
    end_str = schedule_data[weekday]["end"]

    start_minutes = parse_time(start_str)
    end_minutes = parse_time(end_str)
    current_minutes = now.hour * 60 + now.minute

    # Handle overnight ranges
    if start_minutes < end_minutes:
        should_be_muted = start_minutes <= current_minutes < end_minutes
    else:
        should_be_muted = current_minutes >= start_minutes or current_minutes < end_minutes

    # Get actual current mute state
    actual_mute_state = get_volume_mute_state()

    # Enforce mute state if it doesn't match what it should be
    if actual_mute_state != should_be_muted:
        set_volume_mute(should_be_muted)
        
        # Only send notification if:
        # 1. This is the first run (last_mute_state is None), OR
        # 2. The scheduled state changed (last_mute_state != should_be_muted), OR
        # 3. User manually changed it (show notification every time we re-enforce)
        time_since_last_notification = None
        if last_notification_time:
            time_since_last_notification = (now - last_notification_time).total_seconds()
        
        # Send notification on state changes or if user manually toggled (enforce silently if within 30 sec)
        if last_mute_state != should_be_muted or time_since_last_notification is None or time_since_last_notification > 30:
            if should_be_muted:
                send_notification("🔇 Auto Mute", f"Muted system volume ({weekday})")
            else:
                send_notification("🔊 Auto Mute", f"Unmuted system volume ({weekday})")
            last_notification_time = now
    
    last_mute_state = should_be_muted

# Register hotkey: Ctrl+Shift+M to toggle auto-mute
try:
    keyboard.add_hotkey('ctrl+shift+m', toggle_auto_mute)
    hotkey_registered = True
    print("⌨️  Hotkey registered: Ctrl+Shift+M = Toggle Auto Mute ON/OFF")
except Exception as e:
    hotkey_registered = False
    print(f"⚠️  Warning: Could not register hotkey (may need admin rights): {e}")
    print("   Script will still work, but hotkey won't be available")

schedule.every(1).minutes.do(check_mute_time)

print("🔇 Auto Mute running... (Press Ctrl+C to exit)")
if hotkey_registered:
    print("✅ Status: ENABLED - Schedule is being enforced")
else:
    print("   To use hotkey, run as administrator")
check_mute_time()
while True:
    schedule.run_pending()
    time.sleep(30)
