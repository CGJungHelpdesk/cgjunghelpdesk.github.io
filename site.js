// ─────────────────────────────────────────────────────────────────────────
// The one line to change when the app is live: paste the App Store link.
// Example: "https://apps.apple.com/app/jung-helpdesk/id1234567890"
const APP_STORE_URL = "https://apps.apple.com/app/jung-helpdesk/id6806770673";
// ─────────────────────────────────────────────────────────────────────────

for (const link of document.querySelectorAll("[data-store]")) {
  if (APP_STORE_URL) {
    link.href = APP_STORE_URL;
    link.textContent = "Download on the App Store";
  } else {
    link.setAttribute("aria-disabled", "true");
    link.removeAttribute("href");
  }
}
for (const link of document.querySelectorAll(".nav-cta")) {
  if (APP_STORE_URL) link.href = APP_STORE_URL;
}

// A quiet star field behind the hero, in the map's territory colours.
const canvas = document.getElementById("sky");
if (canvas) {
  const ctx = canvas.getContext("2d");
  const colours = ["#D4A95E", "#C48FB4", "#6FBFB4", "#D48A6E", "#9DB878", "#7C756B"];
  const still = matchMedia("(prefers-reduced-motion: reduce)").matches;
  let stars = [], w = 0, h = 0;

  function resize() {
    const ratio = Math.min(devicePixelRatio || 1, 2);
    w = canvas.clientWidth; h = canvas.clientHeight;
    canvas.width = w * ratio; canvas.height = h * ratio;
    ctx.setTransform(ratio, 0, 0, ratio, 0, 0);
    const count = Math.round(Math.min(70, (w * h) / 16000));
    stars = Array.from({ length: count }, (_, i) => ({
      x: Math.random() * w, y: Math.random() * h,
      r: 1 + Math.random() * 2.2, c: colours[i % colours.length],
      vx: (Math.random() - 0.5) * 0.08, vy: (Math.random() - 0.5) * 0.08,
    }));
  }

  function draw() {
    ctx.clearRect(0, 0, w, h);
    ctx.lineWidth = 1;
    for (let i = 0; i < stars.length; i++) {
      for (let j = i + 1; j < stars.length; j++) {
        const a = stars[i], b = stars[j];
        const d = Math.hypot(a.x - b.x, a.y - b.y);
        if (d < 120) {
          ctx.strokeStyle = `rgba(124,117,107,${0.22 * (1 - d / 120)})`;
          ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.stroke();
        }
      }
    }
    for (const s of stars) {
      ctx.globalAlpha = 0.55; ctx.fillStyle = s.c;
      ctx.beginPath(); ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2); ctx.fill();
      if (!still) {
        s.x += s.vx; s.y += s.vy;
        if (s.x < 0 || s.x > w) s.vx *= -1;
        if (s.y < 0 || s.y > h) s.vy *= -1;
      }
    }
    ctx.globalAlpha = 1;
    if (!still) requestAnimationFrame(draw);
  }

  resize(); draw();
  addEventListener("resize", () => { resize(); if (still) draw(); });
}
