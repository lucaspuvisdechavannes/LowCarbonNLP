import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def read_data(path):
    return pd.read_csv(path)


def identify_pareto(scores):
    population_size = scores.shape[0]
    population_ids = np.arange(population_size)
    pareto_front = np.ones(population_size, dtype=bool)

    for i in range(population_size):
        for j in range(population_size):
            if all(scores[j] <= scores[i]) and any(scores[j] < scores[i]):
                pareto_front[i] = 0
                break

    return population_ids[pareto_front]


def plot_pareto_graph(data_frame):
    x = df['perplexity'].tolist()
    y = df['energy_consumption'].tolist()
    scores = np.array(list(zip(x, y)))
    pareto = identify_pareto(scores)
    pareto_front = scores[pareto]

    pareto_front_df = pd.DataFrame(pareto_front)
    pareto_front_df.sort_values(0, inplace=True)
    pareto_front = pareto_front_df.values

    x_pareto = pareto_front[:, 0]
    y_pareto = pareto_front[:, 1]

    sns.set_theme()
    sns.scatterplot(data=df, x='perplexity', y='energy_consumption', hue='position_embedding_type')
    sns.lineplot(x=x_pareto, y=y_pareto)
    plt.xlabel('Perplexity (lower is better)')
    plt.ylabel('Energy Consumption (kWh)')
    plt.show()


def plot_correlation_heatmap(df):
    df = df.drop(['max_position_embeddings', 'type_vocab_size', 'initializer_range', 'layer_norm_eps', 'gradient_checkpointing', 'use_cache', 'energy_loss', 'loss', 'id'], axis=1)
    correlation_matrix = df.corr()

    cmap = sns.diverging_palette(220, 20, as_cmap=True)

    sns.heatmap(correlation_matrix, center=0.0, cmap=cmap)
    plt.show()


if __name__ == '__main__':
    data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
    df = read_data(data_path + '/model_data.csv')

    plot_correlation_heatmap(df)
    # plot_pareto_graph(df)
