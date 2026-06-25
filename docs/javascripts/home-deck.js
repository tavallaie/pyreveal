/**
 * Keep keyboard navigation working when the demo runs inside the docs home iframe.
 */
(function () {
  const frame = document.querySelector(".mdx-home-deck");
  if (!frame) {
    return;
  }

  const focusFrame = () => frame.focus({ preventScroll: true });

  const NAV_KEYS = new Set([
    "ArrowLeft",
    "ArrowRight",
    "ArrowUp",
    "ArrowDown",
    " ",
    "PageUp",
    "PageDown",
    "Home",
    "End",
  ]);

  frame.addEventListener("load", focusFrame);
  focusFrame();

  document.addEventListener(
    "keydown",
    (event) => {
      if (!NAV_KEYS.has(event.key) || document.activeElement === frame) {
        return;
      }
      focusFrame();
    },
    true
  );
})();