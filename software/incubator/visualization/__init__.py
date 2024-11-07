import data_plotting as plot
import pandas as p

if __name__ == '__main__':
    data = p.read_csv('rec_2024-11-07__12_13_11.csv')
    fig = plot.plot_incubator_data(data)
