"""
Task Bar Icon Module

Provides a modular system tray icon for the Auto-Mute application.
Shows visual indicators for:
- Auto-mute enabled/disabled state
- Active/paused status

Usage:
    from task_bar_icon import TaskBarIcon
    
    tray = TaskBarIcon(core_module)
    tray.run()
"""

import threading
import time
from typing import Callable, Optional
from PIL import Image, ImageDraw
import pystray
from pystray import MenuItem as item


class TaskBarIcon:
    """
    System tray icon manager for Auto-Mute application.
    
    Attributes:
        core_module: Reference to the auto_mute_core module
        icon: pystray.Icon instance
        _scheduler_thread: Background thread for running scheduled tasks
        _running: Flag to control the scheduler thread
    """
    
    def __init__(self, core_module):
        """
        Initialize the task bar icon.
        
        Args:
            core_module: The auto_mute_core module containing schedule and state
        """
        self.core = core_module
        self.icon: Optional[pystray.Icon] = None
        self._scheduler_thread: Optional[threading.Thread] = None
        self._running = False
        
    def _create_icon_image(self, enabled: bool) -> Image.Image:
        """
        Create an icon image based on the current state.
        
        Args:
            enabled: Whether auto-mute is currently enabled
            
        Returns:
            PIL Image object for the icon
        """
        # Create a 64x64 image
        width = 64
        height = 64
        image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        # Choose color based on state
        if enabled:
            # Green when enabled
            fill_color = (34, 197, 94, 255)  # Modern green
            outline_color = (22, 163, 74, 255)
        else:
            # Red/orange when paused
            fill_color = (239, 68, 68, 255)  # Modern red
            outline_color = (220, 38, 38, 255)
        
        # Draw a circle
        padding = 4
        draw.ellipse(
            [padding, padding, width - padding, height - padding],
            fill=fill_color,
            outline=outline_color,
            width=3
        )
        
        # Draw a speaker/sound icon overlay
        if enabled:
            # Draw speaker (small rectangle + triangle)
            speaker_x = width // 3
            speaker_y = height // 2
            
            # Speaker body (rectangle)
            draw.rectangle(
                [speaker_x - 6, speaker_y - 6, speaker_x + 2, speaker_y + 6],
                fill=(255, 255, 255, 255)
            )
            
            # Speaker cone (triangle)
            draw.polygon(
                [
                    (speaker_x + 2, speaker_y - 8),
                    (speaker_x + 2, speaker_y + 8),
                    (speaker_x + 12, speaker_y + 12),
                    (speaker_x + 12, speaker_y - 12)
                ],
                fill=(255, 255, 255, 255)
            )
            
            # Sound waves
            for i in range(2):
                offset = speaker_x + 16 + (i * 6)
                arc_size = 8 + (i * 4)
                draw.arc(
                    [offset - arc_size, speaker_y - arc_size, 
                     offset + arc_size, speaker_y + arc_size],
                    start=-45, end=45,
                    fill=(255, 255, 255, 255),
                    width=2
                )
        else:
            # Draw mute symbol (speaker with X)
            speaker_x = width // 3
            speaker_y = height // 2
            
            # Speaker body
            draw.rectangle(
                [speaker_x - 6, speaker_y - 6, speaker_x + 2, speaker_y + 6],
                fill=(255, 255, 255, 255)
            )
            
            # Speaker cone
            draw.polygon(
                [
                    (speaker_x + 2, speaker_y - 8),
                    (speaker_x + 2, speaker_y + 8),
                    (speaker_x + 12, speaker_y + 12),
                    (speaker_x + 12, speaker_y - 12)
                ],
                fill=(255, 255, 255, 255)
            )
            
            # X symbol (two lines)
            x_start = speaker_x + 16
            x_size = 14
            draw.line(
                [x_start, speaker_y - x_size//2, 
                 x_start + x_size, speaker_y + x_size//2],
                fill=(255, 255, 255, 255),
                width=3
            )
            draw.line(
                [x_start, speaker_y + x_size//2, 
                 x_start + x_size, speaker_y - x_size//2],
                fill=(255, 255, 255, 255),
                width=3
            )
        
        return image
    
    def _update_icon(self):
        """Update the icon to reflect current state."""
        if self.icon:
            self.icon.icon = self._create_icon_image(self.core.auto_mute_enabled)
            self.icon.title = self._get_tooltip()
    
    def _get_tooltip(self) -> str:
        """
        Get the tooltip text for the current state.
        
        Returns:
            Tooltip string
        """
        status = "Enabled" if self.core.auto_mute_enabled else "Paused"
        return f"Auto-Mute - {status}"
    
    def _toggle_auto_mute(self, icon, item):
        """
        Toggle auto-mute state (menu action).
        
        Args:
            icon: pystray.Icon instance
            item: MenuItem that was clicked
        """
        self.core.auto_mute_enabled = not self.core.auto_mute_enabled
        status = "ENABLED" if self.core.auto_mute_enabled else "PAUSED"
        
        self.core.send_notification(
            "Auto-Mute Toggle",
            f"Auto-mute is now {status}"
        )
        
        # Update icon appearance
        self._update_icon()
    
    def _check_mute_time_wrapper(self):
        """Wrapper for check_mute_time that updates icon after check."""
        try:
            self.core.check_mute_time()
            # Update icon in case state changed
            self._update_icon()
        except Exception as e:
            print(f"[ERROR] check_mute_time_wrapper failed: {e}")
            import traceback
            traceback.print_exc()
    
    def _run_scheduler(self):
        """Run the schedule checker in a background thread."""
        # Initialize COM for this thread
        import comtypes
        comtypes.CoInitialize()
        
        try:
            # Schedule the check to run every minute
            self.core.schedule.every(1).minutes.do(self._check_mute_time_wrapper)
            
            # Run initial check
            self._check_mute_time_wrapper()
            
            # Keep running scheduled tasks
            while self._running:
                try:
                    self.core.schedule.run_pending()
                    time.sleep(1)
                except Exception as e:
                    print(f"[ERROR] Scheduler error: {e}")
                    import traceback
                    traceback.print_exc()
                    time.sleep(5)  # Wait before retrying
        except Exception as e:
            print(f"[ERROR] Scheduler thread crashed: {e}")
            import traceback
            traceback.print_exc()
        finally:
            # Cleanup COM when thread exits
            comtypes.CoUninitialize()
    
    def _show_status(self, icon, item):
        """
        Show current status (menu action).
        
        Args:
            icon: pystray.Icon instance
            item: MenuItem that was clicked
        """
        import datetime
        status = "Enabled" if self.core.auto_mute_enabled else "Paused"
        current_time = datetime.datetime.now().strftime("%H:%M")
        
        self.core.send_notification(
            "Auto-Mute Status",
            f"Status: {status}\nTime: {current_time}"
        )
    
    def _open_schedule_gui(self, icon, item):
        """
        Open the schedule configuration GUI (menu action).
        
        Args:
            icon: pystray.Icon instance
            item: MenuItem that was clicked
        """
        import subprocess
        import sys
        import os
        
        # Get the path to config_gui.py
        script_dir = os.path.dirname(os.path.abspath(__file__))
        gui_script = os.path.join(script_dir, "config_gui.py")
        
        # Launch the GUI in a new process
        try:
            subprocess.Popen([sys.executable, gui_script])
        except Exception as e:
            self.core.send_notification(
                "Error",
                f"Failed to open schedule GUI: {e}"
            )
    
    def _exit_action(self, icon, item):
        """
        Exit the application (menu action).
        
        Args:
            icon: pystray.Icon instance
            item: MenuItem that was clicked
        """
        self.core.send_notification("Auto-Mute", "Application stopping...")
        self._stop()
        icon.stop()
    
    def _create_menu(self) -> tuple:
        """
        Create the context menu for the tray icon.
        
        Returns:
            Tuple of menu items
        """
        return (
            item(
                'Toggle Auto-Mute',
                self._toggle_auto_mute,
                default=True
            ),
            item('Show Status', self._show_status),
            item('Open Schedule GUI', self._open_schedule_gui),
            item('Exit', self._exit_action)
        )
    
    def _stop(self):
        """Stop the scheduler thread."""
        self._running = False
        if self._scheduler_thread and self._scheduler_thread.is_alive():
            self._scheduler_thread.join(timeout=2)
    
    def run(self):
        """
        Start the task bar icon and begin monitoring.
        This method blocks until the icon is stopped.
        """
        try:
            # Start the scheduler in a background thread
            self._running = True
            self._scheduler_thread = threading.Thread(
                target=self._run_scheduler,
                daemon=True
            )
            self._scheduler_thread.start()
            
            # Create and run the system tray icon (blocks until stopped)
            icon_image = self._create_icon_image(self.core.auto_mute_enabled)
            self.icon = pystray.Icon(
                name="Auto-Mute",
                icon=icon_image,
                title=self._get_tooltip(),
                menu=self._create_menu()
            )
            
            # Run the icon (blocks until icon.stop() is called)
            self.icon.run()
        except Exception as e:
            print(f"[ERROR] Tray icon error: {e}")
            import traceback
            traceback.print_exc()
        finally:
            # Cleanup when icon stops
            self._stop()


def setup_tray_icon(core_module):
    """
    Convenience function to create and run a task bar icon.
    
    This is a legacy-compatible function that matches the old interface.
    
    Args:
        core_module: The auto_mute_core module
    """
    tray = TaskBarIcon(core_module)
    tray.run()
