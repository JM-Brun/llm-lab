-- Give every page a search-engine description without changing its title block.
--
-- Quarto already falls back to the subtitle for og:description and
-- twitter:description, but writes <meta name="description"> only from
-- `description`, which the title block would also display under the subtitle.
-- Filling the `description-meta` template variable alone adds the meta tag and
-- leaves the visible page unchanged. Pages that set `description` keep it.
function Meta(meta)
  if meta.description == nil and meta["description-meta"] == nil and meta.subtitle ~= nil then
    local text = pandoc.utils.stringify(meta.subtitle)
    meta["description-meta"] = pandoc.Inlines({ pandoc.Str(text) })
  end
  return meta
end
