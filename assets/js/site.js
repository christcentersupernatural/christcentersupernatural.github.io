/* ==========================================================================
   Men of the Spirit — motion
   One orchestrated entrance per page: the beam settles, the name comes into
   focus, gold passes across it, the flourish is drawn. Everything after
   that is quiet.
   ========================================================================== */

(function () {
  "use strict";

  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------------------------------------------------------------- beam */

  function beam(canvas) {
    var ctx = canvas.getContext("2d");
    var w = 0, h = 0, dpr = Math.min(window.devicePixelRatio || 1, 2);
    var motes = [];
    var scrollY = 0;

    function size() {
      w = window.innerWidth;
      h = window.innerHeight;
      canvas.width = w * dpr;
      canvas.height = h * dpr;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    }

    for (var i = 0; i < 110; i++) {
      motes.push({
        x: Math.random(),
        y: Math.random(),
        r: Math.random() * 1.5 + 0.3,
        speed: Math.random() * 0.00016 + 0.00004,
        drift: Math.random() * Math.PI * 2,
        alpha: Math.random() * 0.5 + 0.14
      });
    }

    function paint(t) {
      ctx.clearRect(0, 0, w, h);

      /* Ground, with the hall falling away toward the floor. */
      var ground = ctx.createLinearGradient(0, 0, 0, h);
      ground.addColorStop(0, "#080a16");
      ground.addColorStop(1, "#04050c");
      ctx.fillStyle = ground;
      ctx.fillRect(0, 0, w, h);

      /* The shaft drifts slowly, and leans as the reader scrolls. */
      var lean = Math.min(scrollY / Math.max(h, 1), 1.4);
      var cx = w / 2 + Math.sin(t * 0.16) * w * 0.025 - lean * w * 0.06;
      var top = w * 0.055;
      var base = w * 0.44;

      var cone = ctx.createLinearGradient(0, 0, 0, h);
      cone.addColorStop(0, "rgba(226,222,238,.17)");
      cone.addColorStop(0.5, "rgba(216,206,232,.062)");
      cone.addColorStop(1, "rgba(210,200,228,0)");
      ctx.fillStyle = cone;
      ctx.beginPath();
      ctx.moveTo(cx - top, -20);
      ctx.lineTo(cx + top, -20);
      ctx.lineTo(cx + base, h);
      ctx.lineTo(cx - base, h);
      ctx.closePath();
      ctx.fill();

      /* Warm pool where the light lands. */
      var pool = ctx.createRadialGradient(
        cx, h * 0.66, 0, cx, h * 0.66, w * 0.5);
      pool.addColorStop(0, "rgba(201,164,76,.085)");
      pool.addColorStop(0.55, "rgba(160,150,190,.03)");
      pool.addColorStop(1, "rgba(0,0,0,0)");
      ctx.fillStyle = pool;
      ctx.fillRect(0, 0, w, h);

      /* Dust: bright inside the shaft, barely there outside it. */
      for (var i = 0; i < motes.length; i++) {
        var m = motes[i];
        m.y -= m.speed * 16;
        m.drift += 0.008;
        if (m.y < -0.06) { m.y = 1.06; m.x = Math.random(); }

        var px = m.x * w + Math.sin(m.drift) * 12;
        var py = m.y * h;
        var half = top + (py / h) * (base - top);
        var lit = Math.abs(px - cx) < half;

        ctx.beginPath();
        ctx.arc(px, py, m.r, 0, Math.PI * 2);
        ctx.fillStyle = "rgba(242,236,224," +
          (lit ? m.alpha : m.alpha * 0.1).toFixed(3) + ")";
        ctx.fill();
      }
    }

    size();
    window.addEventListener("resize", size);
    window.addEventListener("scroll", function () {
      scrollY = window.scrollY || 0;
    }, { passive: true });

    if (reduce) { paint(0); return; }

    var start = performance.now();
    (function frame(now) {
      paint((now - start) / 1000);
      requestAnimationFrame(frame);
    })(start);
  }

  /* ------------------------------------------------------------ entrance */

  function play(el, frames, options) {
    if (!el) { return; }
    if (reduce) {
      var last = frames[frames.length - 1];
      Object.keys(last).forEach(function (k) { el.style[k] = last[k]; });
      return;
    }
    el.animate(frames, Object.assign({ fill: "forwards" }, options));
  }

  var RISE = [
    { opacity: 0, transform: "translateY(12px)" },
    { opacity: 1, transform: "translateY(0)" }
  ];
  var EASE = "cubic-bezier(.2,.7,.2,1)";

  function entrance(root) {
    var title = root.querySelector("[data-focus]");
    var words = title ? title.querySelectorAll(".w") : [];

    play(root.querySelector("[data-step='eyebrow']"), RISE,
      { duration: 900, delay: 120, easing: EASE });

    /* The name comes into focus one word at a time, as a lens would. */
    for (var i = 0; i < words.length; i++) {
      play(words[i], [
        { opacity: 0, filter: "blur(16px)", transform: "translateY(12px)" },
        { opacity: 1, filter: "blur(0px)", transform: "translateY(0)" }
      ], { duration: 1400, delay: 300 + i * 210, easing: EASE });
    }

    if (title) {
      play(title,
        [{ backgroundPosition: "130% 0" }, { backgroundPosition: "-45% 0" }],
        {
          duration: 2600,
          delay: 480 + words.length * 210,
          easing: "cubic-bezier(.36,.05,.2,1)"
        });
    }

    var path = root.querySelector(".flourish path");
    if (path && !reduce) {
      var len = path.getTotalLength();
      path.style.strokeDasharray = len;
      path.style.strokeDashoffset = len;
      path.animate(
        [{ strokeDashoffset: len }, { strokeDashoffset: 0 }],
        { duration: 1700, delay: 900, easing: "ease-in-out",
          fill: "forwards" });
    }

    ["role", "cue"].forEach(function (step, n) {
      play(root.querySelector("[data-step='" + step + "']"), RISE,
        { duration: 1100, delay: 1250 + n * 450, easing: EASE });
    });
  }

  /* ------------------------------------------------------------- reveals */

  function reveals() {
    var items = document.querySelectorAll(".reveal");
    if (!items.length) { return; }
    if (reduce || !("IntersectionObserver" in window)) {
      items.forEach(function (el) { el.classList.add("in"); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) { return; }
        entry.target.classList.add("in");
        io.unobserve(entry.target);
      });
    }, { threshold: 0.16, rootMargin: "0px 0px -8% 0px" });
    items.forEach(function (el, i) {
      el.style.transitionDelay = (i % 4) * 90 + "ms";
      io.observe(el);
    });
  }

  /* -------------------------------------------------------- plaque light */

  function plaques() {
    document.querySelectorAll(".plaque").forEach(function (card) {
      card.addEventListener("pointermove", function (e) {
        var box = card.getBoundingClientRect();
        card.style.setProperty("--px", (e.clientX - box.left) + "px");
        card.style.setProperty("--py", (e.clientY - box.top) + "px");
      });
    });
  }

  /* Wrap each word of a title so it can be focused independently. */
  function splitWords() {
    document.querySelectorAll("[data-focus]").forEach(function (el) {
      var words = el.textContent.trim().split(/\s+/);
      el.textContent = "";
      words.forEach(function (word, i) {
        var span = document.createElement("span");
        span.className = "w";
        span.textContent = word;
        el.appendChild(span);
        if (i < words.length - 1) {
          el.appendChild(document.createTextNode(" "));
        }
      });
    });
  }

  function init() {
    var canvas = document.querySelector(".beam");
    if (canvas) { beam(canvas); }
    splitWords();
    entrance(document);
    reveals();
    plaques();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
