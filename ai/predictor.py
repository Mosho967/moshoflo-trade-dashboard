def classify_trade(volume: float) -> str:
    if volume > 20000:
        return "HIGH RISK"
    elif volume > 10000:
        return "MODERATE RISK" 
    else:
        return "LOW RISK" 