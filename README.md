# ties481 Hospital flow simulation

This simulation project is build with python and simpy. It is done as an
exercise for the course `ties481 simulation` which is held in the university of
Jyväskylä in the second period of 2022.

## Running

A virtual environment is recommended but not required by any means.

After cloning the project to your local machine start by installing the required
packages

```bash
pip install -r requirements.txt
```

and then run the code with

```bash
py ./simulation/main.py
```

The simulation results are printed to the console, thats it.

## Configuring the simulation

To change the simulation behavior (i.e. operation duration) simply modify the values in the
`simulation/config.py` file.
