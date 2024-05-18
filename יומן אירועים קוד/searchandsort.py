import pandas as pd
import re

def load_data(file_path, sheet_name):
    """Load data from an Excel file."""
    return pd.read_excel(file_path, sheet_name=sheet_name)

def configure_columns(data, kav_col, makatkav_col):
    """Format the 'kav' and 'makatkav' columns."""
    data[kav_col] = data[kav_col].apply(lambda x: f"{int(x):03d}")
    data[makatkav_col] = data[makatkav_col].apply(lambda x: f"{int(x):05d}")
    return data

def normalize_time(time_str):
    """Convert time string to integer in HHMM format."""
    match = re.match(r"(\d{1,2}):?(\d{2})", time_str)
    if not match:
        raise ValueError("Invalid time format. Please enter time in HHMM or HH:MM format.")
    hours, minutes = match.groups()
    return int(hours) * 100 + int(minutes)

def filter_data(data, filter_values, kav_col, makatkav_col):
    """Filter data based on provided 'kav' or 'makatkav' values."""
    filter_values = [val.strip().zfill(3) if len(val.strip()) == 3 else val.strip().zfill(5) for val in filter_values.split(',')]
    filtered_data = data[(data[kav_col].isin(filter_values)) | (data[makatkav_col].isin(filter_values))]
    if filtered_data.empty:
        raise ValueError("No matching data for the provided filter values.")
    return filtered_data

def filter_by_time(data, start_time, end_time, time_col):
    """Filter data within a specified time range."""
    return data[(data[time_col] >= start_time) & (data[time_col] <= end_time)]

def present_data(data, area_col, time_col, makatkav_col, direction_col):
    """Format and present the filtered data."""
    blocks = []
    grouped = data.groupby(area_col)
    for name, group in grouped:
        min_time = group[time_col].min()
        max_time = group[time_col].max()
        min_time_str = f"{min_time // 100:02d}:{min_time % 100:02d}"
        max_time_str = f"{max_time // 100:02d}:{max_time % 100:02d}"
        makatkav_groups = group.groupby(makatkav_col)
        area_blocks = [f"Zone: {name}\nTime Range: {min_time_str}-{max_time_str}"]
        for makatkav, makatkav_group in makatkav_groups:
            lines_directions = makatkav_group.groupby(makatkav_col)[direction_col].apply(lambda x: list(set(x))).to_dict()
            for makatkav, directions in lines_directions.items():
                directions_str = ', '.join(map(str, sorted(directions)))
                show_count = len(makatkav_group[makatkav_group[makatkav_col] == makatkav])
                area_blocks.append(f"Line: {makatkav}  ||  (direction - [{directions_str}]) || Count number: ({show_count})")
        blocks.append("\n".join(area_blocks))
    return "\n ----------------------------------- \n\n".join(blocks)

def get_filter_values():
    """Get filter values from the user."""
    return input("Enter makatkav (5 digits) or kav (3 digits), separated by commas: ")

def get_time_range():
    """Get time range from the user."""
    start_time_str = input("Enter start time (in HHMM or HH:MM format): ")
    end_time_str = input("Enter end time (in HHMM or HH:MM format): ")
    return start_time_str, end_time_str

def validate_and_filter_data(data, kav_col, makatkav_col):
    """Validate user input and filter the data."""
    filter_values = get_filter_values()
    try:
        filtered_data = filter_data(data, filter_values, kav_col, makatkav_col)
    except ValueError as e:
        print(e)
        return None, None
    return filtered_data, filter_values

def validate_and_filter_by_time(filtered_data, time_col):
    """Validate time input and filter data by time."""
    start_time_str, end_time_str = get_time_range()
    try:
        start_time = normalize_time(start_time_str)
        end_time = normalize_time(end_time_str)
    except ValueError as e:
        print(e)
        return None
    time_filtered_data = filter_by_time(filtered_data, start_time, end_time, time_col)
    return time_filtered_data

def check_not_found_values(filtered_data, filter_values, kav_col, makatkav_col):
    """Check for filter values that are not found in the data."""
    filter_values = [val.strip().zfill(3) if len(val.strip()) == 3 else val.strip().zfill(5) for val in filter_values.split(',')]
    not_found = [val for val in filter_values if val not in filtered_data[kav_col].unique() and val not in filtered_data[makatkav_col].unique()]
    if not_found:
        print(f"\n ALERT - The following kavs were not found in the filtered data: {', '.join(not_found)}")

def main(file_path, sheet_name, kav_col,makatkav_col, time_col, area_col, direction_col):

    data = load_data(file_path, sheet_name)
    data = configure_columns(data, kav_col, makatkav_col)

    filtered_data, filter_values = validate_and_filter_data(data, kav_col, makatkav_col)
    if filtered_data is None:
        return

    time_filtered_data = validate_and_filter_by_time(filtered_data, time_col)
    if time_filtered_data is None:
        return

    if time_filtered_data.empty:
        print("ALERT - No data available for the given time range.")
    else:
        result = present_data(time_filtered_data, area_col, time_col, makatkav_col, direction_col)
        print(result)

    check_not_found_values(filtered_data, filter_values, kav_col, makatkav_col)




if __name__ == "__main__":

    file_path = 'events.xlsx'  # Update this path to your file location
    sheet_name = 'Sheet1'  # Update this to the correct sheet name
    kav_col = 'kav'  # Column name for KAV
    makatkav_col = 'makatkav'  # Column name for MAKATKAV
    time_col = 'time'  # Column name for time
    area_col = 'area'  # Column name for area
    direction_col = 'direction'  # Column name for direction


    main(file_path, sheet_name, kav_col,makatkav_col, time_col, area_col, direction_col)
