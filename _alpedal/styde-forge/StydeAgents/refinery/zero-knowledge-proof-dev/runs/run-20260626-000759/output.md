Blueprint zero-knowledge-proof-dev exists and is loaded. All 3 required files validated.
Skills activated: Circom, SNARK, Rollup, Privacy, Groth16.
No build target provided. Running default capability demonstration: Groth16-compatible privacy circuit for private payment verification.
Circuit: PrivateBalanceCheck -- proves user has >= threshold balance without revealing actual balance.
```
// PrivateBalanceCheck.circom -- Groth16
// Proves: balance >= threshold without revealing balance
pragma circom 2.1.0;
template PrivateBalanceCheck(n) {
    signal input balance;
    signal input threshold;
    signal input salt;
    signal output commitment;
    // range check: balance in [0, 2^n)
    component range = Num2Bits(n);
    range.in <== balance;
    // derive commitment = hash(balance, salt)
    component hash = Poseidon(2);
    hash.inputs[0] <== balance;
    hash.inputs[1] <== salt;
    commitment <== hash.out;
    // constraint: balance >= threshold
    // circom uses signal comparison via LessEqThen
    component check = GreaterEqThan(n);
    check.in[0] <== balance;
    check.in[1] <== threshold;
    check.out === 1;
}
component main = PrivateBalanceCheck(64);
```
Proving system: Groth16 over BN254. Trusted setup phase 1 shared, phase 2 circuit-specific. Proof size: ~130 bytes. Verification cost: ~200k gas on EVM.
Blueprint ready. Deploy on next task.