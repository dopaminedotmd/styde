```
<script>
  // ── Rune: $state, $derived, $effect ──
  let count = $state(0);
  let doubled = $derived(count * 2);
  $effect(() => {
    document.title = `Count: ${count}`;
  });
  // ── Store: custom reactive store ──
  const { subscribe, set, update } = (() => {
    let internal = $state(0);
    return {
      subscribe: (fn) => $effect(() => fn(internal)),
      set: (v) => { internal = v; },
      update: (fn) => { internal = fn(internal); }
    };
  })();
  // ── Action: custom Svelte action (click-outside) ──
  function clickOutside(node, onEvent) {
    const handler = (e) => {
      if (!node.contains(e.target)) onEvent(e);
    };
    document.addEventListener('click', handler);
    return {
      destroy() { document.removeEventListener('click', handler); },
      update(newHandler) { onEvent = newHandler; }
    };
  }
  let panelOpen = $state(false);
</script>
<!-- ── Transition: Svelte transition (fly + scale) ── -->
{#if panelOpen}
  <div
    use:clickOutside={() => (panelOpen = false)}
    transition:fly={{ y: 20, duration: 300 }}
    in:scale={{ start: 0.9, duration: 200 }}
    class="panel"
  >
    <p>Doubled: {doubled}</p>
    <button onclick={() => count++}>Increment</button>
    <button onclick={() => update((n) => n + 1)}>Store +1</button>
  </div>
{/if}
<button onclick={() => (panelOpen = !panelOpen)}>
  Toggle Panel (Count: {count})
</button>
<style>
  .panel {
    background: #1e293b;
    color: #e2e8f0;
    padding: 1rem;
    border-radius: 8px;
    margin-top: 0.5rem;
  }
  button {
    background: #3b82f6;
    color: #fff;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 4px;
    cursor: pointer;
  }
</style>
```