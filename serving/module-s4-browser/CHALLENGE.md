# S4 Challenge - Run it in the browser

A real model, in your tab. Run it, then reason about what you saw.

## Run it
1. Open the widget and press "download & run". Note three numbers it reports:
   the backend (WebGPU or WASM), the model size in MB, and the measured tok/s.
   Which of those three is S0's bandwidth clock, and which is S2's bytes?
2. Run the 135M model, then (if your machine allows) the 0.5B. What got better,
   what got slower, and how does the download size explain the difference?

## Reason about it
3. WebGPU and WASM run the SAME model and give the same answers, but WASM is
   ~5-10x slower. Using S2, explain why - what does WebGPU do that WASM cannot?
4. Your friend's phone runs the 135M model fine but cannot load the 1.7B at all.
   Using S0's "fits and flows", explain both facts (what caps loading, what caps
   speed).
5. Nothing you type leaves the tab, and there is no per-call cost. Name two real
   situations where that makes the browser the RIGHT host, and one where it is
   clearly the wrong one.

## Place it
6. S1-S4 all optimized ONE instance for ONE user (read it, made it fast, shipped
   it, ran it in a tab). The browser makes that vivid: one tab, one user. What is
   the question S4 explicitly cannot answer - and which modules do? (Hint: a
   thousand people, one GPU.)

## Done when
You have run a real model in your own browser, can point at which reported
number is the S0 clock, and can explain - to someone who thinks "AI needs the
cloud" - how a real model just ran privately in a tab with no server.
