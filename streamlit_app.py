# streamlit_app.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set up the page
st.set_page_config(page_title="Economics of Adoption Simulator", layout="wide")
sns.set_style("whitegrid")

# App Title and Description
st.title("🌍 Economics of Technology Adoption")
st.markdown("""
This interactive simulator models how **network effects** and **income inequality** together shape the diffusion of technology in a developing economy.
Adjust the sliders to see how different economic conditions change the adoption curve.
""")

# Create a sidebar for user inputs
st.sidebar.header("Control the Economy")

# User Inputs using Sliders
population_size = st.sidebar.slider("Population Size", 500, 5000, 1000)
gini = st.sidebar.slider("Income Inequality (Gini Coefficient)", 0.2, 0.6, 0.45, 0.01)
p = st.sidebar.slider("Strength of Innovation (p)", 0.0, 0.1, 0.02, 0.005)
q = st.sidebar.slider("Strength of Network Effects (q)", 0.1, 0.8, 0.45, 0.01)
income_threshold = st.sidebar.slider("Income Threshold to Adopt", 5000, 30000, 15000, 1000)
time_periods = st.sidebar.slider("Time Periods (Months)", 12, 60, 30)

# Button to run the simulation
if st.sidebar.button("Run Simulation", type="primary"):
    # --- SIMULATION CODE --- 
    np.random.seed(42)  # For reproducible results
    incomes = np.random.pareto(1/gini, population_size) * 20000

    # Model initialization
    can_afford = incomes >= income_threshold
    has_adopted = np.zeros(population_size, dtype=bool)
    initial_adopters = np.random.choice(np.where(can_afford)[0], size=max(10, population_size//100), replace=False)
    has_adopted[initial_adopters] = True
    adoption_timeline = []

    # Run the simulation
    for t in range(time_periods):
        current_adopters = np.sum(has_adopted)
        adoption_timeline.append(current_adopters)
        potential_adopters_idx = np.where(~has_adopted & can_afford)[0]
        for idx in potential_adopters_idx:
            prob_adopt = p + q * (current_adopters / population_size)
            if np.random.rand() < prob_adopt:
                has_adopted[idx] = True

    # --- RESULTS & VISUALIZATION ---
    st.success("Simulation Complete!")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Adoption S-Curve")
        fig1, ax1 = plt.subplots(figsize=(8, 5))
        ax1.plot(adoption_timeline, color='dodgerblue', linewidth=2)
        ax1.axhline(y=np.sum(can_afford), color='crimson', linestyle='--', label='Max Possible Adopters')
        ax1.set_title('Technology Adoption Over Time')
        ax1.set_xlabel('Time (Months)')
        ax1.set_ylabel('Number of Adopters')
        ax1.legend()
        ax1.grid(True)
        st.pyplot(fig1)

    with col2:
        st.subheader("Income Distribution")
        fig2, ax2 = plt.subplots(figsize=(8, 5))
        ax2.hist(incomes, bins=50, color='gold', edgecolor='black', alpha=0.8)
        ax2.axvline(x=income_threshold, color='crimson', linestyle='--', linewidth=2, label='Income Threshold')
        ax2.set_title('Barrier to Adoption')
        ax2.set_xlabel('Income')
        ax2.set_ylabel('Number of People')
        ax2.legend()
        ax2.grid(True)
        st.pyplot(fig2)

    # --- KEY INSIGHTS ---
    st.subheader("📊 Economic Analysis Report")
    total_addressable_market = np.sum(can_afford)
    final_adopters = adoption_timeline[-1]
    market_penetration = (final_adopters / total_addressable_market) * 100 if total_addressable_market > 0 else 0

    insight_container = st.container()
    with insight_container:
        col3, col4, col5 = st.columns(3)
        col3.metric("Total Population", f"{population_size:,}")
        col4.metric("Addressable Market", f"{total_addressable_market:,} ({ (total_addressable_market/population_size)*100:.1f}%)")
        col5.metric("Final Adopters", f"{final_adopters:,}")

        st.info(f"**Market Penetration Rate:** {market_penetration:.1f}%")
        st.caption("This is the percentage of the addressable market that ultimately adopted the technology. Even with strong network effects (q={q}), income inequality prevents full market penetration.".format(q=q))

else:
    # Display this before the first run
    st.info("👆 **Adjust the parameters in the sidebar and click 'Run Simulation' to see the model in action!**")
    st.image("https://images.unsplash.com/photo-1551288049-bebda4e38f71?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80", caption="Economic modelling helps us understand complex realities.")
