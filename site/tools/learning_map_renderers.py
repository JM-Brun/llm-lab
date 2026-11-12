"""Reader-facing renderers for the learning map.

This module owns the *form* of the learning map; ``build_learning_map.py``
owns its *structure*. Every representation of the structure extracted from
the authored Quarto sidebar and page metadata is rendered here so that:

- structure and presentation evolve independently;
- adding a representation means writing one render function and registering
  it in ``REPRESENTATIONS``, without touching the extraction code;
- all reader-facing copy lives in one bilingual dictionary (``COPY``) shared
  by the interactive script, the page shell, and the static list.
"""

from __future__ import annotations

import html
import json
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from typing import Any

COPY: dict[str, dict[str, Any]] = {
    "fr": {
        "viewLabel": "Vue",
        "modePages": "Carte des territoires",
        "modeConcepts": "Notions canoniques",
        "detailsSummary": "Détails",
        "rootIntro": "Choisissez un territoire à explorer, puis affinez rubrique par rubrique.",
        "rootCrumb": "Tous les territoires",
        "backLabel": "Retour aux territoires",
        "pagesUnit": "page",
        "pagesUnitPlural": "pages",
        "territoriesUnit": "territoires",
        "notionsUnit": "notions",
        "notionsUnitSingular": "notion",
        "sectionsLabel": "Rubriques",
        "pagesLabel": "Pages",
        "searchPlaceholderPages": "Filtrer les pages…",
        "searchPlaceholderConcepts": "Filtrer les notions…",
        "searchLabel": "Rechercher dans la carte",
        "loading": "Chargement de la carte…",
        "loadError": "Impossible de charger les données de la carte.",
        "retry": "Réessayer",
        "noResults": "Aucun résultat pour cette recherche.",
        "conceptMatchesHint": "Voir aussi {count} notion(s) dans la vue « Notions canoniques ».",
        "emptyDetails": "Cliquez sur une page ou une notion pour afficher ses détails ici.",
        "crumbsLabel": "Fil d'Ariane",
        "openPage": "Ouvrir la page",
        "asideHint": "Un clic sélectionne sans naviguer ; « Ouvrir la page » ouvre la ressource.",
        "suggestedNext": "Étape suivante suggérée",
        "suggestedPrevious": "Étape précédente suggérée",
        "relatedPages": "Pages liées",
        "relatedConcepts": "Notions liées",
        "sectionHeadingsTitle": "Dans cette page",
        "conceptResources": "Pages associées",
        "relationLegendTitle": "Sens des relations (source → cible)",
        "relationFilterLabel": "Type de relation",
        "relationFilterAll": "Tous les types",
        "relationFamilies": {
            "representational": "Représentation",
            "pedagogical": "Apprentissage",
            "structural": "Structure",
            "constraint": "Contrainte",
            "functional": "Fonctionnement",
            "associative": "Associations",
            "evaluative": "Évaluation",
        },
        "resetView": "Réinitialiser la vue",
        "resetHint": "Efface recherche, filtre et sélection ; Échap remonte d'un niveau à la fois.",
        "copyLink": "Copier le lien",
        "copyHint": "Copie l'URL de la vue courante (recherche, filtre, sélection).",
        "linkCopied": "Lien copié.",
        "linkCopyFailed": "Copie impossible : copiez l'URL depuis la barre d'adresse.",
        "ungroupedConcepts": "Autres notions",
        "hiddenRelations": "{count} relation(s) masquée(s) par la recherche ou le filtre.",
        "viewConcept": "Voir la notion",
        "importanceLabels": {
            "core": "Essentielle",
            "supporting": "Complémentaire",
            "specialized": "Spécialisée",
        },
        "statusLoaded": "Carte chargée.",
        "destinations": {
            "orient": "Parcours et carte des ressources",
            "understand": "Comprendre",
            "build": "Construire",
            "deepen": "Approfondir",
            "practice": "S'exercer",
            "reference": "Références",
        },
    },
    "en": {
        "viewLabel": "View",
        "modePages": "Territory map",
        "modeConcepts": "Canonical concepts",
        "detailsSummary": "Details",
        "rootIntro": "Pick a territory to explore, then drill down section by section.",
        "rootCrumb": "All territories",
        "backLabel": "Back to territories",
        "pagesUnit": "page",
        "pagesUnitPlural": "pages",
        "territoriesUnit": "territories",
        "notionsUnit": "concepts",
        "notionsUnitSingular": "concept",
        "sectionsLabel": "Sections",
        "pagesLabel": "Pages",
        "searchPlaceholderPages": "Filter pages…",
        "searchPlaceholderConcepts": "Filter concepts…",
        "searchLabel": "Search the map",
        "loading": "Loading the map…",
        "loadError": "Could not load the map data.",
        "retry": "Retry",
        "noResults": "No results for this search.",
        "conceptMatchesHint": "See also {count} concept(s) in the “Canonical concepts” view.",
        "emptyDetails": "Click a page or a concept to see its details here.",
        "crumbsLabel": "Breadcrumb",
        "openPage": "Open the page",
        "asideHint": "Clicking selects in place; use “Open the page” to open the resource.",
        "suggestedNext": "Suggested next step",
        "suggestedPrevious": "Suggested previous step",
        "relatedPages": "Related pages",
        "relatedConcepts": "Related concepts",
        "sectionHeadingsTitle": "On this page",
        "conceptResources": "Pages covering this concept",
        "relationLegendTitle": "Relationship meaning (source → target)",
        "relationFilterLabel": "Relation type",
        "relationFilterAll": "All types",
        "relationFamilies": {
            "representational": "Representation",
            "pedagogical": "Learning",
            "structural": "Structure",
            "constraint": "Constraint",
            "functional": "Functioning",
            "associative": "Associations",
            "evaluative": "Evaluation",
        },
        "resetView": "Reset view",
        "resetHint": "Clears search, filter, and selection; Escape steps back one level at a time.",
        "copyLink": "Copy link",
        "copyHint": "Copy the URL of the current view (search, filter, selection).",
        "linkCopied": "Link copied.",
        "linkCopyFailed": "Could not copy: copy the URL from the address bar.",
        "ungroupedConcepts": "Other concepts",
        "hiddenRelations": "{count} relation(s) hidden by the search or filter.",
        "viewConcept": "Show concept",
        "importanceLabels": {
            "core": "Core",
            "supporting": "Supporting",
            "specialized": "Specialized",
        },
        "statusLoaded": "Map loaded.",
        "destinations": {
            "orient": "Learning paths and resource map",
            "understand": "Understand",
            "build": "Build",
            "deepen": "Go deeper",
            "practice": "Practice",
            "reference": "Reference",
        },
    },
}

GENERATED_FILE_NOTE = (
    "<!-- Generated by site/tools/build_learning_map.py; do not edit by hand. -->\n"
)

PROGRESSIVE_MAP_TEMPLATE = r"""<script>
(function () {
  "use strict";

  var DESTINATIONS = ["orient", "understand", "build", "deepen", "practice", "reference"];

  var COPY = __LEARNING_MAP_COPY__;

  function ready(run) {
    if (document.readyState !== "loading") {
      run();
    } else {
      document.addEventListener("DOMContentLoaded", run);
    }
  }

  function el(tag, className, text) {
    var node = document.createElement(tag);
    if (className) {
      node.className = className;
    }
    if (text !== undefined) {
      node.textContent = text;
    }
    return node;
  }

  function appendMarkedText(node, text, query) {
    if (!query) {
      node.appendChild(document.createTextNode(text));
      return;
    }
    var haystack = text.toLowerCase();
    var needle = query.toLowerCase();
    var cursor = 0;
    var index = haystack.indexOf(needle);
    while (index >= 0) {
      if (index > cursor) {
        node.appendChild(document.createTextNode(text.slice(cursor, index)));
      }
      node.appendChild(el("mark", "map-mark", text.slice(index, index + needle.length)));
      cursor = index + needle.length;
      index = haystack.indexOf(needle, cursor);
    }
    if (cursor < text.length) {
      node.appendChild(document.createTextNode(text.slice(cursor)));
    }
  }

  function detectLanguage() {
    var lang = String(document.documentElement.lang || "").slice(0, 2).toLowerCase();
    if (lang !== "fr" && lang !== "en") {
      lang = /\/fr\//.test(window.location.pathname) ? "fr" : "en";
    }
    return lang;
  }

  ready(function () {
    var roots = document.querySelectorAll("[data-learning-map]");
    for (var index = 0; index < roots.length; index += 1) {
      init(roots[index]);
    }
  });

  function init(root) {
    var viewport = root.querySelector("[data-map-viewport]");
    var modeSelect = root.querySelector("[data-map-mode]");
    var searchInput = root.querySelector("[data-map-search]");
    var detailPanel = root.querySelector("[data-map-detail-panel]");
    var statusLine = root.querySelector("[data-map-status]");
    var conceptLegend = root.querySelector(".learning-map-concept-legend");
    var relationFilter = root.querySelector("[data-map-relation-type]");
    var resetButton = root.querySelector("[data-map-reset]");
    var copyButton = root.querySelector("[data-map-copy]");
    if (!viewport || !modeSelect || !searchInput || !detailPanel) {
      return;
    }

    var lang = root.getAttribute("data-language") || detectLanguage();
    if (COPY[lang] === undefined) {
      lang = detectLanguage();
    }
    var copy = COPY[lang];
    var dataSource = root.getAttribute("data-source") || "../learning-map-data-" + lang + ".json";
    var state = {
      mode: "pages",
      areaId: null,
      query: "",
      relationType: "",
      conceptId: null,
      pageId: null,
    };
    var data = null;
    var pageById = {};
    var conceptById = {};
    var areas = [];
    var relationTypes = {};
    var conceptDomainList = [];
    var retryReload = false;
    var commitNextSync = false;
    var searchTimer = null;
    readStateFromHash();
    modeSelect.value = state.mode;
    if (state.query) {
      searchInput.value = state.query;
    }

    updateSearchPlaceholder();
    searchInput.setAttribute("aria-label", copy.searchLabel);
    renderPlaceholder();

    function setStatus(text) {
      if (statusLine) {
        statusLine.textContent = text;
      }
    }

    function clearNode(node) {
      while (node.firstChild) {
        node.removeChild(node.firstChild);
      }
    }

    function renderPlaceholder() {
      clearNode(detailPanel);
      detailPanel.appendChild(el("p", "map-empty", copy.emptyDetails));
    }

    function updateSearchPlaceholder() {
      searchInput.setAttribute(
        "placeholder",
        state.mode === "concepts" ? copy.searchPlaceholderConcepts : copy.searchPlaceholderPages
      );
    }

    function readStateFromHash() {
      if (!window.location.hash || window.location.hash.indexOf("=") === -1) {
        return;
      }
      window.location.hash.slice(1).split("&").forEach(function (part) {
        var pair = part.split("=");
        var key = pair[0];
        var value = pair.slice(1).join("=");
        if (key === "mode" && value === "concepts") {
          state.mode = "concepts";
        } else if (key === "q") {
          try {
            state.query = decodeURIComponent(value);
          } catch (error) {
            state.query = value;
          }
        } else if (key === "area") {
          state.areaId = value;
        } else if (key === "page") {
          state.pageId = value;
        } else if (key === "concept") {
          state.conceptId = value;
        } else if (key === "rel") {
          state.relationType = value;
        }
      });
    }

    function applyHashToState() {
      state.mode = "pages";
      state.query = "";
      state.relationType = "";
      state.areaId = null;
      state.conceptId = null;
      state.pageId = null;
      readStateFromHash();
    }

    function syncStateToHash(commit) {
      var params = [];
      if (state.mode === "concepts") {
        params.push("mode=concepts");
      }
      if (state.query) {
        params.push("q=" + encodeURIComponent(state.query));
      }
      if (state.mode === "pages" && state.areaId) {
        params.push("area=" + state.areaId);
      }
      if (state.mode === "pages" && state.pageId) {
        params.push("page=" + encodeURIComponent(state.pageId));
      }
      if (state.mode === "concepts" && state.relationType) {
        params.push("rel=" + state.relationType);
      }
      if (state.mode === "concepts" && state.conceptId) {
        params.push("concept=" + state.conceptId);
      }
      var hash = params.length ? "#" + params.join("&") : "";
      var current = window.location.hash;
      // Map state always contains "="; any other fragment is an in-page
      // anchor (a guided stage or a heading) that the browser must keep.
      if (!hash && current && current.indexOf("=") === -1) {
        return;
      }
      if (current !== hash) {
        if (commit) {
          window.history.pushState(
            null,
            "",
            hash || window.location.pathname + window.location.search
          );
        } else {
          window.history.replaceState(
            null,
            "",
            hash || window.location.pathname + window.location.search
          );
        }
      }
    }

    function load() {
      var inline = document.querySelector('script[data-map-data]');
      if (inline) {
        try {
          hydrate(JSON.parse(inline.textContent));
        } catch (error) {
          // Malformed inline data falls back to the JSON request below.
        }
      }
      if (!data) {
        fetchMapData();
      }
    }

    function fetchMapData() {
      setStatus(copy.loading);
      window
        .fetch(dataSource)
        .then(function (response) {
          if (!response.ok) {
            throw new Error("HTTP " + response.status);
          }
          return response.json();
        })
        .then(hydrate)
        .catch(function () {
          clearNode(viewport);
          viewport.appendChild(el("p", "map-load-error", copy.loadError));
          var retry = el("button", "map-back", copy.retry);
          retry.type = "button";
          retry.addEventListener("click", function () {
            retryReload = true;
            load();
          });
          viewport.appendChild(retry);
        });
    }

    function hydrate(payload) {
      data = payload;
      pageById = {};
      for (var i = 0; i < data.pages.length; i += 1) {
        pageById[data.pages[i].id] = data.pages[i];
      }
      conceptById = {};
      var concepts = data.concepts || [];
      for (var j = 0; j < concepts.length; j += 1) {
        conceptById[concepts[j].id] = concepts[j];
      }
      if (state.conceptId && !conceptById[state.conceptId]) {
        state.conceptId = null;
      }
      if (state.pageId && !pageById[state.pageId]) {
        state.pageId = null;
      }
      areas = normalizeAreas(data.navigation || []);
      relationTypes = data.concept_relation_types || {};
      conceptDomainList = data.concept_domains || [];
      render();
      fillRelationFilter();
      if (state.conceptId) {
        showConceptDetails(state.conceptId);
      } else if (state.mode === "pages" && state.pageId) {
        showPageDetails(state.pageId);
      }
      setStatus(loadedSummary());
      if (retryReload) {
        retryReload = false;
        modeSelect.focus();
      }
    }

    function loadedSummary() {
      return (
        copy.statusLoaded +
        " " +
        data.pages.length +
        " " +
        (data.pages.length > 1 ? copy.pagesUnitPlural : copy.pagesUnit) +
        " · " +
        areas.length +
        " " +
        copy.territoriesUnit
      );
    }

    function appendRelationOption(parent, kind) {
      var option = el("option", null, relationTypes[kind].label);
      option.value = kind;
      parent.appendChild(option);
    }

    function fillRelationFilter() {
      if (!relationFilter) {
        return;
      }
      clearNode(relationFilter);
      var allOption = el("option", null, copy.relationFilterAll);
      allOption.value = "";
      relationFilter.appendChild(allOption);
      var groupedKinds = [];
      Object.keys(copy.relationFamilies).forEach(function (family) {
        var kinds = Object.keys(relationTypes).filter(function (kind) {
          return relationTypes[kind].family === family;
        });
        if (!kinds.length) {
          return;
        }
        groupedKinds = groupedKinds.concat(kinds);
        var group = el("optgroup", null);
        group.label = copy.relationFamilies[family];
        kinds.forEach(function (kind) {
          appendRelationOption(group, kind);
        });
        relationFilter.appendChild(group);
      });
      Object.keys(relationTypes).forEach(function (kind) {
        if (groupedKinds.indexOf(kind) < 0) {
          appendRelationOption(relationFilter, kind);
        }
      });
      relationFilter.value = state.relationType;
    }

    function normalizeAreas(navigation) {
      if (navigation.length) {
        return navigation.map(function (area) {
          return {
            id: area.id,
            title: area.title,
            pages: area.pages || [],
            sections: area.sections || [],
            destination: areaDestination(area),
          };
        });
      }
      var fallback = {};
      for (var d = 0; d < DESTINATIONS.length; d += 1) {
        fallback[DESTINATIONS[d]] = [];
      }
      var ordered = (data.pages || []).slice().sort(function (a, b) {
        return (a.rank === undefined ? 9999 : a.rank) - (b.rank === undefined ? 9999 : b.rank);
      });
      ordered.forEach(function (page) {
        var key = DESTINATIONS.indexOf(page.destination) >= 0 ? page.destination : "reference";
        fallback[key].push(page.id);
      });
      return DESTINATIONS.filter(function (destination) {
        return fallback[destination].length > 0;
      }).map(function (destination) {
        return {
          id: destination,
          title: copy.destinations[destination],
          pages: fallback[destination],
          sections: [],
          destination: destination,
        };
      });
    }

    function forEachSection(sections, visit) {
      (sections || []).forEach(function (section) {
        visit(section);
        forEachSection(section.sections, visit);
      });
    }

    function areaDestination(area) {
      var ids = (area.pages || []).slice();
      forEachSection(area.sections, function (section) {
        ids = ids.concat(section.pages || []);
      });
      for (var i = 0; i < ids.length; i += 1) {
        var page = pageById[ids[i]];
        if (page) {
          return page.destination;
        }
      }
      return "reference";
    }

    function countSectionPages(section) {
      var total = (section.pages || []).length;
      (section.sections || []).forEach(function (child) {
        total += countSectionPages(child);
      });
      return total;
    }

    function countAreaPages(area) {
      var total = (area.pages || []).length;
      forEachSection(area.sections, function (section) {
        total += (section.pages || []).length;
      });
      return total;
    }

    function chipFor(pageId) {
      var page = pageById[pageId];
      if (!page) {
        return null;
      }
      var chip = el("a", "map-chip", page.title);
      chip.href = page.href;
      chip.setAttribute("data-destination", page.destination);
      chip.setAttribute("data-page-id", page.id);
      if (state.pageId === page.id) {
        chip.setAttribute("aria-current", "true");
      }
      chip.addEventListener("click", function (event) {
        if (event.button === 0 && !event.metaKey && !event.ctrlKey && !event.shiftKey) {
          event.preventDefault();
          showPageDetails(page.id, detailPanel.contains(event.currentTarget));
        }
      });
      return chip;
    }

    function markCurrentChip() {
      var chips = viewport.querySelectorAll("[data-page-id]");
      for (var i = 0; i < chips.length; i += 1) {
        if (chips[i].getAttribute("data-page-id") === state.pageId) {
          chips[i].setAttribute("aria-current", "true");
        } else {
          chips[i].removeAttribute("aria-current");
        }
      }
    }

    function matchesQuery(page, query) {
      var haystack = [
        page.title,
        page.summary,
        page.purpose,
        page.topic,
        (page.section_headings || []).join(" "),
      ].join(" ");
      return haystack.toLowerCase().indexOf(query) >= 0;
    }

    function render() {
      clearNode(viewport);
      updateSearchPlaceholder();
      if (conceptLegend) {
        conceptLegend.hidden = state.mode !== "concepts";
      }
      if (relationFilter && relationFilter.parentElement) {
        relationFilter.parentElement.hidden = state.mode !== "concepts";
      }
      if (state.mode === "concepts") {
        renderConcepts();
      } else if (state.query) {
        renderSearchResults();
      } else if (state.areaId) {
        var area = null;
        for (var i = 0; i < areas.length; i += 1) {
          if (areas[i].id === state.areaId) {
            area = areas[i];
          }
        }
        if (area) {
          renderArea(area);
        } else {
          state.areaId = null;
          renderRoot();
        }
      } else {
        renderRoot();
      }
      syncStateToHash(commitNextSync);
      commitNextSync = false;
    }

    function renderRoot() {
      viewport.appendChild(el("p", "map-intro", copy.rootIntro));
      var grid = el("div", "map-areas");
      areas.forEach(function (area) {
        var card = el("button", "map-area-card");
        card.type = "button";
        card.setAttribute("data-area-id", area.id);
        card.setAttribute("data-destination", area.destination);
        card.appendChild(el("span", "map-area-title", area.title));
        var count = countAreaPages(area);
        card.appendChild(
          el(
            "span",
            "map-area-count",
            count + " " + (count > 1 ? copy.pagesUnitPlural : copy.pagesUnit)
          )
        );
        var previewTitles = (area.sections || []).slice(0, 3).map(function (section) {
          return section.title;
        });
        if (previewTitles.length) {
          card.appendChild(el("span", "map-area-preview", previewTitles.join(" · ")));
        }
        card.addEventListener("click", function () {
          state.areaId = area.id;
          commitNextSync = true;
          render();
          var home = viewport.querySelector("[data-map-home]");
          if (home) {
            home.focus();
          }
        });
        grid.appendChild(card);
      });
      viewport.appendChild(grid);
    }

    function renderArea(area) {
      var crumbs = el("nav", "map-crumbs");
      crumbs.setAttribute("aria-label", copy.crumbsLabel);
      var home = el("button", "map-crumbs-home", copy.rootCrumb);
      home.type = "button";
      home.setAttribute("data-map-home", "true");
      home.setAttribute("aria-label", copy.backLabel);
      home.addEventListener("click", function () {
        state.areaId = null;
        commitNextSync = true;
        render();
        var card = viewport.querySelector('[data-area-id="' + area.id + '"]');
        if (card) {
          card.focus();
        }
      });
      crumbs.appendChild(home);
      crumbs.appendChild(el("span", "map-crumbs-sep", "__CRUMB_SEP__"));
      crumbs.appendChild(el("span", "map-crumbs-current", area.title));
      viewport.appendChild(crumbs);

      function renderSection(section) {
        var card = el("div", "map-section-card");
        var title = el("h3", "map-section-title", section.title);
        title.appendChild(
          el("span", "map-section-count", String(countSectionPages(section)))
        );
        card.appendChild(title);

        var pageIds = section.pages || [];
        if (pageIds.length) {
          var chips = el("div", "map-chips");
          pageIds.forEach(function (pageId) {
            var chip = chipFor(pageId);
            if (chip) {
              chips.appendChild(chip);
            }
          });
          if (chips.firstChild) {
            card.appendChild(chips);
          }
        }

        var children = section.sections || [];
        if (children.length) {
          var nested = el("div", "map-sections map-subsections");
          children.forEach(function (child) {
            nested.appendChild(renderSection(child));
          });
          card.appendChild(nested);
        }
        return card;
      }

      var sections = area.sections || [];
      if (sections.length) {
        var sectionGrid = el("div", "map-sections");
        sections.forEach(function (section) {
          sectionGrid.appendChild(renderSection(section));
        });
        var sectionBlock = el("div", "map-entry-block");
        sectionBlock.appendChild(el("p", "map-entry-label", copy.sectionsLabel));
        sectionBlock.appendChild(sectionGrid);
        viewport.appendChild(sectionBlock);
      }

      if ((area.pages || []).length) {
        var pageBlock = el("div", "map-entry-block");
        pageBlock.appendChild(el("p", "map-entry-label", copy.pagesLabel));
        var chips = el("div", "map-chips");
        (area.pages || []).forEach(function (pageId) {
          var chip = chipFor(pageId);
          if (chip) {
            chips.appendChild(chip);
          }
        });
        pageBlock.appendChild(chips);
        viewport.appendChild(pageBlock);
      }

      var total = countAreaPages(area);
      var areaUnit = total > 1 ? copy.pagesUnitPlural : copy.pagesUnit;
      setStatus(area.title + " — " + total + " " + areaUnit);
    }

    function renderSearchResults() {
      var query = state.query.toLowerCase();
      var matches = (data.pages || []).filter(function (page) {
        return matchesQuery(page, query);
      });
      if (!matches.length) {
        viewport.appendChild(el("p", "map-empty", copy.noResults));
        setStatus(copy.noResults);
        return;
      }
      var grid = el("div", "map-page-grid");
      matches.forEach(function (page) {
        var card = el("a", "map-page-card");
        card.href = page.href;
        card.setAttribute("data-destination", page.destination);
        card.appendChild(el("span", "map-page-meta", copy.destinations[page.destination] || ""));
        var pageTitle = el("span", "map-page-title");
        appendMarkedText(pageTitle, page.title, query);
        card.appendChild(pageTitle);
        if (page.summary || page.purpose) {
          var pageSummary = el("span", "map-page-summary");
          appendMarkedText(pageSummary, page.summary || page.purpose, query);
          card.appendChild(pageSummary);
        }
        card.addEventListener("click", function (event) {
          if (event.button === 0 && !event.metaKey && !event.ctrlKey && !event.shiftKey) {
            event.preventDefault();
            showPageDetails(page.id);
          }
        });
        grid.appendChild(card);
      });
      viewport.appendChild(grid);
      var conceptMatches = (data.concepts || []).filter(function (concept) {
        var haystack = (concept.label + " " + (concept.definition || "")).toLowerCase();
        return haystack.indexOf(query) >= 0;
      });
      if (conceptMatches.length) {
        viewport.appendChild(
          el(
            "p",
            "map-cross-view-hint",
            copy.conceptMatchesHint.replace("{count}", String(conceptMatches.length))
          )
        );
      }
      var resultUnit = matches.length > 1 ? copy.pagesUnitPlural : copy.pagesUnit;
      setStatus(matches.length + " " + resultUnit);
    }

    function renderConceptLegend() {
      if (!conceptLegend) {
        return;
      }
      clearNode(conceptLegend);
      conceptLegend.appendChild(el("h4", "map-concept-legend-title", copy.relationLegendTitle));
      var list = el("ul", "map-concept-legend-list");
      Object.keys(relationTypes).forEach(function (kind) {
        var relation = relationTypes[kind];
        var item = el("li", "map-concept-legend-item");
        var familyLabel = copy.relationFamilies[relation.family] || "";
        if (familyLabel) {
          item.appendChild(
            el(
              "span",
              "map-relation-family map-relation-family--" + relation.family,
              familyLabel
            )
          );
        }
        var direction = relation.direction === "symmetric" ? "↔ " : "→ ";
        item.appendChild(el("span", "map-relation-direction", direction));
        item.appendChild(el("strong", "map-relation-label", relation.label));
        item.appendChild(el("span", "map-relation-description", " — " + relation.description));
        list.appendChild(item);
      });
      if (list.firstChild) {
        conceptLegend.appendChild(list);
      }
    }

    function conceptMatchesFilters(concept, query) {
      if (query) {
        var haystack = (concept.label + " " + (concept.definition || "")).toLowerCase();
        if (haystack.indexOf(query) < 0) {
          return false;
        }
      }
      if (!state.relationType) {
        return true;
      }
      var participates = (data.concept_relations || []).some(function (relation) {
        return (
          relation.type === state.relationType &&
          (relation.from === concept.id || relation.to === concept.id)
        );
      });
      return participates;
    }

    function conceptNeighbors(conceptId) {
      var neighbors = {};
      (data.concept_relations || []).forEach(function (relation) {
        if (state.relationType && relation.type !== state.relationType) {
          return;
        }
        if (relation.from === conceptId) {
          neighbors[relation.to] = true;
        } else if (relation.to === conceptId) {
          neighbors[relation.from] = true;
        }
      });
      return neighbors;
    }

    function countHiddenRelations(visibleConcepts) {
      if (!state.query && !state.relationType) {
        return 0;
      }
      var visibleIds = {};
      visibleConcepts.forEach(function (concept) {
        visibleIds[concept.id] = true;
      });
      var hidden = 0;
      (data.concept_relations || []).forEach(function (relation) {
        var filteredType = Boolean(state.relationType) && relation.type !== state.relationType;
        if (filteredType || !visibleIds[relation.from] || !visibleIds[relation.to]) {
          hidden += 1;
        }
      });
      return hidden;
    }

    function conceptItemFor(concept, neighbors, query) {
      var item = el("button", "map-concept-item");
      item.type = "button";
      item.setAttribute("data-concept-id", concept.id);
      item.setAttribute("aria-pressed", "false");
      var label = el("span", "map-concept-label");
      appendMarkedText(label, concept.label, query);
      item.appendChild(label);
      var importanceLabel = copy.importanceLabels[concept.importance];
      if (importanceLabel) {
        item.appendChild(el("span", "map-concept-importance", importanceLabel));
      }
      if (concept.definition) {
        var definition = el("span", "map-concept-def");
        appendMarkedText(definition, concept.definition, query);
        item.appendChild(definition);
      }
      if (state.conceptId) {
        if (state.conceptId === concept.id) {
          item.setAttribute("aria-pressed", "true");
        } else if (!neighbors[concept.id]) {
          item.classList.add("map-concept-dimmed");
        }
      }
      item.addEventListener("click", function () {
        state.conceptId = concept.id;
        commitNextSync = true;
        render();
        showConceptDetails(concept.id);
        var selected = viewport.querySelector('[data-concept-id="' + concept.id + '"]');
        if (selected) {
          selected.focus();
        }
      });
      return item;
    }

    function renderConcepts() {
      renderConceptLegend();
      var query = state.query.toLowerCase();
      var concepts = (data.concepts || []).filter(function (concept) {
        return conceptMatchesFilters(concept, query);
      });
      if (!concepts.length) {
        viewport.appendChild(el("p", "map-empty", copy.noResults));
        setStatus(copy.noResults);
        return;
      }
      var grouped = {};
      (conceptDomainList || []).forEach(function (domain) {
        grouped[domain.id] = [];
      });
      var ungrouped = [];
      concepts.forEach(function (concept) {
        var matched = false;
        (concept.domains || []).forEach(function (domainId) {
          if (grouped[domainId]) {
            grouped[domainId].push(concept);
            matched = true;
          }
        });
        if (!matched) {
          ungrouped.push(concept);
        }
      });
      var neighbors = state.conceptId ? conceptNeighbors(state.conceptId) : null;
      (conceptDomainList || []).forEach(function (domain) {
        if (!grouped[domain.id].length) {
          return;
        }
        var group = el("section", "map-concept-group");
        var title = el("h3", "map-concept-domain-title", domain.label);
        var count = String(grouped[domain.id].length);
        title.appendChild(el("span", "map-concept-domain-count", count));
        group.appendChild(title);
        var grid = el("div", "map-concept-grid");
        grouped[domain.id].forEach(function (concept) {
          grid.appendChild(conceptItemFor(concept, neighbors, query));
        });
        group.appendChild(grid);
        viewport.appendChild(group);
      });
      if (ungrouped.length) {
        var group = el("section", "map-concept-group");
        var title = el("h3", "map-concept-domain-title", copy.ungroupedConcepts);
        title.appendChild(el("span", "map-concept-domain-count", String(ungrouped.length)));
        group.appendChild(title);
        var grid = el("div", "map-concept-grid");
        ungrouped.forEach(function (concept) {
          grid.appendChild(conceptItemFor(concept, neighbors, query));
        });
        group.appendChild(grid);
        viewport.appendChild(group);
      }
      var hiddenCount = countHiddenRelations(concepts);
      if (hiddenCount > 0) {
        viewport.appendChild(
          el(
            "p",
            "map-hidden-relations",
            copy.hiddenRelations.replace("{count}", String(hiddenCount))
          )
        );
      }
      var conceptUnit = concepts.length > 1 ? copy.notionsUnit : copy.notionsUnitSingular;
      setStatus(concepts.length + " " + conceptUnit);
    }

    function openDetailsBox() {
      var box = root.querySelector("details[data-map-details]");
      if (box && !box.open) {
        box.open = true;
      }
    }

    function showPageDetails(pageId, focusTarget) {
      var page = pageById[pageId];
      if (!page) {
        return;
      }
      state.pageId = pageId;
      syncStateToHash(false);
      clearNode(detailPanel);
      detailPanel.appendChild(el("h3", "map-detail-title", page.title));
      var meta = el("p", "map-detail-meta");
      meta.appendChild(
        el(
          "span",
          "map-detail-badge",
          (copy.destinations[page.destination] || page.destination) + " · " + page.level
        )
      );
      detailPanel.appendChild(meta);
      if (page.summary) {
        detailPanel.appendChild(el("p", "map-detail-summary", page.summary));
      }
      if (page.purpose) {
        detailPanel.appendChild(el("p", "map-detail-purpose", page.purpose));
      }
      var headings = page.section_headings || [];
      if (headings.length) {
        detailPanel.appendChild(el("h4", "map-detail-heading", copy.sectionHeadingsTitle));
        var sectionHeadingList = el("ol", "map-detail-sections");
        headings.forEach(function (heading) {
          var item = el("li", "map-detail-section-item", heading);
          sectionHeadingList.appendChild(item);
        });
        detailPanel.appendChild(sectionHeadingList);
      }
      var related = (page.related || []).filter(function (relatedId) {
        return Boolean(pageById[relatedId]);
      });
      if (related.length) {
        detailPanel.appendChild(el("h4", "map-detail-heading", copy.relatedPages));
        var relatedChips = el("div", "map-chips");
        related.forEach(function (relatedId) {
          var chip = chipFor(relatedId);
          if (chip) {
            relatedChips.appendChild(chip);
          }
        });
        detailPanel.appendChild(relatedChips);
      }
      var previous = (page.route || {}).previous;
      if (previous && pageById[previous]) {
        detailPanel.appendChild(el("h4", "map-detail-heading", copy.suggestedPrevious));
        var previousChips = el("div", "map-chips");
        var previousChip = chipFor(previous);
        if (previousChip) {
          previousChips.appendChild(previousChip);
        }
        detailPanel.appendChild(previousChips);
      }
      var next = (page.route || {}).next;
      if (next && pageById[next]) {
        detailPanel.appendChild(el("h4", "map-detail-heading", copy.suggestedNext));
        var nextChips = el("div", "map-chips");
        var nextChip = chipFor(next);
        if (nextChip) {
          nextChips.appendChild(nextChip);
        }
        detailPanel.appendChild(nextChips);
      }
      var open = el("a", "map-open-page", copy.openPage);
      open.href = page.href;
      detailPanel.appendChild(open);
      openDetailsBox();
      markCurrentChip();
      setStatus(page.title);
      if (focusTarget === "details") {
        var title = detailPanel.querySelector(".map-detail-title");
        if (title) {
          title.tabIndex = -1;
          title.focus();
        }
      }
    }

    function showConceptDetails(conceptId, focusTarget) {
      var concept = conceptById[conceptId];
      if (!concept) {
        return;
      }
      state.pageId = null;
      markCurrentChip();
      clearNode(detailPanel);
      detailPanel.appendChild(el("h3", "map-detail-title", concept.label));
      var importanceLabel = copy.importanceLabels[concept.importance];
      if (importanceLabel) {
        detailPanel.appendChild(el("p", "map-concept-importance", importanceLabel));
      }
      if (concept.definition) {
        detailPanel.appendChild(el("p", "map-detail-purpose", concept.definition));
      }
      var relations = (data.concept_relations || []).filter(function (relation) {
        if (state.relationType && relation.type !== state.relationType) {
          return false;
        }
        return relation.from === conceptId || relation.to === conceptId;
      });
      if (relations.length) {
        detailPanel.appendChild(el("h4", "map-detail-heading", copy.relatedConcepts));
        var relationList = el("ul", "map-detail-relations");
        relations.forEach(function (relation) {
          var outgoing = relation.from === conceptId;
          var otherId = outgoing ? relation.to : relation.from;
          var other = conceptById[otherId];
          var type = relationTypes[relation.type];
          if (other) {
            var label = type ? type.label : relation.type;
            var arrow = type && type.direction === "symmetric" ? " ↔ " : " ";
            var source = outgoing ? concept : other;
            var target = outgoing ? other : concept;
            var family = type ? type.family : "";
            var familyLabel = copy.relationFamilies[family] || "";
            var entry = el(
              "li",
              "map-detail-relation" + (family ? " map-detail-relation--" + family : "")
            );
            if (familyLabel) {
              entry.appendChild(
                el(
                  "span",
                  "map-relation-family map-relation-family--" + family,
                  familyLabel
                )
              );
            }
            entry.appendChild(
              document.createTextNode(source.label + " " + label + arrow + target.label)
            );
            var link = el("button", "map-concept-link", copy.viewConcept);
            link.type = "button";
            link.addEventListener("click", function () {
              state.conceptId = other.id;
              commitNextSync = true;
              render();
              showConceptDetails(other.id, "details");
            });
            entry.appendChild(link);
            relationList.appendChild(entry);
          }
        });
        if (relationList.firstChild) {
          detailPanel.appendChild(relationList);
        }
      }
      var resources = concept.resources || [];
      if (resources.length) {
        detailPanel.appendChild(el("h4", "map-detail-heading", copy.conceptResources));
        var chips = el("div", "map-chips");
        resources.forEach(function (resource) {
          var chip = chipFor(resource.id);
          if (chip) {
            chips.appendChild(chip);
          }
        });
        detailPanel.appendChild(chips);
      }
      openDetailsBox();
      setStatus(concept.label);
      if (focusTarget === "details") {
        var title = detailPanel.querySelector(".map-detail-title");
        if (title) {
          title.tabIndex = -1;
          title.focus();
        }
      }
    }

    modeSelect.addEventListener("change", function () {
      state.mode = modeSelect.value;
      state.conceptId = null;
      state.pageId = null;
      commitNextSync = true;
      render();
    });

    searchInput.addEventListener("input", function () {
      if (searchTimer) {
        window.clearTimeout(searchTimer);
      }
      searchTimer = window.setTimeout(function () {
        searchTimer = null;
        state.query = searchInput.value.trim();
        render();
      }, 120);
    });

    if (relationFilter) {
      relationFilter.addEventListener("change", function () {
        state.relationType = relationFilter.value;
        commitNextSync = true;
        render();
      });
    }

    if (resetButton) {
      resetButton.addEventListener("click", function () {
        commitNextSync = true;
        state.query = "";
        state.relationType = "";
        state.areaId = null;
        state.conceptId = null;
        state.pageId = null;
        searchInput.value = "";
        if (relationFilter) {
          relationFilter.value = "";
        }
        render();
        renderPlaceholder();
        modeSelect.focus();
      });
    }

    if (copyButton) {
      copyButton.addEventListener("click", function () {
        syncStateToHash(false);
        var url = window.location.href;
        function reportCopied(successful) {
          setStatus(successful ? copy.linkCopied : copy.linkCopyFailed);
        }
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(url).then(
            function () {
              reportCopied(true);
            },
            function () {
              reportCopied(false);
            }
          );
        } else {
          reportCopied(false);
        }
      });
    }

    document.addEventListener("keydown", function (event) {
      if (event.key !== "Escape" || !data) {
        return;
      }
      var target = event.target;
      if (target && target !== document.body && !root.contains(target)) {
        return;
      }
      if (state.query) {
        commitNextSync = true;
        state.query = "";
        searchInput.value = "";
        render();
      } else if (state.mode === "concepts" && state.conceptId) {
        commitNextSync = true;
        state.conceptId = null;
        render();
        renderPlaceholder();
      } else if (state.mode === "concepts" && state.relationType) {
        commitNextSync = true;
        state.relationType = "";
        if (relationFilter) {
          relationFilter.value = "";
        }
        render();
      } else if (state.mode === "pages" && state.areaId) {
        commitNextSync = true;
        state.areaId = null;
        render();
      } else if (state.pageId) {
        commitNextSync = true;
        state.pageId = null;
        markCurrentChip();
        renderPlaceholder();
        syncStateToHash(commitNextSync);
        commitNextSync = false;
      }
    });

    window.addEventListener("popstate", function () {
      if (!data) {
        return;
      }
      applyHashToState();
      modeSelect.value = state.mode;
      searchInput.value = state.query;
      if (relationFilter) {
        relationFilter.value = state.relationType;
      }
      render();
      if (state.mode === "concepts" && state.conceptId) {
        showConceptDetails(state.conceptId);
      } else if (state.mode === "pages" && state.pageId) {
        showPageDetails(state.pageId);
      } else {
        renderPlaceholder();
      }
    });

    load();
  }
})();
</script>
"""

TERRITORY_MAP_TEMPLATE = """<div class="learning-map" data-learning-map
  data-language="__LANGUAGE__" data-source="__DATA_SOURCE__">
  <div class="learning-map-toolbar">
    <div class="learning-map-filter">
      <label for="learning-map-mode">__VIEW_LABEL__</label>
      <select id="learning-map-mode" data-map-mode>
        <option value="pages">__MODE_PAGES__</option>
        <option value="concepts">__MODE_CONCEPTS__</option>
      </select>
    </div>
    <div class="learning-map-relation-filter" hidden>
      <label for="learning-map-relation-type">__RELATION_FILTER_LABEL__</label>
      <select id="learning-map-relation-type" data-map-relation-type></select>
    </div>
    <div class="learning-map-search">
      <label for="learning-map-search">__SEARCH_LABEL__</label>
      <input id="learning-map-search" data-map-search type="search" autocomplete="off">
    </div>
    <div class="learning-map-actions">
      <button type="button" class="map-copy" data-map-copy title="__COPY_HINT__">
        __COPY_LINK__
      </button>
      <button type="button" class="map-reset" data-map-reset title="__RESET_HINT__">
        __RESET_VIEW__
      </button>
    </div>
  </div>
  <div class="learning-map-concept-legend" hidden></div>
  <div class="learning-map-layout">
    <div class="learning-map-canvas learning-map-viewport" data-map-viewport>
      <p class="map-load-status">__LOADING__</p>
    </div>
    <aside class="learning-map-details">
      <details data-map-details open>
        <summary>__DETAILS_SUMMARY__</summary>
        <p class="map-selection-hint">__ASIDE_HINT__</p>
        <div class="map-detail-panel" data-map-detail-panel></div>
      </details>
    </aside>
  </div>
  <p class="learning-map-status" data-map-status role="status" aria-live="polite">__LOADING__</p>
</div>
"""


def escape_markdown_text(value: str) -> str:
    """Escape Markdown constructs that would change list or link structure.

    Paired backticks in authored titles are preserved on purpose: they delimit
    code spans such as GPT configuration (with `gpt_config.py` inline), and
    escaping them, or the characters inside the span, leaks backslashes into
    the rendered text. Underscores, periods and similar characters stay
    literal because they are harmless inside link text and list items.
    """
    special = "\\*[]"
    return "".join(f"\\{character}" if character in special else character for character in value)


def _copy_for(language: str) -> dict[str, Any]:
    """Return the copy for one language, rejecting unknown languages."""
    if language not in COPY:
        raise ValueError(f"unsupported learning-map language: {language!r}")
    return COPY[language]


def _fill(template: str, values: dict[str, str]) -> str:
    """Replace every sentinel token in a template with its rendered value."""
    for sentinel, value in values.items():
        template = template.replace(sentinel, value)
    return template


def render_map_script() -> str:
    """Return the interactive include shared by every script-driven representation."""
    copy_json = json.dumps(COPY, ensure_ascii=False, indent=2)
    script = PROGRESSIVE_MAP_TEMPLATE.replace("__LEARNING_MAP_COPY__", copy_json)
    script = script.replace("__CRUMB_SEP__", "\u203a")
    return GENERATED_FILE_NOTE + script


def render_territory_map(
    language: str, navigation: list[dict[str, Any]], page_by_id: dict[str, dict[str, Any]]
) -> str:
    """Return the localized interactive shell markup for the drill-down map."""
    copy = _copy_for(language)
    return (
        GENERATED_FILE_NOTE
        + "```{=html}\n"
        + _fill(
            TERRITORY_MAP_TEMPLATE,
            {
                "__LANGUAGE__": language,
                "__DATA_SOURCE__": f"../learning-map-data-{language}.json",
                "__VIEW_LABEL__": html.escape(copy["viewLabel"]),
                "__MODE_PAGES__": html.escape(copy["modePages"]),
                "__MODE_CONCEPTS__": html.escape(copy["modeConcepts"]),
                "__SEARCH_LABEL__": html.escape(copy["searchLabel"]),
                "__RELATION_FILTER_LABEL__": html.escape(copy["relationFilterLabel"]),
                "__RESET_VIEW__": html.escape(copy["resetView"]),
                "__RESET_HINT__": html.escape(copy["resetHint"]),
                "__COPY_LINK__": html.escape(copy["copyLink"]),
                "__COPY_HINT__": html.escape(copy["copyHint"]),
                "__LOADING__": html.escape(copy["loading"]),
                "__DETAILS_SUMMARY__": html.escape(copy["detailsSummary"]),
                "__ASIDE_HINT__": html.escape(copy["asideHint"]),
            },
        )
        + "```\n"
    )


def render_inline_map_data(payload: dict[str, Any]) -> str:
    """Return the map payload as an inline JSON script next to the map shell.

    Embedding the data removes the loading state and the failure path of a
    second request; the JSON request stays available as a fallback when the
    inline block is missing or malformed.
    """
    data = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    return (
        GENERATED_FILE_NOTE
        + "```{=html}\n"
        + '<script type="application/json" data-map-data>'
        + data
        + "</script>\n"
        + "```\n"
    )


def render_resource_list(
    language: str, navigation: list[dict[str, Any]], page_by_id: dict[str, dict[str, Any]]
) -> str:
    """Return the whole nested navigation as a static, script-free Markdown list."""
    _copy_for(language)  # validate the language even though the list has no copy
    lines: list[str] = []

    def append_section(section: dict[str, Any], indent: int) -> None:
        prefix = " " * indent
        lines.append(f"{prefix}- {escape_markdown_text(str(section['title']))}")
        for page_id in section.get("pages", []):
            page = page_by_id.get(page_id)
            if page is not None:
                lines.append(
                    f"{' ' * (indent + 2)}- [{escape_markdown_text(page['title'])}]({page['href']})"
                )
        for child in section.get("sections", []):
            append_section(child, indent + 2)

    for area in navigation:
        lines.append(f"- **{escape_markdown_text(str(area['title']))}**")
        for section in area.get("sections", []):
            append_section(section, 2)
        for page_id in area.get("pages", []):
            page = page_by_id.get(page_id)
            if page is not None:
                lines.append(f"  - [{escape_markdown_text(page['title'])}]({page['href']})")
    return GENERATED_FILE_NOTE + "\n".join(lines) + "\n"


@dataclass(frozen=True)
class Representation:
    """One reader-facing form rendered from the learning-map structure."""

    id: str
    artifact: str
    interactive: bool
    render: Callable[[str, list[dict[str, Any]], dict[str, dict[str, Any]]], str]


REPRESENTATIONS: Mapping[str, Representation] = {
    "territories": Representation(
        id="territories",
        artifact="map-territories",
        interactive=True,
        render=render_territory_map,
    ),
    "list": Representation(
        id="list",
        artifact="map-list",
        interactive=False,
        render=render_resource_list,
    ),
}
