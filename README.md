# Events Data Analysis

This script helps in analyzing events data stored in an Excel file. It provides functionalities to filter data based on event codes (MAKATKAV or KAV) and time ranges.

## Installation

1. Clone this repository:

    git clone https://github.com/wweavishay/Metropline

2. Navigate to the project directory:

    cd events-data-analysis

3. Install the required dependencies:

    pip install pandas openpyxl

## Usage

1. Make sure you have an Excel file containing events data. The file should have columns named kav, makatkav, time, area, and direction.

2. Run the script:

    python events_analysis.py

3. Follow the on-screen prompts to filter the data based on event codes and time ranges.

## Example

Suppose we have an Excel file events.xlsx with the following data:

kav   | makatkav | time | area | direction 
-------|----------|------|------|-----------
001   | 00001    | 900  | A    | North     
002   | 00002    | 930  | B    | South     
003   | 00003    | 1000 | A    | East      

If we want to filter events for KAV 002 and time range from 09:00 to 10:30, the output would be:

Zone: B
Time Range: 09:30-09:30
Line: 00002  ||  (direction - [South]) || Count number: (1)

## License

This project is licensed under the MIT License - see the LICENSE file for details.
