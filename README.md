# pAIcman

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

# Launch one of our algorithms
At the project's root
```
python main.py <map_path> <team1_decision_algo> <team2_decision_algo>
```
With `map_path` an optional argument that default to `maps/original.txt`.
With `team1_decision_algo` and `team2_decision_algo` defaulting to `utility` and `strategy_triangle`
