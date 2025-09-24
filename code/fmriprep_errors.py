import os
import glob
from bs4 import BeautifulSoup

def parse_fmriprep_report(report_path):
    """extracts all errors and warnings from a single fmriprep report
    Input: 
    Output: dictionary of warning and error messages
    """
    results = {"errors": [], "warnings": []}

    with open(report_path, "r") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    # extract errors
    error = soup.find(id = "errors") # searches hmtl for error tags
    if error:
        for z in error.find_all("li"): # finds all errors inside error message (<li>):
            text = z.get_text(strip = True) # extracts text from li
            if text and text != "No errors to report!": # checks if empty or non error
                results["errors"].append(text) # if error, adds to results dict

    # extract warnings
    warning = soup.find(id = "warnings") # searches hmtl for warning tags
    if warning:
        for y in error.find_all("li"): # finds all warnings inside error message (<li>):
            text = y.get_text(strip = True) # extracts text from li
            if text and text != "No warnings to report!": # checks if empty or non error
                results["warnings"].append(text) # if error, adds to results dict

    return results

def generate_subject_report(subject_dir):
    """Generate a summary of fMRIPrep report(s) for one subject
    Input: one subject directory path
    Output: dict
    """
    html_reports = glob.glob(os.path.join(subject_dir, "*.html")) # finds all html files in folder
    summary = {} # empty results dict
    
    for report_path in html_reports: # loops through each report file
        summary[os.path.basename(report_path)] = parse_fmriprep_report(report_path) # keeps only file name, extracts errors/warnings
    
    return summary

if __name__ == "__main__":
    sub_id = "sub-100003"
    subject_dir = os.path.expanduser(f"~/Desktop/BIDSOutput/{sub_id}/func") # defines folder with html reports
    report = generate_subject_report(subject_dir) # calls function
    
    print("===== fMRIPrep Report Summary =====")
    for report_file, results in report.items():
        print(f"\nReport: {report_file}")
        
        if results["errors"]:
            print("  Errors:")
            for z in results["errors"]:
                print(f"   - {z}")
        else:
            print("  No errors found.")
        
        if results["warnings"]:
            print("  Warnings:")
            for y in results["warnings"]:
                print(f"   - {y}")
        else:
            print("  No warnings found.")