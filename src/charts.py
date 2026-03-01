import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

PALETTE = px.colors.qualitative.Set2
BLINKIT_YELLOW = "#F9C440"
BLINKIT_GREEN = "#1CA454"
BACKGROUND = "#0E1117"
SURFACE = "#1E2130"
TEXT_COLOR = "#E8EAF0"

CHART_DEFAULTS = {
    "paper_bgcolor": BACKGROUND,
    "plot_bgcolor": SURFACE,
    "font": {"color": TEXT_COLOR, "family": "Inter, sans-serif"},
    "margin": {"t": 40, "b": 20, "l": 20, "r": 20},
}


def _apply_defaults(fig: go.Figure) -> go.Figure:
    fig.update_layout(**CHART_DEFAULTS)
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=True, gridcolor="#2D3144", zeroline=False)
    return fig


def donut_fat_content(data: pd.DataFrame) -> go.Figure:
    fig = px.pie(
        data,
        names="fat_content",
        values="total_sales",
        hole=0.55,
        color_discrete_sequence=[BLINKIT_YELLOW, BLINKIT_GREEN],
        title="Sales by Fat Content",
    )
    fig.update_traces(textinfo="percent+label", pull=[0.03, 0])
    return _apply_defaults(fig)


def bar_item_type(data: pd.DataFrame) -> go.Figure:
    fig = px.bar(
        data,
        x="total_sales",
        y="category",
        orientation="h",
        color="total_sales",
        color_continuous_scale=[[0, SURFACE], [1, BLINKIT_YELLOW]],
        title="Sales by Item Type",
        labels={"total_sales": "Total Sales ($)", "category": ""},
    )
    fig.update_coloraxes(showscale=False)
    return _apply_defaults(fig)


def line_establishment_trend(data: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=data["year"],
            y=data["total_sales"],
            mode="lines+markers",
            name="Total Sales",
            line={"color": BLINKIT_YELLOW, "width": 2.5},
            marker={"size": 7, "color": BLINKIT_YELLOW},
            fill="tozeroy",
            fillcolor="rgba(249,196,64,0.12)",
        )
    )
    fig.update_layout(title="Outlet Establishment Trend vs Sales", xaxis_title="Year", yaxis_title="Total Sales ($)")
    return _apply_defaults(fig)


def donut_outlet_size(data: pd.DataFrame) -> go.Figure:
    fig = px.pie(
        data,
        names="size",
        values="total_sales",
        hole=0.55,
        color_discrete_sequence=PALETTE,
        title="Sales by Outlet Size",
    )
    fig.update_traces(textinfo="percent+label", pull=[0.03, 0, 0])
    return _apply_defaults(fig)


def bar_location_type(data: pd.DataFrame) -> go.Figure:
    fig = px.bar(
        data,
        x="location",
        y="total_sales",
        color="location",
        color_discrete_sequence=PALETTE,
        title="Sales by Location Tier",
        labels={"total_sales": "Total Sales ($)", "location": ""},
    )
    fig.update_layout(showlegend=False)
    return _apply_defaults(fig)


def grouped_bar_fat_location(data: pd.DataFrame) -> go.Figure:
    fig = px.bar(
        data,
        x="location",
        y="total_sales",
        color="fat_content",
        barmode="group",
        color_discrete_sequence=[BLINKIT_YELLOW, BLINKIT_GREEN],
        title="Fat Content Sales by Location",
        labels={"total_sales": "Total Sales ($)", "location": "", "fat_content": "Fat Content"},
    )
    return _apply_defaults(fig)


def bar_outlet_age_band(data: pd.DataFrame) -> go.Figure:
    fig = px.bar(
        data,
        x="age_band",
        y="total_sales",
        color="total_sales",
        color_continuous_scale=[[0, SURFACE], [1, BLINKIT_GREEN]],
        title="Sales by Outlet Age",
        labels={"total_sales": "Total Sales ($)", "age_band": "Outlet Age Band"},
    )
    fig.update_coloraxes(showscale=False)
    return _apply_defaults(fig)


def bar_top_items(data: pd.DataFrame) -> go.Figure:
    fig = px.bar(
        data.sort_values("total_sales"),
        x="total_sales",
        y="item_identifier",
        color="item_type",
        orientation="h",
        color_discrete_sequence=PALETTE,
        title="Top 10 Items by Sales",
        labels={"total_sales": "Total Sales ($)", "item_identifier": "", "item_type": "Category"},
    )
    return _apply_defaults(fig)


def histogram_rating(data: pd.DataFrame) -> go.Figure:
    fig = px.bar(
        data,
        x="rating",
        y="count",
        color_discrete_sequence=[BLINKIT_YELLOW],
        title="Rating Distribution",
        labels={"rating": "Rating", "count": "Number of Items"},
    )
    return _apply_defaults(fig)


def outlet_type_table(data: pd.DataFrame) -> go.Figure:
    display = data.copy()
    display["total_sales"] = display["total_sales"].map("${:,.0f}".format)
    display["average_sales"] = display["average_sales"].map("${:,.2f}".format)
    display["average_rating"] = display["average_rating"].map("{:.2f}".format)
    display["average_visibility"] = display["average_visibility"].map("{:.4f}".format)
    display.columns = ["Outlet Type", "Total Sales", "Item Count", "Avg Sales", "Avg Rating", "Avg Visibility"]

    fig = go.Figure(
        data=[
            go.Table(
                header=dict(
                    values=list(display.columns),
                    fill_color=BLINKIT_YELLOW,
                    font=dict(color="#000", size=12, family="Inter, sans-serif"),
                    align="left",
                    height=32,
                ),
                cells=dict(
                    values=[display[col] for col in display.columns],
                    fill_color=[[SURFACE if i % 2 == 0 else "#252840" for i in range(len(display))]],
                    font=dict(color=TEXT_COLOR, size=11, family="Inter, sans-serif"),
                    align="left",
                    height=28,
                ),
            )
        ]
    )
    fig.update_layout(title="Outlet Type Performance Comparison", **CHART_DEFAULTS)
    return fig
