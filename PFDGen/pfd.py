import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objs as go

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div([
    html.H1("Interactive Process Flow Diagram Generator"),

    # Role Definition
    html.Div([
        html.H3("Define Roles"),
        dcc.Input(id='role-name', type='text', placeholder='Role Name', debounce=True),
        dcc.Input(id='role-color', type='color', placeholder='Role Color', value='#ff0000'),
        dcc.Dropdown(
            id='role-shape',
            options=[
                {'label': 'Ellipse', 'value': 'ellipse'},
                {'label': 'Box', 'value': 'box'},
                {'label': 'Diamond', 'value': 'diamond'},
                {'label': 'Circle', 'value': 'circle'},
                {'label': 'Hexagon', 'value': 'hexagon'}
            ],
            placeholder='Select Shape'
        ),
        html.Button('Add Role', id='add-role', n_clicks=0),
        html.Div(id='role-output'),
    ], style={'margin-bottom': '20px'}),

    # Process Flow Definition
    html.Div([
        html.H3("Define Process Flow"),
        dcc.Input(id='step-name', type='text', placeholder='Step Name', debounce=True),
        dcc.Dropdown(
            id='step-role',
            options=[],
            placeholder='Select Role'
        ),
        dcc.Dropdown(
            id='step-orientation',
            options=[
                {'label': 'Left to Right', 'value': 'LR'},
                {'label': 'Top to Bottom', 'value': 'TB'},
                {'label': 'Bottom to Top', 'value': 'BT'},
                {'label': 'Right to Left', 'value': 'RL'}
            ],
            placeholder='Select Orientation'
        ),
        html.Button('Add Step', id='add-step', n_clicks=0),
        html.Div(id='steps-output')
    ], style={'margin-bottom': '20px'}),

    # Graph Output
    html.Div([
        dcc.Graph(id='process-flow-graph')
    ])
])

# Store roles and steps in memory
roles = []
steps = []

@app.callback(
    Output('role-output', 'children'),
    Input('add-role', 'n_clicks'),
    State('role-name', 'value'),
    State('role-color', 'value'),
    State('role-shape', 'value')
)
def add_role(n_clicks, role_name, role_color, role_shape):
    if n_clicks > 0 and role_name and role_color and role_shape:
        role = {'name': role_name, 'color': role_color, 'shape': role_shape}
        roles.append(role)
        return f"Role {role_name} added with color {role_color} and shape {role_shape}"

@app.callback(
    Output('step-role', 'options'),
    Input('role-output', 'children')
)
def update_role_dropdown(role_output):
    return [{'label': role['name'], 'value': role['name']} for role in roles]

@app.callback(
    Output('steps-output', 'children'),
    Output('process-flow-graph', 'figure'),
    Input('add-step', 'n_clicks'),
    State('step-name', 'value'),
    State('step-role', 'value'),
    State('step-orientation', 'value')
)
def add_step(n_clicks, step_name, step_role, step_orientation):
    if n_clicks > 0 and step_name and step_role and step_orientation:
        step = {'name': step_name, 'role': step_role, 'orientation': step_orientation}
        steps.append(step)

    # Create nodes and edges for the graph
    nodes = []
    edges = []
    positions = {
        'LR': (1, 0),
        'TB': (0, 1),
        'BT': (0, -1),
        'RL': (-1, 0)
    }
    x, y = 0, 0

    for step in steps:
        role = next(role for role in roles if role['name'] == step['role'])
        nodes.append(go.Scatter(
            x=[x], y=[y],
            text=step['name'],
            mode='markers+text',
            marker=dict(size=20, color=role['color'], symbol=role['shape']),
            textposition='bottom center'
        ))
        if len(nodes) > 1:
            prev_x, prev_y = nodes[-2]['x'][0], nodes[-2]['y'][0]
            edge_x = [prev_x, x]
            edge_y = [prev_y, y]
            edges.append(go.Scatter(
                x=edge_x, y=edge_y,
                mode='lines',
                line=dict(color='black')
            ))
        dx, dy = positions[step['orientation']]
        x += dx * 2
        y += dy * 2

    figure = go.Figure(data=nodes + edges)
    figure.update_layout(showlegend=False)

    steps_output = f"Step {step_name} added as {step_role} with orientation {step_orientation}"
    return steps_output, figure

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
