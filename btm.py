import math
import datetime
import scipy.stats as st
import pandas as pd
import matplotlib.pyplot as plt

from tree import OverlappingTree

# s_0 = 1259.09
# k = 1255.27
s_0 = 1692.6
k = 16700
sigma = 0.9910
r = 0.03875
# now = datetime.datetime.now(datetime.timezone.utc)
# now = datetime.datetime(2022, 11, 15, 12, 0, 0, 0, datetime.timezone.utc)
now = datetime.datetime(2022, 11, 15, 14, 0, 0, 0, datetime.timezone.utc)
_t = (datetime.datetime(2022, 11, 16, 12, 0, 0, 0, datetime.timezone.utc) - now)
# _t = (datetime.datetime(2022, 11, 18, 8, 0, 0, 0, datetime.timezone.utc) - now)
# _t = (datetime.datetime(2022, 11, 25, 8, 0, 0, 0, datetime.timezone.utc) - now)
# _t = (datetime.datetime(2022, 12, 30, 8, 0, 0, 0, datetime.timezone.utc) - now)
t = (_t.total_seconds()) / 86400 / 365


def btm_price(n, american=False):

    # start = datetime.datetime.now()
    start = datetime.datetime.now()

    put_tree = OverlappingTree(n)
    call_tree = OverlappingTree(n)
    move_tree = OverlappingTree(n)
    put_tree_2 = OverlappingTree(n)
    call_tree_2 = OverlappingTree(n)
    move_tree_2 = OverlappingTree(n)
    d_t = t / n
    u = math.exp(sigma * math.sqrt(d_t))
    d = 1 / u
    p_u = (math.exp(r * d_t) - d) / (u - d)
    p_d = 1 - p_u

    u_2 = math.exp((sigma + 0.00001) * math.sqrt(d_t))
    d_2 = 1 / u_2
    p_u_2 = (math.exp(r * d_t) - d_2) / (u_2 - d_2)
    p_d_2 = 1 - p_u_2

    d_r = math.exp(-r * d_t)
    for i in range(-n, n + 1):
        s = s_0 * u ** i
        s_2 = s_0 * u_2 ** i
        put_tree[n, i] = max(k - s, 0)
        call_tree[n, i] = max(s - k, 0)
        move_tree[n, i] = abs(s - k)
        put_tree_2[n, i] = max(k - s_2, 0)
        call_tree_2[n, i] = max(s_2 - k, 0)
        move_tree_2[n, i] = abs(s_2 - k)
    for i in range(n - 1, -1, -1):
        for j in range(-i, i + 1):
            s = s_0 * u ** j
            s_2 = s_0 * u_2 ** j
            if not american:
                # force the first arg of max to be 0, effectively nullifying it
                s = k
                s_2 = k
            put_tree[i, j] = max(k - s, d_r * (p_u * put_tree[i + 1, j + 1] + p_d * put_tree[i + 1, j - 1]))
            call_tree[i, j] = max(s - k, d_r * (p_u * call_tree[i + 1, j + 1] + p_d * call_tree[i + 1, j - 1]))
            move_tree[i, j] = max(abs(s - k), d_r * (p_u * move_tree[i + 1, j + 1] + p_d * move_tree[i + 1, j - 1]))
            put_tree_2[i, j] = max(k - s_2, d_r * (p_u_2 * put_tree_2[i + 1, j + 1] + p_d_2 * put_tree_2[i + 1, j - 1]))
            call_tree_2[i, j] = max(s_2 - k, d_r * (p_u_2 * call_tree_2[i + 1, j + 1] + p_d_2 * call_tree_2[i + 1, j - 1]))
            move_tree_2[i, j] = max(abs(s_2 - k), d_r * (p_u_2 * move_tree_2[i + 1, j + 1] + p_d_2 * move_tree_2[i + 1, j - 1]))
    print(f"              n: {n}")
    print(" time to expiry: ", _t)
    print(f"years to expiry: {t:.6f}")
    print(f" days to expiry: {t * 365:.6f}")
    print(f"strike: {k:.2f}")
    print(f"spot:   {s_0:.2f}")
    print(f"IV:     {sigma:.2%}")
    print(f"r:      {r:.2%}")
    print(f"put:  {put_tree[0, 0]:.6f}")
    put_tree.print_greeks(s_0, u, d, d_t)
    print(f"  vega%: {1000 * (put_tree_2[0, 0] - put_tree[0, 0]):.6f}")
    print(f"call: {call_tree[0, 0]:.6f}")
    call_tree.print_greeks(s_0, u, d, d_t)
    print(f"  vega%: {1000 * (call_tree_2[0, 0] - call_tree[0, 0]):.6f}")
    print(f"move: {move_tree[0, 0]:.6f}")
    move_tree.print_greeks(s_0, u, d, d_t)
    print(f"  vega%: {1000 * (move_tree_2[0, 0] - move_tree[0, 0]):.6f}")
    print("time taken: ", datetime.datetime.now() - start)
    return {
        "put": {
            "price": put_tree[0, 0],
            "greeks": put_tree.greeks(s_0, u, d, d_t)
        },
        "call": {
            "price": call_tree[0, 0],
            "greeks": call_tree.greeks(s_0, u, d, d_t)
        },
        "move": {
            "price": move_tree[0, 0],
            "greeks": move_tree.greeks(s_0, u, d, d_t)
        },
        "time": datetime.datetime.now() - start
    }


def plots():
    d1 = (math.log(s_0 / k) + (r + sigma * sigma / 2) * t) / (sigma * math.sqrt(t))
    d2 = d1 - sigma * math.sqrt(t)
    call_price = s_0 * st.norm.cdf(d1) - k * math.exp(-r * t) * st.norm.cdf(d2)
    put_price = k * math.exp(-r * t) * st.norm.cdf(-d2) - s_0 * st.norm.cdf(-d1)
    print(f"call price: {call_price:.6f}")
    print(f"put price: {put_price:.6f}")
    put_data = []
    call_data = []
    move_data = []
    for i in range(100, 1001, 20):
        price = btm_price(i)
        put_data.append({
            "n": i,
            "put_price": price["put"]["price"],
            "real_price": put_price,
        })
        call_data.append({
            "n": i,
            "call_price": price["call"]["price"],
            "real_price": call_price,
        })
        move_data.append({
            "n": i,
            "move_price": price["move"]["price"],
            "real_price": call_price + put_price,
        })
    put_df = pd.DataFrame(put_data)
    call_df = pd.DataFrame(call_data)
    move_df = pd.DataFrame(move_data)
    put_df.plot(x="n", y=["put_price", "real_price"])
    plt.title("Put Option Price")
    plt.show()
    call_df.plot(x="n", y=["call_price", "real_price"])
    plt.title("Call Option Price")
    plt.show()
    move_df.plot(x="n", y=["move_price", "real_price"])
    plt.title("MOVE Price")
    plt.show()


if __name__ == '__main__':
    btm_price(800)
    btm_price(800, True)
