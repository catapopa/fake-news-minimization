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

    # Track infected nodes per iteration
    infected_counts = [sum(1 for status in step['status'].values() if status == 1) for step in iterations]
    
    return infected_counts