from downloader import  *
from itertools import permutations

def calculate_distance(x1, y1, x2, y2):
    return round(math.sqrt((x2-x1)**2 + (y2-y1)**2))


def calculate_time(distance, speed):
    SYSTEM_SCALE = 3
    DOCKING_SECONDS = 30
    return ((distance * SYSTEM_SCALE) / speed) + DOCKING_SECONDS


def calculate_fuel_cost(distance, fuel_efficiency, docking_efficiency, origin_location_type):
    flight_cost = math.round((distance * fuel_efficiency) / 30)
    docking_cost = (docking_efficiency if origin_location_type == "PLANET" else 0) + 1
    return flight_cost + docking_cost


def get_systems_matrix(*systems):
    if len(systems) == 0:
        systems = SYSTEMS
    return {s : [ [ h["symbol"] for h in l ] , [ [ calculate_distance(a["x"],a["y"],b["x"],b["y"]) for b in l ] for a in l ] ] for s , l in get_systems(*systems).items()}


def travelling_salesman_problem(*systems):
    if len(systems) == 0:
        systems = SYSTEMS
    
    def inner(system):
        header = system[0] 
        system = system[1]
        n = len(system)
        m = min([(sum([system[p[i]][p[(i+1) % len(p)]] for i in range(len(p))]), p) for p in permutations(range(len(system))) if p < p[::-1]])
        return [header[i] for i in m[1]]
    
    for k,v in get_systems_matrix(*systems).items():
        with open(f"utils/systems/tsp/TSP_{k}.json", "w") as file:
            print(k)
            file.write(json.dumps({k: inner(v)}, indent=4))

travelling_salesman_problem()
