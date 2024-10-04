import tkinter as tk
from tkinter import messagebox

# Function to ensure that mix percentages add up to 100%
def validate_percentages():
    try:
        total_percentage = (
            float(water_percentage_entry.get()) +
            float(boric_acid_percentage_entry.get()) +
            float(tru_core_percentage_entry.get()) +
            float(chromostop_percentage_entry.get())
        )
        return total_percentage == 100
    except ValueError:
        return False

# Function to enable or disable input fields based on input
def disable_fields(except_field):
    fields = [total_weight_entry, water_weight_entry, boric_acid_weight_entry, tru_core_weight_entry, chromostop_weight_entry]
    for field in fields:
        if field != except_field:
            field.config(state=tk.DISABLED)

def enable_all_fields():
    total_weight_entry.config(state=tk.NORMAL)
    water_weight_entry.config(state=tk.NORMAL)
    boric_acid_weight_entry.config(state=tk.NORMAL)
    tru_core_weight_entry.config(state=tk.NORMAL)
    chromostop_weight_entry.config(state=tk.NORMAL)

# Function to monitor user input and disable other fields
def on_entry_change(event):
    widget = event.widget
    if widget.get():  # If there is an input in the field
        disable_fields(widget)
    else:  # If the field is cleared, enable all fields again
        enable_all_fields()

# Function to calculate the weight of each chemical based on the total weight or raw weights if provided
def calculate_weights(total_weight=None):
    try:
        # Get the mix percentages
        water_percentage = float(water_percentage_entry.get()) / 100
        boric_acid_percentage = float(boric_acid_percentage_entry.get()) / 100
        tru_core_percentage = float(tru_core_percentage_entry.get()) / 100
        chromostop_percentage = float(chromostop_percentage_entry.get()) / 100

        # If total weight is provided, calculate the weights based on percentages
        if total_weight:
            water_weight = total_weight * water_percentage
            boric_acid_weight = total_weight * boric_acid_percentage
            tru_core_weight = total_weight * tru_core_percentage
            chromostop_weight = total_weight * chromostop_percentage
        else:
            # Calculate total weight if one of the raw weights is provided
            if water_weight_entry.get():
                total_weight = float(water_weight_entry.get()) / water_percentage
            elif boric_acid_weight_entry.get():
                total_weight = float(boric_acid_weight_entry.get()) / boric_acid_percentage
            elif tru_core_weight_entry.get():
                total_weight = float(tru_core_weight_entry.get()) / tru_core_percentage
            elif chromostop_weight_entry.get():
                total_weight = float(chromostop_weight_entry.get()) / chromostop_percentage

            # Now calculate all weights based on the determined total weight
            water_weight = total_weight * water_percentage
            boric_acid_weight = total_weight * boric_acid_percentage
            tru_core_weight = total_weight * tru_core_percentage
            chromostop_weight = total_weight * chromostop_percentage

        return water_weight, boric_acid_weight, tru_core_weight, chromostop_weight, total_weight
    except ValueError:
        return None

# Function to calculate the total cost per pound of the finished mix
def calculate_total_cost():
    try:
        # Get the cost per pound and mix percentages
        water_cost = float(water_cost_entry.get())
        water_percentage = float(water_percentage_entry.get()) / 100
        boric_acid_cost = float(boric_acid_cost_entry.get())
        boric_acid_percentage = float(boric_acid_percentage_entry.get()) / 100
        tru_core_cost = float(tru_core_cost_entry.get())
        tru_core_percentage = float(tru_core_percentage_entry.get()) / 100
        chromostop_cost = float(chromostop_cost_entry.get())
        chromostop_percentage = float(chromostop_percentage_entry.get()) / 100

        # Calculate the total cost per pound of the mix
        total_cost = (
            (water_cost * water_percentage) +
            (boric_acid_cost * boric_acid_percentage) +
            (tru_core_cost * tru_core_percentage) +
            (chromostop_cost * chromostop_percentage)
        )
        return total_cost
    except ValueError:
        return None

# Function to calculate the mix and update the UI
def calculate_mix():
    try:
        # Validate that the mix percentages add up to 100%
        if not validate_percentages():
            result_label.config(text="Mix percentages must add up to 100%.", fg="red")
            return

        # Get the total weight if provided
        total_weight = float(total_weight_entry.get()) if total_weight_entry.get() else None

        # Calculate the weights for each chemical
        weights = calculate_weights(total_weight)
        if weights is None:
            result_label.config(text="Please enter valid numbers for the mix.", fg="red")
            return

        water_weight, boric_acid_weight, tru_core_weight, chromostop_weight, total_weight = weights

        # Calculate the total cost per pound of the mix
        total_cost = calculate_total_cost()
        if total_cost is None:
            result_label.config(text="Please enter valid numbers for $/lb and percentages.", fg="red")
            return

        # Display the weight breakdown and total cost
        water_weight_label_result.config(text=f"{water_weight:.2f} lbs" if water_weight is not None else "")
        boric_acid_weight_label_result.config(text=f"{boric_acid_weight:.2f} lbs" if boric_acid_weight is not None else "")
        tru_core_weight_label_result.config(text=f"{tru_core_weight:.2f} lbs" if tru_core_weight is not None else "")
        chromostop_weight_label_result.config(text=f"{chromostop_weight:.2f} lbs" if chromostop_weight is not None else "")
        total_weight_label_result.config(text=f"Total Weight: {total_weight:.2f} lbs")
        result_label.config(text=f"Total Cost per Pound: ${total_cost:.2f}", fg="green")

    except ValueError:
        result_label.config(text="Please enter valid numeric values.", fg="red")

# Create the main window
root = tk.Tk()
root.title("514 Kopcoat Calculator")

# Make the window resizable and set a minimum size
root.resizable(True, True)
root.minsize(700, 600)  # Minimum size of the window

# Define a more modern color scheme and fonts
bg_color = "#f0f4f8"  # Light background
label_color = "#37474f"  # Dark label text
input_bg_color = "#e3f2fd"  # Light blue for inputs
button_color = "#0288d1"  # Blue button
button_text_color = "#ffffff"  # White button text

root.configure(bg=bg_color)

# Create the layout
frame = tk.Frame(root, bg=bg_color)
frame.grid(sticky="nsew", padx=20, pady=10)

frame.grid_columnconfigure(0, weight=0)  # Label column
frame.grid_columnconfigure(1, weight=1)  # Input column

# Default mix percentages
default_percentages = {
    "water": 73.5,
    "boric_acid": 3.5,
    "tru_core": 21,
    "chromostop": 2,
}

# Autopopulate costs per pound
default_costs = {
    "water": 0,
    "boric_acid": 0.8586,
    "tru_core": 13.0857,
    "chromostop": 5.1237,
}

# Add input fields for total weight at the top
tk.Label(frame, text="Total Weight (lbs):", bg=bg_color, fg=label_color, font=("Helvetica", 10)).grid(row=0, column=0, pady=3, sticky="e")
total_weight_entry = tk.Entry(frame, bg=input_bg_color)
total_weight_entry.grid(row=0, column=1, padx=5, pady=3)
total_weight_entry.bind("<KeyRelease>", on_entry_change)

# Add labels and input fields for each chemical with weight (lbs), $/lb, and percentage inputs
chemicals = [
    ("Water", "water"),
    ("Boric Acid", "boric_acid"),
    ("Tru-Core Concentrate", "tru_core"),
    ("Chromostop", "chromostop")
]

# Dynamically create the labels and input fields for each chemical
for idx, (label, name) in enumerate(chemicals):
    # Chemical name label
    tk.Label(frame, text=f"{label}:", bg=bg_color, fg=label_color, font=("Helvetica", 10)).grid(row=idx+1, column=0, pady=3, sticky="e")

    # Weight input
    tk.Label(frame, text="Weight (lbs):", bg=bg_color, fg=label_color, font=("Helvetica", 10)).grid(row=idx+1, column=1, pady=3, sticky="e")
    globals()[f"{name}_weight_entry"] = tk.Entry(frame, bg=input_bg_color, width=6)
    globals()[f"{name}_weight_entry"].grid(row=idx+1, column=2, padx=5, pady=3)
    globals()[f"{name}_weight_entry"].bind("<KeyRelease>", on_entry_change)

    # $/lb input (autopopulated)
    tk.Label(frame, text="$/lb:", bg=bg_color, fg=label_color, font=("Helvetica", 10)).grid(row=idx+1, column=3, pady=3, sticky="e")
    globals()[f"{name}_cost_entry"] = tk.Entry(frame, bg=input_bg_color, width=7)
    globals()[f"{name}_cost_entry"].grid(row=idx+1, column=4, padx=5, pady=3)
    globals()[f"{name}_cost_entry"].insert(0, f"{default_costs[name]:.4f}")  # Auto-populate the cost per lb

    # Percentage input with default percentage
    tk.Label(frame, text="% Mix:", bg=bg_color, fg=label_color, font=("Helvetica", 10)).grid(row=idx+1, column=5, pady=3, sticky="e")
    globals()[f"{name}_percentage_entry"] = tk.Entry(frame, bg=input_bg_color, width=4)
    globals()[f"{name}_percentage_entry"].grid(row=idx+1, column=6, padx=5, pady=3)
    globals()[f"{name}_percentage_entry"].insert(0, str(default_percentages[name]))  # Pre-fill with default percentages

# Calculate button
calculate_button = tk.Button(frame, text="Calculate Mix", command=calculate_mix, bg=button_color, fg=button_text_color, font=("Helvetica", 10))
calculate_button.grid(row=len(chemicals)+1, column=0, columnspan=7, pady=10)

# Labels to display the weight breakdown
tk.Label(frame, text="Water Weight: ", bg=bg_color, fg=label_color, font=("Helvetica", 10)).grid(row=len(chemicals)+2, column=0, sticky="e")
water_weight_label_result = tk.Label(frame, text="", bg=bg_color, fg=label_color)
water_weight_label_result.grid(row=len(chemicals)+2, column=1)

tk.Label(frame, text="Boric Acid Weight: ", bg=bg_color, fg=label_color, font=("Helvetica", 10)).grid(row=len(chemicals)+3, column=0, sticky="e")
boric_acid_weight_label_result = tk.Label(frame, text="", bg=bg_color, fg=label_color)
boric_acid_weight_label_result.grid(row=len(chemicals)+3, column=1)

tk.Label(frame, text="Tru-Core Concentrate Weight: ", bg=bg_color, fg=label_color, font=("Helvetica", 10)).grid(row=len(chemicals)+4, column=0, sticky="e")
tru_core_weight_label_result = tk.Label(frame, text="", bg=bg_color, fg=label_color)
tru_core_weight_label_result.grid(row=len(chemicals)+4, column=1)

tk.Label(frame, text="Chromostop Weight: ", bg=bg_color, fg=label_color, font=("Helvetica", 10)).grid(row=len(chemicals)+5, column=0, sticky="e")
chromostop_weight_label_result = tk.Label(frame, text="", bg=bg_color, fg=label_color)
chromostop_weight_label_result.grid(row=len(chemicals)+5, column=1)

# Label to display the total weight and total cost per pound result
total_weight_label_result = tk.Label(frame, text="", fg=label_color, bg=bg_color, font=("Helvetica", 10))
total_weight_label_result.grid(row=len(chemicals)+6, column=0, columnspan=7)

result_label = tk.Label(frame, text="", fg="red", bg=bg_color)
result_label.grid(row=len(chemicals)+7, column=0, columnspan=7)

# Add copyright notice
copyright_label = tk.Label(frame, text="© Brandon Barefield, 2024", font=("Helvetica", 8), fg="gray", bg=bg_color)
copyright_label.grid(row=len(chemicals)+8, column=0, columnspan=7, pady=10)

# Start the Tkinter event loop
root.mainloop()
