# tree-of-thoughts

> **Archived historical prototype — May–June 2023.**
>
> This repository is no longer maintained and is not expected to run
> against current OpenAI APIs without modification.

This project explored whether GPT-4 results could be improved by arranging
multiple model calls into explicit stages such as planning, implementation,
research, and refinement.

At each stage, the program generated several candidate responses, asked
GPT-4 to vote among them, retained the winner, and passed that winner into
the next stage. It also supported reinserting selected ancestor responses
and saving intermediate generations and votes to disk.

The project should be read as an artifact of the early 2023
chain-of-thought / tree-of-thought experimentation period, not as a
production library.

## Known limitations

- No committed benchmark or evidence that the workflow outperformed a
  strong single prompt.
- Generation and evaluation used the same model.
- Candidate order was not randomized.
- The effective implementation retained only one live path and did not
  backtrack.
- Cached files were not keyed by prompt, model, or configuration.
- The OpenAI integration and dependency declarations are obsolete.
- The repository contains no complete public example workflow.

## Lessons

The enduring ideas were explicit intermediate artifacts, configurable
reasoning stages, resumable model calls, and selective reuse of earlier
context. The principal failure was building a general orchestration system
before establishing a repeatable evaluation loop.
