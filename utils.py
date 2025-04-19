import streamlit as st


def plotly_chart_no_controls(fig, **kwargs):
    fig.update_layout(
        dragmode=False,
        xaxis_fixedrange=True,
        yaxis_fixedrange=True
    )
    return st.plotly_chart(fig, config={"displayModeBar": False}, **kwargs)
