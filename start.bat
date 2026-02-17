rem Step 1: Activate Miniconda, use the actual path where your Miniconda/Ananconda is installed.
call "E:\miniconda3\Scripts\activate.bat" "E:\miniconda3\"

rem Step 2: Activate Conda environment. 
call conda activate commander_games

rem Step 3: Change directory to the desired folder.
cd /d "E:\webservers\commander_games"

rem Step 4: pull from github
git pull

rem Step 5: Run the Python script.
flask run --host=0.0.0.0

rem Step 6: Keep the command prompt open after execution (optional)
cmd /k