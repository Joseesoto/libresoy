for s in spreads_info:
    st.markdown(f"""
        <div style='background-color:#f0f4f8; padding:16px; margin-top:30px; border-radius:10px; box-shadow:0 2px 6px rgba(0,0,0,0.05); font-family:Arial, sans-serif;'>
            <div style='margin-bottom:12px;'>
                <div style='font-size:18px; font-weight:bold;'>Par: {s["pair"]}</div>
                <div style='font-size:16px;'>Spread: <span style='color:#007bff; font-weight:600;'>{s["spread"]:.2f}%</span></div>
            </div>

            <div style='display:flex; flex-direction:column; gap:10px;'>
                <a href="{s["buy_link"]}" target="_blank" style='background-color:#b30000; color:white; padding:10px 14px; border-radius:6px; text-align:center; text-decoration:none; font-weight:600;'>
                    🟢 Comprar en {s["buy_exchange"]} @ {s["buy_price"]:.{decimales}f}
                </a>
                <a href="{s["sell_link"]}" target="_blank" style='background-color:#006400; color:white; padding:10px 14px; border-radius:6px; text-align:center; text-decoration:none; font-weight:600;'>
                    🔴 Vender en {s["sell_exchange"]} @ {s["sell_price"]:.{decimales}f}
                </a>
            </div>

            <div style='margin-top:16px; overflow-x:auto;'>
    """, unsafe_allow_html=True)

    # Estilos condicionales en tabla
    best_ask = s["group"]["ask"].min()
    best_bid = s["group"]["bid"].max()

    display_df = s["group"].copy()
    display_df.columns = ["exchange", "bid", "ask", "link"]

    display_df["bid"] = display_df["bid"].apply(
        lambda x: f"<span style='color:#006400; font-weight:bold'>{x:.{decimales}f}</span>" if x == best_bid else f"{x:.{decimales}f}"
    )
    display_df["ask"] = display_df["ask"].apply(
        lambda x: f"<span style='color:#b30000; font-weight:bold'>{x:.{decimales}f}</span>" if x == best_ask else f"{x:.{decimales}f}"
    )

    display_df["exchange"] = display_df.apply(
        lambda row: f"<a href='{row['link']}' target='_blank'>{row['exchange']}</a>", axis=1
    )
    display_df = display_df.drop(columns=["link"])

    st.markdown(
        f"""
        <div style='margin-top:0px; max-width: 100%;'>
            {display_df.to_html(escape=False, index=False, classes="dataframe table table-striped", border=0)}
        </div>
        </div>
        """,
        unsafe_allow_html=True
    )
