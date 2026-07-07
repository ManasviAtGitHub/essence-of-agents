# Challenge - be the grammar, then be the verifier

The tool catalog:
```
get_weather(city)        -> {rain, temp}
add_to_cart(item)        -> {}
search(query)            -> {top}
send_email(to)           -> {}
```

## Part 1 - mask the distribution (be the grammar)
The front-end is decoding this partial plan and is about to emit the next token:
```
n1 = get_weather(city="Paris")
n2 = if n1.____
```
The model proposes these candidates with these (illustrative) raw scores:

| candidate | kind        | raw score |
|-----------|-------------|-----------|
| `temp`    | field       | 1.8 |
| `rain`    | field       | 2.0 |
| `city`    | field       | 1.5 |
| `top`     | field       | 1.2 |

1. Which candidates are **legal** here, and why are the others masked?
   (Hint: what is the return schema of the tool that produced `n1`?)
2. After masking, renormalize the legal candidates into probabilities
   (softmax over the legal scores only). Which token does temperature-0
   decoding emit?

<details><summary>answer</summary>

`n1` came from `get_weather`, whose **return** schema is `{rain, temp}`. So only
`.rain` and `.temp` are legal; `.city` was an *input* (not an output) and `.top`
belongs to `search` - both masked. Renormalizing `{rain:2.0, temp:1.8}`:
`e^2.0 / (e^2.0 + e^1.8) = 0.55`, `e^1.8/... = 0.45`. Temperature 0 takes the
argmax of the legal set -> `rain`.
</details>

## Part 2 - run the verifier (be the backend)
Type-check each plan. For each, say PASS or the exact compile error:

- **A**
  ```
  n1 = get_weather(city="Paris")
  n2 = if n1.rain: add_to_cart(item="umbrella")
  ```
- **B**
  ```
  n1 = get_weather(city="Paris")
  n2 = if n3.rain: add_to_cart(item="umbrella")
  ```
- **C**
  ```
  n1 = add_to_cart(city="Paris")
  ```
- **D**
  ```
  n1 = get_weather(city="Paris")
  n2 = if n1.top: send_email(to="me")
  ```

<details><summary>answer</summary>

- **A - PASS.** Tools exist; `city`/`item` are valid args; `n1` is defined
  before `n2` uses it; `n1.rain` is a real return field; acyclic.
- **B - FAIL:** `n2` references `n3`, which is never defined (used before
  defined).
- **C - FAIL:** `add_to_cart` has no arg `city` (its only arg is `item`). This
  is the grammar-legal-but-wrong case a weak verifier would miss.
- **D - FAIL:** `n1` (a `get_weather` result) has no field `top`; `top` belongs
  to `search`.
</details>

## The point
Part 1 is the front-end (constrained decoding at the sampler); Part 2 is the
backend (the verifier). A compiler is exactly the two of them wired together -
and a stochastic model can wear the front-end hat only because the grammar and
the verifier make its mistakes impossible or loud.
