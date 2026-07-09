

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------------------
# Load Data
# ---------------------------------------------------------------
URL = ("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/"
       "IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/"
       "historical_automobile_sales.csv")

data = pd.read_csv(URL)

# ---------------------------------------------------------------
# TASK 2.1: Create the Dash app with a meaningful title
# ---------------------------------------------------------------
app = dash.Dash(__name__)
app.title = "Automobile Sales Statistics Dashboard"

# Year list for dropdown
year_list = [i for i in range(1980, 2024, 1)]

# ---------------------------------------------------------------
# TASK 2.2: App Layout
# ---------------------------------------------------------------
app.layout = html.Div(
    children=[

        # --- Title ---
        html.H1(
            "Automobile Sales Statistics Dashboard",
            style={
                "textAlign": "center",
                "color": "#503D36",
                "fontSize": "24px",
                "fontFamily": "Arial, sans-serif",
                "padding": "20px"
            }
        ),

        # --- Dropdown 1: Report Type ---
        html.Div([
            html.Label(
                "Select Statistics:",
                style={"fontWeight": "bold", "fontFamily": "Arial"}
            ),
            dcc.Dropdown(
                id="dropdown-statistics",
                options=[
                    {"label": "Yearly Statistics",    "value": "Yearly Statistics"},
                    {"label": "Recession Period Statistics", "value": "Recession Period Statistics"},
                ],
                value="Select Statistics",
                placeholder="Select a report type",
                style={"width": "80%", "padding": "3px", "fontSize": "20px",
                       "textAlignLast": "center"}
            )
        ]),

        # --- Dropdown 2: Year ---
        html.Div([
            html.Label(
                "Select Year:",
                style={"fontWeight": "bold", "fontFamily": "Arial"}
            ),
            dcc.Dropdown(
                id="select-year",
                options=[{"label": i, "value": i} for i in year_list],
                value="Select Year",
                placeholder="Select year",
                style={"width": "80%", "padding": "3px", "fontSize": "20px",
                       "textAlignLast": "center"}
            )
        ]),

        # --- Output container ---
        html.Div(id="output-container", className="chart-grid",
                 style={"display": "flex", "flexWrap": "wrap"})
    ]
)

# ---------------------------------------------------------------
# TASK 2.3: Enable/Disable Year dropdown based on Report Type
# ---------------------------------------------------------------
@app.callback(
    Output("select-year", "disabled"),
    Input("dropdown-statistics", "value")
)
def update_input_container(selected_statistics):
    if selected_statistics == "Yearly Statistics":
        return False   # enable year dropdown
    return True        # disable for Recession report


# ---------------------------------------------------------------
# TASK 2.4: Callback for graphs
# ---------------------------------------------------------------
@app.callback(
    Output("output-container", "children"),
    [Input("dropdown-statistics", "value"),
     Input("select-year", "value")]
)
def update_output_container(selected_statistics, input_year):

    # ============================================================
    # RECESSION PERIOD STATISTICS
    # ============================================================
    if selected_statistics == "Recession Period Statistics":

        recession_data = data[data["Recession"] == 1]

        # --- Chart R1: Average automobile sales over recession years (line) ---
        yearly_rec = (recession_data.groupby("Year")["Automobile_Sales"]
                      .mean().reset_index())
        R_chart1 = dcc.Graph(
            figure=px.line(
                yearly_rec, x="Year", y="Automobile_Sales",
                title="Average Automobile Sales Fluctuation Over Recession Period"
            )
        )

        # --- Chart R2: Average vehicles sold by vehicle type (bar) ---
        avg_sales = (recession_data.groupby("Vehicle_Type")["Automobile_Sales"]
                     .mean().reset_index())
        R_chart2 = dcc.Graph(
            figure=px.bar(
                avg_sales, x="Vehicle_Type", y="Automobile_Sales",
                title="Average Number of Vehicles Sold by Vehicle Type during Recession"
            )
        )

        # --- Chart R3: Total expenditure share by vehicle type (pie) ---
        exp_rec = (recession_data.groupby("Vehicle_Type")["Advertising_Expenditure"]
                   .sum().reset_index())
        R_chart3 = dcc.Graph(
            figure=px.pie(
                exp_rec, values="Advertising_Expenditure", names="Vehicle_Type",
                title="Total Expenditure Share by Vehicle Type During Recessions"
            )
        )

        # --- Chart R4: Effect of unemployment rate on vehicle type & sales (bar) ---
        unemp_data = (recession_data.groupby(["unemployment_rate", "Vehicle_Type"])
                      ["Automobile_Sales"].mean().reset_index())
        R_chart4 = dcc.Graph(
            figure=px.bar(
                unemp_data, x="unemployment_rate", y="Automobile_Sales",
                color="Vehicle_Type",
                barmode="group",
                title="Effect of Unemployment Rate on Vehicle Type and Sales"
            )
        )

        return [
            html.Div([R_chart1, R_chart2],
                     style={"display": "flex", "flexWrap": "wrap"}),
            html.Div([R_chart3, R_chart4],
                     style={"display": "flex", "flexWrap": "wrap"})
        ]

    # ============================================================
    # YEARLY STATISTICS
    # ============================================================
    elif (selected_statistics == "Yearly Statistics" and
          isinstance(input_year, int)):

        yearly_data = data[data["Year"] == input_year]

        # --- Chart Y1: Yearly automobile sales (line) ---
        yas = (data.groupby("Year")["Automobile_Sales"]
               .mean().reset_index())
        Y_chart1 = dcc.Graph(
            figure=px.line(
                yas, x="Year", y="Automobile_Sales",
                title="Yearly Automobile Sales Using Line Chart for the Whole Period"
            )
        )

        # --- Chart Y2: Total monthly sales for selected year (line) ---
        mas = (yearly_data.groupby("Month")["Automobile_Sales"]
               .sum().reset_index())
        Y_chart2 = dcc.Graph(
            figure=px.line(
                mas, x="Month", y="Automobile_Sales",
                title=f"Total Monthly Automobile Sales in {input_year}"
            )
        )

        # --- Chart Y3: Average vehicles sold by vehicle type (bar) ---
        avr_vd = (yearly_data.groupby("Vehicle_Type")["Automobile_Sales"]
                  .mean().reset_index())
        Y_chart3 = dcc.Graph(
            figure=px.bar(
                avr_vd, x="Vehicle_Type", y="Automobile_Sales",
                title=f"Average Vehicles Sold by Vehicle Type in {input_year}"
            )
        )

        # --- Chart Y4: Total advertisement expenditure by vehicle type (pie) ---
        exp_data = (yearly_data.groupby("Vehicle_Type")["Advertising_Expenditure"]
                    .sum().reset_index())
        Y_chart4 = dcc.Graph(
            figure=px.pie(
                exp_data, values="Advertising_Expenditure", names="Vehicle_Type",
                title=f"Total Advertisement Expenditure by Vehicle Type in {input_year}"
            )
        )

        return [
            html.Div([Y_chart1, Y_chart2],
                     style={"display": "flex", "flexWrap": "wrap"}),
            html.Div([Y_chart3, Y_chart4],
                     style={"display": "flex", "flexWrap": "wrap"})
        ]

    return []


# ---------------------------------------------------------------
# Run the app
# ---------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
