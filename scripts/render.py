import sys, pathlib
from playwright.sync_api import sync_playwright
src = pathlib.Path(sys.argv[1]).resolve(); out = pathlib.Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width':1080,'height':1350})
    pg.goto(src.as_uri()); pg.evaluate("document.fonts.ready"); pg.evaluate("window.bgReady || null"); pg.wait_for_timeout(400)
    bad = pg.evaluate("""[...document.querySelectorAll('.slide')].flatMap((s,i)=>{const r=s.getBoundingClientRect();return [...s.querySelectorAll('*')].filter(e=>{const q=e.getBoundingClientRect();return q.width&&(q.bottom>r.bottom+1||q.right>r.right+1||e.scrollWidth>e.clientWidth+2&&getComputedStyle(e).overflow!=='visible')}).map(e=>`slide ${i+1}: <${e.tagName.toLowerCase()} class=${e.className}> overflows`)})""")
    bad += pg.evaluate("""[...document.querySelectorAll('.slide')].flatMap((s,i)=>[...s.querySelectorAll('.panel')].filter(p=>{const r=p.getBoundingClientRect();const lim=r.bottom-parseFloat(getComputedStyle(p).paddingBottom);return [...p.querySelectorAll('*')].some(e=>{const q=e.getBoundingClientRect();return q.height&&q.bottom>lim+1})}).map(()=>`slide ${i+1}: content runs into the white panel's bottom padding -> shorten the copy`))""")
    bad += pg.evaluate("""[...document.querySelectorAll('.cover')].flatMap((c,i)=>[...c.querySelectorAll('h1,h2')].filter(e=>{const lh=parseFloat(getComputedStyle(e).lineHeight);const n=Math.round(e.getBoundingClientRect().height/lh);return e.tagName==='H1'?n>3:n>1}).map(e=>`cover: <${e.tagName.toLowerCase()}> has too many lines (title max 3, subtitle max 1) -> shorten the copy`))""")
    n = len(pg.query_selector_all('.slide'))
    if n < 6: bad.append(f'{n} slides (fewer than the default 6)')
    bad += pg.evaluate("""(()=>{const s=[...document.querySelectorAll('.slide')];const n=s.length;return s.flatMap((el,i)=>{const p=el.querySelector('.page');const v=p?p.textContent.trim():'';return p&&v!==`${i+1}/${n}`?[`slide ${i+1}: page number ${v} -> change to ${i+1}/${n}`]:[]})})()""")
    bad += pg.evaluate("""[...document.querySelectorAll('.slide')].flatMap((s,i)=>[...s.querySelectorAll('.hl')].flatMap(e=>{const c=getComputedStyle(e);const t=e.textContent.trim().slice(0,20);const r=[];if(c.color!=='rgb(255, 42, 129)')r.push(`slide ${i+1}: highlight "${t}" is not pink (#FF2A81) -> check whether another rule overrides it`);if(e.tagName==='SPAN'&&c.display==='block')r.push(`slide ${i+1}: highlight "${t}" became a block and breaks the line -> check the span rule of its parent`);return r}))""")
    # Placeholders such as {{ACCOUNT}} (the Instagram handle on the Follow button) must be replaced before rendering
    bad += pg.evaluate("""[...document.querySelectorAll('.slide')].flatMap((s,i)=>(s.innerText.match(/\\{\\{[^}]*\\}\\}/g)||[]).map(m=>`slide ${i+1}: placeholder ${m} is still in the slide -> replace it (e.g., the Instagram handle on the Follow button)`))""")
    # Fonts that failed to load (e.g., the fonts/ folder wasn't copied next to slides.html) would silently fall back to another typeface
    bad += pg.evaluate("""[...new Set([...document.fonts].filter(f=>f.status==='error').map(f=>f.family+' '+f.weight))].map(f=>`font failed to load: ${f} -> copy the skill's assets/fonts/ next to slides.html as fonts/`)""")
    print('\n'.join(bad) or 'No overflow')
    miss = pg.evaluate("[...document.querySelectorAll('[data-missing]')].map(e=>e.dataset.bg)")
    if miss: print('Missing background photo (solid color used instead): ' + ', '.join(miss))
    if n > 6: print(f'{n} slides (default 6 + {n-6} added: confirm the added content is essential and only overflowed because of the large type)')
    for i, s in enumerate(pg.query_selector_all('.slide'), 1):
        s.screenshot(path=str(out / f'{i:02d}.png'))
    b.close()
