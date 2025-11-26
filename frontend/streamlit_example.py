import streamlit as st
import time
import pandas as pd
import numpy as np
from threading import Thread
from windows_stubs.backend import system_engine, all_measurements
from frontend.frontend import tab_1, tab_2, tab_3

from streamlit_autorefresh import st_autorefresh


import matplotlib.pyplot as plt


if "thread_started" not in st.session_state:
    st.session_state.thread_started = False

# ----------------------------
# Background Data Function
# ----------------------------
def background_function():
    system_engine.run_test()
    while system_engine.test_running():
        measurements = system_engine.get_measurements()

        # Store new measurement
        all_measurements.append(measurements)
        # Sleep between measurements
        time.sleep(1)


# ----------------------------
# Streamlit UI
# ----------------------------
st.title("Cyclic Data Visualization with Background Thread")
st.write("Data updates automatically every time Streamlit reruns.")

# Start background thread
if st.button("Start test"):
    if not st.session_state.thread_started:
        system_engine.state = "RUNNING"
        thread = Thread(target=background_function, daemon=True)
        thread.start()

        st.session_state.thread_started = True
        st.success("Background function started!")
    else:
        system_engine.state = "STOPED"
        st.session_state.thread_started = False
        st.info("Background function stoped!")


# ----------------------------
# Tabs (Multiple Charts)
# ----------------------------
tab1, tab2, tab3 = st.tabs(["Chart A", "Chart B", "Raw Data"])

# Convert to DataFrame
df = pd.DataFrame(all_measurements)

with tab1:
    if not df.empty:
        st.title("Drive temperatures")
        fig, axes = plt.subplots(2, 4, figsize=(18, 10))

        for i, ax in enumerate(axes.flatten()):
            ax.plot(df.index, df.iloc[:, i])
            ax.set_title(df.columns[i])
            ax.grid(True)
        plt.tight_layout()
        st.pyplot(fig)
    else:
        st.write("Waiting for data...")
        
with tab2:
    tab_2(df)

with tab3:
    tab_3(df)

st.session_state

# Run the autorefresh about every 2000 milliseconds (2 seconds)
count = st_autorefresh(interval=2000, key="fizzbuzzcounter")
