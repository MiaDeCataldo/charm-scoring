# [BNL] CHARM Flanker/NBack/SPRT Scoring

## First Time Setup:

1. For this code to be able to run, your computer must have a Python interpreter (v3 or greater). Confirm this by entering the following command into a terminal window: ```python3 --version```. If python3 is "not found", it can be downloaded at https://www.python.org/downloads/ (on Windows it is easiest to use the Microsoft Store).

2. Download the source code to your own computer. 
    - Select the green "<> Code" button at the top right of https://github.com/zekissel/charm-scoring, and download as a ZIP file. Unzip and move the same location as your ***Participant sub-folders*** folder.
        - For example, if your file path is ***CHARM/Participant sub-folders***, save to ***CHARM/charm-scoring*** 
    - Alternatively, use the git command-line tool to copy the repository directly to the current working directory (requires installing git: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git): ```git clone https://github.com/MiaDeCataldo/charm-scoring```

3. In the ***Participant sub-folders*** folder and save all task .csv into their respective subfolders named ***sub_Cxxxx***. 
    - *If the folder/subfolder and/or file names do not match exactly (including capitalization), the files will not be recongnized and no data will be analyzed*
    - *For NBack scoring, all files should be named ***Cxxxx_DualNBack_Task_*.csv*** where the asterick can be any number of any character (a timestamp)*
    - *For SRT scoring, all files should be named ***Cxxxx_SRT_*.csv***
    -_ *For Flanker scoring, all files should be named ***Cxxxx_flanker.csv***

4. In a terminal window, navigate to the project directory where the ***Participant sub-folders*** file is. (for example ***CHARM***)
    - On Mac:  right click the project directory folder and select "Open in Terminal".
    - On Window's File Explorer: open the project directory folder and type "cmd" in the file address bar.
    - Alternatively, use the ```cd <destination>``` command to navigate through directories in a terminal interface. If you cloned the repository using ```git clone``` in step 2, you should already be in the correct directory.
    - *The command ```pwd``` in a terminal will print the working directory. Use this to confirm where you are*

5. Create an environment in order to install Pandas (framework used to manipulate data): Enter ```python3 -m venv .venv``` into terminal ("-m venv" sets "mode" to virtual environment, and ".venv" is name of resulting directory that contains environment). 

    - *For WINDOWS: I've found it is easiest to skip steps 5 and 6*

6. Put the environment that was just created into context using command: ```source .venv/bin/activate```

7. Install dependency using ```pip install pandas``` (pip is a Python package manager, and Pandas is a data manipulation framework for Python)
    - When installing Python dependencies from a provided source, the convention is to provide a file ***requirements.txt*** that contains all necessary package names. This repository has such a provided file, so alternatively you could enter the command ```pip install -r requirements.txt``` ("-r" signals that the next argument will be a requirements file)

8. Execute Python script with ```python3 ./charm-scoring/score-flanker.py``` (to score flanker) 
   - *To score Nback data execute with  ```python3 ./charm-scoring/score-nback.py```
   - *To score SRT data execute with  ```python3 ./charm-scoring/score-SPRT.py```

10. The outputted scores will be written to file ***charm-scoring/flanker_scores.csv***. Use command ```cat <file>``` to display the contents of the file to terminal: ```cat charm-scoring/scoring_file.csv``` (or view in Excel, Sheets, notepad, etc.)
    -*Nback will be written to ***charm-scoring/nback_scores.csv***
    -*SRT will be written to ***charm-scoring/sprt_scores.csv***

12. To remove the virtual environment from context, use command ```deactivate```


## For Future Runs:
1. Once you create the virtual environment and install Pandas to it, you can reuse this environment again the next time. If you already have the environment configured, navigate to the same project directory and use the same command to set context: ```source .venv/bin/activate```
2. Dependecies are already installed this time; you can execute the Python code that uses Pandas by using the command ```python3 score-flanker.py```.
3. If a participant file is added, removed, or changed, then the script will need to be run again in order to update calculations and re-export ***flanker_scores.csv***
4. When done executing code that requires Pandas, use command ```deactivate```, or just exit terminal (standard Python code can be executed without this virtual environment; when Pandas or other dependencies are required, then we can create an environment to manage and contain our packages)


---
*Although using virtual environments is highly recommended, it is possible to execute the code without one. If too many difficulties are faced, then Steps 5, 6, and 10 can be skipped during initial setup. In this scenario, Steps 1 and 4 can be skipped during future runs*

*If no virtual environment is created (and ```pip install pandas``` is run) then the package will be installed globally. This has no explicit downside, but can lead to disorganization and misconfiguration down the line*


## Repository Breakdown:
1. **score-x.py** (where x is **flanker**, **nback**, or **sprt**): Python source code; reads all properly formatted CSVs from the ***Participant sub-folders/sub_Cxxxx*** directory and exports results to ***x_scores.csv***. Once all packages are installed, activate this script with ```python3 score-x.py```

2. **requirements.txt**: text file that contains all necessary packages (contains all packages and dependecies necessary for Pandas). Install requirements with ```pip install -r requirements.txt```

3. **Participant sub-folders/sub_Cxxxx**: directory, subdirectory, and participant files that MUST BE CREATED AND RENAMED BY YOU, to match the schema set in ***score-x.py*** (when initially downloading this repository, these folders will not be present).

4. **LICENSE.md** & **README.md**: open-source MIT license and directions for use, respectively (".md" file extension means "Markdown": these files are best viewed on Github, or any other markdown viewer; that way they'll be formatted nicely, not just a monospace text blob).

5. **.gitignore**: file that declares which local files I don't want to send to this repository. For example, the ".venv" directory is a part of this file: it would be unneccessary to save this environment to Github; instead, I've added the requirements.txt file so that any user can create their own environment with the same specifications.
