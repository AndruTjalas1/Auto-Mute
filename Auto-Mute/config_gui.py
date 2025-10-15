import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

CONFIG_FILE = "config.json"

class AutoMuteConfigGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto Mute - Schedule Configuration")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Header
        header = tk.Label(
            root, 
            text="🔇 Auto Mute Schedule Configuration",
            font=("Segoe UI", 16, "bold"),
            bg="#2c3e50",
            fg="white",
            pady=15
        )
        header.pack(fill=tk.X)
        
        # Instructions
        instructions = tk.Label(
            root,
            text="Set the times when your system should be muted for each day of the week.\nUse 24-hour format (HH:MM). Overnight ranges are supported (e.g., 22:00 to 07:00).",
            font=("Segoe UI", 9),
            fg="#555",
            justify=tk.LEFT,
            pady=10
        )
        instructions.pack(padx=20, anchor=tk.W)
        
        # Main frame for schedule
        main_frame = tk.Frame(root, bg="white")
        main_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        
        # Headers
        tk.Label(main_frame, text="Day", font=("Segoe UI", 10, "bold"), bg="white", width=12).grid(row=0, column=0, padx=5, pady=5)
        tk.Label(main_frame, text="Start Time", font=("Segoe UI", 10, "bold"), bg="white", width=12).grid(row=0, column=1, padx=5, pady=5)
        tk.Label(main_frame, text="End Time", font=("Segoe UI", 10, "bold"), bg="white", width=12).grid(row=0, column=2, padx=5, pady=5)
        tk.Label(main_frame, text="Enabled", font=("Segoe UI", 10, "bold"), bg="white", width=10).grid(row=0, column=3, padx=5, pady=5)
        
        # Days of the week
        self.days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        self.entries = {}
        
        # Load existing config
        config = self.load_config()
        
        # Create entries for each day
        for i, day in enumerate(self.days, start=1):
            # Day label
            day_label = tk.Label(
                main_frame, 
                text=day, 
                font=("Segoe UI", 10),
                bg="white",
                anchor=tk.W
            )
            day_label.grid(row=i, column=0, padx=5, pady=8, sticky=tk.W)
            
            # Start time entry
            start_var = tk.StringVar(value=config.get(day, {}).get("start", "22:00"))
            start_entry = ttk.Entry(main_frame, textvariable=start_var, width=10, font=("Segoe UI", 10))
            start_entry.grid(row=i, column=1, padx=5, pady=8)
            
            # End time entry
            end_var = tk.StringVar(value=config.get(day, {}).get("end", "07:00"))
            end_entry = ttk.Entry(main_frame, textvariable=end_var, width=10, font=("Segoe UI", 10))
            end_entry.grid(row=i, column=2, padx=5, pady=8)
            
            # Enabled checkbox
            enabled_var = tk.BooleanVar(value=day in config)
            enabled_check = ttk.Checkbutton(main_frame, variable=enabled_var)
            enabled_check.grid(row=i, column=3, padx=5, pady=8)
            
            self.entries[day] = {
                "start": start_var,
                "end": end_var,
                "enabled": enabled_var
            }
        
        # Button frame
        button_frame = tk.Frame(root, bg="white")
        button_frame.pack(pady=15)
        
        # Save button
        save_btn = tk.Button(
            button_frame,
            text="💾 Save Schedule",
            command=self.save_config,
            font=("Segoe UI", 11, "bold"),
            bg="#27ae60",
            fg="white",
            padx=20,
            pady=10,
            relief=tk.FLAT,
            cursor="hand2"
        )
        save_btn.pack(side=tk.LEFT, padx=5)
        
        # Apply to all button
        apply_all_btn = tk.Button(
            button_frame,
            text="📋 Apply to All Days",
            command=self.apply_to_all,
            font=("Segoe UI", 11),
            bg="#3498db",
            fg="white",
            padx=20,
            pady=10,
            relief=tk.FLAT,
            cursor="hand2"
        )
        apply_all_btn.pack(side=tk.LEFT, padx=5)
        
        # Reset button
        reset_btn = tk.Button(
            button_frame,
            text="🔄 Reset to Defaults",
            command=self.reset_to_defaults,
            font=("Segoe UI", 11),
            bg="#95a5a6",
            fg="white",
            padx=20,
            pady=10,
            relief=tk.FLAT,
            cursor="hand2"
        )
        reset_btn.pack(side=tk.LEFT, padx=5)
        
        # Status bar
        self.status_label = tk.Label(
            root,
            text="Ready",
            font=("Segoe UI", 9),
            bg="#ecf0f1",
            fg="#555",
            pady=5,
            anchor=tk.W,
            padx=10
        )
        self.status_label.pack(fill=tk.X, side=tk.BOTTOM)
    
    def load_config(self):
        """Load existing configuration from config.json"""
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r") as f:
                    return json.load(f)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load config: {e}")
                return {}
        return {}
    
    def validate_time(self, time_str):
        """Validate time format HH:MM"""
        try:
            parts = time_str.split(":")
            if len(parts) != 2:
                return False
            hour, minute = int(parts[0]), int(parts[1])
            return 0 <= hour <= 23 and 0 <= minute <= 59
        except:
            return False
    
    def save_config(self):
        """Save the configuration to config.json"""
        config = {}
        
        for day, entries in self.entries.items():
            if entries["enabled"].get():
                start_time = entries["start"].get().strip()
                end_time = entries["end"].get().strip()
                
                # Validate times
                if not self.validate_time(start_time):
                    messagebox.showerror("Invalid Time", f"Invalid start time for {day}: {start_time}\nUse format HH:MM (e.g., 22:00)")
                    return
                
                if not self.validate_time(end_time):
                    messagebox.showerror("Invalid Time", f"Invalid end time for {day}: {end_time}\nUse format HH:MM (e.g., 07:00)")
                    return
                
                config[day] = {
                    "start": start_time,
                    "end": end_time
                }
        
        # Save to file
        try:
            with open(CONFIG_FILE, "w") as f:
                json.dump(config, f, indent=2)
            
            self.status_label.config(text="✓ Schedule saved successfully!", fg="#27ae60")
            messagebox.showinfo("Success", "Schedule saved successfully!\n\nThe Auto Mute script will use the new schedule.")
            
            # Reset status after 3 seconds
            self.root.after(3000, lambda: self.status_label.config(text="Ready", fg="#555"))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save config: {e}")
            self.status_label.config(text="✗ Failed to save", fg="#e74c3c")
    
    def apply_to_all(self):
        """Apply Monday's schedule to all days"""
        monday_start = self.entries["Monday"]["start"].get()
        monday_end = self.entries["Monday"]["end"].get()
        monday_enabled = self.entries["Monday"]["enabled"].get()
        
        if not self.validate_time(monday_start) or not self.validate_time(monday_end):
            messagebox.showerror("Invalid Time", "Please set valid times for Monday first.")
            return
        
        response = messagebox.askyesno(
            "Apply to All Days",
            f"Apply Monday's schedule ({monday_start} - {monday_end}) to all days?"
        )
        
        if response:
            for day in self.days:
                self.entries[day]["start"].set(monday_start)
                self.entries[day]["end"].set(monday_end)
                self.entries[day]["enabled"].set(monday_enabled)
            
            self.status_label.config(text="✓ Applied to all days", fg="#3498db")
            self.root.after(3000, lambda: self.status_label.config(text="Ready", fg="#555"))
    
    def reset_to_defaults(self):
        """Reset all days to default schedule"""
        response = messagebox.askyesno(
            "Reset to Defaults",
            "Reset all days to default schedule (22:00 - 07:00)?\n\nWeekends will be set to 23:00 - 08:00."
        )
        
        if response:
            weekday_default = {"start": "22:00", "end": "07:00"}
            weekend_default = {"start": "23:00", "end": "08:00"}
            
            for day in self.days:
                if day in ["Saturday", "Sunday"]:
                    self.entries[day]["start"].set(weekend_default["start"])
                    self.entries[day]["end"].set(weekend_default["end"])
                else:
                    self.entries[day]["start"].set(weekday_default["start"])
                    self.entries[day]["end"].set(weekday_default["end"])
                
                self.entries[day]["enabled"].set(True)
            
            self.status_label.config(text="✓ Reset to defaults", fg="#95a5a6")
            self.root.after(3000, lambda: self.status_label.config(text="Ready", fg="#555"))

def main():
    root = tk.Tk()
    app = AutoMuteConfigGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
