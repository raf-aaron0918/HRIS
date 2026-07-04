export function extractModuleMarkup(rawHtml) {
  const match = rawHtml.match(
    /<div class="row g-3">[\s\S]*?(?=\n\s*<\/div>\s*<\/div>\s*<\/div>\s*<!-- \[ Main Content \] end -->)/
  );
  return match ? match[0] : "";
}

export function extractInlineScript(rawHtml) {
  const matches = [...rawHtml.matchAll(/<script(?:[^>]*)>([\s\S]*?)<\/script>/g)];
  if (!matches.length) {
    return "";
  }
  return matches[matches.length - 1][1] || "";
}

function createScopedDocument(root) {
  return {
    body: document.body,
    createElement: (...args) => document.createElement(...args),
    getElementById: (id) => root.querySelector(`#${id}`),
    querySelector: (selector) => root.querySelector(selector),
    querySelectorAll: (selector) => root.querySelectorAll(selector),
    addEventListener: (...args) => document.addEventListener(...args),
    removeEventListener: (...args) => document.removeEventListener(...args),
  };
}

function buildScope(root, extraScope = {}) {
  const scope = {
    window,
    document: createScopedDocument(root),
    console,
    Blob,
    URL,
    Math,
    Date,
    setTimeout,
    clearTimeout,
    setInterval,
    clearInterval,
    performance,
    navigator,
    ...extraScope,
  };

  root.querySelectorAll("[id]").forEach((element) => {
    scope[element.id] = element;
  });

  return scope;
}

export function mountLegacyModule(root, rawHtml, extraScope = {}) {
  const markup = extractModuleMarkup(rawHtml);
  const script = extractInlineScript(rawHtml);

  root.innerHTML = markup;

  if (!script.trim()) {
    return;
  }

  const scope = buildScope(root, extraScope);
  const runner = new Function("scope", `with (scope) { ${script} }`);
  runner(scope);
}
