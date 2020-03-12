# A* Path Planner

Get the requirements:
```
pip3 install -r requirements.txt
```
Install the package:
```
pip3 install --user -e .
```

## Create a map

```
python3 generate_map.py map_name min_n_runs min_n_obstacles max_n_obstacles 
```

## Get path between to poses in the map

```
python3 get_path.py map_name pose_1 pose_2
```

## Plot a map

```
python3 plot.py map_name
```