"""
Plotting functions for Uniswap V3 trade cost analysis.
"""

import plotly.graph_objects as go
from plotly.subplots import make_subplots


def plot_amount_in_vs_out(df, token_in_symbol, token_out_symbol):
    """
    Plot actual vs ideal output amounts.

    Args:
        df: DataFrame with trade cost analysis results
        token_in_symbol: Symbol of input token
        token_out_symbol: Symbol of output token

    Returns:
        plotly Figure object
    """
    fig = go.Figure()

    # Actual amount out
    fig.add_trace(
        go.Scatter(
            x=df["amount_in"],
            y=df["amount_out"],
            mode="lines+markers",
            name=f"Actual {token_out_symbol} Output",
            line=dict(color="#1f77b4", width=3),
            marker=dict(size=8),
            hovertemplate="<b>Input:</b> %{x:,.0f} "
            + token_in_symbol
            + "<br>"
            + "<b>Actual Output:</b> %{y:.8f} "
            + token_out_symbol
            + "<br>"
            + "<extra></extra>",
        )
    )

    # Ideal amount out (at mid price)
    fig.add_trace(
        go.Scatter(
            x=df["amount_in"],
            y=df["ideal_amount_out"],
            mode="lines+markers",
            name=f"Ideal {token_out_symbol} Output (Mid Price)",
            line=dict(color="#2ca02c", width=2, dash="dash"),
            marker=dict(size=6, symbol="x"),
            hovertemplate="<b>Input:</b> %{x:,.0f} "
            + token_in_symbol
            + "<br>"
            + "<b>Ideal Output:</b> %{y:.8f} "
            + token_out_symbol
            + "<br>"
            + "<extra></extra>",
        )
    )

    fig.update_layout(
        title=f"Uniswap V3: {token_in_symbol} → {token_out_symbol} Trade Size Analysis",
        xaxis=dict(
            title=f"Amount In ({token_in_symbol})",
            type="log",
            tickformat=",.0f",
            tickangle=-45,
            gridcolor="lightgray",
        ),
        yaxis=dict(title=f"Amount Out ({token_out_symbol})", gridcolor="lightgray"),
        template="plotly_white",
        hovermode="closest",
        height=500,
        showlegend=True,
    )

    return fig


def plot_price_impact(df, token_in_symbol, token_out_symbol):
    """
    Plot price impact vs trade size.

    Args:
        df: DataFrame with trade cost analysis results
        token_in_symbol: Symbol of input token
        token_out_symbol: Symbol of output token

    Returns:
        plotly Figure object
    """
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df["amount_in"],
            y=df["price_impact_bps"],
            mode="lines+markers",
            name="Price Impact",
            line=dict(color="#ff7f0e", width=3),
            marker=dict(size=8),
            hovertemplate="<b>Trade Size:</b> %{x:,.0f} "
            + token_in_symbol
            + "<br>"
            + "<b>Price Impact:</b> %{y:.2f} bps (%{customdata:.2f}%)<br>"
            + "<extra></extra>",
            customdata=df["price_impact_pct"],
        )
    )

    fig.update_layout(
        title=f"Price Impact vs Trade Size ({token_in_symbol} → {token_out_symbol})",
        xaxis=dict(
            title=f"Amount In ({token_in_symbol})",
            type="log",
            tickformat=",.0f",
            tickangle=-45,
            gridcolor="lightgray",
        ),
        yaxis=dict(title="Price Impact (basis points)", gridcolor="lightgray"),
        template="plotly_white",
        hovermode="closest",
        height=500,
    )

    return fig


def plot_cost_of_impact(df, token_in_symbol, token_out_symbol):
    """
    Plot cost of price impact (tokens lost due to slippage).

    Args:
        df: DataFrame with trade cost analysis results
        token_in_symbol: Symbol of input token
        token_out_symbol: Symbol of output token

    Returns:
        plotly Figure object
    """
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df["amount_in"],
            y=df["cost_of_impact"],
            mode="lines+markers",
            name=f"Cost in {token_out_symbol}",
            line=dict(color="#d62728", width=3),
            marker=dict(size=8),
            hovertemplate="<b>Trade Size:</b> %{x:,.0f} "
            + token_in_symbol
            + "<br>"
            + "<b>Lost:</b> %{y:.8f} "
            + token_out_symbol
            + "<br>"
            + "<b>Lost ($):</b> $%{customdata:,.2f}<br>"
            + "<extra></extra>",
            customdata=df["cost_of_impact_usd"],
        )
    )

    fig.update_layout(
        title=f"Cost of Price Impact ({token_in_symbol} → {token_out_symbol})",
        xaxis=dict(
            title=f"Amount In ({token_in_symbol})",
            type="log",
            tickformat=",.0f",
            tickangle=-45,
            gridcolor="lightgray",
        ),
        yaxis=dict(title=f"Tokens Lost ({token_out_symbol})", gridcolor="lightgray"),
        template="plotly_white",
        hovermode="closest",
        height=500,
    )

    return fig


def plot_combined_analysis(df, token_in_symbol, token_out_symbol):
    """
    Create a 2x2 grid of plots showing comprehensive trade analysis.

    Args:
        df: DataFrame with trade cost analysis results
        token_in_symbol: Symbol of input token
        token_out_symbol: Symbol of output token

    Returns:
        plotly Figure object

    Plots included:
        - Top-left: Actual vs Ideal output amounts
        - Top-right: Price impact in basis points
        - Bottom-left: Execution prices (exec price, price after trade, mid price before trade)
        - Bottom-right: Gas costs in USD
    """
    fig = make_subplots(
        rows=2,
        cols=2,
        subplot_titles=(
            "Amount Out vs Amount In",
            "Price Impact (bps)",
            f"Execution Price ({token_in_symbol}/{token_out_symbol})",
            "Gas Cost (USD)",
        ),
        specs=[
            [{"secondary_y": False}, {"secondary_y": False}],
            [{"secondary_y": False}, {"secondary_y": False}],
        ],
    )

    # Actual Amount Out
    fig.add_trace(
        go.Scatter(
            x=df["amount_in"],
            y=df["amount_out"],
            mode="lines+markers",
            name="Actual Output",
            line=dict(color="#1f77b4", width=2),
            legendgroup="output",
        ),
        row=1,
        col=1,
    )

    # Ideal Amount Out
    fig.add_trace(
        go.Scatter(
            x=df["amount_in"],
            y=df["ideal_amount_out"],
            mode="lines+markers",
            name="Ideal Output",
            line=dict(color="#2ca02c", width=2, dash="dash"),
            marker=dict(size=6, symbol="x"),
            legendgroup="output",
        ),
        row=1,
        col=1,
    )

    # Price Impact
    fig.add_trace(
        go.Scatter(
            x=df["amount_in"],
            y=df["price_impact_bps"],
            mode="lines+markers",
            name="Price Impact",
            line=dict(color="#ff7f0e", width=2),
        ),
        row=1,
        col=2,
    )

    # Execution Price (inverted to show token_in per token_out)
    fig.add_trace(
        go.Scatter(
            x=df["amount_in"],
            y=df["exec_price_inv"],
            mode="lines+markers",
            name="Exec Price",
            line=dict(color="#d62728", width=2),
        ),
        row=2,
        col=1,
    )

    # Add price after trade line (inverted)
    fig.add_trace(
        go.Scatter(
            x=df["amount_in"],
            y=df["price_after_inv"],
            mode="lines+markers",
            name="Price After",
            line=dict(color="#9467bd", width=2, dash="dot"),
            marker=dict(size=6, symbol="diamond"),
        ),
        row=2,
        col=1,
    )

    # Add mid price reference line (inverted)
    fig.add_trace(
        go.Scatter(
            x=df["amount_in"],
            y=df["mid_price_inv"],
            mode="lines",
            name="Mid Price (Before)",
            line=dict(color="#2ca02c", width=1, dash="dash"),
        ),
        row=2,
        col=1,
    )

    # Gas Cost in USD
    fig.add_trace(
        go.Scatter(
            x=df["amount_in"],
            y=df["gas_cost_usd"],
            mode="lines+markers",
            name="Gas Cost",
            line=dict(color="#9467bd", width=2),
            hovertemplate="<b>Trade Size:</b> %{x:,.0f} "
            + token_in_symbol
            + "<br>"
            + "<b>Gas Cost:</b> $%{y:.2f}<br>"
            + "<extra></extra>",
        ),
        row=2,
        col=2,
    )

    # Update xaxis properties
    fig.update_xaxes(
        title_text=f"{token_in_symbol} Input",
        type="log",
        tickformat=",.0f",
        tickangle=-45,
        row=1,
        col=1,
    )
    fig.update_xaxes(
        title_text=f"{token_in_symbol} Input",
        type="log",
        tickformat=",.0f",
        tickangle=-45,
        row=1,
        col=2,
    )
    fig.update_xaxes(
        title_text=f"{token_in_symbol} Input",
        type="log",
        tickformat=",.0f",
        tickangle=-45,
        row=2,
        col=1,
    )
    fig.update_xaxes(
        title_text=f"{token_in_symbol} Input",
        type="log",
        tickformat=",.0f",
        tickangle=-45,
        row=2,
        col=2,
    )

    # Update yaxis properties
    fig.update_yaxes(title_text=f"{token_out_symbol} Output", row=1, col=1)
    fig.update_yaxes(title_text="bps", row=1, col=2)
    fig.update_yaxes(title_text=f"{token_in_symbol}/{token_out_symbol}", row=2, col=1)
    fig.update_yaxes(title_text="Gas Cost (USD)", row=2, col=2)

    fig.update_layout(
        title_text=f"Comprehensive Trade Analysis: {token_in_symbol} → {token_out_symbol}",
        showlegend=True,
        height=800,
        template="plotly_white",
    )

    return fig


def print_summary_stats(df, token_in_symbol, token_out_symbol, pool_address, fee):
    """
    Print summary statistics for trade cost analysis.

    Args:
        df: DataFrame with trade cost analysis results
        token_in_symbol: Symbol of input token
        token_out_symbol: Symbol of output token
        pool_address: Address of the Uniswap V3 pool
        fee: Fee tier in basis points
    """
    print(f"Trade Cost Analysis Summary: {token_in_symbol} → {token_out_symbol}")
    print("=" * 60)
    print(f"\nPool: {pool_address}")
    print(f"Fee Tier: {fee / 10000}%")
    print(f"ETH Price: ${df['eth_price_usd'].iloc[0]:,.2f}")
    print(
        f"\nTrade Size Range: ${df['amount_in'].min():,.0f} - ${df['amount_in'].max():,.0f}"
    )
    print(f"\nPrice Impact:")
    print(
        f"  Min: {df['price_impact_bps'].min():.2f} bps ({df['price_impact_pct'].min():.2f}%)"
    )
    print(
        f"  Max: {df['price_impact_bps'].max():.2f} bps ({df['price_impact_pct'].max():.2f}%)"
    )
    print(
        f"  Mean: {df['price_impact_bps'].mean():.2f} bps ({df['price_impact_pct'].mean():.2f}%)"
    )
    print(f"\nExecution Price:")
    print(f"  Min: {df['exec_price'].min():.10f} {token_out_symbol}/{token_in_symbol}")
    print(f"  Max: {df['exec_price'].max():.10f} {token_out_symbol}/{token_in_symbol}")
    print(
        f"  Mid Price: {df['mid_price'].iloc[0]:.10f} {token_out_symbol}/{token_in_symbol}"
    )
    print(
        f"  (Inverted) Min: {df['exec_price_inv'].min():.2f} {token_in_symbol}/{token_out_symbol}"
    )
    print(
        f"  (Inverted) Max: {df['exec_price_inv'].max():.2f} {token_in_symbol}/{token_out_symbol}"
    )
    print(
        f"  (Inverted) Mid Price: {df['mid_price_inv'].iloc[0]:.2f} {token_in_symbol}/{token_out_symbol}"
    )
    print(f"\nCost of Impact:")
    print(f"  Total tokens lost: {df['cost_of_impact'].sum():.8f} {token_out_symbol}")
    print(f"  Total USD lost: ${df['cost_of_impact_usd'].sum():,.2f}")
    print(f"  Average cost per trade: ${df['cost_of_impact_usd'].mean():,.2f}")
    print(f"\nGas Costs:")
    print(f"  Min: {df['gas_estimate'].min():,} gas (${df['gas_cost_usd'].min():.2f})")
    print(f"  Max: {df['gas_estimate'].max():,} gas (${df['gas_cost_usd'].max():.2f})")
    print(
        f"  Mean: {df['gas_estimate'].mean():,.0f} gas (${df['gas_cost_usd'].mean():.2f})"
    )
    print(f"  Total gas cost: ${df['gas_cost_usd'].sum():.2f}")
