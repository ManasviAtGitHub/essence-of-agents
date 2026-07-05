# By hand - size a small model

## 1. Quantization bytes
Size = params x bits / 8. Compute the disk size (GB, 1e9 bytes) for a 7B model:
- fp16 (16 bits)   - int8 (8 bits)   - int4 (4 bits)
Which of these fits in an 8 GB laptop GPU alongside a little overhead?

## 2. Scaling ratios
- Chinchilla-optimal training tokens for a 3B model? (~20 x params)
- Llama-3-8B used ~15T tokens. Tokens per parameter? How many times past
  Chinchilla-"optimal" is that?
- In one sentence: why is overtraining a SMALL model a good idea even though
  it is "compute-suboptimal" by Chinchilla?

## 3. Soft targets
A teacher's next-token distribution is [0.90 "Paris", 0.06 "Lyon", 0.03
"France", 0.01 other]. The hard label is just "Paris".
- What extra information does the soft target carry that the hard label does
  not?
- Why does that make the student learn faster / generalize better?

## 4. Stack the tools
You have a 671B reasoning teacher and need something to run on a phone.
- Sketch the pipeline using all three tools (distill, then quantize; overtrain
  is the student's own training).
- Estimate the final disk size if the student is 3B at int4.

## 5. Name the cost
For each tool, name the ONE cost it primarily reduces:
overtraining, distillation, quantization. (Data? inference compute? memory/
bytes? parameter count?) Where do they overlap, where are they orthogonal?

## Stretch
- The student's ceiling is roughly the teacher. So how does the FRONTIER ever
  advance, if distillation only copies? What must still happen with a big,
  expensive run?
- int4 barely hurts, int2 breaks. Propose an experiment (with an eval set from
  course 1's Module 10) to find the precision floor for a specific model.
