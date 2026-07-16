# S5 Challenge - Serve many

Packing a GPU with users. Show you can reason about the two mechanisms.

## The griddle (batching)
1. A batch of 8 requests. Seven finish in 20 tokens; one runs to 500. Under
   STATIC batching, how many of the 8 slots are doing useful work for most of
   those 500 steps? What does that say about utilization - and cost?
2. Continuous batching admits a new request the moment a slot frees. In one
   sentence, why does that keep the GPU near 100% busy where static cannot?
3. Batching amortizes S0's doorway. If reading the weights is the same cost for
   a batch of 1 or 32, what is the (rough) per-user cost difference - and why is
   that the reason serving is cheaper at scale?

## The lockers (paged attention)
4. A request might produce 5 tokens or 5,000; you cannot know in advance.
   Explain why reserving a max-size KV block per request wastes memory, and how
   fixed-size pages handed out on demand fix it - using the "lockers, not
   shelves" idea.
5. A chatbot gives every user the same 2,000-token system prompt. With paged +
   shared prefixes, how many copies of that prompt's KV pages are stored for
   1,000 users? Connect this to Module 3's prompt caching.

## Put it together
6. Continuous batching keeps the GPU busy; paged/shared KV lets more requests
   fit. Which one raises throughput by using COMPUTE better, and which by using
   MEMORY better? Then: name the S5 lever that is really M5 wearing a serving
   hat.

## Done when
You can explain, with the 8-slot griddle and the locker wall, why one GPU can
serve many users at once - and name which mechanism attacks idle compute and
which attacks wasted memory.
