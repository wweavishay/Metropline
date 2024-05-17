import pandas as pd
import re

# Load the Excel file
file_path = 'events.xlsx'  # Update this path to your file location
data = pd.read_excel(file_path)

# Ensure the kav and makatkav columns are strings and properly formatted
data['kav'] = data['kav'].apply(lambda x: f"{int(x):03d}")
data['makatkav'] = data['makatkav'].apply(lambda x: f"{int(x):05d}")

# Function to normalize time format
def normalize_time(time_str):
    match = re.match(r"(\d{1,2}):?(\d{2})", time_str)
    if not match:
        raise ValueError("Invalid time format. Please enter time in HHMM or HH:MM format.")
    hours, minutes = match.groups()
    return int(hours) * 100 + int(minutes)

# Function to filter the data based on user's input
def filter_data(data, filter_values):
    filter_values = [val.strip() for val in filter_values.split(',')]
    filter_values = [val.zfill(3) if len(val) == 3 else val.zfill(5) for val in filter_values]

    filtered_data = data[(data['kav'].isin(filter_values)) | (data['makatkav'].isin(filter_values))]

    if filtered_data.empty:
        raise ValueError("No matching data for the provided filter values.")

    return filtered_data

# Function to filter data by time range
def filter_by_time(data, start_time, end_time):
    return data[(data['time'] >= start_time) & (data['time'] <= end_time)]

# Function to present data in blocks
# Function to present data in blocks
def present_data(data):
    blocks = []
    grouped = data.groupby('area')
    for name, group in grouped:
        min_time = group['time'].min()
        max_time = group['time'].max()
        min_time_str = f"{min_time // 100:02d}:{min_time % 100:02d}"
        max_time_str = f"{max_time // 100:02d}:{max_time % 100:02d}"
        makatkav_groups = group.groupby('makatkav')
        area_blocks = [f"Zone: {name}\nTime Range: {min_time_str}-{max_time_str}"]
        for makatkav, makatkav_group in makatkav_groups:
            lines_directions = makatkav_group.groupby('makatkav')['direction'].apply(lambda x: list(set(x))).to_dict()
            for makatkav, directions in lines_directions.items():
                directions_str = ', '.join(map(str, sorted(directions)))
                show_count = len(makatkav_group[makatkav_group['makatkav'] == makatkav])
                area_blocks.append(f"Line: {makatkav}  ||  (direction - [{directions_str}]) || Count number: ({show_count})")

        blocks.append("\n".join(area_blocks))
    return "\n ----------------------------------- \n\n".join(blocks)


# Main function to run the script
def main():
    filter_values = input("Enter MAKATKAV (5 digits) or KAV (3 digits), separated by commas: ")
    try:
        filtered_data = filter_data(data, filter_values)
    except ValueError as e:
        print(e)
        return

    start_time_str = input("Enter start time (in HHMM or HH:MM format): ")
    end_time_str = input("Enter end time (in HHMM or HH:MM format): ")
    print("----------------------------------------------------------------------------")

    try:
        start_time = normalize_time(start_time_str)
        end_time = normalize_time(end_time_str)
    except ValueError as e:
        print(e)
        return

    time_filtered_data = filter_by_time(filtered_data, start_time, end_time)

    if time_filtered_data.empty:
        print("ALERT - No data available for the given time range.")
    else:
        result = present_data(time_filtered_data)
        print(result)

    # Check for KAVs not found in the filtered data
    filter_values = [val.strip().zfill(3) if len(val.strip()) == 3 else val.strip().zfill(5) for val in filter_values.split(',')]
    not_found = [val for val in filter_values if val not in time_filtered_data['kav'].unique() and val not in time_filtered_data['makatkav'].unique()]

    if not_found:
        print(f"\n ALERT - The following KAVs were not found in the filtered data: {', '.join(not_found)}")

# Run the main function
if __name__ == "__main__":
    main()