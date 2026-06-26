constant product AMM design.
core formula: x * y = k
reserve x = token A, reserve y = token B, product k invariant.
swap delta_x in, get delta_y out:
delta_y = y - (k / (x + delta_x))
with 0.3% fee:
delta_x_in_with_fee = delta_x * 0.997
k = x * y
delta_y = y - (k / (x + delta_x_in_with_fee))
fee = delta_x * 0.003
liquidity provision: mint LP tokens = sqrt(delta_x * delta_y) adjusted for proportion. deposit proportional to reserves or suffer penalty via concentrated divergence.
lending pool design. overcollateralized. collateral factor = 0.75. borrow 75% max of deposited collateral value. liquidation threshold at 80%. liquidator gets 5% bonus + repays debt.
stable swap AMM for correlated assets:
x + y = constant sum at peg
x * y = constant product off peg
amplification factor A controls curve shape:
(x * y * A * D) + (x + y) * D^2 = (A * D^3) + (D^3)
where D = total liquidity. high A = flat near peg for low slippage. low A = behaves like CPMM.
staking rewards: stake LP tokens, earn governance tokens. rewards per second = total_allocated / total_staked * user_stake. checkpoint at every action. reward debt accounting:
user.owed = user.staked * (accumulated_reward_per_share - user.reward_debt)
yield farming: multi-pool reward distribution. masterchef pattern. alloc points per pool. total alloc points. block or timestamp based emission.
governance: token weighted voting. proposal threshold = 1% of supply. quorum = 4% of supply. majority wins. timelock = 48 hours on execution.
which component do you want implemented?