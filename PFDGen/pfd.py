import streamlit as st
import graphviz
from instructions import instructions

def main():
    st.title("Advanced Process Flow Diagram Generator")

    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Home", "Instructions"])

    if page == "Instructions":
        instructions()
    else:
        # Sidebar inputs for role definitions
        st.sidebar.header("Define Roles")
        num_roles = st.sidebar.number_input("Number of Roles", min_value=1, max_value=10, value=3, step=1)

        roles = {}
        for i in range(num_roles):
            role_name = st.sidebar.text_input(f"Role {i+1} Name", f"Role {i+1}")
            role_color = st.sidebar.color_picker(f"Role {i+1} Color", "#ff0000", key=f"role_color_{i}")
            role_shape = st.sidebar.selectbox(f"Role {i+1} Shape", ["ellipse", "box", "diamond", "circle", "hexagon"], key=f"role_shape_{i}")
            roles[role_name] = {"color": role_color, "shape": role_shape}

        # Sidebar inputs for process flow
        st.sidebar.header("Define Your Process")
        num_steps = st.sidebar.number_input("Number of Main Steps", min_value=2, max_value=10, value=3, step=1)

        process_steps = []
        for i in range(num_steps):
            step = st.sidebar.text_input(f"Main Step {i+1} Name", f"Step {i+1}")
            role = st.sidebar.selectbox(f"Main Step {i+1} Role", list(roles.keys()), key=f"role_{i}")
            orientation = st.sidebar.selectbox(f"Orientation to Next Step", ["left to right", "top to bottom", "bottom to top", "right to left"], key=f"orientation_{i}")
            num_sub_steps = st.sidebar.number_input(f"Number of Sub-Steps under Main Step {i+1}", min_value=0, max_value=5, value=0, step=1, key=f"num_sub_{i}")
            sub_steps = []
            for j in range(num_sub_steps):
                sub_step = st.sidebar.text_input(f"Sub-Step {j+1} under Main Step {i+1} Name", f"Sub-Step {i+1}.{j+1}", key=f"sub_step_{i}_{j}")
                sub_role = st.sidebar.selectbox(f"Sub-Step {j+1} Role", list(roles.keys()), key=f"sub_role_{i}_{j}")
                sub_steps.append((sub_step, sub_role))
            
            process_steps.append((step, role, orientation, sub_steps))

        # Create a Graphviz graph object
        dot = graphviz.Digraph()

        # Add nodes and edges to the graph
        for i, (step_name, role, orientation, sub_steps) in enumerate(process_steps):
            role_attrs = roles[role]
            dot.node(f'Step{i+1}', step_name, color=role_attrs["color"], shape=role_attrs["shape"], style="filled", fillcolor=role_attrs["color"])
            if i > 0:
                if orientation == "left to right":
                    dot.edge(f'Step{i}', f'Step{i+1}', dir="forward")
                elif orientation == "top to bottom":
                    dot.edge(f'Step{i}', f'Step{i+1}', dir="forward", constraint="false")
                elif orientation == "bottom to top":
                    dot.edge(f'Step{i+1}', f'Step{i}', dir="forward", constraint="false")
                elif orientation == "right to left":
                    dot.edge(f'Step{i+1}', f'Step{i}', dir="forward")
            
            for j, (sub_step_name, sub_role) in enumerate(sub_steps):
                sub_role_attrs = roles[sub_role]
                dot.node(f'Step{i+1}.{j+1}', sub_step_name, color=sub_role_attrs["color"], shape=sub_role_attrs["shape"], style="filled", fillcolor=sub_role_attrs["color"])
                dot.edge(f'Step{i+1}', f'Step{i+1}.{j+1}', dir="forward")

        # Render the Graphviz graph
        st.subheader("Generated Process Flow Diagram")
        st.graphviz_chart(dot)

        # Export functionality
        st.sidebar.header("Export Diagram")
        if st.sidebar.button("Export as PNG"):
            dot.format = 'png'
            dot.render('process_flow_diagram', view=True)
            st.sidebar.write("Diagram exported as process_flow_diagram.png")

if __name__ == "__main__":
    main()
