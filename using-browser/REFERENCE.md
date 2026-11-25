# Using a Browser: Recipes

Run each snippet with the browser tool's script-evaluation action.

- [React handlers on canvas and SVG](#react-handlers-on-canvas-and-svg)
- [React-controlled inputs](#react-controlled-inputs)
- [Contenteditable editors (Lexical)](#contenteditable-editors-lexical)
- [Reading React state from the fiber](#reading-react-state-from-the-fiber)
- [Drag and drop](#drag-and-drop)
- [Slowing one request](#slowing-one-request)
- [Touch emulation](#touch-emulation)
- [Throttling WebRTC media](#throttling-webrtc-media)

## React handlers on canvas and SVG

React attaches one root listener and routes events through its own tree, so events made in a script (`mousedown`/`mouseup`/`click` via `dispatchEvent`, or pointer events) do not reach the handlers on drawing surfaces. Call the handler props instead:

```js
const getProps = () => el[Object.keys(el).find(k => k.startsWith('__reactProps$'))];
const evt = (x, y) => ({ clientX: x, clientY: y, button: 0, target: el, currentTarget: el,
  preventDefault() {}, stopPropagation() {} });
getProps().onMouseDown(evt(x0, y0));
for (const [x, y] of path) getProps().onMouseMove(evt(x, y));
getProps().onMouseUp(evt(xN, yN));
```

Read the props again before every call: a captured props object holds old closures, so the second step of a drag runs against stale state. Confirm the gesture landed where it is stored, not only on screen.

## React-controlled inputs

React overrides the `value` property and listens only for its own change event, so `el.value = 'x'` followed by an `input` event changes nothing. Prefer the tool's fill or type action. From a script, use the native setter:

```js
const setter = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set;
setter.call(el, 'x');
el.dispatchEvent(new Event('input', { bubbles: true }));
```

## Contenteditable editors (Lexical)

Rich-text editors reject property assignment and most selection helpers: `innerText = …` leaves the editor state unchanged, and `execCommand('selectAll')` can append instead of replace. Lexical editors match `[contenteditable="true"][data-lexical-editor="true"]`.

```js
// insert
editor.focus();
document.execCommand('insertText', false, 'hello');

// replace
editor.focus();
const range = document.createRange();
range.selectNodeContents(editor);
const sel = getSelection();
sel.removeAllRanges();
sel.addRange(range);
document.execCommand('insertText', false, 'replacement');
```

Some editors mount only after their placeholder is clicked, and their submit button enables only once the editor holds text. Click the visible placeholder before you type.

## Reading React state from the fiber

When a UI state is hard to explain from the props, walk up the fiber from a DOM node:

```js
let f = el[Object.keys(el).find(k => k.startsWith('__reactFiber$'))];
for (; f; f = f.return) {
  if (f.memoizedProps && f.type?.displayName) console.log(f.type.displayName, f.memoizedProps, f.memoizedState);
}
```

It shows a context provider's value, a parent's hook state, or a prop that arrives `undefined` because the query that feeds it left a field out.

## Drag and drop

The browser fires `drop` only on a target whose last `dragover` handler called `preventDefault()`. When a drag ends with `dragend` and no `drop`, the target refused the drop; the tool did not fail. A tool's drag action runs the whole gesture in one call. To act in the middle of a drag (refetch the page, change the data from another tab), fire the events yourself and pass one `DataTransfer` through all of them:

```js
const dt = new DataTransfer();
const fire = (el, type) =>
  el.dispatchEvent(new DragEvent(type, { bubbles: true, cancelable: true, dataTransfer: dt }));

fire(source, 'dragstart');
// change the page or the data here
fire(target, 'dragenter');
fire(target, 'dragover');
const accepted = !fire(target, 'drop'); // dispatchEvent returns false when a handler called preventDefault
fire(source, 'dragend');
```

These events reach React's handlers on ordinary elements. Drawing surfaces still need the handler props, as above.

## Slowing one request

To act while a request is in flight (a second click, a navigation, a drop), make that one request slow. Install the wrapper before the page's own scripts run, through the tool's init-script option when it navigates: a client that kept its own reference to `fetch` earlier ignores the wrapper.

```js
window.__slow = {}; // { getNodeCounts: 4000 } holds the request whose body names getNodeCounts for 4 s
const realFetch = window.fetch;
window.fetch = async (...args) => {
  const body = typeof args[1]?.body === 'string' ? args[1].body : '';
  const name = Object.keys(window.__slow).find(key => body.includes(key));
  if (name) await new Promise(resolve => setTimeout(resolve, window.__slow[name]));
  return realFetch(...args);
};
```

Set `window.__slow` from a later script, act during the delay, then clear it.

## Touch emulation

Pages that read `navigator.maxTouchPoints` or touch media queries stay in desktop mode when only the window size changes. Use the tool's device emulation with touch on. In Chrome DevTools MCP that is `emulate` with a viewport such as `375x667x2,touch`; `resize_page` changes only the size. With the `mobile` flag added there, clicks have been seen landing at about 0.75 of the element's real coordinates. Keep `touch`, drop `mobile` unless the page needs a mobile user-agent, and reset emulation between devices.

## Throttling WebRTC media

Browser network throttling offers fixed profiles for HTTP traffic and has been seen leaving WebRTC (UDP) media unthrottled. For numbers a decision rests on, limit the incoming path in the operating system (Linux: `tc` with an `ifb` device):

1. **Find every remote address.** Read `getStats()` on the `RTCPeerConnection` and list the remote candidate of every `candidate-pair` in state `succeeded`. A server can answer on several addresses and move between them.
2. **Limit only those addresses**, inbound, at an exact rate, with optional delay and loss. Changing the rule needs root, so run one long-lived helper in a terminal the human can see and let them type the password.
3. **Prove it in every run.** The `tc -s` counters must grow, and the received bitrate (`bytesReceived` of the video `inbound-rtp`) must stay at or under the limit. Discard a run that breaks either check.
4. **Make the content move.** A still picture needs little bandwidth, so a limit shows only while the picture changes.
5. **Close each connection before the next run.** A reload can leave the server sending to the old page, which eats the next run's bandwidth.
