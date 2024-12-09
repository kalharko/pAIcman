# pAIcman
Multi agent decision making algorithms for a team game of pacman.
Project made in the context of an artificial intelligence class at the UTBM.
Project made by:
- Cloarec Florian
- Mann William
- Dewasmes Oscar
- Dreano Hermance
- Le Guilly Erwann

# Installation

Cloner le projet
```
git clone https://github.com/kalharko/pAIcman
```
Go into the project
```
cd pAIcman
```
Create a python virtual environnement :
```
python -m venv env
```
Enter the virtual environnement:
```
source env/bin/activate
```
or (windows powershell)
```
.\env\Scripts\Activate.ps1
```
Install the necessary dependencies:
```
pip install -r requirements.txt
```

# Launch one of the algorithms
At the project's root
```
python main.py <map_path> <team1_decision_algo> <team2_decision_algo>
```
With `map_path` an optional argument that default to `maps/original.txt`.
With `team1_decision_algo` and `team2_decision_algo` defaulting to `utility` and `strategy_triangle`


# End of project presentation
Here are some extracts of the presentation the team made to our professors.

![](Documentation/images/AI50%20Presentation%20Pac%20mac%20project.png)
![](Documentation/images/AI50%20Presentation%20Pac%20mac%20project_1.png)
![](Documentation/images/AI50%20Presentation%20Pac%20mac%20project_2.png)
![](Documentation/images/AI50%20Presentation%20Pac%20mac%20project_3.png)
![](Documentation/images/AI50%20Presentation%20Pac%20mac%20project_4.png)
![](Documentation/images/AI50%20Presentation%20Pac%20mac%20project_5.png)
![](Documentation/images/AI50%20Presentation%20Pac%20mac%20project_6.png)
![](Documentation/images/AI50%20Presentation%20Pac%20mac%20project_7.png)
MAS = Multi Agent System

![](Documentation/images/AI50%20Presentation%20Pac%20mac%20project_8.png)
![](Documentation/images/AI50%20Presentation%20Pac%20mac%20project_9.png)
We implemented 2 team strategies, the first one beeing a utility algorithm. Following are examples of the different parameters taken into account by the utility algorithm. 

![](Documentation/images/AI50%20Presentation%20Pac%20mac%20project_10.png)
![](Documentation/images/AI50%20Presentation%20Pac%20mac%20project_11.png)
![](Documentation/images/AI50%20Presentation%20Pac%20mac%20project_12.png)
![](Documentation/images/AI50%20Presentation%20Pac%20mac%20project_13.png)
![](Documentation/images/AI50%20Presentation%20Pac%20mac%20project_14.png)
![](Documentation/images/AI50%20Presentation%20Pac%20mac%20project_15.png)
![](Documentation/images/AI50%20Presentation%20Pac%20mac%20project_16.png)
The second team strategy implemented is a collection of behavior algorithms that are performant in specific situation. An overarching algorithm attributes the best behavior to each members of the team.

![](Documentation/images/AI50%20Presentation%20Pac%20mac%20project_17.png)
![](Documentation/images/AI50%20Presentation%20Pac%20mac%20project_18.png)
![](Documentation/images/AI50%20Presentation%20Pac%20mac%20project_19.png)
![](Documentation/images/AI50%20Presentation%20Pac%20mac%20project_20.png)
![](Documentation/images/AI50%20Presentation%20Pac%20mac%20project_21.png)
![](Documentation/images/AI50%20Presentation%20Pac%20mac%20project_22.png)
![](Documentation/images/AI50%20Presentation%20Pac%20mac%20project_23.png)
![](Documentation/images/AI50%20Presentation%20Pac%20mac%20project_24.png)
![](Documentation/images/AI50%20Presentation%20Pac%20mac%20project_25.png)
![](Documentation/images/AI50%20Presentation%20Pac%20mac%20project_26.png)
![](Documentation/images/AI50%20Presentation%20Pac%20mac%20project_27.png)
![](Documentation/images/AI50%20Presentation%20Pac%20mac%20project_28.png)