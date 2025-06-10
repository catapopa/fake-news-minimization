import ndlib.models.epidemics as ep
import ndlib.models.ModelConfig as mc
import pickle

G = pickle.load(open("graph.pkl", "rb"))

def simulate_icm_spread(G=G, fraction_infected=0.05, probability=0.1, steps=30):
    # Setup ICM model
    model = ep.IndependentCascadesModel(G)

    # Configure the model
    config = mc.Configuration()
    config.add_model_parameter('fraction_infected', fraction_infected)
    config.add_model_parameter('probability', probability)
    model.set_initial_status(config)

    # Simulate spread
    iterations = model.iteration_bunch(steps)

    infected_counts = []
    infected_nodes = []
    for step in iterations:
        infected = [n for n, status in step['status'].items() if status == 1]
        infected_counts.append(len(infected))
        infected_nodes.append(infected)

    return infected_counts, infected_nodes

def simulate_icm_spread_total(G=G, fraction_infected=0.05, probability=0.1, steps=30):
    model = ep.IndependentCascadesModel(G)
    config = mc.Configuration()
    config.add_model_parameter('fraction_infected', fraction_infected)
    config.add_model_parameter('probability', probability)
    model.set_initial_status(config)

    iterations = model.iteration_bunch(steps)

    all_infected = set()
    for step in iterations:
        infected = [n for n, status in step['status'].items() if status == 1]
        all_infected.update(infected)

    return all_infected