# Artifact Format

> **Output language**: Write in the language specified in the sub-agent prompt's meta block. Code snippets, file paths, and technical terms remain as-is.

Output format for Phase 3 Deep Dive. `artifacts/modules/{module}.md`

---

## Principles

Free-form prose + provenance tags. Not a structured schema. Since AI reads this, the more information the better.

Provenance tags go inline immediately after a claim:
```
[provenance:code_derived file:src/ae.c:L42]
[provenance:author_stated source:"URL"]
[provenance:synthesized]
```

---

## Example: libuv Event Loop

```markdown
# Event Loop

## Why It Exists

The immediate catalyst for libuv's creation was the need to port Node.js to Windows in 2011. The Unix world was split between epoll (Linux) and kqueue (macOS/BSD), while Windows had IOCP (I/O Completion Ports) — a fundamentally different paradigm. epoll and kqueue follow a readiness model: "notify me when an event occurs on this fd." IOCP follows a completion model: "notify me when this I/O operation finishes." The two models operate at different levels of abstraction.
[provenance:author_stated source:"https://nikhilm.github.io/uvbook/basics.html"]

Bert Belder's conclusion was "don't hide the differences — normalize them." libuv is not a thin wrapper. It unifies the two paradigms into a single readiness model without sacrificing platform-specific optimizations.
[provenance:author_stated source:"Bert Belder, NodeConf 2012"]

## uv_loop_t: This Struct Is the Philosophy

uv_loop_t is not a simple data container. The very existence of this struct is a declaration that "there is no global state."
[provenance:code_derived file:include/uv.h:L218]

Examining the fields reveals the design philosophy. active_handles and active_reqs are counters, not collections — the loop does not own handles. Each handle merely references the loop. This asymmetry matters: the loop does not manage handle lifetimes.
[provenance:code_derived file:include/uv.h:L220-L240]

## uv__run: The Heartbeat

...

## Boundaries

What the Event Loop knows: when I/O events occur, when timers expire, and in what order to invoke callbacks.

What the Event Loop does not know: what those callbacks do, how long they take, or what to do if they fail. This ignorance is libuv's core abstraction. The fact that a blocking callback stalls the entire loop is a direct consequence of this boundary.
[provenance:synthesized]

## Trade-offs

**What was given up: Multicore utilization**
A single loop runs on a single thread. On an 8-core server, 7 cores sit idle. This is not a mistake — it is a choice.

**What was gained: Complete state isolation and predictability**
No locks. No race conditions. Execution order is entirely predictable. The reason Node.js can handle tens of thousands of concurrent connections on a single thread is this very choice.

The evidence is that uv_loop_t contains no mutex. No synchronization primitives for multithreading exist anywhere in the struct.
[provenance:code_derived file:include/uv.h:L218-L310]

**The limits of this choice gave birth to the Thread Pool**
CPU-bound tasks (file I/O, DNS resolution, encryption) that block the loop are handled by the Thread Pool. But this is a compromise of the pure async model — the Thread Pool's very existence is an admission that the Event Loop alone is not enough.
[provenance:synthesized]

## Official Narrative vs Code

Documentation introduces libuv as a "cross-platform asynchronous I/O library." Not wrong, but looking at the actual uv__io_poll implementation, "thin abstraction" is a stretch.

The Linux epoll path (src/unix/linux-core.c:L212) and the macOS kqueue path (src/unix/kqueue.c:L89) contain deep platform-specific optimizations. epoll_pwait's signal mask handling and kqueue's kevent64 usage each embrace their platform's characteristics. libuv does not hide the differences — it normalizes them while extracting the maximum strength of each platform. "Thin wrapper" is far less honest a description.
[provenance:code_derived file:src/unix/linux-core.c:L212]
[provenance:code_derived file:src/unix/kqueue.c:L89]
[provenance:synthesized]

## Self-Verification Summary
- code_derived claims: 12 verified
- Tags corrected: 1 (linux-core.c line number corrected)
- Claims removed: 0
```

> **Note**: Every Phase 3 artifact must include a self-verification summary at the end. See the Self-Verify section in `references/phase3-deep-dive.md`.
