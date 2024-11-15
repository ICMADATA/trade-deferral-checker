# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 16:52:12 2024

@author: SimoneBruno
"""


#%%
import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc

# Define exchange rates for EUR and GBP
eur_xe = {
    "EUR": 1,    
    "USD": 0.9,   
    "GBP": 1.186,    
    "PLN": 0.2337,     
    "HUF": 0.0025,     
    "CZK": 0.04,      
    "RON": 0.2,      
    "NOK": 0.085,      
    "DKK": 0.13,     
    "SEK": 0.088,    
    "ISK": 0.0065,        
    "BGN": 0.51,     
    "CHF": 1.07,       
    "CAD": 0.67,     
    "JPY": 0.0063
}

gbp_xe = {
    "EUR": 0.8422,    
    "USD": 0.7581,   
    "GBP": 1,    
    "PLN": 0.2,     
    "HUF": 0.0021 ,     
    "CZK": 0.034,      
    "RON": 0.1693,      
    "NOK": 0.071,      
    "DKK": 0.1128,     
    "SEK": 0.074,    
    "ISK": 0.0055,        
    "BGN": 0.4304,     
    "CHF": 0.8975,       
    "CAD": 0.5612,     
    "JPY": 0.005293
}

# Country and Currency options
country_options = [
    {'label': 'UK', 'value': 'UK'},
    {'label': 'France', 'value': 'FR'},
    {'label': 'Germany', 'value': 'DE'},
    {'label': 'Italy', 'value': 'IT'},
    {'label': 'United States', 'value': 'US'},
    {'label': 'Spain', 'value': 'ES'},
    {'label': 'Other', 'value': 'Other'}
]

currency_options = [
    {"label": "EUR", "value": "EUR"}, {"label": "USD", "value": "USD"},
    {"label": "GBP", "value": "GBP"}, {"label": "PLN", "value": "PLN"},
    {"label": "HUF", "value": "HUF"}, {"label": "CZK", "value": "CZK"},
    {"label": "RON", "value": "RON"}, {"label": "NOK", "value": "NOK"},
    {"label": "DKK", "value": "DKK"}, {"label": "SEK", "value": "SEK"},
    {"label": "ISK", "value": "ISK"}, {"label": "BGN", "value": "BGN"},
    {"label": "CHF", "value": "CHF"}, {"label": "CAD", "value": "CAD"},
    {"label": "JPY", "value": "JPY"}
]

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Define layout
app.layout = dbc.Container([
    # Title Card
dbc.Row([
    dbc.Col([
        dbc.Card([
            dbc.CardBody([
                html.H1("ICMA bonds trade deferral checker", className="text-center", style={"font-weight": "bold"}),
                html.P([
                    html.Span("Instructions:", style={"font-weight": "bold"}), 
                    f"Use the left card to calculate deferral times for Sovereign and Other Public Bond and the right one for Covered, Corporate, Convertible and Other Bonds.\n",
                    html.Br(),
                    f"\n Add all fields then click on the 'Calculate Deferral Time' buttons",
                                    
                ], className="text-center", style={"font-size": "20px"}),
                html.P([
                   html.Span("Disclaimer:", style={"font-weight": "bold"}),
                   "This page is provided for information purposes only and should not be relied upon as legal, financial, or other professional advice. ",
                   "ICMA does not represent or warrant that it is accurate or complete and neither ICMA nor its employees shall have any liability arising from or relating to the use of this page or its contents."

               ], className="text-center", style={"font-size": "12px", "margin-top": "10px"})
            ])
        ], className="mb-4", style={'border': '1px solid #ccc', 'border-radius': '8px', 'padding': '20px', 'background-color': '#f8f9fa'})
    ], width=12),
], className="mb-4"),


    dbc.Row([
        # Left Column: Sovereign and Other Public Bond (Wrapped in a Box)
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H3("Sovereign and Other Public Bond"),

                    html.Label("Is Strip or Inflation Linked?"),
                    dcc.RadioItems(id='strip-inflation', options=[
                        {'label': 'Yes', 'value': 'Yes'}, {'label': 'No', 'value': 'No'}
                    ], value='No',inline=True),

                    html.Label("Issuer Country"),
                    dcc.Dropdown(id='issuer-country', options=country_options, placeholder="Select Country"),

                    html.Br(),  # Adds a space between the rows

                    html.Label("Issue Size Currency"),
                    dcc.Dropdown(id='issue-currency', options=currency_options, placeholder="Select Currency"),

                    html.Br(),  # Adds a space between the rows

                    html.Label("Issue Size"),
                    dcc.Input(id='issue-size', type='number', placeholder="Enter Issue Size"),

                    html.Br(),  # Adds a space between the rows

                    html.Label("Maturity"),
                    dcc.Dropdown(id='maturity-dropdown', options=[
                        {'label': '<5 years', 'value': '<5'},
                        {'label': '5-15 years', 'value': '5-15'},
                        {'label': '>15 years', 'value': '>15'}
                    ], placeholder="Select Maturity"),

                    html.Br(),  # Adds a space between the rows

                    html.Label("Trade Size (in the same currency of issue currency)"),
                    dcc.Input(id='trade-size', type='number', placeholder="Enter Trade Size"),
                    
                    html.Br(),
                    
                    
                    dbc.Button("Calculate Deferral Time", id="calculate-button", color="primary", className="mt-3"),
                    
                    # Output for the original calculation
                    html.Div(id='output-result', className="mt-3"),

                    # Output for the new EU deferral time calculation
                    html.Div(id='output-result-2', className="mt-3"),
                    
                    html.Div(id='output-result-3', className="mt-3")

                ])
            ], className="mb-4", style={'border': '1px solid #ccc', 'border-radius': '8px', 'padding': '20px'}),  # Border and Padding
        ], width=6),

        # Right Column: (No Changes)
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H3("Covered, Corporate, Convertible and Other Bonds"),

                    html.Label("Issue Size Currency"),
                    dcc.Dropdown(id='issue-currency-2', options=currency_options, placeholder="Select Currency"),

                    html.Br(),  # Adds a space between the rows

                    html.Label("Issue Size"),
                    dcc.Input(id='issue-size-2', type='number', placeholder="Enter Issue Size"),

                    html.Br(), # Adds a space between the rows

                    html.Label("Rating"),
                    
                    dcc.Dropdown(id='rating-dropdown', options=[
                        {'label': 'Investment Grade (IG)', 'value': 'IG'},
                        {'label': 'High Yield (HY)', 'value': 'HY'}
                    ], placeholder="Select Rating"),

                    html.Br(),  # Adds a space between the rows

                    html.Label("Trade Size (in the same currency of issue currency)"),
                    dcc.Input(id='trade-size-2', type='number', placeholder="Enter Trade Size"),
                    html.Br(),
                    dbc.Button("Calculate Deferral Times", id="calculate-deferral-button", color="primary", className="mt-3"),

                    
                    html.Div(id='deferral-output-1', className="mt-3"),  # First output: Dynamic message
                    html.Div(id='deferral-output-2', className="mt-3"),  # Second output: Dynamic message
                    html.Div(id='deferral-output-3', className="mt-3")   # Third output: Static message

                ])
            ], className="mb-4", style={'border': '1px solid #ccc', 'border-radius': '8px', 'padding': '20px'}),  # Border and Padding
        ], width=6),

    ], className="mb-4"),
    
    dbc.Row([
    dbc.Col([
        dbc.Card([
            dbc.CardBody([
                html.H4("Contact Us"),
                html.P(
                    "For questions, to submit a bug, or to contact us, please email data@icmagroup.org or call +44 20 7213 0312."
                ),
                html.P([
                   html.Span("© International Capital Market Association (ICMA), Zurich, 2024. All rights reserved.:", style={"font-weight": "bold"}),
                   

               ], className="mb4", style={"font-size": "12px", "margin-top": "10px"})
                
            ])
        ], className="mb-4", style={'border': '1px solid #ccc', 'border-radius': '8px', 'padding': '20px'}),
    ], width=12),
], className="mb-4")
    
], fluid=True,
    

    )


# Define the new function for calculating EU-specific deferral time
def calculate_deferral_time_EU(issue_size_eur, trade_size_eur):
    if trade_size_eur < 5 * (10**6):
        return "Price and volume in real time"
    
    if issue_size_eur >= 1 * (10**9):
        if 5 * (10**6) <= trade_size_eur < 15 * (10**6):
            return "Price and volume deferred 15 minutes"
        elif 15 * (10**6) <= trade_size_eur < 50 * (10**6):
            return "EOD price deferral and 1 week volume deferral"
    
    elif issue_size_eur < 1 * (10**9):
        if 5 * (10**6) <= trade_size_eur < 15 * (10**6):
            return "Price and volume deferred EOD"
        elif 15 * (10**6) <= trade_size_eur < 50 * (10**6):
            return "EOD price deferral and 2 week volume deferral"
    
    if trade_size_eur >= 50 * (10**6):
        return "Price and volume deferred 4 weeks"
    
    return "Unknown condition"


# Callback to handle both the original deferral time logic and the new EU deferral time logic
@app.callback(
    [Output('output-result', 'children'),  # First message output
     Output('output-result-2', 'children'),
     Output('output-result-3', 'children')],  
    [
        Input('calculate-button', 'n_clicks')
    ],
    [
        State('strip-inflation', 'value'),
        State('issuer-country', 'value'),
        State('issue-currency', 'value'),
        State('issue-size', 'value'),
        State('maturity-dropdown', 'value'),
        State('trade-size', 'value')
    ]
)
def calculate_deferral_time(n_clicks, strip_inflation, issuer_country, issue_currency, issue_size, maturity, trade_size):
    if issue_size is None or trade_size is None:
        return "Please fill all fields then click Calculate.", "",""

    # Convert Issue Size and Trade Size into EUR and GBP
    issue_size_eur = issue_size * eur_xe.get(issue_currency, 1)
    issue_size_gbp = issue_size * gbp_xe.get(issue_currency, 1)
    trade_size_eur = trade_size * eur_xe.get(issue_currency, 1)
    trade_size_gbp = trade_size * gbp_xe.get(issue_currency, 1)
    
    # First Logic for Deferral Time (Existing)
    uno = "Price and volume in real time"
    due = "Price and volume deferred 1 day"
    tre = "Price and volume deferred 2 weeks"
    quattro = "Price and volume deferred 3 months"

    # Logic for calculating message based on issue_size and trade_size (GB)
    if issue_size_gbp >= 2 * (10**9): 
        if issuer_country in ['UK', 'FR', 'DE', 'IT', 'US', 'ES'] and strip_inflation == 'No':
            if maturity == '<5':
                if trade_size_gbp <= 15 * (10**6):
                    message = uno
                elif 15 * (10**6) < trade_size_gbp < 50 * (10**6):
                    message = due
                elif 50 * (10**6) < trade_size_gbp <= 500 * (10**6):
                    message = tre
                elif trade_size_gbp > 500 * (10**6):
                    message = quattro
                    
            elif maturity =='5-15':
                if trade_size_gbp <= 10 * (10**6):
                    message = uno
                elif 10 * (10**6) < trade_size_gbp <= 25 * (10**6):
                    message = due
                elif 25 * (10**6) < trade_size_gbp <= 250 * (10**6):
                    message = tre
                elif trade_size_gbp > 250 * (10**6):
                    message = quattro
            elif maturity =='>15':
                if trade_size_gbp <= 5 * (10**6):
                    message = uno
                elif 5 * (10**6) < trade_size_gbp <= 10 * (10**6):
                    message = due
                elif 10 * (10**6) < trade_size_gbp <= 100 * (10**6):
                    message = tre
                elif trade_size_gbp > 100 * (10**6):
                    message = quattro
        else:
            if trade_size_gbp <= 1 * (10**6):
                message = uno
            elif 1 * (10**6) < trade_size_gbp <= 5 * (10**6):
                message = due
            elif 5 * (10**6) < trade_size_gbp <= 25 * (10**6):
                message = tre
            elif trade_size_gbp > 25 * (10**6):
                message = quattro

    elif issue_size_gbp < 2 * (10**9):
        if trade_size_gbp <= 1 * (10**6):
            message = uno
        elif 1 * (10**6) < trade_size_gbp <= 2.5 * (10**6):
            message = due
        elif 2.5 * (10**6) < trade_size_gbp <= 10 * (10**6):
            message = tre
        elif trade_size_gbp > 10 * (10**6):
            message = quattro
    else:
        message = "Enter all fields or contact ICMA"

    # Calculate the second message using the EU logic
    eu_message = calculate_deferral_time_EU(issue_size_eur, trade_size_eur)

    message_with_flag_uk = html.Div([
        html.Img(src="https://upload.wikimedia.org/wikipedia/commons/8/83/Flag_of_the_United_Kingdom_%283-5%29.svg", style={'height': '20px', 'width': 'auto'}),
        html.Span(f" {message}")
    ])  

    message_with_flag_eu = html.Div([
        html.Img(src="https://upload.wikimedia.org/wikipedia/commons/b/b7/Flag_of_Europe.svg", style={'height': '20px', 'width': 'auto'}),
        html.Span(f" {eu_message}")
    ])      
    
    eu_dmo_message =  html.Div([
        html.Img(src="https://upload.wikimedia.org/wikipedia/commons/b/b7/Flag_of_Europe.svg", style={'height': '20px', 'width': 'auto'}),
        html.Span("Depending on specific DMO, trade might be eligible for a 6 months defferal")
    ])      
    

    # Return both messages
    return message_with_flag_uk, message_with_flag_eu, eu_dmo_message


@app.callback(
    [Output('deferral-output-1', 'children'),  # First output: Deferral Time based on GBP
     Output('deferral-output-2', 'children'),  # Second output: Deferral Time based on EUR
     Output('deferral-output-3', 'children')],  # Third output: Static output
    [
        Input('calculate-deferral-button', 'n_clicks')
    ],
    [
        State('issue-currency-2', 'value'),
        State('issue-size-2', 'value'),
        State('trade-size-2', 'value'),
        State('rating-dropdown', 'value')
    ]
)
def calculate_deferral_times(n_clicks, issue_currency, issue_size, trade_size, rating):
    if not n_clicks:
        return "Please fill all fields then click Calculate.", "", ""  # No button click yet, so return empty strings
    
    if issue_size is None or trade_size is None or issue_currency is None or rating is None:
        return "Please fill all fields then click Calculate.", "", ""  # Return error message if fields are missing
    
    # Convert Issue Size and Trade Size into EUR and GBP
    issue_size_eur = issue_size * eur_xe.get(issue_currency, 1)
    issue_size_gbp = issue_size * gbp_xe.get(issue_currency, 1)
    trade_size_eur = trade_size * eur_xe.get(issue_currency, 1)
    trade_size_gbp = trade_size * gbp_xe.get(issue_currency, 1)

    # Calculate the first output (based on GBP logic and rating)
    if issue_size_gbp >= 500 * (10**6) and issue_currency in ['EUR', 'USD', 'GBP']:
        if rating == 'IG':
            if trade_size_gbp <= 1 * (10**6):
                deferral_1 = "Price and volume in real time"
            elif 1 * (10**6) < trade_size_gbp <= 5 * (10**6):
                deferral_1 = "Price and volume deferred 1 day"
            elif 5 * (10**6) < trade_size_gbp <= 25 * (10**6):
                deferral_1 = "Price and volume deferred 2 weeks"
            elif trade_size_gbp > 25 * (10**6):
                deferral_1 = "Price and volume deferred 3 months"
        elif rating == 'HY':
            if trade_size_gbp <= 1 * (10**6):
                deferral_1 = "Price and volume in real time"
            elif 1 * (10**6) < trade_size_gbp <= 2.5 * (10**6):
                deferral_1 = "Price and volume deferred 1 day"
            elif 2.5 * (10**6) < trade_size_gbp <= 10 * (10**6):
                deferral_1 = "Price and volume deferred 2 weeks"
            elif trade_size_gbp > 10 * (10**6):
                deferral_1 = "Price and volume deferred 3 months"
    elif (issue_size_gbp < 500 * (10**6)) or (issue_size_gbp >= 500 * (10**6) and issue_currency not in ['EUR', 'USD', 'GBP']):
        if trade_size_gbp <= 0.5 * (10**6):
            deferral_1 = "Price and volume in real time"
        elif 0.5 * (10**6) < trade_size_gbp <= 2.5 * (10**6):
            deferral_1 = "Price and volume deferred 1 day"
        elif 2.5 * (10**6) < trade_size_gbp <= 10 * (10**6):
            deferral_1 = "Price and volume deferred 2 weeks"
        elif trade_size_gbp > 10 * (10**6):
            deferral_1 = "Price and volume deferred 3 months"
    else:
        deferral_1 = "Enter all fields or contact ICMA"

    # Calculate the second output (based on EUR logic)
    if trade_size_eur < 1 * (10**6):
        deferral_2 = "Price and volume in real time (corporate, convertible and other bonds)"
    elif issue_size_eur >= 500 * (10**6) and 1 * (10**6) <= trade_size_eur < 5 * (10**6):
        deferral_2 = "Price and volume deferred 15 minutes (corporate, convertible and other bonds)"
    elif issue_size_eur >= 500 * (10**6) and 5 * (10**6) <= trade_size_eur < 15 * (10**6):
        deferral_2 = "EOD price deferral and 1 week volume deferral (corporate, convertible and other bonds)"
    elif issue_size_eur < 500 * (10**6) and 1 * (10**6) <= trade_size_eur < 5 * (10**6):
        deferral_2 = "Price and volume deferred EOD (corporate, convertible and other bonds)"
    elif issue_size_eur < 500 * (10**6) and 5 * (10**6) <= trade_size_eur < 15 * (10**6):
        deferral_2 = "EOD price deferral and 2 week volume deferral (corporate, convertible and other bonds)"
    elif trade_size_eur >= 15 * (10**6):
        deferral_2 = "Price and volume deferred 4 weeks (corporate, convertible and other bonds)"
    else:
        deferral_2 = "Enter all fields or contact ICMA"
        
        
    # Calculate the 3rd output (based on EUR logic)
    if trade_size_eur < 5 * (10**6):
        deferral_3 = "Price and volume in real time (covered bonds only)"
    elif issue_size_eur >= 250 * (10**6) and 5 * (10**6) <= trade_size_eur < 15 * (10**6):
        deferral_3 = "Price and volume deferred 15 minutes (covered bonds only)"
    elif issue_size_eur >= 250 * (10**6) and 15 * (10**6) <= trade_size_eur < 50 * (10**6):
        deferral_3 = "EOD price deferral and 1 week volume deferral (covered bonds only)"
    elif issue_size_eur < 250 * (10**6) and 5 * (10**6) <= trade_size_eur < 15 * (10**6):
        deferral_3 = "Price and volume deferred EOD (covered bonds only)"
    elif issue_size_eur < 250 * (10**6) and 15 * (10**6) <= trade_size_eur < 50 * (10**6):
        deferral_3 = "EOD price deferral and 2 week volume deferral (covered bonds only)"
    elif trade_size_eur >= 50 * (10**6):
        deferral_3 = "Price and volume deferred 4 weeks (covered bonds only)"
    else:
        deferral_3 = "Enter all fields or contact ICMA"
    
    
    
    deferral_1_with_flag = html.Div([
        html.Img(src="https://upload.wikimedia.org/wikipedia/commons/8/83/Flag_of_the_United_Kingdom_%283-5%29.svg", style={'height': '20px', 'width': 'auto'}),
        html.Span(f" {deferral_1}")
    ])  # UK flag for the first output

    deferral_2_with_flag = html.Div([
        html.Img(src="https://upload.wikimedia.org/wikipedia/commons/b/b7/Flag_of_Europe.svg", style={'height': '20px', 'width': 'auto'}),
        html.Span(f" {deferral_2}")
    ])  # EU flag for the second output

    deferral_3_with_flag = html.Div([
        html.Img(src="https://upload.wikimedia.org/wikipedia/commons/b/b7/Flag_of_Europe.svg", style={'height': '20px', 'width': 'auto'}),
        html.Span(f" {deferral_3}")
    ])  # EU flag for the third output

    # Return all three outputs
    return deferral_1_with_flag, deferral_2_with_flag, deferral_3_with_flag





    # Return all three outputs
    return deferral_1_with_flag, deferral_2_with_flag, deferral_3_with_flag





# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)


