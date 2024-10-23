# Assignment Problem Solver

This program solves the assignment problem using linear programming. It allows users to input a cost matrix for assigning agents to tasks, or it can use a default cost matrix.

## Features
- Accepts user input for agents, tasks, and costs.
- Balances the cost matrix by adding dummy agents or tasks as needed.
- Solves the assignment problem and provides optimal assignments and total cost.

### What is PuLP?

**PuLP** is a Python library used for formulating and solving linear programming (LP) problems, which include optimization problems with a linear objective function and linear constraints. It is a free and open-source library that allows users to describe optimization problems in a simple and declarative way using Python. PuLP can interface with various optimization solvers, including the default CBC (COIN-OR branch and cut) solver.

### Key Concepts of PuLP:

1. **Linear Programming (LP):**
   Linear programming is a method for optimizing a linear objective function, subject to linear equality and inequality constraints.
   - **Objective function**: A linear equation that defines what we are trying to optimize (minimize or maximize).
   - **Constraints**: Linear inequalities or equalities that the solution must satisfy.
   - **Decision variables**: Variables that represent the decisions we need to make.

2. **Binary Integer Programming:**
   PuLP also supports integer programming (IP) and binary integer programming (BIP), where decision variables are restricted to integers or binary values (0 or 1). Binary decision variables are often used in assignment problems, where a variable is either assigned (`1`) or not assigned (`0`).

3. **Solvers:**
   PuLP relies on external solvers to find optimal solutions for LP problems. Some popular solvers that can be used with PuLP include:
   - **CBC** (the default solver in PuLP)
   - **Gurobi**
   - **CPLEX**
   - **GLPK**

   These solvers use mathematical techniques like the simplex method, interior-point methods, and branch-and-bound for integer programming to find optimal solutions.

### How PuLP Works:

1. **Define the Problem:**
   PuLP starts by defining an optimization problem, specifying whether it’s a minimization or maximization problem. This is done using the `LpProblem` class.

   ```python
   prob = pulp.LpProblem("Assignment_Problem", pulp.LpMinimize)
   ```

   This creates an instance of an optimization problem called `Assignment_Problem` where the objective is to minimize the total cost.

2. **Decision Variables:**
   Next, PuLP allows you to define decision variables using the `LpVariable` class. In the assignment problem, the decision variables are binary (either an agent is assigned to a task or not).

   ```python
   x = [[pulp.LpVariable(f'x{i}{j}', cat='Binary') for j in range(num_tasks)] for i in range(num_agents)]
   ```

   - `x[i][j]`: Represents whether agent `i` is assigned to task `j` (`1`) or not (`0`).
   - `cat='Binary'`: Ensures that the variable can only take values 0 or 1 (for binary decision-making).

3. **Objective Function:**
   After defining the decision variables, you specify the objective function. In our case, we aim to minimize the total cost of assignments. This is done by summing the costs of all agent-task pairs:

   ```python
   prob += pulp.lpSum(cost_matrix[i][j] * x[i][j] for i in range(num_agents) for j in range(num_tasks))
   ```

   This line adds the objective function to the problem by multiplying the cost of assigning agent `i` to task `j` by the decision variable `x[i][j]` and summing these products for all agent-task pairs.

4. **Constraints:**
   Constraints are the conditions that must be met for a solution to be valid. In the assignment problem:
   - Each agent is assigned exactly one task.
   - Each task is assigned exactly one agent.

   These are modeled as equality constraints in PuLP:

   - Agent constraints:
     ```python
     for i in range(num_agents):
         prob += pulp.lpSum(x[i][j] for j in range(num_tasks)) == 1
     ```
     This ensures that each agent `i` is assigned to exactly one task.

   - Task constraints:
     ```python
     for j in range(num_tasks):
         prob += pulp.lpSum(x[i][j] for i in range(num_agents)) == 1
     ```
     This ensures that each task `j` is assigned to exactly one agent.

5. **Solving the Problem:**
   After defining the problem, objective function, and constraints, the problem is solved using the `solve()` method. PuLP then calls the default solver (or any other installed solver) to find the optimal solution.

   ```python
   prob.solve(pulp.PULP_CBC_CMD(msg=False))
   ```

   - `pulp.PULP_CBC_CMD(msg=False)`: This tells PuLP to use the CBC solver (default) without printing additional messages. If you want detailed output, you can set `msg=True`.

6. **Interpreting the Solution:**
   Once the problem is solved, the decision variables contain the optimal solution. The value of each variable (`x[i][j]`) indicates whether agent `i` is assigned to task `j`. The `pulp.value()` function is used to retrieve the value of the decision variables.

   ```python
   for i in range(num_agents):
       for j in range(num_tasks):
           if pulp.value(x[i][j]) == 1:
               print(f"{agents[i]} assigned to {tasks[j]} with cost {cost_matrix[i][j]}")
   ```

   The total cost is the sum of all costs for the optimal assignment.

### Example of PuLP Usage in the Code:

Consider the following example problem:
- **Agents:** Agent 0, Agent 1, Agent 2
- **Tasks:** Task 0, Task 1, Task 2
- **Cost Matrix:**

   |         | Task 0 | Task 1 | Task 2 |
   |---------|--------|--------|--------|
   | Agent 0 |   4    |   2    |   5    |
   | Agent 1 |   3    |   7    |   9    |
   | Agent 2 |   8    |   1    |   6    |

The script formulates the problem in PuLP and solves it as follows:

- **Decision Variables:** 
   - `x00`, `x01`, `x02`: Whether Agent 0 is assigned to Task 0, Task 1, Task 2.
   - `x10`, `x11`, `x12`: Whether Agent 1 is assigned to Task 0, Task 1, Task 2.
   - `x20`, `x21`, `x22`: Whether Agent 2 is assigned to Task 0, Task 1, Task 2.

- **Objective Function:** Minimize the total cost of the assignment:
   \[
   	ext{Minimize} \quad 4x_{00} + 2x_{01} + 5x_{02} + 3x_{10} + 7x_{11} + 9x_{12} + 8x_{20} + 1x_{21} + 6x_{22}
   \]

- **Constraints:**
   - Each agent is assigned to exactly one task.
   - Each task is assigned to exactly one agent.

The solver finds an optimal assignment (e.g., Agent 0 to Task 1, Agent 1 to Task 0, and Agent 2 to Task 2) that minimizes the total cost.

### Benefits of Using PuLP:
- **Ease of Use:** PuLP allows you to describe optimization problems in a declarative way without dealing with low-level solver details.
- **Flexibility:** Supports a wide variety of optimization problems (LP, ILP, MILP, etc.).
- **Multiple Solvers:** Works with different solvers, giving users flexibility to choose based on problem complexity and performance.

In summary, PuLP provides a powerful yet simple way to model and solve optimization problems like assignment problems in Python.
## Complexity Analysis

### 1. `balance_matrix` Function
- **Time Complexity**: O(max(n, m)), where `n` is the number of agents and `m` is the number of tasks.

### 2. `solve_assignment_problem` Function
- **Creating Decision Variables**: O(n * m)
- **Objective Function**: O(n * m)
- **Constraints**: O(n + m)
- **Total Complexity**: O(n * m)

### 3. `get_user_input` Function
- **Time Complexity**: O(n + m + n * m) = O(n * m)

### 4. `main` Function
- Coordinates the flow of the program, no additional complexity.

### Overall Time Complexity
- O(n * m), driven by cost matrix input and solving the assignment problem. ==> O(n^2)

### Space Complexity
- O(n * m) for the cost matrix and decision variables. ==> O(n^2)