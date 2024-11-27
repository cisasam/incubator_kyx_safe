import data_plotting as plot
import pandas as p

if __name__ == '__main__':
    data1 = p.read_csv('365-3775-state.csv')
    data2 = p.read_csv('params2-state.csv')
    data3 = p.read_csv('cbair-error-state.csv')
    data4 = p.read_csv('gbox-error-state.csv')
    fig = plot.plot_incubator_data(data1,data2,data3,data4)
    #fig = plot.plot_controller_data(data)
    fig.savefig('params_comparison.eps', format='eps')
