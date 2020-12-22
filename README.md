![alt text](http://greengrowthindex.gggi.org/wp-content/uploads/2019/09/LOGO_GGGI_GREEN_350x131px_002trans_Prancheta-1.png)

# GraphModels
A framework to compute Green Growth models using computational graphs.

# INSTALLATION

TO DO

# HOW TO

The program parses a graph_specifications list. It is a **list** of **nodes** that fully defines the graph. This graph is then used to build a **model function**. This function takes a **set of inputs and parameters** and returns the **set of all the variables and outputs** computed by the model as well as the input and parameters.

<font color='red'>THE FORMATTING IS ESSENTIAL</font>


## Nodes definitions

Each node is defined by a **dictionary** of properties:

Two types of nodes are possible:

### 1. Non computational nodes (inputs or parameters):

```python
node_1 = {'type': 'input',
          'unit': '$',
          'code': 'Var 1',
          'name': 'Variable 1'
          }
```      
### 2. Computational nodes (variables or outputs)

```python
node_2 = {'type': 'variable',
          'code': 'Var 2',
          'name': 'Variable 2',
          'unit': '$ per capita',
          'in': ['Par 1', 'Var 1'],
          'computation': {'name': 'Par 1 * Var 1',
                          'formula': lambda X: X['Par 1'] * X['Var 1']}
          }
```

**Note:** In order to define computational nodes, a computation must be defined.A computation dictionary must include a name for the computation (for visual purposes) as well as a formula for the computation. **The formula must take a dictionary X as input**. This dictionary X is the "state of the system" up to this point of the graph. It contains all the parameters, inputs, and variables computed previously.


## Full example

```python
from graphmodels.graphmodel import GraphModel

graph_specifications = [
    {'type': 'input',
     'unit': '',
     'id': 'In 1',
     'name': 'Input 1',
     },
    {'type': 'parameter',
     'unit': '',
     'id': 'Par 1',
     'name': 'Parameter 1',
     },
    {'type': 'variable',
     'id': 'Var 1',
     'name': 'Variable 1',
     'unit': '',
     'in': ['Par 1', 'In 1'],
     'computation': {'name': 'Par 1 * In 1',
                     'formula': lambda X: X['Par 1'] * X['In 1']}
     },
    {'type': 'parameter',
     'unit': '',
     'id': 'Par 3',
     'name': 'Parameter 3',
     },
    {'type': 'output',
     'id': 'Out 1',
     'name': 'Output 1',
     'unit': '',
     'in': ['Var 1', 'Var 2', 'Par 3'],
     'computation': {'name': 'Var 1 + Var 2 + Par 3',
                     'formula': lambda X: X['Var 1'] + X['Var 2'] + X['Par 3']}
     },
    {'type': 'input',
     'unit': '',
     'id': 'In 2',
     'name': 'Input 2',
     },
    {'type': 'parameter',
     'unit': '',
     'id': 'Par 2',
     'name': 'Parameter 2',
     },
    {'type': 'variable',
     'id': 'Var 2',
     'name': 'Variable 2',
     'unit': '',
     'in': ['Par 2', 'In 2'],
     'computation': {'name': 'Par 2 / In 2',
                     'formula': lambda X: X['Par 2'] / X['In 2']}
     },
]


inputs_parameters = {
    'In 1': 5,
    'In 2': 4,
    'Par 1': 3,
    'Par 2': 5,
    'Par 3': 5
}


Model = GraphModel(graph_specifications)

Model.run(inputs_parameters)
```
