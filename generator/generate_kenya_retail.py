#!/usr/bin/env python3
import argparse
import os

import numpy as np
import pandas as pd

START, END = "2024-01-01", "2025-12-31"

CATEGORIES = ["Staples", "Dairy & Eggs", "Beverages", "Fresh Produce",
              "Bakery", "Household", "Personal Care", "Meat & Fish"]

PRODUCTS = [
    ("Maize Flour 2kg", 0, 120, 145), ("Wheat Flour 2kg", 0, 130, 160),
    ("Rice Pishori 1kg", 0, 170, 210), ("Sugar 1kg", 0, 140, 175),
    ("Cooking Oil 1L", 0, 260, 320), ("Salt 500g", 0, 25, 40),
    ("Spaghetti 400g", 0, 70, 95),
    ("Fresh Milk 500ml", 1, 50, 65), ("Fresh Milk 1L", 1, 95, 120),
    ("Yoghurt 500ml", 1, 90, 120), ("Butter 250g", 1, 220, 280),
    ("Cheddar Cheese 200g", 1, 260, 330), ("Eggs Tray 30", 1, 380, 450),
    ("Tea Leaves 500g", 2, 190, 240), ("Instant Coffee 100g", 2, 300, 380),
    ("Soda 500ml", 2, 40, 60), ("Soda 2L", 2, 90, 120),
    ("Bottled Water 1.5L", 2, 45, 70), ("Fruit Juice 1L", 2, 130, 170),
    ("Tomatoes 1kg", 3, 70, 100), ("Onions 1kg", 3, 60, 90),
    ("Potatoes 1kg", 3, 55, 80), ("Sukuma Wiki Bunch", 3, 15, 30),
    ("Bananas 1kg", 3, 60, 90), ("Avocado Each", 3, 20, 40),
    ("Cabbage Each", 3, 40, 70), ("Carrots 1kg", 3, 65, 95),
    ("Bread White 400g", 4, 55, 65), ("Bread Brown 400g", 4, 60, 75),
    ("Chapati Pack 5", 4, 80, 110), ("Mandazi Pack 6", 4, 60, 90),
    ("Cake Slice", 4, 70, 110),
    ("Laundry Soap Bar 1kg", 5, 160, 210), ("Washing Powder 1kg", 5, 190, 250),
    ("Toilet Paper 10 Pack", 5, 230, 300), ("Dishwashing Liquid 750ml", 5, 150, 200),
    ("Bleach 1L", 5, 120, 170),
    ("Bathing Soap 175g", 6, 55, 80), ("Toothpaste 100g", 6, 90, 130),
    ("Body Lotion 400ml", 6, 280, 380), ("Sanitary Pads 8s", 6, 80, 115),
    ("Shampoo 400ml", 6, 250, 330), ("Deodorant 150ml", 6, 180, 250),
    ("Beef 1kg", 7, 520, 650), ("Whole Chicken 1.5kg", 7, 600, 780),
    ("Tilapia 1kg", 7, 450, 580), ("Sausages 500g", 7, 280, 360),
]
BRANDS = ["Mama Pride", "Pwani Fresh", "Savanna Gold", "Kijani Farm",
          "Jua Kali", "Highland", "Rift Valley Select", "Lakeside"]
CAT_POP = np.array([2.0, 1.5, 1.4, 2.0, 1.8, 0.9, 0.8, 0.8])

# (name, county, format, opened)
STORES = [
    ("Westlands Hypermarket", "Nairobi", "Hypermarket", "2019-03-01"),
    ("Kilimani Express", "Nairobi", "Express", "2020-06-15"),
    ("Eastlands Supermarket", "Nairobi", "Supermarket", "2018-09-10"),
    ("Karen Supermarket", "Nairobi", "Supermarket", "2021-02-20"),
    ("Nakuru Town Supermarket", "Nakuru", "Supermarket", "2019-11-05"),
    ("Lanet Express", "Nakuru", "Express", "2022-04-18"),
    ("Nyali Supermarket", "Mombasa", "Supermarket", "2020-01-25"),
    ("Mombasa Road Express", "Mombasa", "Express", "2023-03-12"),
    ("Kisumu Central", "Kisumu", "Supermarket", "2021-08-30"),
    ("Eldoret Town", "Uasin Gishu", "Supermarket", "2020-10-09"),
    ("Thika Town Supermarket", "Kiambu", "Supermarket", "2019-07-22"),
    ("Nyeri Town", "Nyeri", "Express", "2022-09-01"),
]
STORE_W = np.array([.16, .09, .12, .08, .09, .05, .09, .05, .07, .07, .08, .05])

COUNTIES = ["Nairobi", "Kiambu", "Nakuru", "Mombasa", "Kisumu",
            "Uasin Gishu", "Nyeri", "Machakos", "Kajiado"]
COUNTY_W = np.array([.34, .12, .14, .12, .08, .08, .05, .04, .03])

FIRST = ["Wanjiku", "Otieno", "Achieng", "Kamau", "Mwangi", "Njeri", "Odhiambo",
         "Akinyi", "Kiptoo", "Chebet", "Mutua", "Kioko", "Wambui", "Omondi",
         "Atieno", "Kimani", "Nyambura", "Barasa", "Naliaka", "Mohamed",
         "Fatuma", "Hassan", "Amina", "Ochieng", "Jepkemboi", "Muthoni",
         "Gitau", "Wairimu", "Karanja", "Kiplagat"]
LAST = ["Kariuki", "Maina", "Otieno", "Ouma", "Kiprop", "Korir", "Mutiso",
        "Wekesa", "Njoroge", "Wafula", "Mwende", "Githinji", "Abdi", "Ali",
        "Cheruiyot", "Nyongesa", "Onyango", "Waweru", "Kilonzo", "Mbugua"]


def messy_case(rng, series, frac):
    s = series.copy()
    idx = s.index[rng.random(len(s)) < frac]
    for i in idx:
        v = s.at[i]
        choice = rng.integers(0, 3)
        s.at[i] = v.upper() if choice == 0 else v.lower() if choice == 1 else f" {v} "
    return s, len(idx)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="kenya_retail_data")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--customers", type=int, default=3000)
    ap.add_argument("--daily-orders", type=float, default=52.0)
    a = ap.parse_args()

    rng = np.random.default_rng(a.seed)
    os.makedirs(a.out, exist_ok=True)
    issues = {}

    categories = pd.DataFrame({
        "category_id": range(1, len(CATEGORIES) + 1),
        "category_name": CATEGORIES,
    })

    products = pd.DataFrame(PRODUCTS, columns=["product_name", "cat_idx",
                                               "unit_cost", "list_price"])
    products.insert(0, "product_id", range(1, len(products) + 1))
    products["category_id"] = products.cat_idx + 1
    products["brand"] = rng.choice(BRANDS, len(products))
    products["is_active"] = rng.random(len(products)) > 0.04
    products["updated_at"] = pd.Timestamp("2025-01-01")
    base_products = products.copy()  # clean copy used for pricing
    rank = rng.permutation(len(products)) + 1
    pop = CAT_POP[products.cat_idx.values] / rank ** 0.7
    pop = pop / pop.sum()

    m = rng.random(len(products)) < 0.06
    products.loc[m, "product_name"] = products.loc[m, "product_name"] + " "
    issues["products: product_name with trailing space"] = int(m.sum())
    m = rng.random(len(products)) < 0.10
    products.loc[m, "brand"] = products.loc[m, "brand"].str.lower()
    issues["products: brand in lowercase"] = int(m.sum())
    products_out = products[["product_id", "product_name", "category_id", "brand",
                             "unit_cost", "list_price", "is_active", "updated_at"]]

    stores = pd.DataFrame(STORES, columns=["store_name", "county",
                                           "store_format", "opened_date"])
    stores.insert(0, "store_id", range(1, len(stores) + 1))

    n = a.customers
    signup = pd.to_datetime("2022-01-01") + pd.to_timedelta(
        rng.integers(0, 1400, n), unit="D")  # up to ~Oct 2025
    cust = pd.DataFrame({
        "customer_id": [f"CUS-{i:05d}" for i in range(1, n + 1)],
        "full_name": [f"{rng.choice(FIRST)} {rng.choice(LAST)}" for _ in range(n)],
        "phone": [f"0{rng.choice([7, 1])}{rng.integers(0, 10**8):08d}" for _ in range(n)],
        "county": rng.choice(COUNTIES, n, p=COUNTY_W),
        "segment": rng.choice(["Regular", "Loyalty", "Wholesale"], n,
                              p=[.72, .24, .04]),
        "signup_date": signup.normalize(),
    })
    cust = cust.sort_values("signup_date").reset_index(drop=True)
    cust["updated_at"] = cust.signup_date

    n_dup = int(n * 0.02)
    dup_src = cust.sample(n_dup, random_state=a.seed).copy()
    dup_src["orig_id"] = dup_src.customer_id
    dup_src["customer_id"] = [f"CUS-{n + i + 1:05d}" for i in range(n_dup)]
    dup_map = dict(zip(dup_src.orig_id, dup_src.customer_id))
    issues["customers: duplicate people (second customer_id)"] = n_dup

    movers = cust[cust.signup_date < "2025-03-01"].sample(
        int(n * 0.06), random_state=a.seed + 1).copy()
    movers["county"] = [rng.choice([c for c in COUNTIES if c != old])
                        for old in movers.county]
    movers["updated_at"] = pd.to_datetime("2025-03-01") + pd.to_timedelta(
        rng.integers(0, 240, len(movers)), unit="D")
    customers_updates = movers[["customer_id", "full_name", "phone", "county",
                                "segment", "signup_date", "updated_at"]]
    issues["customers_updates: customers who changed county"] = len(movers)

    dates = pd.date_range(START, END)
    t = np.arange(len(dates)) / len(dates)
    wd_mult = np.array([.9, .9, .95, 1.0, 1.15, 1.35, 1.2])[dates.day_of_week.values]
    dom = dates.day.values
    me_mult = np.where((dom >= 25) | (dom <= 2), 1.35, 1.0)   # pay-day effect
    mon_mult = np.where(dates.month == 12, 1.25, np.where(dates.month == 1, .95, 1.0))
    lam = a.daily_orders * wd_mult * me_mult * mon_mult * (1 + 0.25 * t)
    counts = rng.poisson(lam)
    N = int(counts.sum())

    hours = np.arange(7, 22)
    hw = np.array([2, 3, 4, 5, 6, 6, 5, 5, 6, 7, 8, 8, 6, 4, 2], dtype=float)
    hour = rng.choice(hours, N, p=hw / hw.sum())
    secs = hour * 3600 + rng.integers(0, 3600, N)
    order_ts = pd.to_datetime(np.repeat(dates.values, counts)) + pd.to_timedelta(secs, unit="s")
    orders = pd.DataFrame({"order_ts": np.sort(order_ts.values)})
    orders["order_id"] = [f"ORD-{i:06d}" for i in range(1, N + 1)]
    orders["order_date"] = orders.order_ts.dt.normalize()
    tfrac = ((orders.order_date - pd.Timestamp(START)).dt.days / len(dates)).values
    orders["is_online"] = rng.random(N) < (0.10 + 0.15 * tfrac)   # online grows over time
    orders["store_id"] = rng.choice(stores.store_id.values, N, p=STORE_W)

    signup_sorted = cust.signup_date.values
    k = np.searchsorted(signup_sorted, orders.order_date.values, side="right")
    k = np.maximum(k, 1)
    idx = np.floor(k * rng.random(N) ** 1.4).astype(int)
    cust_ids = cust.customer_id.values[idx].astype(object)
    for orig, dup in dup_map.items():
        mask = (cust_ids == orig) & (rng.random(N) < 0.5)
        cust_ids[mask] = dup
    walkin = (~orders.is_online.values) & (rng.random(N) < 0.20)
    cust_ids[walkin] = None
    orders["customer_id"] = cust_ids
    issues["orders: in-store orders with NULL customer_id (walk-ins)"] = int(walkin.sum())

    online_status = rng.choice(["delivered", "cancelled", "returned"], N, p=[.89, .07, .04])
    store_status = rng.choice(["completed", "cancelled", "refunded"], N, p=[.985, .007, .008])
    orders["status_clean"] = np.where(orders.is_online, online_status, store_status)
    orders["status"] = orders.status_clean
    m = rng.random(N) < 0.01
    orders.loc[m, "status"] = orders.loc[m, "status"].str.upper()
    issues["orders: status with inconsistent casing"] = int(m.sum())
    orders["channel"] = np.where(orders.is_online, "online", "in_store")
    lag_hours = np.where(orders.is_online, rng.integers(0, 72, N), 0)
    orders["updated_at"] = orders.order_ts + pd.to_timedelta(lag_hours, unit="h")

    n_items = rng.choice(np.arange(1, 10), N,
                         p=[.18, .22, .20, .15, .10, .07, .04, .03, .01])
    total_items = int(n_items.sum())
    oi_order_idx = np.repeat(np.arange(N), n_items)
    prod_idx = rng.choice(len(products), total_items, p=pop)
    qty = rng.choice([1, 2, 3, 4, 6, 12], total_items,
                     p=[.45, .25, .12, .08, .06, .04])
    seg_map = dict(zip(cust.customer_id, cust.segment))
    seg_map.update({d: seg_map[o] for o, d in dup_map.items()})
    seg = orders.customer_id.map(seg_map).values[oi_order_idx]
    qty = np.where(seg == "Wholesale", qty * 3, qty)

    od = orders.order_date.values[oi_order_idx]
    month_idx = ((pd.DatetimeIndex(od).year - 2024) * 12
                 + pd.DatetimeIndex(od).month - 1).values
    base_price = base_products.list_price.values[prod_idx]
    price = np.round(base_price * (1 + 0.004 * month_idx) / 5) * 5      # slow inflation
    gross = qty * price
    promo = rng.random(total_items) < 0.12
    discount = np.where(promo, np.round(gross * rng.choice([.05, .10, .15, .20], total_items)), 0.0)

    items = pd.DataFrame({
        "order_id": orders.order_id.values[oi_order_idx],
        "product_id": base_products.product_id.values[prod_idx],
        "quantity": qty,
        "unit_price": price,
        "discount_amount": discount,
    })
    line_total = gross - discount
    totals = pd.Series(line_total).groupby(items.order_id.values).sum()

    m = (items.discount_amount == 0) & (rng.random(total_items) < 0.35)
    items.loc[m, "discount_amount"] = np.nan
    issues["order_items: discount_amount NULL instead of 0"] = int(m.sum())
    dups = items.sample(int(total_items * 0.0015), random_state=a.seed + 2)
    items.insert(0, "order_item_id", range(1, total_items + 1))
    dups = items.loc[dups.index]                       # same order_item_id
    items = pd.concat([items, dups]).sort_values("order_item_id").reset_index(drop=True)
    issues["order_items: exact duplicate rows (same order_item_id)"] = len(dups)

    po = orders.loc[orders.status_clean != "cancelled",
                    ["order_id", "order_ts", "is_online"]].copy()
    po["total"] = po.order_id.map(totals)
    before = len(po)
    po = po[rng.random(len(po)) > 0.01]               # 1% of paid orders lose payment
    issues["orders (non-cancelled) with NO payment row"] = before - len(po)
    n_po = len(po)
    meth_on = rng.choice(["mpesa", "card", "cash"], n_po, p=[.75, .20, .05])
    meth_st = rng.choice(["mpesa", "card", "cash"], n_po, p=[.62, .23, .15])
    method = np.where(po.is_online.values, meth_on, meth_st)
    split = (rng.random(n_po) < 0.05) & (po.total.values > 500)
    first_amt = np.where(split, np.round(po.total.values * rng.uniform(.5, .7, n_po)),
                         po.total.values)
    p1 = pd.DataFrame({
        "order_id": po.order_id.values,
        "payment_ts": po.order_ts.values + pd.to_timedelta(rng.integers(0, 300, n_po), unit="s"),
        "method": np.where(split, "mpesa", method),
        "amount": first_amt, "status": "success"})
    p2 = pd.DataFrame({
        "order_id": po.order_id.values[split],
        "payment_ts": p1.payment_ts.values[split] + pd.Timedelta(minutes=1),
        "method": "cash",
        "amount": po.total.values[split] - first_amt[split], "status": "success"})
    pay = pd.concat([p1, p2])
    issues["payments: orders paid with two methods (split)"] = int(split.sum())
    # failed M-Pesa attempts before a successful retry
    mp = pay[pay.method == "mpesa"]
    failed = mp[rng.random(len(mp)) < 0.03].copy()
    failed["status"] = "failed"
    failed["payment_ts"] = failed.payment_ts - pd.to_timedelta(rng.integers(60, 240, len(failed)), unit="s")
    issues["payments: failed M-Pesa attempts (status='failed')"] = len(failed)
    pay = pd.concat([pay, failed]).sort_values("payment_ts").reset_index(drop=True)
    pay.insert(0, "payment_id", range(1, len(pay) + 1))
    chars = np.array(list("ABCDEFGHJKLMNPQRSTUVWXYZ0123456789"))
    refs = ["".join(r) for r in chars[rng.integers(0, len(chars), (len(pay), 10))]]
    pay["mpesa_ref"] = np.where((pay.method == "mpesa") & (pay.status == "success"), refs, None)
    pay["currency"] = "KES"
    pay = pay[["payment_id", "order_id", "payment_ts", "method", "amount",
               "currency", "status", "mpesa_ref"]]

    cust_county = dict(zip(cust.customer_id, cust.county))
    cust_county.update({d: cust_county[o] for o, d in dup_map.items()})
    dv = orders[orders.is_online & orders.status_clean.isin(["delivered", "returned"])].copy()
    nd = len(dv)
    carrier = rng.choice(["Carrier A", "Carrier B", "Carrier C"], nd, p=[.45, .35, .20])
    promised_days = rng.choice([1, 2, 3], nd, p=[.3, .5, .2])
    delay_ab = rng.choice([-1, 0, 1, 2, 4], nd, p=[.15, .55, .18, .08, .04])
    delay_c = rng.choice([0, 1, 2, 4, 6], nd, p=[.30, .25, .20, .15, .10])
    delay = np.where(carrier == "Carrier C", delay_c, delay_ab)
    promised_date = dv.order_date.values + pd.to_timedelta(promised_days, unit="D")
    delivered_ts = (pd.to_datetime(promised_date) + pd.to_timedelta(delay, unit="D")
                    + pd.to_timedelta(rng.integers(9, 19, nd), unit="h"))
    delivered_ts = pd.DatetimeIndex(np.maximum(
        delivered_ts.values, (dv.order_ts + pd.Timedelta(hours=3)).values))
    deliveries = pd.DataFrame({
        "order_id": dv.order_id.values, "carrier": carrier,
        "promised_date": pd.to_datetime(promised_date).date,
        "delivered_ts": delivered_ts,
        "delivery_county": dv.customer_id.map(cust_county).values,
    })
    m = rng.random(nd) < 0.02
    deliveries.loc[m, "delivered_ts"] = pd.NaT
    issues["deliveries: delivered orders with NULL delivered_ts"] = int(m.sum())
    deliveries.insert(0, "delivery_id", range(1, nd + 1))
    delay_days = pd.Series(delay, index=deliveries.index)

    ok = deliveries.delivered_ts.notna().values & (rng.random(nd) < 0.45)
    r = deliveries[ok]
    d_days = delay_days[ok].values  # days late vs promised date
    mean = np.where(d_days <= 0, 4.4, np.where(d_days <= 2, 3.5, 2.2))
    score = np.clip(np.round(rng.normal(mean, 0.8)), 1, 5).astype(int)
    reviews = pd.DataFrame({
        "review_id": range(1, len(r) + 1),
        "order_id": r.order_id.values,
        "score": score,
        "created_at": r.delivered_ts.values + pd.to_timedelta(rng.integers(1, 6, len(r)), unit="D"),
    })

    cust_out = pd.concat([cust, dup_src.drop(columns="orig_id")]).reset_index(drop=True)
    cust_out["county"], n_case = messy_case(rng, cust_out.county, 0.04)
    issues["customers: county with wrong casing / extra spaces"] = n_case
    m = rng.random(len(cust_out)) < 0.03
    cust_out.loc[m, "phone"] = None
    issues["customers: NULL phone"] = int(m.sum())
    cust_out = cust_out.sort_values("customer_id").reset_index(drop=True)

    orders_out = orders[["order_id", "customer_id", "store_id", "order_ts",
                         "channel", "status", "updated_at"]]

    files = {
        "categories": categories, "products": products_out, "stores": stores,
        "customers": cust_out, "customers_updates": customers_updates,
        "orders": orders_out, "order_items": items, "payments": pay,
        "deliveries": deliveries, "reviews": reviews,
    }
    for name, df in files.items():
        df.to_csv(os.path.join(a.out, f"{name}.csv"), index=False)
        print(f"{name:20s} {len(df):>8,} rows")

    with open(os.path.join(a.out, "planted_issues.txt"), "w") as f:
        f.write("PLANTED DATA ISSUES (answer key)\n"
                "Do your own profiling first, then check this list.\n\n")
        for k_, v in issues.items():
            f.write(f"- {k_}: {v}\n")
        f.write(
            "\nPATTERNS BAKED INTO THE DATA (find them with queries/Power BI)\n"
            "- Sales spike around month-end (days 25-2), on weekends, and in December.\n"
            "- Online share of orders grows over the two years.\n"
            "- Carrier C delivers late more often than Carriers A and B.\n"
            "- Late deliveries (3+ days past promise) get much lower review scores.\n"
            "- Wholesale customers buy larger quantities.\n"
            "- Prices rise slowly over time (inflation), so use the unit_price on the line.\n"
            "- Some customers moved county (see customers_updates.csv): use SCD Type 2.\n")


if __name__ == "__main__":
    main()