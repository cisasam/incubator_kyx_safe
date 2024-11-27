
import matplotlib.pyplot as plt


def plot_incubator_data(data1,data2,data3,data4):
    plt.rcParams['text.usetex'] = True
    plt.rcParams.update({'font.size': 9})
    

    plt.rc('text.latex', preamble=r'\usepackage{xspace}')
    fig, (ax1) = plt.subplots(1, 1)

    ax1.plot((data1["time"]-data1["time"][0])/10e8, data1["average_temperature"], label=r'$T_c^1$')
    ax1.plot((data2["time"]-data2["time"][0])/10e8, data2["average_temperature"], label=r'$T_c^2$')
    ax1.plot((data3["time"]-data3["time"][0])/10e8, data3["average_temperature"], label=r'$T_c^3$')
    ax1.plot((data4["time"]-data4["time"][0])/10e8, data4["average_temperature"], label=r'$T_c^4$', color='tab:purple')
    

    ax1.hlines(y=37.75, colors='k', xmin=0, xmax=((data1['time'].iloc[-1])-data1["time"][0])/10e8, label='Bounds')
    ax1.hlines(y=36.5, colors='k', xmin=0, xmax=((data1['time'].iloc[-1])-data1["time"][0])/10e8)
    ax1.set_ylabel("Temperature (°C)")
    ax1.set_xlabel("time (s)")

    ax1.legend(loc=4)
    

    fig.align_xlabels()
    plt.xlim(0,600)
    fig.set_figwidth(4.2)
    fig.set_figheight(3)
    fig.set_layout_engine(layout='constrained')
    plt.show()
    return fig

def plot_controller_data(data):
    plt.rcParams['text.usetex'] = True
    plt.rc('text.latex', preamble=r'\usepackage{xspace}')
    fig, (ax1) = plt.subplots(1, 1)

    ax1.plot((data["plant_time"]-data["time"][0])/10e8, data["t_heater"], label=r"$T_h$")
    ax1.plot((data["plant_time"]-data["time"][0])/10e8, data["ubound_h"], label='safeToHeat')
    ax1.plot((data["plant_time"]-data["time"][0])/10e8, data["lbound_h"], label='safeToCool')
    ax1.set_ylabel("Temperature (°C)")

    ax1.legend(loc=4)
    ax1.set_xlabel("time (s)")
    fig.align_xlabels()

    plt.xlim(0,600)

    plt.show()
    return fig



def plotly_incubator_data(data, compare_to=None, heater_T_data=None, events=None,
                          overlay_heater=True, show_actuators=False,
                          show_hr_time=False):
    nRows = 2
    titles = ["Incubator Temperature (°C)", "Room Temperature (°C)"]
    if show_actuators:
        nRows += 1
        titles.append("Actuators")
    if heater_T_data is not None:
        nRows += 1
        titles.append("Heatbed Temperature (°C)")

    x_title = "Timestamp" if show_hr_time else "Time (s)"

    time_field = "timestamp_ns" if show_hr_time else "time"

    fig = make_subplots(rows=nRows, cols=1, shared_xaxes=True,
                        x_title=x_title,
                        subplot_titles=titles)

    fig.add_trace(go.Scatter(x=data[time_field], y=data["average_temperature"], name="avg_T"), row=1, col=1)
    if overlay_heater:
        fig.add_trace(go.Scatter(x=data[time_field], y=[40 if b else 30 for b in data["heater_on"]], name="heater_on"), row=1, col=1)

    if events is not None:
        for i, r in events.iterrows():
            # Get the closest timestamp_ns to the event time
            closest_ts = min(data[time_field], key=lambda x:abs(x-r[time_field]))
            # Get the average temperature for that timestamp_ns
            avg_temp = data.loc[data.index[data[time_field] == closest_ts]]["average_temperature"].iloc[0]

            fig.add_annotation(x=r[time_field], y=avg_temp,
                               text=r["event"],
                               showarrow=True,
                               arrowhead=1)

    if compare_to is not None:
        for res in compare_to:
            if "T" in compare_to[res]:
                fig.add_trace(go.Scatter(x=compare_to[res][time_field], y=compare_to[res]["T"], name=f"avg_temp({res})"), row=1, col=1)
            if "T_object" in compare_to[res]:
                fig.add_trace(go.Scatter(x=compare_to[res][time_field], y=compare_to[res]["T_object"], name=f"T_object({res})"), row=1, col=1)

    fig.add_trace(go.Scatter(x=data[time_field], y=data["T_room"], name="room"), row=2, col=1)

    next_row = 3

    if show_actuators:
        fig.add_trace(go.Scatter(x=data[time_field], y=data["heater_on"], name="heater_on"), row=next_row, col=1)
        fig.add_trace(go.Scatter(x=data[time_field], y=data["fan_on"], name="fan_on"), row=next_row, col=1)

        if compare_to is not None:
            for res in compare_to:
                if "in_lid_open" in compare_to[res]:
                    fig.add_trace(go.Scatter(x=compare_to[res][time_field], y=compare_to[res]["in_lid_open"], name=f"in_lid_open({res})"), row=next_row, col=1)

        next_row += 1

    if heater_T_data is not None:
        for trace in heater_T_data:
            fig.add_trace(go.Scatter(x=heater_T_data[trace][time_field], y=heater_T_data[trace]["T_heater"],
                                     name=f"T_heater({trace})"), row=next_row, col=1)
        next_row += 1

    fig.update_layout()

    return fig


def show_plotly(fig):
    fid, target_html = tempfile.mkstemp(".html")
    os.close(fid)
    fig.write_html(target_html, auto_open=True)
