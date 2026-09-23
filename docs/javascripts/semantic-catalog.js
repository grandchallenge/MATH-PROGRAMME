(() => {
  const root = document.getElementById("semantic-catalog");
  if (!root) return;

  const controls = {
    query: document.getElementById("catalog-query"),
    provider: document.getElementById("catalog-provider"),
    msc: document.getElementById("catalog-msc"),
    status: document.getElementById("catalog-status"),
    language: document.getElementById("catalog-language"),
    assurance: document.getElementById("catalog-assurance"),
    campaign: document.getElementById("catalog-campaign"),
  };
  const summary = document.getElementById("catalog-summary");
  const results = document.getElementById("catalog-results");
  let entries = [];

  const values = (field) => [...new Set(entries.flatMap((entry) => Array.isArray(entry[field]) ? entry[field] : [entry[field]]).filter(Boolean))].sort();
  const fill = (name, field) => values(field).forEach((value) => controls[name].add(new Option(value, value)));
  const escapeHtml = (value) => String(value).replace(/[&<>"]/g, (character) => ({"&": "&amp;", "<": "&lt;", ">": "&gt;", "\"": "&quot;"})[character]);
  const has = (entry, field, wanted) => !wanted || (Array.isArray(entry[field]) ? entry[field].includes(wanted) : entry[field] === wanted);

  function render() {
    const query = controls.query.value.trim().toLowerCase();
    const matches = entries.filter((entry) => {
      const text = [entry.id, entry.title, entry.provider, entry.msc, ...(entry.status || []), ...(entry.campaign || [])].join(" ").toLowerCase();
      return (!query || text.includes(query))
        && has(entry, "provider", controls.provider.value)
        && has(entry, "msc", controls.msc.value)
        && has(entry, "status", controls.status.value)
        && has(entry, "language", controls.language.value)
        && has(entry, "assurance", controls.assurance.value)
        && has(entry, "campaign", controls.campaign.value);
    });
    summary.textContent = `${matches.length.toLocaleString()} of ${entries.length.toLocaleString()} protected catalog entries`;
    results.innerHTML = matches.slice(0, 100).map((entry) => `
      <article class="catalog-entry">
        <div><strong>${escapeHtml(entry.title)}</strong></div>
        <div><code>${escapeHtml(entry.id)}</code> · ${escapeHtml(entry.provider)} · ${escapeHtml(entry.msc || "MSC unresolved")}</div>
        <div><span class="catalog-badge">${escapeHtml(entry.assurance)}</span>${entry.language ? ` <span class="catalog-badge">${escapeHtml(entry.language)}</span>` : ""}</div>
        ${entry.status?.length ? `<div>Attributed status: ${escapeHtml(entry.status.join(", "))}</div>` : ""}
        ${entry.campaign?.length ? `<div>Reviewed campaign relation: ${escapeHtml(entry.campaign.join(", "))}</div>` : ""}
        <small>${escapeHtml(entry.warning)}</small>
      </article>`).join("");
    if (matches.length > 100) results.insertAdjacentHTML("beforeend", `<p>Showing the first 100 matches. Narrow the filters to inspect the remaining ${(matches.length - 100).toLocaleString()}.</p>`);
  }

  fetch(root.dataset.index)
    .then((response) => { if (!response.ok) throw new Error(`HTTP ${response.status}`); return response.json(); })
    .then((payload) => {
      entries = payload.entries;
      fill("provider", "provider"); fill("msc", "msc"); fill("status", "status");
      fill("language", "language"); fill("assurance", "assurance"); fill("campaign", "campaign");
      Object.values(controls).forEach((control) => control.addEventListener("input", render));
      render();
    })
    .catch((error) => { summary.textContent = `Catalog metadata could not be loaded: ${error.message}`; });
})();
