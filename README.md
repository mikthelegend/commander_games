# Commander Games

## What is this project?
This project analyses data about games of commander (a Magic: The Gathering format). That data is stored on a google sheet, from which it is obtained using GoogleAPI, then processed in python to provide useful insights & analysis. The project also provides a web interface through which you can request and view this data.

## Setup / Environment
The dependancies for this project are listed in `environment.yml`, and can be installed using `conda env create -f environment.yml`. If this fails (which it has before), create an empty environment called `commander_games` and install the dependancies manually using `pip install [dependancy]`.

Then, to run the app, perform the following commands:
```
conda deactivate                # Remove (base) from the env
conda activate commander_games  # Add (commander_games) to the env
flask run --host=0.0.0.0        # Omit the host flag when testing
```
