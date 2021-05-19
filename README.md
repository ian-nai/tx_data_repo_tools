# tx_data_repo_tools
Code to help with various tasks related to the Texas Data Repository.

## file_change.py
This script iterates through a folder and does two things:
* Converts specified proprietary file formats to open formats (e.g., .pptx to .pdf)
* Checks if R and Python code is valid, and prints any errors encountered if it is not

## search_date_range.py
This script allows you to search through uploads to the TDR within a specified date range, then returns lists of the dataverses uploaded in that date range along with the files they contain. It ouputs a .xlsx with the dataverses and their files (with specified file formats highlighted in red in order to aid with identifying proprietary formats that need to be converted), as well as a .csv with the same information (but no color coding due to the limitations of the .csv format).
