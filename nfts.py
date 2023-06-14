# NFTS
import api
import ca


prices = {
    "eth": {
        "eco": "0.3 ETH - 500 Supply",
        "liq": "0.75 ETH - 250 Supply",
        "dex": "1.5 ETH - 150 Supply",
        "borrow": "2 ETH - 100 Supply",
        "magister": "50 ETH - 49 Supply",
    },
    "arb": {
        "eco": "0.3 ETH - 500 Supply",
        "liq": "0.75 ETH - 250 Supply",
        "dex": "1.5 ETH - 150 Supply",
        "borrow": "2 ETH - 100 Supply",
        "magister": "50 ETH - 49 Supply",
    },
    "opti": {
        "eco": "0.3 ETH - 500 Supply",
        "liq": "0.75 ETH - 250 Supply",
        "dex": "1.5 ETH - 150 Supply",
        "borrow": "2 ETH - 100 Supply",
        "magister": "50 ETH - 49 Supply",
    },
    "bsc": {
        "eco": "1.5 BNB - 500 Supply",
        "liq": "3.75 BNB - 250 Supply",
        "dex": "7.5 BNB - 150 Supply",
        "borrow": "10 BNB - 100 Supply",
        "magister": "150 BNB - 49 Supply",
    },
    "poly": {
        "eco": "390 MATIC - 500 Supply",
        "liq": "975 MATIC - 250 Supply",
        "dex": "1950 MATIC - 150 Supply",
        "borrow": "2600 MATIC - 100 Supply",
        "magister": "45000 MATIC - 49 Supply",
    },
}


counts = {
    "eth": {
        "eco": int(api.get_nft_holder_count(ca.eco, "?chain=eth-main")) or 0,
        "liq": int(api.get_nft_holder_count(ca.liq, "?chain=eth-main")) or 0,
        "dex": int(api.get_nft_holder_count(ca.dex, "?chain=eth-main")) or 0,
        "borrow": int(api.get_nft_holder_count(ca.borrow, "?chain=eth-main")) or 0,
        "magister": int(api.get_nft_holder_count(ca.magister, "?chain=eth-main")) or 0
    },
    "arb": {
        "eco": int(api.get_nft_holder_count(ca.eco, "?chain=arbitrum-main")) or 0,
        "liq": int(api.get_nft_holder_count(ca.liq, "?chain=arbitrum-main")) or 0,
        "dex": int(api.get_nft_holder_count(ca.dex, "?chain=arbitrum-main")) or 0,
        "borrow": int(api.get_nft_holder_count(ca.borrow, "?chain=arbitrum-main")) or 0,
        "magister": int(api.get_nft_holder_count(ca.magister, "?chain=arbitrum-main")) or 0
    },
    "opti": {
        "eco": int(api.get_nft_holder_count(ca.eco, "?chain=optimism-main")) or 0,
        "borrow": int(api.get_nft_holder_count(ca.borrow, "?chain=optimism-main")) or 0,
        "dex" : int(api.get_nft_holder_count(ca.dex, "?chain=optimism-main")) or 0,
        "liq": int(api.get_nft_holder_count(ca.liq, "?chain=optimism-main")) or 0,
        "magister": int(api.get_nft_holder_count(ca.magister, "?chain=optimism-main")) or 0
    },
    "poly": {
        "eco": int(api.get_nft_holder_count(ca.eco, "?chain=poly-main")) or 0,
        "borrow": int(api.get_nft_holder_count(ca.borrow, "?chain=poly-main")) or 0,
        "dex": int(api.get_nft_holder_count(ca.dex, "?chain=poly-main")) or 0,
        "liq": int(api.get_nft_holder_count(ca.liq, "?chain=poly-main")) or 0,
        "magister": int(api.get_nft_holder_count(ca.magister, "?chain=poly-main")) or 0
    },
    "bsc": {
        "eco": 0,
        "borrow": 0,
        "dex": 0,
        "liq": 0,
        "magister": 0
    }
}


discount = {
    "eco": {
        "x7100": 25,
        "x7R": 10,
        "x7DAO": 10,
    },
    "liq": {
        "x7100": 50,
        "x7R": 25,
        "x7DAO": 15,
    },
    "dex": {
        "LP Fee discounts while trading on Xchange"
    },
    "borrow": {
        "Fee discounts for borrowing funds for ILL on Xchange"
    },
    "magister": {
        "x7R": 25,
        "x7100": 25,

    }
}
