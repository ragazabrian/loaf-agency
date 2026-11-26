// Calls back once the image is ready, or has failed: the page re-measures
// its height when every image is done, so a failed or rejected decode
// (Safari rejects some) mustn't leave it waiting for ever
const decodeImage = (src, callback) => {
  const img = new Image()
  let called = false
  const done = () => {
    if (called) return
    called = true
    callback()
  }
  if (img.decode) {
    img.src = src
    img.decode().then(done, done)
  } else {
    img.onload = img.onerror = () => {
      img.onload = img.onerror = null
      done()
    }
    img.src = src
  }
  return img
}

const toFixed = (n, p) => {
  var p = p !== undefined ? Math.pow(10, p) : 1000
  return Math.round(n * p) / p
}

// True when the browser should handle a link click itself (new tab/window,
// download, middle click), so SPA click handlers can step aside and let the
// real href do its job
const isModifiedClick = (event) => {
  return !!(
    event &&
    (event.metaKey ||
      event.ctrlKey ||
      event.shiftKey ||
      event.altKey ||
      (event.button !== undefined && event.button !== 0))
  )
}

// Sets <meta name="robots"> for the current view, or removes it when content
// is empty. The shell in index.html has none, so removing it restores the
// default (index, follow). Google reads robots meta set by JavaScript.
const setRobotsMeta = (content) => {
  let tag = document.head.querySelector('meta[name="robots"]')
  if (!content) {
    if (tag) tag.parentNode.removeChild(tag)
    return
  }
  if (!tag) {
    tag = document.createElement('meta')
    tag.setAttribute('name', 'robots')
    document.head.appendChild(tag)
  }
  tag.setAttribute('content', content)
}

// Plain text from a string that may hold HTML or entities
const plainText = (value) => {
  if (typeof value !== 'string' || !value) return ''
  const div = document.createElement('div')
  div.innerHTML = value
  return (div.textContent || '').replace(/\s+/g, ' ').trim()
}

// Alt text for an ACF image (or any object with alt/caption): the media
// library's alt text, else its caption, else the first non-empty fallback
// (context such as "Client — Project title"). Media titles are skipped on
// purpose: they're usually file names ("Artboard – 14").
const imageAlt = (image, ...fallbacks) => {
  const candidates = [image && image.alt, image && image.caption].concat(fallbacks)
  for (let i = 0; i < candidates.length; i++) {
    const text = plainText(candidates[i])
    if (text) return text
  }
  return ''
}

// "Client — Title" for a case study (global API items keep ACF in acf[0],
// showcase-linked items in acf)
const workLabel = (item) => {
  if (!item) return ''
  const acf = Array.isArray(item.acf) ? item.acf[0] || {} : item.acf || {}
  const client = plainText(acf.client)
  const title = plainText(item.post_title)
  return client && title ? client + ' — ' + title : client || title
}

export { decodeImage, toFixed, isModifiedClick, setRobotsMeta, plainText, imageAlt, workLabel }


// WEBPACK FOOTER //
// ./src/utils.js