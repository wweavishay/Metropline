import pandas as pd
import re

def load_data(file_path, sheet_name):
    return pd.read_excel(file_path, sheet_name=sheet_name)

def configure_columns(data, kav_col, makatkav_col, time_col, area_col, direction_col):
    data[kav_col] = data[kav_col].apply(lambda x: f"{int(x):03d}")
    data[makatkav_col] = data[makatkav_col].apply(lambda x: f"{int(x):05d}")
    return data

def normalize_time(time_str):
    match = re.match(r"(\d{1,2}):?(\d{2})", time_str)
    if not match:
        raise ValueError("Invalid time format. Please enter time in HHMM or HH:MM format.")
    hours, minutes = match.groups()
    return int(hours) * 100 + int(minutes)

def filter_data(data, filter_values, kav_col, makatkav_col):
    filter_values = [val.strip() for val in filter_values.split(',')]
    filter_values = [val.zfill(3) if len(val) == 3 else val.zfill(5) for val in filter_values]

    filtered_data = data[(data[kav_col].isin(filter_values)) | (data[makatkav_col].isin(filter_values))]

    if filtered_data.empty:
        raise ValueError("No matching data for the provided filter values.")

    return filtered_data

def filter_by_time(data, start_time, end_time, time_col):
    return data[(data[time_col] >= start_time) & (data[time_col] <= end_time)]

def present_data(data, area_col, time_col, makatkav_col, direction_col):
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

def main():
    file_path = 'events.xlsx'  # Update this path to your file location
    sheet_name = 'Sheet1'  # Update this to the correct sheet name
    kav_col = 'kav'  # Column name for KAV
    makatkav_col = 'makatkav'  # Column name for MAKATKAV
    time_col = 'time'  # Column name for time
    area_col = 'area'  # Column name for area
    direction_col = 'direction'  # Column name for direction

    data = load_data(file_path, sheet_name)
    data = configure_columns(data, kav_col, makatkav_col, time_col, area_col, direction_col)

    filter_values = input(f"Enter {makatkav_col} (5 digits) or {kav_col} (3 digits), separated by commas: ")
    try:
        filtered_data = filter_data(data, filter_values, kav_col, makatkav_col)
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

    time_filtered_data = filter_by_time(filtered_data, start_time, end_time, time_col)

    if time_filtered_data.empty:
        print("ALERT - No data available for the given time range.")
    else:
        result = present_data(time_filtered_data, area_col, time_col, makatkav_col, direction_col)
        print(result)

    filter_values = [val.strip().zfill(3) if len(val.strip()) == 3 else val.strip().zfill(5) for val in filter_values.split(',')]
    not_found = [val for val in filter_values if val not in time_filtered_data[kav_col].unique() and val not in time_filtered_data[makatkav_col].unique()]

    if not_found:
        print(f"\n ALERT - The following {kav_col}s were not found in the filtered data: {', '.join(not_found)}")

if __name__ == "__main__":
    main()
