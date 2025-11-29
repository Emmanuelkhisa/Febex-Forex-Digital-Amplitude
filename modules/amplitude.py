import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime, timedelta
import calendar 

# Define the sets of consecutive trading sessions and their default colors
SESSION_SETS = {
    'Asian': {'sessions': ['SYD', 'SYD-TOK', 'TOK'], 'colors': ['blue', 'c', '#FF00FF']}, # blue, cyan, magenta (close to image pink) - Using bright magenta hex
    'London': {'sessions': ['LDN', 'LDN-NY', 'NY'], 'colors': ['red', 'orange', 'purple']},
    'New York': {'sessions': ['NY', 'NY-SYD', 'SYD'], 'colors': ['darkgreen', 'olive', 'teal']},
    'Tokyo': {'sessions': ['TOK', 'TOK-LDN', 'LDN'], 'colors': ['brown', 'sienna', 'peru']}
}

DATA_FILE = 'forex_session_data_blocks.csv' # Changed filename to indicate block storage

def ensure_data_file_exists():
    """Creates the CSV file with headers if it doesn't exist."""
    if not os.path.exists(DATA_FILE):
        header = ['Date', 'Session_Set', 'Session1_Outcome', 'Session2_Outcome', 'Session3_Outcome']
        df = pd.DataFrame(columns=header)
        df.to_csv(DATA_FILE, index=False)

def get_date_input(prompt):
    """Gets and validates a date input from the user."""
    while True:
        date_str = input(prompt)
        try:
            return datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")

def input_data_block():
    """Prompts user for a block of data for a date range and session set, skipping weekends."""
    print("\n--- Input Data Block ---")

    print("\nAvailable Session Sets:")
    set_options = list(SESSION_SETS.keys())
    for i, set_name in enumerate(set_options):
        print(f"{i + 1}. {set_name}: {', '.join(SESSION_SETS[set_name]['sessions'])}")

    while True:
        choice = input("Select the session set for the data block (enter number): ")
        try:
            choice_index = int(choice) - 1
            if 0 <= choice_index < len(set_options):
                set_name = set_options[choice_index]
                sessions_info = SESSION_SETS[set_name]
                sessions = sessions_info['sessions']
                break
            else:
                 print("Invalid choice. Please enter a number from the list.")
        except ValueError:
            print("Invalid choice. Please enter a number from the list.")

    start_date = get_date_input("Enter the Start Date period (YYYY-MM-DD): ")
    end_date = get_date_input("Enter the End Date period (YYYY-MM-DD): ")

    if start_date > end_date:
        print("Start date cannot be after end date. Please try again.")
        return

    current_date = start_date
    data_to_append = []

    print(f"\n--- Enter Binary Outcomes (0 or 1) for {set_name} Sessions from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')} (Weekdays Only) ---")
    print("Enter '1' for Buy/Long bias, '0' for Sell/Short bias (or Doji).")
    print("Enter an empty line to finish input before the end date.")


    while current_date <= end_date:
        # --- Check if the current_date is a weekend ---
        if current_date.weekday() >= 5: # Monday is 0, Sunday is 6
            print(f"Skipping weekend day: {current_date.strftime('%Y-%m-%d')}") 
            current_date += timedelta(days=1)
            continue # Move to the next day and skip input prompt
        # --- End of Weekend Check ---

        date_str = current_date.strftime('%Y-%m-%d')
        input_prompt = f"Enter data for {date_str} ({', '.join(sessions)}): "
        line_input = input(input_prompt)

        if line_input == "":
            confirm = input("Noticed an empty input. Have you finished with your inputs? Y/N: ")
            if confirm.lower() == 'y':
                break
            else:
                print("Continuing input...")
                continue # Go back to the current date prompt

        # --- Validate the 3-digit binary input ---
        if len(line_input) == 3 and all(c in '01' for c in line_input):
            outcomes = [int(line_input[0]), int(line_input[1]), int(line_input[2])]
            data_to_append.append({
                'Date': date_str,
                'Session_Set': set_name,
                'Session1_Outcome': outcomes[0],
                'Session2_Outcome': outcomes[1],
                'Session3_Outcome': outcomes[2]
            })
            current_date += timedelta(days=1) # Move to the next day only after successful input
        else:
            print("Invalid input format. Please enter exactly 3 digits (0s and 1s) like '101' or an empty line to finish.")
            # Stay on the same date to re-prompt

    if data_to_append:
        # Append to CSV
        ensure_data_file_exists() # Ensures file exists before appending

        # --- Handle empty file case gracefully using try-except ---
        try:
            df_existing = pd.read_csv(DATA_FILE)
        except pd.errors.EmptyDataError:
            # If the file is empty, create an empty DataFrame with the correct columns
            df_existing = pd.DataFrame(columns=['Date', 'Session_Set', 'Session1_Outcome', 'Session2_Outcome', 'Session3_Outcome'])
        # --- End Handle empty file case ---

        df_new = pd.DataFrame(data_to_append)

        # Check for and remove duplicate entries (same Date and Session_Set) before appending
        # Convert dates to string for robust comparison if df_existing has mixed types
        df_existing['Date'] = df_existing['Date'].astype(str)
        df_new['Date'] = df_new['Date'].astype(str)

        # Create a key for merging/dropping duplicates
        df_existing['_key'] = df_existing['Date'] + '_' + df_existing['Session_Set']
        df_new['_key'] = df_new['Date'] + '_' + df_new['Session_Set']

        # Filter out rows from df_new that are already in df_existing
        rows_to_add = df_new[~df_new['_key'].isin(df_existing['_key'])].copy()

        # Drop the temporary key column
        # Check if _key column exists before dropping (in case df_existing was empty initially)
        if '_key' in df_existing.columns:
             df_existing = df_existing.drop(columns=['_key'])
        if '_key' in df_new.columns: # This should always exist for df_new here
             df_new = df_new.drop(columns=['_key'])
        if '_key' in rows_to_add.columns: # This should always exist for rows_to_add here
             rows_to_add = rows_to_add.drop(columns=['_key'])


        if not rows_to_add.empty:
            # Ensure the columns match the expected CSV order before writing
            csv_header_order = ['Date', 'Session_Set', 'Session1_Outcome', 'Session2_Outcome', 'Session3_Outcome']
            rows_to_add[csv_header_order].to_csv(DATA_FILE, mode='a', header=False, index=False)
            print(f"\nAppended {len(rows_to_add)} new day(s) of data for {set_name} sessions.")
        else:
            print("\nNo new unique data days to append for this date range and session set.")

    else:
        print("\nNo valid data was entered.")


def calculate_amplitude(session_data_series):
    """Calculates the digital amplitude for a single session's binary series."""
    amplitude = []
    n = len(session_data_series)
    for i in range(n):
        if i < 2:
            # Boundary condition for the first two days (using 0-based index)
            amplitude.append(0)
        else:
            # Get the 3-day ending sequence (0-based index)
            sequence = (session_data_series[i-2], session_data_series[i-1], session_data_series[i])
            # Apply the amplitude rules
            if sequence in [(0, 1, 1), (1, 1, 1)]:
                amplitude.append(1)
            elif sequence in [(1, 0, 0), (0, 0, 0)]:
                amplitude.append(-1)
            else: # Sequences 001, 010, 101, 110
                amplitude.append(0)
    return amplitude

def plot_amplitude_chart():
    """Prompts user to select a session set and plots the amplitude chart."""
    # --- Add dark background style ---
    plt.style.use('dark_background')
    # --- End of Add ---

    print("\n--- Select Session Set to Display ---")

    print("Available Session Sets with Data:")
    ensure_data_file_exists()
    df = pd.read_csv(DATA_FILE)
    if df.empty:
        print("No data available to plot yet. Please input data first.")
        return

    # Ensure Date column is datetime objects, needed for sorting
    df['Date'] = pd.to_datetime(df['Date'])

    valid_sets_with_data = df['Session_Set'].unique()

    if not valid_sets_with_data.tolist():
        print("No data available for any defined session sets found.")
        return


    display_options = valid_sets_with_data.tolist()
    display_options.sort() # Sort alphabetically for consistent numbering

    for i, set_name in enumerate(display_options):
        print(f"{i + 1}. {set_name}")

    while True:
        choice = input("Select the session set to plot (enter number): ")
        try:
            choice_index = int(choice) - 1
            if 0 <= choice_index < len(display_options):
                set_name = display_options[choice_index]
                # Find the actual session names and colors using the selected set_name
                sessions_info = SESSION_SETS[set_name]
                sessions = sessions_info['sessions']
                colors = sessions_info['colors']
                break
            else:
                 print("Invalid choice. Please enter a number from the list.")
        except ValueError:
            print("Invalid choice. Please enter a number from the list.")


    # Filter data for the selected set and sort by date
    set_df = df[df['Session_Set'] == set_name].sort_values(by='Date').reset_index(drop=True)

    num_days = len(set_df)
    if num_days < 3:
        print(f"Need at least 3 days of data for {set_name} to calculate amplitude. Currently have {num_days} days.")
        return

    # Extract binary outcomes for each session in the set
    # Use iloc to select columns by index (0, 1, 2 relative to the SessionX_Outcome columns)
    session1_data = set_df['Session1_Outcome'].tolist()
    session2_data = set_df['Session2_Outcome'].tolist()
    session3_data = set_df['Session3_Outcome'].tolist()
    # We still need dates for sorting the data correctly before plotting
    # dates = set_df['Date'].tolist()


    # Calculate amplitude for each session series
    amplitude1 = calculate_amplitude(session1_data)
    amplitude2 = calculate_amplitude(session2_data)
    amplitude3 = calculate_amplitude(session3_data)

    # Get session names from the selected set
    session1_name = sessions[0]
    session2_name = sessions[1]
    session3_name = sessions[2]

    # --- Use numerical Day Number for x-axis ---
    day_numbers = list(range(1, num_days + 1))
    # --- End of Change ---


    # Plotting
    plt.figure(figsize=(12, 6))

    # Plot amplitude lines with specified colors against Day Number
    plt.plot(day_numbers, amplitude1, marker='o', linestyle='-', label=f'{session1_name} Amplitude', color=colors[0], alpha=0.7)
    plt.plot(day_numbers, amplitude2, marker='o', linestyle='-', label=f'{session2_name} Amplitude', color=colors[1], alpha=0.7)
    plt.plot(day_numbers, amplitude3, marker='o', linestyle='-', label=f'{session3_name} Amplitude', color=colors[2], alpha=0.7)

    # Set title and labels
    plt.title(f'Febex Digital Amplitude Over Time ({set_name} Sessions)')
    # --- Label x-axis as Day Number ---
    plt.xlabel('Day Number')
    # --- End of Change ---
    plt.ylabel('Digital Amplitude (3-Day Ending Pattern)')
    plt.yticks([-1, -0.5, 0, 0.5, 1]) # Ensure y-axis ticks are at these levels
    plt.grid(True, axis='y', linestyle='--', alpha=0.6)
    plt.legend()

    # --- Add x-axis limits to match original chart's appearance ---
    # Set x-axis limits from 0 up to the number of days + 2 for padding
    plt.xlim(0, num_days + 2)
    # --- End of Add ---

    # --- Remove date-specific x-axis formatting ---
    # plt.xticks(rotation=45)
    # --- End of Removal ---
    plt.tight_layout() # Adjust layout

    # Display the plot
    plt.show()

# --- Main Program Loop ---
# ... (rest of the main loop remains the same) ...
if __name__ == "__main__":
    ensure_data_file_exists() # Make sure the file is ready on first run

    while True:
        print("\n--- Febex Digital Amplitude Program ---")
        print("1. Input data block (for a date range)")
        print("2. View Digital Amplitude Chart")
        print("3. Exit")

        main_choice = input("Enter your choice (1, 2, or 3): ")

        if main_choice == '1':
            input_data_block() # Use the new input function
        elif main_choice == '2':
            plot_amplitude_chart()
        elif main_choice == '3':
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
