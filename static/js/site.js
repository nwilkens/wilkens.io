(function () {
  var header = document.getElementById("site-header");
  var scrolled = ["bg-background/80", "backdrop-blur-md", "border-b", "border-border"];
  var progress = document.getElementById("reading-progress");

  function onScroll() {
    var past = window.scrollY > 20;
    header.classList.toggle("bg-transparent", !past);
    scrolled.forEach(function (c) { header.classList.toggle(c, past); });
    if (progress) {
      var max = document.documentElement.scrollHeight - window.innerHeight;
      progress.style.width = (max > 0 ? Math.min(100, (window.scrollY / max) * 100) : 0) + "%";
    }
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  var toggle = document.getElementById("nav-toggle");
  var menu = document.getElementById("mobile-navigation");
  toggle.addEventListener("click", function () {
    var open = menu.hidden;
    menu.hidden = !open;
    toggle.setAttribute("aria-expanded", String(open));
    toggle.setAttribute("aria-label", open ? "Close navigation" : "Open navigation");
    toggle.querySelector('[data-nav-icon="open"]').hidden = open;
    toggle.querySelector('[data-nav-icon="close"]').hidden = !open;
  });

  var filters = document.getElementById("project-filters");
  if (filters) {
    var on = filters.dataset.on.split(" ");
    var off = filters.dataset.off.split(" ");
    filters.addEventListener("click", function (e) {
      var button = e.target.closest("button[data-tag]");
      if (!button) return;
      filters.querySelectorAll("button[data-tag]").forEach(function (b) {
        var active = b === button;
        off.forEach(function (c) { b.classList.toggle(c, !active); });
        on.forEach(function (c) { b.classList.toggle(c, active); });
      });
      document.querySelectorAll("[data-project]").forEach(function (card) {
        var tags = JSON.parse(card.dataset.tags);
        card.hidden = button.dataset.tag !== "" && tags.indexOf(button.dataset.tag) === -1;
      });
    });
  }
})();
