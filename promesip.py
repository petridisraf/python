import pandas as pd
import matplotlib.pyplot as plt
import os

# Function to convert timecode to seconds
def timecode_to_seconds(tc):
    if pd.isnull(tc):
        return 0
    h, m, s, f = map(int, tc.split(':'))
    return h * 3600 + m * 60 + s + f / 30  # Assuming 30 fps

# Function to prepare the dataframe
def prepare_dataframe(csv_file):
    df = pd.read_csv(csv_file)
    df['Source In Sec'] = df['Source In'].apply(timecode_to_seconds)
    df['Source Out Sec'] = df['Source Out'].apply(timecode_to_seconds)
    df['Record Duration Sec'] = df['Record Duration'].apply(timecode_to_seconds)
    return df

# Load and prepare the first CSV file
csv_file1 = 'sound_3B.csv'  # Replace with your first CSV file path
df1 = prepare_dataframe(csv_file1)

# Load and prepare other CSV files
csv_files = ['JRA3-001_3B.csv', 'JRA3-002_3B.csv', 'JRA3-003_3B.csv', 'JRA3-004_3B.csv', 'JRA3-005_3B.csv', 'JRA3-006_3B.csv', 'JRA3-007_3B.csv', 'JRA3-008_3B.csv', 'JRA3-009_3B.csv', 'JRA3-010_3B.csv', 'JRA3-011_3B.csv']  # Replace with your other CSV file paths

# Define a dictionary for tag colors
tag_colors = {
    'Αέτωμα/στέγη ναού': 'blue',
    'Κένταυροι': 'red',
    'Κένταυροι-Μέση Κενταύρων και πάνω-Δεξής Κένταυρος': 'red',
    'Κένταυροι-Μέση Κενταύρων και κάτω-Δεξής Κένταυρος': 'red',
    'Κένταυροι-Μέση Κενταύρων και πάνω-Αριστερός Κένταυρος': 'red',
    'Κένταυροι-Μέση Κενταύρων και κάτω-Αριστερός Κένταυρος': 'red',
    'Κένταυροι-Μεση Κενταύρων και πάνω-Δεξής Κένταυρος': 'red',
    'Κένταυροι-Μεση Κενταύρων και κάτω-Δεξής Κένταυρος': 'red',
    'Κένταυροι-Μεση Κενταύρων και πάνω-Αριστερός Κένταυρος': 'red',
    'Κένταυροι-Μεση Κενταύρων και κάτω-Αριστερός Κένταυρος': 'red',
    'Κένταυροι-Μεση Κενταύρων και κάτω-Αριστερός Κένταύρος': 'red',
    'Δεξής Κένταυρος-Αριστερός Κένταυρος': 'red',
    'Δεξής Κένταυρος': 'red',
    'Αριστερός Κένταυρος': 'red',
    'Μέση Κενταύρων και πάνω': 'red',
    'Μεση Κενταύρων και κάτω': 'red',
    'Λαπίθες': 'orange',
    'Απόλλωνας': 'green',
    'Δεξί χέρι Απόλλωνα': 'green',
    'Κεφάλι Απόλλωνα': 'green',
    'Απόλλωνας-Δεξί χέρι Απόλλωνα': 'green',
    'Απόλλωνας-Κεφάλι Απόλλωνα': 'green',
    'Αριστερή γυναίκα': 'purple',
    'Δεξιά γυναίκα': 'purple',
    'Αριστερή γυναίκα-Δεξιά γυναίκα': 'purple',
    'Δεξιά άνδρας-Βασιλιάς Λαπιθών': 'black',
    'Αριστερά άνδρας': 'black',
    'Δεξιά άνδρας-Βασιλιάς Λαπιθών -Αριστερά άνδρας': 'black'
    # Add more tags and colors as needed
}

fig, ax = plt.subplots(figsize=(14, 8))

# Function to plot each dataframe
def plot_dataframe(ax, df, y_pos):
    for idx, row in df.iterrows():
        start_time = row['Source In Sec']
        end_time = row['Source Out Sec']
        duration = end_time - start_time
        tag = row['Notes']
        color = tag_colors.get(tag, 'gray')  # Default to gray if tag is not found
        rect = plt.Rectangle((start_time, y_pos - 0.1), duration, 0.2, color=color, alpha=0.5)
        ax.add_patch(rect)

# Plot the first dataframe
plot_dataframe(ax, df1, 1)

# Plot the other dataframes
for i, csv_file in enumerate(csv_files, start=2):
    df = prepare_dataframe(csv_file)
    plot_dataframe(ax, df, i)

# Set the y-ticks and labels with smaller font size
ax.set_yticks(list(range(1, len(csv_files) + 2)))
ax.set_yticklabels([os.path.splitext(os.path.basename(csv_file))[0] for csv_file in [csv_file1] + csv_files], fontsize=8)  # Smaller font size

# Labeling the timeline
ax.set_xlabel('Time (seconds)')
ax.set_ylabel('')

# Set limits and grid
ax.set_ylim(0.8, len(csv_files) + 1.2)
ax.grid(True, which='both', axis='x', linestyle='--', linewidth=0.5)

# Add legend in a separate window
legend_fig = plt.figure(figsize=(8, 6))
legend_handles = [plt.Line2D([0], [0], color=color, lw=4) for color in tag_colors.values()]
legend_labels = list(tag_colors.keys())
legend = legend_fig.legend(legend_handles, legend_labels, title="Tag Colors", loc='center')


ax.set_title('Video Clips Comparison Timeline')

plt.tight_layout()
plt.show()
