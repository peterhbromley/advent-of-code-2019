
def get_input(input_path):
    orbits = []
    with open(input_path) as f:
        line = f.readline()
        while line:
            orbits.append(line.strip('\n').split(')'))
            line = f.readline()
    return orbits


def build_orbit_graph(orbit_pairs):
    return {orbiter : orbitee for orbitee, orbiter in orbit_pairs}


def get_counts(graph):
    orbiters = set(graph.keys())
    orbitees = set(graph.values())
    not_orbited = orbiters - orbitees
    memo = {}

    def get_counts_helper(planet):
        if planet not in graph.keys():
            return 0
        elif planet not in memo.keys():
            next_planet = graph[planet]
            memo[planet] = 1 + get_counts_helper(next_planet)
        return memo[planet]
    
    for outer_planet in not_orbited:
        memo[outer_planet] = get_counts_helper(outer_planet)
    
    return sum(memo.values())


def orbital_transfers(graph):
    you_planet = graph['YOU']
    santa_planet = graph['SAN']

    you_to_start = []
    while you_planet in graph.keys():
        you_to_start.append(you_planet)
        you_planet = graph[you_planet]
    
    santa_to_you_path = []
    while santa_planet not in you_to_start:
        santa_to_you_path.append(santa_planet)
        santa_planet = graph[santa_planet]
    
    you_to_santa_path = you_to_start[:you_to_start.index(santa_planet) + 1]

    full_path = you_to_santa_path + santa_to_you_path

    return len(full_path) - 1


def main():
    orbits = get_input('input.txt')
    graph = build_orbit_graph(orbits)
    total_orbits = get_counts(graph)
    path_to_santa = orbital_transfers(graph)
    print('Answer to part 1: {}'.format(total_orbits))
    print('Answer to part 2: {}'.format(path_to_santa))
            
        
main()
