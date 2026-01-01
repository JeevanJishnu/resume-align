# Streamlit Cloud Entry Point
# This is a lightweight wrapper that only loads what's needed for cloud deployment

import streamlit as st
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

# Import the dashboard
try:
    from dashboard import *
except Exception as e:
    st.error(f"Failed to load dashboard: {str(e)}")
    st.stop()
