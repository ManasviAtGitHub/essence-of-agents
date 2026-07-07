# Challenge - grade the trajectory, save the swarm

## Part 1 - leave-one-out (be Tongyi's baseline)
Four full research trajectories earn rewards [1, 0, 1, 1].
Compute each trajectory's leave-one-out advantage:
adv_i = r_i - mean(all rewards EXCEPT r_i).

<details><summary>answer</summary>
- adv_1 = 1 - mean(0,1,1) = 1 - 0.67 = +0.33
- adv_2 = 0 - mean(1,1,1) = 0 - 1.00 = -1.00
- adv_3 = 1 - mean(1,0,1) = 1 - 0.67 = +0.33
- adv_4 = 1 - mean(1,0,1) = +0.33
The one failure is judged against a perfect peer group and punished hard;
each success is judged only against the others. No value network needed -
the group IS the baseline (M7's idea, per-trajectory).
</details>

## Part 2 - serial collapse
An orchestrator must finish 8 equal subtasks. Reward = 1 - 0.05 x
(wall-clock time units). One worker does one subtask per time unit.
1. Reward if the orchestrator funnels everything through ONE worker?
2. Reward if it spawns FOUR workers?
3. If the time penalty were removed, what do both strategies earn - and
   what does the orchestrator therefore never learn?

<details><summary>answer</summary>
1. T = 8 -> reward = 1 - 0.40 = 0.60.
2. T = 2 -> reward = 1 - 0.10 = 0.90.
3. Both earn 1.0 - parallelism is unrewarded, so the policy drifts to the
   simplest habit: one worker, serial. That drift is SERIAL COLLAPSE; the
   wall-clock term (PARL's shaping, simplified here) is what makes
   delegation worth learning.
</details>

## Part 3 - trained or scripted?
In a 2026 frontier agent stack, label each as usually TRAINED (in weights)
or SCRIPTED (in code/prompts): A. which tool to call next; B. the MCP
protocol handshake; C. spawning sub-agents; D. the sandbox boundary.

<details><summary>answer</summary>
A. TRAINED (agentic RL - Tongyi, Composer). B. SCRIPTED - protocols are
fixed plumbing (that is their point). C. TRAINED at the frontier (PARL) -
this is the newest migration. D. SCRIPTED - security boundaries must never
be learned behavior (course 1 M9's lesson survives intact).
</details>
