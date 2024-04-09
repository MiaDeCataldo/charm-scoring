# [BNL] Charm Flanker Scoring

## First Time Setup:

1. For this code to be able to run, your computer must have a Python interpreter (v3 or greater). Confirm this by entering the following command into a terminal window: ```python3 --version```. If python3 is "not found", it can be downloaded at https://www.python.org/downloads/

2. Download the source code to your own computer. 
    - Select the green "<> Code" button at the top right of https://github.com/zekissel/flanker-scoring, and download as a ZIP file. Unzip and move the contents to a convenient location.
    - Alternatively, use the git command-line tool to copy the repository directly to the current working directory (requires installing git: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git): ```git clone https://github.com/zekissel/flanker-scoring```

3. In the same directory/folder as the downloaded source code, create a folder named ```Flanker_csv```, and place all participant CSVs into this folder. All of the file names should have the format ```C2xxx_flanker.csv```.
    - *If the folder and/or file names do not match exactly (including capitalization), the files will not be recongnized and no data will be analyzed*

4. In a terminal window, navigate to the project directory.
    - This is possible using Window's File Explorer or Mac's Finder; just right click the flanker-scoring folder and select "Open in Terminal". 
    - Alternatively, use the ```cd <destination>``` command to navigate through directories in a terminal interface. If you cloned the repository using ```git clone``` in step 2, the command ```cd flanker-scoring``` will move you to the correct directory.
    - *The command ```pwd``` in a terminal will print the working directory. Use this to confirm where you are*

5. Create an environment in order to install Pandas (framework used to manipulate data): Enter
```python3 -m venv .venv``` into terminal ("-m venv" sets "mode" to virtual environment, and ".venv" is name of resulting directory that contains environment)

6. Put the environment that was just created into context using command: ```source .venv/bin/activate```

7. Install dependency using ```pip install pandas``` (pip is a Python package manager, and Pandas is a data manipulation framework for Python)
    - When installing Python dependencies from a provided source, the convention is to provide a file ```requirements.txt``` that contains all necessary package names. This repository has such a provided file, so alternatively you could enter the command ```pip install -r requirements.txt``` ("-r" signals that the next argument will be a requirements file)

8. Execute Python script with ```python3 score.py```

9. The outputted scores will be written to file ```scoring_file.csv``` in the same directory. Use command ```cat <file>``` to display the contents of the file to terminal: ```cat scoring_file.csv``` (or view in Excel, Sheets, notepad, etc.)

10. To remove the virtual environment from context, use command ```deactivate```


## For Future Runs:
1. Once you create the virtual environment and install Pandas to it, you can reuse this environment again the next time. If you already have the environment configured, navigate to the same project directory and use the same command to set context: ```source .venv/bin/activate```
2. Dependecies are already installed this time; you can execute the Python code that uses Pandas by using the command ```python3 score.py```.
3. If a participant file is added, removed, or changed, then the script will need to be run again in order to update calculations and re-export ```scoring_file.csv```
4. When done executing code that requires Pandas, use command ```deactivate```, or just exit terminal (standard Python code can be executed without this virtual environment; when Pandas or other dependencies are required, then we can create an environment to manage and contain our packages)


---
*Although using virtual environments is highly recommended, it is possible to execute the code without one. If too many difficulties are faced, then Steps 5, 6, and 10 can be skipped during initial setup. In this scenario, Steps 1 and 4 can be skipped during future runs*

*If no virtual environment is created (and ```pip install pandas``` is run) then the package will be installed globally. This has no explicit downside, but can lead to disorganization and misconfiguration down the line*
