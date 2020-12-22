![alt text](http://greengrowthindex.gggi.org/wp-content/uploads/2019/09/LOGO_GGGI_GREEN_350x131px_002trans_Prancheta-1.png)

# GraphModels
A framework to compute Green Growth models using computational graphs.

# INSTALLATION

TO DO

# HOW TO

The program parses a graph_specifications list. It is a **list** of **nodes** that fully defines the graph. This graph is then used to build a **model function**. This function takes a **set of inputs and parameters** and returns the **set of all the variables and outputs** computed by the model as well as the input and parameters.

<font color='red'>THE FORMATTING IS ESSENTIAL</font>


The list is as follow:
```python
graph_specifications = [node_1, node_2, node_3]
```

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

#### Computation definition

In order to define computational nodes, a computation must be defined by a computation dictionary including a name for the computation (for visual purposes) as well as a formula for the computation.
