import pulp
import random

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
        for row in cost_matrix:
            row.extend([0] * (num_agents - num_tasks))
        tasks.extend([f"Dummy Task {i}" for i in range(num_agents - num_tasks)])

    elif num_tasks > num_agents:
        for _ in range(num_tasks - num_agents):
            cost_matrix.append([0] * num_tasks)
        agents.extend([f"Dummy Agent {i}" for i in range(num_tasks - num_agents)])

    return cost_matrix, agents, tasks

def solve_assignment_problem(cost_matrix, agents, tasks):
    num_agents = len(agents)
    num_tasks = len(tasks)
    prob = pulp.LpProblem("Assignment_Problem", pulp.LpMinimize)
    x = [[pulp.LpVariable(f'x{i}{j}', cat='Binary') for j in range(num_tasks)] for i in range(num_agents)]

    prob += pulp.lpSum(cost_matrix[i][j] * x[i][j] for i in range(num_agents) for j in range(num_tasks))

    for i in range(num_agents):
        prob += pulp.lpSum(x[i][j] for j in range(num_tasks)) == 1

    for j in range(num_tasks):
        prob += pulp.lpSum(x[i][j] for i in range(num_agents)) == 1

    prob.solve(pulp.PULP_CBC_CMD(msg=False))

    print("\nOptimal Assignment:")
    total_cost = 0
    for i in range(num_agents):
        for j in range(num_tasks):
            if pulp.value(x[i][j]) == 1:
                print(f"{agents[i]} assigned to {tasks[j]} with cost {cost_matrix[i][j]}")
                total_cost += cost_matrix[i][j]
    print(f"\nOptimal Total Cost: {total_cost}\n")

def get_user_input():
    num_agents = int(input("Enter the number of agents: "))
    agents = []

    for i in range(num_agents):
        agent_name = input(f"Enter the name of agent {i+1}: ")
        agents.append(agent_name)

    num_tasks = int(input("Enter the number of tasks: "))
    tasks = []

    for i in range(num_tasks):
        task_name = input(f"Enter the name of task {i+1}: ")
        tasks.append(task_name)

    cost_matrix = []

    for i in range(num_agents):
        costs = []
        for j in range(num_tasks):
            cost = random.randint(1, 9)
            costs.append(cost)
        cost_matrix.append(costs)

    return cost_matrix, agents, tasks

def main():
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

    cost_matrix, agents, tasks = balance_matrix(cost_matrix, agents, tasks)

    print("\nInput Cost Matrix:")
    for i in range(len(agents)):
        for j in range(len(tasks)):
            print(f"{agents[i]} -> {tasks[j]}: Cost = {cost_matrix[i][j]}")
    
    solve_assignment_problem(cost_matrix, agents, tasks)

if __name__ == "__main__":
    main()
