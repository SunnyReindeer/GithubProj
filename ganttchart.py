import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import numpy as np

# Define the Project Data with all phases and subtasks
# Format: (Task Name, Start Date, End Date, Phase Number)
tasks = [
    # Phase 1: Research and Planning (Jul - Sep 2025)
    ("Phase 1: Research & Planning", "2025-07-01", "2025-09-30", 1),
    ("  Study project background", "2025-07-01", "2025-07-31", 1),
    ("  Define problems", "2025-08-01", "2025-08-15", 1),
    ("  Proposed approach", "2025-08-16", "2025-09-30", 1),
    
    # Phase 2: Draft Design (Sep - Dec 2025)
    ("Phase 2: Draft Design", "2025-09-01", "2025-12-31", 2),
    ("  Define user requirements", "2025-09-01", "2025-09-30", 2),
    ("  Draft UI Design", "2025-10-01", "2025-11-15", 2),
    ("  Find API data source", "2025-10-01", "2025-10-31", 2),
    ("  Research related design", "2025-11-16", "2025-12-31", 2),
    
    # Phase 3: Robo-Advisor Algo Refinement (Dec 2025 - Jan 2026)
    ("Phase 3: Robo-Advisor Algo Refinement", "2025-12-01", "2026-01-31", 3),
    ("  Robo-Logic implementation", "2025-12-01", "2026-01-15", 3),
    ("  User acceptance testing", "2026-01-16", "2026-01-25", 3),
    ("  Improve and polish algorithm", "2026-01-26", "2026-01-31", 3),
    
    # Phase 4: Integration with Other Module (Feb - Apr 2026)
    ("Phase 4: Integration with Other Module", "2026-02-01", "2026-04-30", 4),
    ("  Module linking to trading simulator", "2026-02-01", "2026-03-31", 4),
    ("  User acceptance testing", "2026-04-01", "2026-04-20", 4),
    
    # Phase 5: Final Polish and Reporting (Apr 2026)
    ("Phase 5: Final Polish & Reporting", "2026-04-01", "2026-04-30", 5),
    ("  UI/UX cleanup", "2026-04-01", "2026-04-20", 5),
    ("  Report writing", "2026-04-21", "2026-04-30", 5),
]

# Color scheme for different phases
phase_colors = {
    1: '#4e79a7',  # Blue
    2: '#59a14f',  # Green
    3: '#f28e2b',  # Orange
    4: '#e15759',  # Red
    5: '#76b7b2',  # Teal
}

# Convert dates and prepare data
task_names = []
start_dates = []
end_dates = []
durations = []
colors = []

for task in tasks:
    task_name, start_str, end_str, phase = task
    start_date = datetime.strptime(start_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_str, "%Y-%m-%d")
    duration = (end_date - start_date).days + 1  # +1 to include end date
    
    task_names.append(task_name)
    start_dates.append(start_date)
    end_dates.append(end_date)
    durations.append(duration)
    colors.append(phase_colors[phase])

# Create the Gantt Chart
fig, ax = plt.subplots(figsize=(14, 10))

# Create horizontal bars
y_positions = np.arange(len(task_names))
bars = ax.barh(y_positions, durations, left=start_dates, color=colors, 
               edgecolor='black', linewidth=0.5, height=0.6, alpha=0.8)

# Format the X-Axis (Dates)
ax.xaxis_date()
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
plt.xticks(rotation=45, ha='right')

# Set Y-axis labels
ax.set_yticks(y_positions)
ax.set_yticklabels(task_names)
ax.invert_yaxis()  # Phase 1 on top

# Add Labels and Title
ax.set_xlabel("Timeline", fontsize=12, fontweight='bold')
ax.set_ylabel("Tasks", fontsize=12, fontweight='bold')
ax.set_title("4. Proposed Schedule - Intelligent Investment Advisory System", 
             fontsize=14, fontweight='bold', pad=20)
ax.grid(axis='x', linestyle='--', alpha=0.3, which='both')
ax.grid(axis='y', linestyle='-', alpha=0.1)

# Add legend for phases
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor=phase_colors[1], label='Phase 1: Research & Planning'),
    Patch(facecolor=phase_colors[2], label='Phase 2: Draft Design'),
    Patch(facecolor=phase_colors[3], label='Phase 3: Robo-Advisor Refinement'),
    Patch(facecolor=phase_colors[4], label='Phase 4: Integration'),
    Patch(facecolor=phase_colors[5], label='Phase 5: Final Polish & Reporting'),
]
ax.legend(handles=legend_elements, loc='upper right', fontsize=9)

# Adjust layout
plt.tight_layout()

# Save the chart
plt.savefig('project_schedule_gantt.png', dpi=300, bbox_inches='tight')
print("Gantt chart saved as 'project_schedule_gantt.png'")

# Show the plot
plt.show()