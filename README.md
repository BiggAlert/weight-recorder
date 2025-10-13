# Weight Recorder Desktop App

A simple desktop application for recording weight entries, converting between pounds (lbs) and kilograms (kg), and visualizing weight trends over time using a graph.

## Features

- Support for multiple user profiles
- Record weight entries with date and time for each profile
- Choose between lbs and kg units
- Real-time conversion display
- View weight progress with an interactive graph per profile
- Generate detailed reports with statistics and trends per profile
- Data stored in separate CSV files for each profile

## Requirements

- Python 3.x
- Required packages: tkinter, matplotlib, pandas

## Installation

1. Navigate to the project directory:

   ```bash
   cd /home/donnovan/CascadeProjects/windsurf-project/weight_recorder
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

### One-Click Run (Recommended)

- Double-click `run.sh` in your file manager or run `./run.sh` in the terminal for quick launch.

### Manual Run

Run the application:

```bash
python main.py
```

- Select or create a profile from the dropdown menu
- Enter your weight in the input field
- Select the unit (lbs or kg)
- The app will show the conversion in real-time
- Click "Add Entry" to save the record to the selected profile
- Click "View Graph" to see your weight trend over time for that profile
- Click "Generate Report" to view statistics and trends for that profile
- Click "Exit" to close the application

## Data Storage

Weight entries are stored in separate CSV files for each profile in the `profiles/` directory. Each profile's file (e.g., `profiles/John.csv`) includes date, weight, and unit for each entry.

## Graph

The graph displays weight in pounds (lbs) over time for the selected profile. If entries are in kg, they are converted to lbs for consistency in the visualization.

## Reports

The "Generate Report" feature provides a summary of your weight data for the selected profile, including:

- Total number of entries
- Date range of records
- Average, minimum, and maximum weight (in lbs)
- Overall weight trend (gain or loss since first entry)

This helps you track your progress and identify patterns in your weight management for each profile.

## Notes

- Tkinter is used for the GUI (comes with Python standard library)
- Matplotlib is used for plotting the graph
- Pandas is used for data manipulation and storage
