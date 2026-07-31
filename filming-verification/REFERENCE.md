# Filming Verification — Reference

Snippets are Playwright-flavoured because that is driver A; the shapes port to any runner.

## Caption helper

The caption is the deliverable. `measured` must be a value read back from the app, not a
string you wrote by hand.

```ts
const CAPTION_MS = 2600;

async function caption(page: Page, step: string, claim: string, measured: string) {
    await page.evaluate(
        ({ step, claim, measured }) => {
            document.getElementById('film-caption')?.remove();
            const el = document.createElement('div');
            el.id = 'film-caption';
            el.style.cssText = [
                'position:fixed',
                'inset:auto 0 0 0',
                'z-index:2147483647',
                'background:rgba(12,14,18,0.94)',
                'color:#fff',
                'font:14px/1.5 ui-monospace,Menlo,monospace',
                'padding:14px 20px',
                'border-top:3px solid #22c55e',
                'pointer-events:none',
                'white-space:pre-wrap',
            ].join(';');
            el.innerHTML =
                `<div style="font-size:17px;font-weight:700;margin-bottom:6px">${step}</div>` +
                `<div style="opacity:.75">${claim}</div>` +
                `<div style="color:#4ade80;margin-top:6px">✔ ${measured}</div>`;
            document.body.appendChild(el);
        },
        { step, claim, measured }
    );
    await page.waitForTimeout(CAPTION_MS);
}
```

Usage — note the assertion *next to* the caption, so a wrong value fails the run instead of
being narrated:

```ts
const accept = await page.getByTestId(SELECTORS.uploadInput).getAttribute('accept');
expect(accept).toContain('application/pdf');
await caption(page, '3 — Upload button accepts PDFs', 'Now uses the shared accept map.', `accept = ${accept}`);
```

## Throwaway config

Mirror the project's smoke/sanity config, then override recording. Delete after the run.

```ts
export default defineConfig({
    testDir: './tests',
    fullyParallel: false,
    workers: 1,
    retries: 0,
    reporter: [['list']],
    use: {
        video: { mode: 'on', size: { width: 1600, height: 900 } },
        viewport: { width: 1600, height: 900 },
        trace: 'off',
    },
    projects: [
        { name: 'login', testMatch: 'login.ts' },
        {
            name: 'chromium',
            testMatch: /myfilm\.ts/, // NOT *.spec.ts — the suite must not collect it
            use: { ...devices['Desktop Chrome'] },
            dependencies: ['login'],
        },
    ],
});
```

## The recording-context swap

Page objects that call `browser.newContext()` in their own `init()` never see `use.video`.
Build a recording context with the same stored auth and hand it to the POM:

```ts
const filmContext = await browser.newContext({
    storageState: `${AUTH_FILES_DIR}/owner.json`,
    viewport: { width: 1600, height: 900 },
    recordVideo: { dir: 'film', size: { width: 1600, height: 900 } },
});
const page = await filmContext.newPage();
actions.page = page;                        // POM helpers now drive the filmed page
await actions.loadStorageInPage(page);      // suppresses first-run dialogs

// ... steps ...

const videoPath = await page.video()?.path();
await filmContext.close();                  // closing flushes the file to disk
console.log(`FILM: ${videoPath}`);
```

Symptom that you forgot the swap: the run passes and no video file exists.

## Simulating a drag-over

Drag hints only render mid-drag. Dispatch the events with a real `DataTransfer`, then read
the hint on a **later** tool call — React needs a tick to re-render.

```ts
await page.evaluate(sel => {
    const dt = new DataTransfer();
    dt.items.add(new File(['x'], 'a.pdf', { type: 'application/pdf' }));
    for (const type of ['dragenter', 'dragover']) {
        document.querySelector(sel)?.dispatchEvent(new DragEvent(type, { bubbles: true, dataTransfer: dt }));
    }
}, '.app-container');
```

## Check the film before delivering

Extract a few frames and actually view them.

```bash
# ffmpeg
ffmpeg -i film.webm -vf fps=1/3 frames/frame%02d.jpg

# GStreamer fallback (no ffmpeg installed)
gst-launch-1.0 -q filesrc location=film.webm ! matroskademux ! vp8dec ! videorate \
  ! video/x-raw,framerate=1/3 ! jpegenc quality=80 ! multifilesink location=frames/frame%02d.jpg
```

Look for: a modal covering the UI, captions clipped at the viewport edge, a surface that
never actually loaded.

## Speed up

```bash
# ffmpeg — 1.5x
ffmpeg -i film.webm -filter:v "setpts=PTS/1.5" -an film-1.5x.webm

# GStreamer fallback — rate>1 speeds up; verify the output duration
gst-launch-1.0 -q filesrc location=film.webm ! matroskademux ! vp8dec ! videorate rate=1.5 \
  ! videoconvert ! vp8enc deadline=1 threads=4 ! webmmux ! filesink location=film-1.5x.webm

gst-discoverer-1.0 film-1.5x.webm | grep -i duration     # confirm, don't assume
```

Deliver the sped-up file; keep the 1x beside it when the human may want to pause. Quote both
durations.

## Duration budget

`raw ≈ steps × CAPTION_MS + navigation`. Nine captions at 2.6s ≈ 27s raw ≈ 18s at 1.5x.
Want it shorter? Cut steps or shorten captions — not more speed.
