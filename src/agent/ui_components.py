import streamlit as st
import plotly.express as px
from agent.database_utils import run_query
import sqlparse 
import pandas as pd
import plotly.express as px
from agent.theme_manager import style_plotly_figure

def render_header():
    st.title("📊 EPP SLA Reporter")
    st.markdown("### Natural Language to Business Intelligence")
    st.info("""
    **User Guide:** Type your question in plain English. The AI will generate SQL, 
    fetch data from the versioned registry, and visualize the results. 
    Select multiple models in the sidebar to compare performance.
    """)


def render_result_panel(model_name, model_data):
    """Renders the sub-panel for a specific model's output."""
    with st.container(border=True):
        st.subheader(f"🤖 Model: {model_name}")
        
        if model_data.get("error"):
            st.error(f"API Error: {model_data['error']}")
            return

        raw_sql = model_data.get("sql", "")
        latency = model_data.get("latency", 0)
        
        # Format SQL for UI
        formatted_sql = sqlparse.format(raw_sql, reindent=True, keyword_case='upper')

        st.caption(f"Latency: {latency:.2f}s")
        st.code(formatted_sql, language="sql")

        # Execute Query
        df = run_query(raw_sql)
        
        if isinstance(df, str):
            st.error(f"Execution Error: {df}")
        else:
            tab1, tab2 = st.tabs(["📄 Table", "📈 Chart"])
            with tab1:
                st.dataframe(df, use_container_width=True)
            with tab2:
                # CALLING THE SEPARATE FUNCTION HERE
                render_dynamic_chart(df)


def render_dynamic_chart(df):
    """Refined charting logic that handles Date+Hour, Dates, or Categories."""
    if df.empty:
        st.write("No data available to generate a chart.")
        return

    cols_df = df.columns
    # Identify numeric columns, excluding 'hour' from being treated as a Y-axis value
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    numeric_cols = [c for c in numeric_cols if c.lower() != "hour"]

    # Heuristics to find Time/Date columns
    date_col = next((c for c in cols_df if "date" in c.lower()), None)
    hour_col = next((c for c in cols_df if "hour" in c.lower()), None)

    fig = None

    # SCENARIO 1: Combined Date + Hour
    if date_col and hour_col and numeric_cols:
        try:
            # Create a synthetic datetime for plotting
            df["datetime_idx"] = pd.to_datetime(df[date_col]) + pd.to_timedelta(df[hour_col], unit="h")
            
            fig = px.line(
                df.sort_values("datetime_idx"),
                x="datetime_idx",
                y=numeric_cols[0],
                markers=True,
                template="plotly_dark",
                title=f"{numeric_cols[0]} Trend (Hourly)"
            )
            fig.update_xaxes(tickformat="%b %d, %H:%M")
        except Exception as e:
            st.warning(f"Note: Could not combine date/hour for charting: {e}")

    # SCENARIO 2: Date Only
    elif date_col and numeric_cols:
        fig = px.line(
            df.sort_values(date_col), 
            x=date_col, 
            y=numeric_cols[0], 
            markers=True, 
            template="plotly_dark"
        )

    # SCENARIO 3: Hour Only
    elif hour_col and numeric_cols:
        fig = px.line(
            df.sort_values(hour_col), 
            x=hour_col, 
            y=numeric_cols[0], 
            markers=True, 
            template="plotly_dark"
        )

    # SCENARIO 4: General Category vs Number (Bar Chart)
    elif numeric_cols:
        fig = px.bar(
            df, 
            x=cols_df[0], 
            y=numeric_cols[0], 
            template="plotly_dark"
        )

    # Final Render
    if fig:
        #fig.update_layout(margin=dict(l=10, r=10, t=40, b=10))
        #st.plotly_chart(fig, use_container_width=True)
        # Apply the theme to the plotly object
        fig = style_plotly_figure(fig) 
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("Insufficient numeric data to generate a visualization.")


def render_footer():
    st.markdown("---")
    # Change 'unsafe_allow_name' to 'unsafe_allow_html'
    st.markdown(
        "<center>EPP SLA Reporter v3.0 | BI Engineering 2026</center>", 
        unsafe_allow_html=True
    )
