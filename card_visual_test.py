card_values = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'J', 'Q', 'K', 'A']
card_symbol = ['♠', '♥', '♦', '♣']

for symbol in card_symbol:
    for value in card_values:
        print(f"""
        ┌─────────┐
        │{value}        │
        │{symbol}        │
        │         │
        │    {symbol}    │
        │         │
        │        {symbol}│
        │        {value}│
        └─────────┘
              """)

for symbol_idx in range(1, len(card_symbol)):
    for value_idx in range(1, len(card_values)):
        symbol = card_symbol[symbol_idx]
        value = card_values[value_idx]

        previous_value = card_values[value_idx - 1]

        print(f'''
        ┌──┌─────────┐
        │{symbol} │{symbol}        │
        │{previous_value} │{value}        │
        │  │         │
        │  │    {symbol}    │
        │  │         │
        │  │        {symbol}│
        │  │        {value}│
        └──└─────────┘
        ''')
