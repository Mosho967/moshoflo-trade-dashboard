def classify_trade(volume: float) -> str:
   
    # if volume is less than 1000, classify as low risk
    if volume < 1000:
        return "LOW RISK"
    
    # If volume is between 1000 and 10000, classify as medium risk
    elif volume < 10000:
        return "MEDIUM RISK"
    else:
        return "HIGH RISK"