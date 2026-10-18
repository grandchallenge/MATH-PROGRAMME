// Load MathJax only on MkDocs pages with Arithmatex-generated math.
// Documentary pages already include their own pinned MathJax loader.
(() => {
  if (!document.querySelector(".arithmatex")) return;
  if (document.querySelector('script[src*="tex-mml-chtml.js"]')) return;

  window.MathJax = {
    tex: {
      inlineMath: [["\\(", "\\)"]],
      displayMath: [["\\[", "\\]"]],
      processEscapes: true,
      tags: "none"
    },
    options: {
      ignoreHtmlClass: ".*",
      processHtmlClass: "arithmatex"
    }
  };

  const script = document.createElement("script");
  script.src = "https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-mml-chtml.js";
  script.defer = true;
  script.crossOrigin = "anonymous";
  script.referrerPolicy = "no-referrer";
  document.head.appendChild(script);
})();
