---
icon: lucide/file-output
---

# PDF export

PyReveal exports HTML, not PDF files. PDF export uses reveal.js print layout in the browser.

## Quick workflow

```python
from pyreveal import Presentation, Slide

deck = Presentation("Talk")
deck.add(Slide.make_title("My Talk"))
deck.save("output/talk.html", pdf_hint=True)
# Console prints: PDF export URL: output/talk.html?print-pdf
```

Open the `?print-pdf` URL in Chromium (Chrome or Edge), then print to PDF.

## Build the print URL

```python
Presentation.pdf_print_url("output/talk.html")
# -> output/talk.html?print-pdf
```

`save(pdf_hint=True)` prints the same URL after writing the file.

## Browser steps

1. Save the deck with `deck.save("path/to/deck.html")`.
2. Open `path/to/deck.html?print-pdf` in Chromium.
3. Wait for the deck to finish layout (all slides visible in print view).
4. Print (Ctrl+P / Cmd+P) and choose **Save as PDF**.

Optional: enable print layout when authoring:

```python
deck.print_view()
```

See [reveal.js PDF export](https://revealjs.com/pdf-export/) for recommended print settings (margins, background graphics, page size).

## What PyReveal does not do

- No server-side PDF rendering
- No headless Chrome automation in the library

For CI or batch export, run Chromium with the print URL yourself or use a separate tool.

## Caveats

- Fragments: reveal.js can expand fragments for print; test your deck in the print URL.
- Speaker notes: not included in the slide PDF (use speaker view separately).
- Custom assets: save copies images and local files into the output folder; remote URLs are left as-is.

## Related

- [Configuration](configuration.md) — `save()`, `print_view()`
- [Reveal.js feature support](reveal-features.md) — parity overview