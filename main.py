import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import os

def load_profiles(profiles_dir):
    return [f.replace('.csv', '') for f in os.listdir(profiles_dir) if f.endswith('.csv')]

class WeightRecorderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weight Recorder")
        self.root.geometry("450x400")

        # Profiles directory and current profile
        self.profiles_dir = "profiles"
        os.makedirs(self.profiles_dir, exist_ok=True)
        self.current_profile = None
        self.profiles = load_profiles(self.profiles_dir)

        # Create UI elements
        self.create_widgets()

        # Load profiles and set default
        if self.profiles:
            self.current_profile = self.profiles[0]
            self.load_data()
        else:
            self.create_new_profile_dialog()

    def create_widgets(self):
        # Profile selection
        profile_frame = tk.Frame(self.root)
        profile_frame.pack(pady=10)

        tk.Label(profile_frame, text="Profile:").grid(row=0, column=0, padx=5)
        self.profile_var = tk.StringVar()
        self.profile_menu = tk.OptionMenu(profile_frame, self.profile_var, "")
        self.profile_menu.grid(row=0, column=1, padx=5)
        self.update_profile_menu()

        # Trace changes to profile_var
        self.profile_var.trace('w', self.on_profile_change)

        # Weight input
        tk.Label(self.root, text="Enter Weight:").pack(pady=5)
        self.weight_entry = tk.Entry(self.root)
        self.weight_entry.pack(pady=5)

        # Unit selection
        self.unit_var = tk.StringVar(value="lbs")
        tk.Radiobutton(self.root, text="Pounds (lbs)", variable=self.unit_var, value="lbs").pack()
        tk.Radiobutton(self.root, text="Kilograms (kg)", variable=self.unit_var, value="kg").pack()

        # Converted weight display
        self.converted_label = tk.Label(self.root, text="")
        self.converted_label.pack(pady=5)

        # Buttons
        tk.Button(self.root, text="Add Entry", command=self.add_entry).pack(pady=10)
        tk.Button(self.root, text="View Graph", command=self.view_graph).pack(pady=5)
        tk.Button(self.root, text="Generate Report", command=self.generate_report).pack(pady=5)
        tk.Button(self.root, text="Exit", command=self.root.quit).pack(pady=5)

    @property
    def data_file(self):
        return os.path.join(self.profiles_dir, f"{self.current_profile}.csv") if self.current_profile else None

    def update_profile_menu(self):
        # Clear existing menu
        menu = self.profile_menu['menu']
        menu.delete(0, 'end')
        # Add profiles
        for profile in self.profiles:
            menu.add_command(label=profile, command=lambda p=profile: self.profile_var.set(p))
        if self.profiles:
            self.profile_var.set(self.profiles[0])

    def create_new_profile_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Create New Profile")
        dialog.geometry("300x150")

        tk.Label(dialog, text="Enter profile name:").pack(pady=10)
        name_entry = tk.Entry(dialog)
        name_entry.pack(pady=5)

        def create_profile():
            name = name_entry.get().strip()
            if name and name not in self.profiles:
                self.profiles.append(name)
                self.update_profile_menu()
                self.current_profile = name
                self.load_data()
                dialog.destroy()
            else:
                messagebox.showerror("Error", "Invalid or duplicate profile name.")

        tk.Button(dialog, text="Create", command=create_profile).pack(pady=10)

    def on_profile_change(self, *args):
        self.current_profile = self.profile_var.get()
        self.load_data()

    def update_conversion(self, event=None):
        try:
            weight = float(self.weight_entry.get())
            unit = self.unit_var.get()
            if unit == "lbs":
                converted = weight * 0.453592  # lbs to kg
                self.converted_label.config(text=f"{weight} lbs = {converted:.2f} kg")
            else:
                converted = weight / 0.453592  # kg to lbs
                self.converted_label.config(text=f"{weight} kg = {converted:.2f} lbs")
        except ValueError:
            self.converted_label.config(text="")

    def add_entry(self):
        if not self.current_profile:
            messagebox.showerror("Error", "Please select a profile.")
            return

        try:
            weight = float(self.weight_entry.get())
            unit = self.unit_var.get()
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Append to profile-specific CSV
            with open(self.data_file, 'a') as f:
                f.write(f"{date},{weight},{unit}\n")

            messagebox.showinfo("Success", "Weight entry added!")
            self.weight_entry.delete(0, tk.END)
            self.converted_label.config(text="")
            self.load_data()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid weight.")

    def load_data(self):
        if self.data_file and os.path.exists(self.data_file):
            self.df = pd.read_csv(self.data_file, names=['date', 'weight', 'unit'])
            # Convert all to kg for consistency
            self.df['weight_kg'] = self.df.apply(lambda row: row['weight'] * 0.453592 if row['unit'] == 'lbs' else row['weight'], axis=1)
            self.df['date'] = pd.to_datetime(self.df['date'])
        else:
            self.df = pd.DataFrame(columns=['date', 'weight', 'unit', 'weight_kg'])

    def view_graph(self):
        if self.df.empty:
            messagebox.showinfo("No Data", "No weight data available to graph.")
            return

        plt.figure(figsize=(10, 5))
        # Convert weight to lbs for display
        weight_lbs = self.df['weight_kg'] * 2.20462
        plt.plot(self.df['date'], weight_lbs, marker='o')
        plt.xlabel('Date')
        plt.ylabel('Weight (lbs)')
        plt.title(f'Weight Over Time - Profile: {self.current_profile}')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def generate_report(self):
        if self.df.empty:
            messagebox.showinfo("No Data", "No weight data available to generate a report.")
            return

        # Calculate statistics in lbs
        total_entries = len(self.df)
        avg_weight = self.df['weight_kg'].mean() * 2.20462
        min_weight = self.df['weight_kg'].min() * 2.20462
        max_weight = self.df['weight_kg'].max() * 2.20462
        start_date = self.df['date'].min().strftime('%Y-%m-%d')
        end_date = self.df['date'].max().strftime('%Y-%m-%d')
        
        # Calculate weight change in lbs
        if total_entries > 1:
            weight_change = (self.df['weight_kg'].iloc[-1] - self.df['weight_kg'].iloc[0]) * 2.20462
            change_text = f"{'Gain' if weight_change > 0 else 'Loss'} of {abs(weight_change):.2f} lbs"
        else:
            change_text = "Not enough data for trend analysis"

        # Create report text
        report = f"""
Weight Recording Report - Profile: {self.current_profile}

Total Entries: {total_entries}
Date Range: {start_date} to {end_date}

Statistics (in lbs):
- Average Weight: {avg_weight:.2f}
- Minimum Weight: {min_weight:.2f}
- Maximum Weight: {max_weight:.2f}

Overall Trend: {change_text}
        """

        # Display report in a message box
        messagebox.showinfo("Weight Report", report)

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = WeightRecorderApp(root)
    root.mainloop()
