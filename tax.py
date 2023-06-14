# TAX


info = {
    'eth': {
        'x7r': 6,
        'x7dao': 6,
        'x7100': 2,
        'liq_discount': 25,
        'eco_discount': 10,
        'magister_discount': 25
    },
    'opti': {
        'x7r': 6,
        'x7dao': 6,
        'x7100': 2,
        'liq_discount': 25,
        'eco_discount': 10,
        'magister_discount': 25
    },
    'poly': {
        'x7r': 6,
        'x7dao': 6,
        'x7100': 2,
        'liq_discount': 25,
        'eco_discount': 10,
        'magister_discount': 25
    },
    'arb': {
        'x7r': 6,
        'x7dao': 6,
        'x7100': 2,
        'liq_discount': 25,
        'eco_discount': 10,
        'magister_discount': 25
    },
    'bsc': {
        'x7r': 6,
        'x7dao': 6,
        'x7100': 2,
        'liq_discount': 25,
        'eco_discount': 10,
        'magister_discount': 25
    }
}

def generate_info(network):
    network_info = info.get(network)
    if network_info:
        x7r = network_info['x7r']
        x7dao = network_info['x7dao']
        x7100 = network_info['x7100']
        liq_discount = network_info['liq_discount']
        eco_discount = network_info['eco_discount']
        magister_discount = network_info['magister_discount']
        
        network_info_str = (
            f"*X7 Finance Tax Info ({network.upper()})*\nUse `/tax [chain-name]` for other chains\n\n"
            f"X7R: {x7r}%\nX7DAO: {x7dao}%\n"
            f"X7101-X7105: {x7100}%\n\n"
            f"*Tax with NFTs*\n"
            f"Liquidity Maxi:\n"
            f"X7R: {x7r-(x7r*liq_discount/100)}%\n"
            f"X7DAO: {x7dao-(x7dao*liq_discount/100)}%\n"
            f"X7101-X7105: {x7100-(x7100*liq_discount/100)}%\n\n"
            f"Ecosystem Maxi:\n"
            f"X7R: {x7r-(x7r*eco_discount/100)}%\n"
            f"X7DAO: {x7dao-(x7dao*eco_discount/100)}%\n"
            f"X7101-X7105: {x7100-(x7100*eco_discount/100)}%\n\n"
            f"Magister:\n"
            f"X7R: {x7r-(x7r*magister_discount/100)}%\n"
            f"X7DAO: {x7dao}%\n"
            f"X7101-X7105: {x7100-(x7100*magister_discount/100)}%\n"
        )
        
        return network_info_str
    
    return None
