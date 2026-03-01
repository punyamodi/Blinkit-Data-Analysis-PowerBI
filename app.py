import io

import pandas as pd
import streamlit as st

from src import charts, metrics, pipeline

st.set_page_config(
    page_title="Blinkit Sales Analytics",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
        body { font-family: 'Inter', sans-serif; }
        .metric-card {
            background: #1E2130;
            border-radius: 12px;
            padding: 20px 24px;
            border-left: 4px solid #F9C440;
        }
        .metric-label { font-size: 13px; color: #9BA3BA; margin-bottom: 4px; }
        .metric-value { font-size: 28px; font-weight: 700; color: #F9C440; }
        .metric-sub { font-size: 12px; color: #6B7280; margin-top: 4px; }
        .section-header {
            font-size: 15px;
            font-weight: 600;
            color: #E8EAF0;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-bottom: 12px;
        }
        [data-testid="stSidebar"] { background-color: #161824; }
        .stPlotlyChart { border-radius: 8px; overflow: hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def get_data() -> pd.DataFrame:
    return pipeline.load()


df_full = get_data()

with st.sidebar:
    st.markdown("## Filters")

    location_options = sorted(df_full["outlet_location_type"].unique())
    selected_locations = st.multiselect(
        "Location Tier",
        options=location_options,
        default=location_options,
    )

    size_options = sorted(df_full["outlet_size"].unique())
    selected_sizes = st.multiselect(
        "Outlet Size",
        options=size_options,
        default=size_options,
    )

    item_type_options = sorted(df_full["item_type"].unique())
    selected_item_types = st.multiselect(
        "Item Type",
        options=item_type_options,
        default=item_type_options,
    )

    fat_options = sorted(df_full["item_fat_content"].unique())
    selected_fat = st.multiselect(
        "Fat Content",
        options=fat_options,
        default=fat_options,
    )

    outlet_type_options = sorted(df_full["outlet_type"].unique())
    selected_outlet_types = st.multiselect(
        "Outlet Type",
        options=outlet_type_options,
        default=outlet_type_options,
    )

    year_min = int(df_full["outlet_establishment_year"].min())
    year_max = int(df_full["outlet_establishment_year"].max())
    selected_years = st.slider(
        "Establishment Year",
        min_value=year_min,
        max_value=year_max,
        value=(year_min, year_max),
    )

    st.markdown("---")
    st.markdown(
        "<span style='color:#6B7280;font-size:12px'>Blinkit Sales Analytics · 2024</span>",
        unsafe_allow_html=True,
    )

df = df_full[
    df_full["outlet_location_type"].isin(selected_locations)
    & df_full["outlet_size"].isin(selected_sizes)
    & df_full["item_type"].isin(selected_item_types)
    & df_full["item_fat_content"].isin(selected_fat)
    & df_full["outlet_type"].isin(selected_outlet_types)
    & df_full["outlet_establishment_year"].between(selected_years[0], selected_years[1])
]

st.title("Blinkit Sales Analytics Dashboard")
st.markdown(
    f"Showing **{len(df):,}** records · "
    f"Filtered from {len(df_full):,} total",
    unsafe_allow_html=False,
)

st.markdown("---")

kpi_data = metrics.kpis(df)
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(
        f"""<div class="metric-card">
            <div class="metric-label">Total Sales</div>
            <div class="metric-value">${kpi_data['total_sales']:,.0f}</div>
            <div class="metric-sub">All filtered transactions</div>
        </div>""",
        unsafe_allow_html=True,
    )

with c2:
    st.markdown(
        f"""<div class="metric-card">
            <div class="metric-label">Average Sales</div>
            <div class="metric-value">${kpi_data['average_sales']:,.2f}</div>
            <div class="metric-sub">Per transaction</div>
        </div>""",
        unsafe_allow_html=True,
    )

with c3:
    st.markdown(
        f"""<div class="metric-card">
            <div class="metric-label">Items Sold</div>
            <div class="metric-value">{kpi_data['item_count']:,}</div>
            <div class="metric-sub">Unique transactions</div>
        </div>""",
        unsafe_allow_html=True,
    )

with c4:
    st.markdown(
        f"""<div class="metric-card">
            <div class="metric-label">Average Rating</div>
            <div class="metric-value">{kpi_data['average_rating']:.2f} / 5</div>
            <div class="metric-sub">Customer satisfaction</div>
        </div>""",
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

col_left, col_right = st.columns([1, 2])

with col_left:
    st.plotly_chart(
        charts.donut_fat_content(metrics.sales_by_fat_content(df)),
        use_container_width=True,
    )

with col_right:
    st.plotly_chart(
        charts.bar_item_type(metrics.sales_by_item_type(df)),
        use_container_width=True,
    )

col_a, col_b, col_c = st.columns(3)

with col_a:
    st.plotly_chart(
        charts.donut_outlet_size(metrics.sales_by_outlet_size(df)),
        use_container_width=True,
    )

with col_b:
    st.plotly_chart(
        charts.bar_location_type(metrics.sales_by_location_type(df)),
        use_container_width=True,
    )

with col_c:
    st.plotly_chart(
        charts.grouped_bar_fat_location(metrics.sales_by_fat_and_location(df)),
        use_container_width=True,
    )

st.plotly_chart(
    charts.line_establishment_trend(metrics.outlet_establishment_trend(df)),
    use_container_width=True,
)

col_d, col_e = st.columns(2)

with col_d:
    st.plotly_chart(
        charts.bar_outlet_age_band(metrics.sales_by_outlet_age_band(df)),
        use_container_width=True,
    )

with col_e:
    st.plotly_chart(
        charts.histogram_rating(metrics.rating_distribution(df)),
        use_container_width=True,
    )

st.plotly_chart(
    charts.bar_top_items(metrics.top_items_by_sales(df, n=10)),
    use_container_width=True,
)

st.plotly_chart(
    charts.outlet_type_table(metrics.outlet_type_comparison(df)),
    use_container_width=True,
)

st.markdown("---")
st.markdown("### Export Filtered Data")

csv_buffer = io.StringIO()
df.to_csv(csv_buffer, index=False)
st.download_button(
    label="Download CSV",
    data=csv_buffer.getvalue(),
    file_name="blinkit_filtered_data.csv",
    mime="text/csv",
)
