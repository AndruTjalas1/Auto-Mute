#!/usr/bin/env python3
"""
Auto Mute - Main Entry Point

Main script that runs the auto-mute functionality.
Use --tray flag to enable system tray icon.

Usage:
    python auto_mute.py          # Console mode
    python auto_mute.py --tray   # With system tray icon

Note: The tray icon may show harmless COM cleanup errors on exit. 
These are from the pycaw library and don't affect operation.
When running via pythonw.exe (as in run_auto_mute.vbs), these errors are hidden.
"""

import sys
import time
import threading
import keyboard
import auto_mute_core
import comtypes
import warnings
import os

# Suppress resource warnings
warnings.filterwarnings("ignore", category=ResourceWarning)

# Redirect stderr to suppress COM cleanup errors
class SuppressComErrors:
    def __init__(self, stderr):
        self.stderr = stderr
        self.suppress = False
    
    def write(self, text):
        if "access violation" not in text.lower():
            self.stderr.write(text)
    
    def flush(self):
        self.stderr.flush()
    
    def __getattr__(self, name):
        return getattr(self.stderr, name)

# Only suppress errors in tray mode
if "--tray" in sys.argv:
    sys.stderr = SuppressComErrors(sys.stderr)
def toggle_auto_mute():
    """Toggle auto-mute on/off via hotkey."""
    auto_mute_core.auto_mute_enabled = not auto_mute_core.auto_mute_enabled
    status = "ENABLED" if auto_mute_core.auto_mute_enabled else "DISABLED"
    auto_mute_core.send_notification(
        "Auto-Mute Toggle",
        f"Auto-mute is now {status}"
    )
    print(f"\nAuto-mute {status}")


def setup_hotkey():
    """Setup the global hotkey (Ctrl+Shift+M) to toggle auto-mute."""
    try:
        keyboard.add_hotkey('ctrl+shift+m', toggle_auto_mute)
        print("Hotkey registered: Ctrl+Shift+M")
        return True
    except PermissionError:
        print("Warning: Could not register hotkey - requires administrator privileges")
        print("Note: Auto-mute will still work, but hotkey will be disabled")
        return False
    except Exception as e:
        print(f"Warning: Could not register hotkey: {e}")
        print("Note: Hotkeys require administrator privileges")
        return False


def run_console_mode():
    """Run in console mode without system tray."""
    print("Starting Auto-Mute in console mode...")
    print("Auto-mute is ENABLED")
    
    # Initialize COM for this thread (required for audio utilities)
    comtypes.CoInitialize()
    
    setup_hotkey()
    auto_mute_core.send_notification(
        "Auto-Mute Started",
        "Running in console mode. Press Ctrl+Shift+M to toggle."
    )
    
    # Clear any existing scheduled jobs
    auto_mute_core.schedule.clear()
    
    # Schedule the check to run every minute
    auto_mute_core.schedule.every(1).minutes.do(auto_mute_core.check_mute_time)
    
    # Run initial check
    auto_mute_core.check_mute_time()
    
    print("\nPress Ctrl+C to exit...")
    try:
        while True:
            auto_mute_core.schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\nShutting down Auto-Mute...")
        auto_mute_core.send_notification("Auto-Mute", "Auto-mute stopped")
    finally:
        # Cleanup scheduler
        auto_mute_core.schedule.clear()
        # Cleanup COM when exiting
        comtypes.CoUninitialize()


def run_tray_mode():
    """Run with system tray icon."""
    try:
        import task_bar_icon
    except ImportError:
        print("Error: task_bar_icon module not found or dependencies missing.")
        print("Please install: pip install pystray Pillow")
        sys.exit(1)
    
    print("Starting Auto-Mute with system tray icon...")
    print("(May take a moment to initialize system tray...)")
    
    # Keep notifications enabled (they work fine)
    # Just make sure they're initialized before pystray
    
    # Initialize COM for main thread (required for audio utilities)
    try:
        comtypes.CoInitialize()
    except Exception as e:
        print(f"Warning: COM initialization had issues: {e}")
    
    # Setup hotkey (non-fatal if fails)
    try:
        setup_hotkey()
    except Exception as e:
        print(f"Warning: Hotkey setup failed: {e}")
    
    # Send startup notification while COM is ready
    try:
        auto_mute_core.send_notification(
            "Auto-Mute Started",
            "Running with system tray icon. Press Ctrl+Shift+M to toggle."
        )
    except Exception as e:
        print(f"Warning: Notification failed: {e}")
    
    # Setup and run tray icon (pass the core module)
    # Note: task_bar_icon.setup_tray_icon blocks until the icon is closed
    try:
        # Clear any existing scheduled jobs before starting
        auto_mute_core.schedule.clear()
        task_bar_icon.setup_tray_icon(auto_mute_core)
    except Exception as e:
        print(f"[ERROR] Tray mode crashed: {e}")
        import traceback
        traceback.print_exc()
        # Allow graceful fallback
        raise
    finally:
        # Cleanup scheduler
        try:
            auto_mute_core.schedule.clear()
        except:
            pass
        # Cleanup COM when exiting
        try:
            comtypes.CoUninitialize()
        except:
            pass


def main():
    """Main entry point."""
    if "--tray" in sys.argv:
        run_tray_mode()
    else:
        run_console_mode()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nShutting down...")
    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()
