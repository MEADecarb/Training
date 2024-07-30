import streamlit as st
import graphviz

def main():
    st.title("Advanced Process Flow Diagram Generator")

    # Sidebar inputs for process flow
    st.sidebar.header("Define Your Process")
    num_steps = st.sidebar.number_input("Number of Steps", min_value=2, max_value=10, value=3, step=1)
    process_steps = []
    for i in range(num_steps):
        step = st.sidebar.text_input(f"Step {i+1} Name", f"Step {i+1}")
        color = st.sidebar.color_picker(f"Step {i+1} Color", "#ff0000")
        shape = st.sidebar.selectbox(f"Step {i+1} Shape", ["ellipse", "box", "diamond", "circle", "hexagon"])
        process_steps.append((step, color, shape))

    # Create a Graphviz graph object
    dot = graphviz.Digraph()

    # Add nodes and edges to the graph
    for i in range(num_steps):
        step_name, step_color, step_shape = process_steps[i]
        dot.node(f'Step{i+1}', step_name, color=step_color, shape=step_shape, style="filled", fillcolor=step_color)
        if i > 0:
            dot.edge(f'Step{i}', f'Step{i+1}')

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
