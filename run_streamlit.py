# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 09:52:39 2024

@author: tnjsp
"""

import os
import subprocess

def run_script_in_winpython():
    # Define the directory to cd into
    target_directory = r"C:\Users\tnjsp\OneDrive\Documents\Py_Scripts\WPy64-31090\Projects\FFE-Draft-Aid-master"
    
    # Prompt the user for the Python script name
    script_name = "Draft_Optimizer_Streamlit.py"
    #script_name = "Streamlit_practice.py"
    #script_name = "Streamlit_practice2.py"
    
    # Build the command to run
    command = f'streamlit run {script_name}'
    
    # Construct the full command to open WinPython Command Prompt, cd into the directory, and run the script
    full_command = f'start cmd /k "cd /d {target_directory} && {command}"'
    
    # Run the command
    subprocess.run(full_command, shell=True)

if __name__ == "__main__":
    run_script_in_winpython()
