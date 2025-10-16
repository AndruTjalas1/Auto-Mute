"""
Auto Mute - Core Module
Contains the core audio muting logic and utilities.
This module is imported by auto_mute.py (the main script).
"""

import datetime
import time
import json
import os
import ctypes
import schedule
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from plyer import notification

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(SCRIPT_DIR, "config.json")

# Global state
auto_mute_enabled = True
last_mute_state = None
last_notification_time = None

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
        timeout=5
    )

def load_schedule():
    """Load schedule from config.json."""
    if not os.path.exists(CONFIG_FILE):
        raise FileNotFoundError(f"Config file '{CONFIG_FILE}' not found.")
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def parse_time(timestr):
    """Parse HH:MM time string to minutes since midnight."""
    hour, minute = map(int, timestr.split(":"))
    return hour * 60 + minute

def check_mute_time():
    """Check current time and enforce mute schedule."""
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
        
        # Only send notification on state changes
        time_since_last_notification = None
        if last_notification_time:
            time_since_last_notification = (now - last_notification_time).total_seconds()
        
        if last_mute_state != should_be_muted or time_since_last_notification is None or time_since_last_notification > 30:
            if should_be_muted:
                send_notification("🔇 Auto Mute", f"Muted system volume ({weekday})")
            else:
                send_notification("🔊 Auto Mute", f"Unmuted system volume ({weekday})")
            last_notification_time = now
    
    last_mute_state = should_be_muted
