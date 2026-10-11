#!/usr/bin/env python3
"""T05 frozen 10 browser checks. Synthetic only; no NOAA calls."""
from __future__ import annotations
import json, os, pathlib, re, shutil, sys
from playwright.sync_api import sync_playwright
ROOT=pathlib.Path(__file__).resolve().parent.parent
CONTRACT=json.loads((ROOT/'FROZEN-TESTS.json').read_text())
assert len(CONTRACT['tests'])==10
def rec(day,latest,mx=None,time=None):
    r={'signal_id':'aurora-kilpisjarvi-ovation','record_date':day,'normalized_value':latest,'unit':'pt','source_time':time or day+'T12:04:00Z','fetched_at':day+'T15:00:00Z'}
    if mx is not None:r.update(max_value=mx,max_source_time=time or day+'T12:04:00Z')
    return r
def test_one(browser,case):
    context=browser.new_context(viewport={'width':1440,'height':900})
    page=context.new_page()
    html=(ROOT/'index.html').read_text()
    html=re.sub(r'<script[^>]*src="[^"]+"[^>]*></script>','',html)
    html=re.sub(r'<link rel="stylesheet"[^>]+>','',html)
    page.set_content(html,wait_until='domcontentloaded')
    page.add_style_tag(content=(ROOT/'styles.css').read_text())
    fixtures={x.stem:json.loads(x.read_text()) for x in (ROOT/'assets/studio-task-assets/t04-real-information-board/fixtures').glob('*.json')}
    page.evaluate("""(fixtures) => {
       const storage = () => {
         const map=new Map();
         return {getItem:k=>map.has(k)?map.get(k):null,setItem:(k,v)=>map.set(String(k),String(v)),removeItem:k=>map.delete(k),clear:()=>map.clear()};
       };
       Object.defineProperty(window,'localStorage',{configurable:true,value:storage()});
       Object.defineProperty(window,'sessionStorage',{configurable:true,value:storage()});
       window.__T05_FORCE_TEST_MODE__=true;
       window.fetch=(url)=>{
         const m=String(url).match(/fixtures\\/([^/]+)\\.json/);
         if(m && fixtures[m[1]])return Promise.resolve(new Response(JSON.stringify(fixtures[m[1]]),{status:200}));
         return Promise.resolve(new Response('not found',{status:404}));
       };
    }""",fixtures)
    page.add_script_tag(content=(ROOT/'max-history-data.js').read_text())
    page.add_script_tag(content=(ROOT/'app.js').read_text())
    page.wait_for_function("!!window.__T05_TEST && !!window.MaxHistoryData")
    def setrows(rows): page.evaluate('(x)=>window.__T05_TEST.setRecords(x)',rows)
    def openit(): page.locator('#viewMaxHistory').click();page.locator('#maxHistoryDialog').wait_for(state='visible')
    try:
        if case=='T05-H01':
            setrows([rec('2026-10-09',9,9),rec('2026-10-10',16,16)]);openit()
            assert page.locator('#maxHistoryDialog').evaluate('(x)=>x.open')
            assert page.locator('.max-folder-tab').count()==1
            rect=page.locator('#maxHistoryDialog').bounding_box()
            assert 0<=rect['x'] and rect['x']+rect['width']<=1441
            page.keyboard.press('Escape')
            page.set_viewport_size({'width':390,'height':844});openit();page.wait_for_timeout(100)
            rect=page.locator('#maxHistoryDialog').bounding_box()
            assert 0<=rect['x'] and rect['x']+rect['width']<=391
            assert page.locator('#maxHistoryRows').evaluate('(e)=>e.scrollWidth<=e.clientWidth+1')
        elif case=='T05-H02':
            setrows([rec('2026-10-09',9,9)]);openit()
            snap=page.evaluate('()=>({live:localStorage.getItem("aot_live_records_v1"),events:localStorage.getItem("aot_aurora_events_v1")})')
            page.locator('#maxHistoryClose').click()
            assert not page.locator('#maxHistoryDialog').evaluate('(x)=>x.open'),'Close × did not close the modal'
            openit();page.keyboard.press('Escape')
            assert not page.locator('#maxHistoryDialog').evaluate('(x)=>x.open')
            assert snap==page.evaluate('()=>({live:localStorage.getItem("aot_live_records_v1"),events:localStorage.getItem("aot_aurora_events_v1")})')
        elif case=='T05-H03':
            setrows([rec('2026-10-08',8,8),rec('2026-10-10',10,10),rec('2026-10-09',9,9)])
            openit()
            assert page.locator('.max-history-row time').all_text_contents()==['2026-10-10','2026-10-09','2026-10-08']
        elif case=='T05-H04':
            setrows([rec('2026-10-09',12,65,'2026-10-09T11:20:00Z')]);openit()
            assert page.locator('.max-history-row .max-history-pt').inner_text()=='65 pt'
            assert page.locator('.max-history-row .max-history-fill').evaluate('(e)=>e.style.width')=='65%'
        elif case=='T05-H05':
            setrows([rec('2026-08-25',12,65,'2026-08-25T11:20:00Z')]);openit()
            page.locator('.max-history-row').click()
            assert '2026-08-25 11:20 UTC' in page.locator('#maxHistoryDetail').inner_text()
        elif case=='T05-H06':
            setrows([rec('2026-10-09',5,9,'2026-10-09T12:04:00Z'),rec('2026-10-10',13,16,'2026-10-10T02:24:00Z')]);openit()
            page.locator('[data-date="2026-10-09"]').click()
            detail=page.locator('#maxHistoryDetail').inner_text()
            for fragment in ['2026-10-09','9 pt','5 pt','2026-10-09 12:04 UTC']:
                assert fragment in detail,f'Missing {fragment} in selected day details'
        elif case=='T05-H07':
            setrows([rec('2026-08-24',29,29),rec('2026-08-25',65,65),rec('2026-08-26',65,65)]);openit()
            assert page.locator('#maxHistoryHighest').inner_text()=='65 pt'
            assert page.locator('#maxHistoryPeakDate').inner_text()=='2026-08-26'
        elif case=='T05-H08':
            def step(day,value,stamp):page.evaluate('(x)=>window.__T05_TEST.stepReading(x)',rec(day,value,None,stamp))
            step('2026-10-09',12,'2026-10-09T00:00:00Z')
            step('2026-10-09',30,'2026-10-09T03:00:00Z')
            step('2026-10-10',18,'2026-10-09T15:15:00Z')
            records=page.evaluate('()=>window.__T05_TEST.getRecords()')
            assert len(records)==2
            bydate={r['record_date']:r for r in records}
            assert bydate['2026-10-09']['normalized_value']==30 and bydate['2026-10-09']['max_value']==30
            assert bydate['2026-10-10']['normalized_value']==18 and bydate['2026-10-10']['max_value']==18
            openit();assert page.locator('.max-history-row').count()==2
        elif case=='T05-H09':
            setrows([]);openit()
            assert 'No records yet' in page.locator('#maxHistoryRows').inner_text()
            page.keyboard.press('Escape')
            setrows([rec('2026-10-09',12,None,'2026-10-09T03:00:00Z')]);openit()
            assert page.locator('.max-history-row .max-history-pt').inner_text()=='12 pt'
            assert '2026-10-09 03:00 UTC' in page.locator('.max-history-row .max-history-source').inner_text()
        elif case=='T05-H10':
            setrows([rec('2026-10-09',5,9)])
            before=page.evaluate('()=>({live:localStorage.getItem("aot_live_records_v1"),events:localStorage.getItem("aot_aurora_events_v1"),mock:sessionStorage.getItem("aot_t05_history_fixtures_only")})')
            page.locator('#previewButton').click();page.locator('#previewSlider').fill('85');page.locator('#previewClose').click()
            page.locator('[data-view-target="verification"]').click()
            page.locator('[data-action="resetReplay"]').click();page.locator('[data-action="successSequence"]').click()
            page.wait_for_timeout(150)
            after=page.evaluate('()=>({live:localStorage.getItem("aot_live_records_v1"),events:localStorage.getItem("aot_aurora_events_v1"),mock:sessionStorage.getItem("aot_t05_history_fixtures_only")})')
            assert before==after
        else:raise ValueError(case)
        return 'PASS',''
    except Exception as exc:return 'FAIL',str(exc).strip() or type(exc).__name__
    finally:context.close()
def main():
    with sync_playwright() as p:
        chrome=os.environ.get('T05_CHROME_PATH') or shutil.which('chromium') or shutil.which('google-chrome')
        browser=p.chromium.launch(headless=True,**({'executable_path':chrome} if chrome else {}),args=['--no-sandbox'])
        try: results=[dict(id=t['id'],status=status,detail=reason) for t in CONTRACT['tests'] for status,reason in [test_one(browser,t['id'])]]
        finally:browser.close()
    summary={'test_contract_revision':CONTRACT['test_contract_revision'],'tests':results,'total':len(results),'passed':sum(r['status']=='PASS' for r in results),'failed':sum(r['status']=='FAIL' for r in results),'error_round':any(r['status']=='FAIL' for r in results)}
    print(json.dumps(summary,indent=2,ensure_ascii=False))
    # AI B should save its own output separately. Never overwrite frozen A evidence.
    return 0 if summary['failed']==0 else 1
if __name__=='__main__':sys.exit(main())
