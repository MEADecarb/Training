import streamlit as st
import graphviz

def main():
    st.title("Advanced Process Flow Diagram Generator")

    # Sidebar inputs for process flow
    st.sidebar.header("Define Your Process")
    num_steps = st.sidebar.number_input("Number of Main Steps", min_value=2, max_value=10, value=3, step=1)

    process_steps = []
    for i in range(num_steps):
        step = st.sidebar.text_input(f"Main Step {i+1} Name", f"Step {i+1}")
        color = st.sidebar.color_picker(f"Main Step {i+1} Color", "#ff0000")
        shape = st.sidebar.selectbox(f"Main Step {i+1} Shape", ["ellipse", "box", "diamond", "circle", "hexagon"], key=f"shape_{i}")
        
        num_sub_steps = st.sidebar.number_input(f"Number of Sub-Steps under Main Step {i+1}", min_value=0, max_value=5, value=0, step=1, key=f"num_sub_{i}")
        sub_steps = []
        for j in range(num_sub_steps):
            sub_step = st.sidebar.text_input(f"Sub-Step {j+1} under Main Step {i+1} Name", f"Sub-Step {i+1}.{j+1}", key=f"sub_step_{i}_{j}")
            sub_color = st.sidebar.color_picker(f"Sub-Step {j+1} under Main Step {i+1} Color", "#00ff00", key=f"sub_color_{i}_{j}")
            sub_shape = st.sidebar.selectbox(f"Sub-Step {j+1} under Main Step {i+1} Shape", ["ellipse", "box", "diamond", "circle", "hexagon"], key=f"sub_shape_{i}_{j}")
            sub_steps.append((sub_step, sub_color, sub_shape))
        
        process_steps.append((step, color, shape, sub_steps))

    # Create a Graphviz graph object
    dot = graphviz.Digraph()

    # Add nodes and edges to the graph
    for i, (step_name, step_color, step_shape, sub_steps) in enumerate(process_steps):
        dot.node(f'Step{i+1}', step_name, color=step_color, shape=step_shape, style="filled", fillcolor=step_color)
        if i > 0:
            dot.edge(f'Step{i}', f'Step{i+1}')
        
        for j, (sub_step_name, sub_step_color, sub_step_shape) in enumerate(sub_steps):
            dot.node(f'Step{i+1}.{j+1}', sub_step_name, color=sub_step_color, shape=sub_step_shape, style="filled", fillcolor=sub_step_color)
            dot.edge(f'Step{i+1}', f'Step{i+1}.{j+1}')

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
