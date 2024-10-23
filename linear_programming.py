import pulp
import random

# Default cost matrix
default_cost_matrix = [
    [4, 2, 5],
    [3, 7, 9],
    [8, 1, 6]
]

default_agents = ["Agent 0", "Agent 1", "Agent 2"]
default_tasks = ["Task 0", "Task 1", "Task 2"]

def balance_matrix(cost_matrix, agents, tasks):
    num_agents = len(agents)
    num_tasks = len(tasks)

    if num_agents > num_tasks:
        # Add dummy tasks
        for row in cost_matrix:
            row.extend([0] * (num_agents - num_tasks))
        tasks.extend([f"Dummy Task {i}" for i in range(num_agents - num_tasks)])

    elif num_tasks > num_agents:
        # Add dummy agents
        for _ in range(num_tasks - num_agents):
            cost_matrix.append([0] * num_tasks)
        agents.extend([f"Dummy Agent {i}" for i in range(num_tasks - num_agents)])

    return cost_matrix, agents, tasks

def solve_assignment_problem(cost_matrix, agents, tasks):
    # Number of agents and tasks
    num_agents = len(agents)
    num_tasks = len(tasks)

    # Create the 'prob' variable to contain the problem data
    prob = pulp.LpProblem("Assignment_Problem", pulp.LpMinimize)

    # Create decision variables
    x = [[pulp.LpVariable(f'x{i}{j}', cat='Binary') for j in range(num_tasks)] for i in range(num_agents)]

    # Objective function: Minimize the total assignment cost
    prob += pulp.lpSum(cost_matrix[i][j] * x[i][j] for i in range(num_agents) for j in range(num_tasks))

    # Constraints: Each agent is assigned to exactly one task
    for i in range(num_agents):
        prob += pulp.lpSum(x[i][j] for j in range(num_tasks)) == 1

    # Constraints: Each task is assigned to exactly one agent
    for j in range(num_tasks):
        prob += pulp.lpSum(x[i][j] for i in range(num_agents)) == 1

    # Solve the problem without printing solver output
    prob.solve(pulp.PULP_CBC_CMD(msg=False))

    # Display the solution
    print("\nOptimal Assignment:")
    total_cost = 0
    for i in range(num_agents):
        for j in range(num_tasks):
            if pulp.value(x[i][j]) == 1:
                print(f"{agents[i]} assigned to {tasks[j]} with cost {cost_matrix[i][j]}")
                total_cost += cost_matrix[i][j]
    print(f"\nOptimal Total Cost: {total_cost}\n")

def get_user_input():
    # Get number of agents
    num_agents = int(input("Enter the number of agents: "))
    agents = []

    # Get agent names
    for i in range(num_agents):
        agent_name = input(f"Enter the name of agent {i+1}: ")
        agents.append(agent_name)

    # Get number of tasks
    num_tasks = int(input("Enter the number of tasks: "))
    tasks = []

    # Get agent names
    for i in range(num_tasks):
        task_name = input(f"Enter the name of task {i+1}: ")
        tasks.append(task_name)

    # Initialize cost matrix
    cost_matrix = []

    # Get costs for each agent-task combination
    for i in range(num_agents):
        costs = []
        for j in range(num_tasks):
            # Generate a random cost between 1 and 9
            cost = random.randint(1, 9)
            costs.append(cost)
        cost_matrix.append(costs)

    return cost_matrix, agents, tasks

def main():
    # Ask if user wants to provide input or use the default matrix
    use_default = input("Do you want to use the default cost matrix? (yes/no): ").strip().lower()

    if use_default == "yes":
        cost_matrix = default_cost_matrix
        agents = default_agents
        tasks = default_tasks
        print("\nUsing default cost matrix and agents...\n")
    else:
        cost_matrix, agents, tasks = get_user_input()
        print("\nGenerated Random Cost Matrix:")
        for i in range(len(agents)):
            for j in range(len(tasks)):
                print(f"{agents[i]} -> {tasks[j]}: Cost = {cost_matrix[i][j]}")

    # Balance the matrix if agents and tasks are not equal
    cost_matrix, agents, tasks = balance_matrix(cost_matrix, agents, tasks)

    print("\nInput Cost Matrix:")
    for i in range(len(agents)):
        for j in range(len(tasks)):
            print(f"{agents[i]} -> {tasks[j]}: Cost = {cost_matrix[i][j]}")
    
    # Solve the assignment problem
    solve_assignment_problem(cost_matrix, agents, tasks)

if __name__ == "__main__":
    main()
