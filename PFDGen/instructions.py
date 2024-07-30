import streamlit as st

def instructions():
    st.title("Instructions for Process Flow Diagram Generator")
    
    st.header("Step-by-Step Guide")
    
    st.subheader("1. Define Roles")
    st.write("""
    - Go to the sidebar and enter the number of roles you want to define.
    - For each role, provide a name, select a color, and choose a shape.
    - Click 'Add Role' to save each role.
    """)

    st.subheader("2. Define Process Flow")
    st.write("""
    - Enter the number of main steps in your process.
    - For each main step, provide a name, select a role from the dropdown, and choose the orientation of the arrow to the next step.
    - Optionally, you can define sub-steps for each main step by providing their names and selecting roles for them.
    """)

    st.subheader("3. Generate and View Diagram")
    st.write("""
    - Once you have defined all roles and steps, the process flow diagram will be automatically generated and displayed.
    - You can see the diagram update in real-time as you make changes.
    """)

    st.subheader("4. Export Diagram")
    st.write("""
    - If you wish to save the diagram, enter a file name and click the 'Export as PNG' button in the sidebar.
    - The diagram will be saved as a PNG file with the provided file name.
    """)

if __name__ == "__main__":
    instructions()
