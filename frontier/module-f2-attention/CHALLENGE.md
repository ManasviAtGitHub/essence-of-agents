# Challenge - three designs, one bill

Context: 128,000 tokens already read; one new token arrives.

1. FULL attention (M2/M3's design): how many past entries does the new
   token's attention READ? What is stored?
2. SPARSE (DSA-style, top-k = 2,048): how many entries are READ? What is
   stored? What extra component had to run first, and over how many tokens?
3. LINEAR (fixed-state, DeltaNet-style): how many entries are READ? What is
   stored?
4. Name the documented failure risk of each design (one line each).

<details><summary>answer</summary>

1. Reads all **128,000** K,V entries; stores all 128,000 (M3's bill).
2. Reads only **2,048** (~1.6%) - but the INDEXER first scored all 128,000
   (cheaply, low precision). Storage is still the full cache: DSA cuts
   READS, not memory - until compression (V4's CSA/HCA) shrinks storage too.
3. Reads a **constant-size state** (the notebook) - independent of context.
   Stores only that state: O(1) memory at any length.
4. FULL: the n^2 bill itself (cost). SPARSE: the indexer becomes the new
   bottleneck (why GLM-5 added IndexShare) and can mis-rank what matters.
   LINEAR: documented reasoning degradation at scale - MiniMax M2 reverted
   to full attention after hybrids lost multi-hop reasoning (Oct 2025).
</details>

## The point
"How does this model afford 1M context?" is now a one-question diagnosis:
what does one new token READ, and what is STORED? Every 2026 flagship is one
of these three answers - or a ratio between them.
