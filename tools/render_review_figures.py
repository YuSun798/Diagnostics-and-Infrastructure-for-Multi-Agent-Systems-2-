from pathlib import Path
import svgwrite, cairosvg

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'figure_sources'
SRC.mkdir(exist_ok=True)
OUT = ROOT

NAVY='#203040'; GRAY='#66727D'; LINE='#D7DEE5'; WHITE='#FFFFFF'
BLUE='#2F6B9A'; BLUE_L='#EAF2F8'
ORANGE='#C77A2D'; ORANGE_L='#FFF3E6'
TEAL='#3E8E8A'; TEAL_L='#E9F5F4'
PURPLE='#7A5FA3'; PURPLE_L='#F1ECF8'
RED='#B84A4A'; RED_L='#FCECEC'
GREEN='#3F8A64'; GREEN_L='#EAF6EF'
PALE='#F5F7F9'
FONT='DejaVu Sans, Arial, sans-serif'

def dwg_new(name,w,h):
    return svgwrite.Drawing(str(SRC/(name+'.svg')), size=(f'{w}px',f'{h}px'), viewBox=f'0 0 {w} {h}')

def rect(d,x,y,w,h,fill=WHITE,stroke=LINE,sw=2,r=16):
    d.add(d.rect(insert=(x,y),size=(w,h),rx=r,ry=r,fill=fill,stroke=stroke,stroke_width=sw))

def text(d,x,y,s,size=24,fill=NAVY,weight='normal',anchor='start',family=FONT):
    d.add(d.text(s,insert=(x,y),fill=fill,font_size=size,font_weight=weight,font_family=family,text_anchor=anchor))

def multiline(d,x,y,lines,size=22,fill=NAVY,weight='normal',anchor='middle',gap=1.25):
    t=d.text('',insert=(x,y),fill=fill,font_size=size,font_weight=weight,font_family=FONT,text_anchor=anchor)
    for i,line in enumerate(lines):
        t.add(d.tspan(line,x=[x],dy=[0 if i==0 else size*gap]))
    d.add(t)

def line(d,x1,y1,x2,y2,stroke=GRAY,sw=3,arrow=False):
    if arrow:
        marker=d.marker(insert=(10,5),size=(10,10),orient='auto',markerUnits='strokeWidth')
        marker.add(d.path(d='M 0 0 L 10 5 L 0 10 z',fill=stroke))
        d.defs.add(marker)
        d.add(d.line((x1,y1),(x2,y2),stroke=stroke,stroke_width=sw,marker_end=marker.get_funciri()))
    else:
        d.add(d.line((x1,y1),(x2,y2),stroke=stroke,stroke_width=sw))

def save(d,name):
    svg=str(SRC/(name+'.svg')); pdf=str(ROOT/(name+'.pdf'))
    d.save(); cairosvg.svg2pdf(url=svg,write_to=pdf)

name='fig1_overview'; W,H=1400,520; d=dwg_new(name,W,H)
text(d,55,48,'MULTI-AGENT RUNTIME STACK',34,NAVY,'bold'); text(d,1345,48,'Review scope',24,GRAY,'bold','end')
rect(d,55,70,1290,105,PALE,'#7A8793',3,22); text(d,80,105,'ORCHESTRATION LAYER',26,NAVY,'bold'); text(d,1320,105,'well surveyed elsewhere',20,GRAY,'normal','end')
for x,w,title,sub in [(80,380,'Workflow frameworks','LangGraph / CrewAI'),(510,380,'Agent orchestration','coordination / routing'),(940,380,'Multi-agent SDKs','execution / tools')]:
    rect(d,x,118,w,44,WHITE,LINE,1.5,10); text(d,x+w/2,144,title,20,NAVY,'bold','middle'); text(d,x+w/2,166,sub,15,GRAY,'normal','middle')
rect(d,55,195,1290,120,BLUE_L,BLUE,3,22); text(d,80,230,'DIAGNOSTICS LAYER',26,BLUE,'bold'); text(d,1320,230,'retain evidence for diagnosis',19,BLUE,'bold','end')
items=[('Failure localization','responsible agent / step'),('Observability','traces / provenance'),('Safety','guardrails / intervention'),('Benchmarks','failure / reliability')]
for i,(a,b) in enumerate(items):
    x=78+i*315; rect(d,x,244,285,55,WHITE,'#B8D0E4',1.5,10); text(d,x+142.5,267,a,19,NAVY,'bold','middle'); text(d,x+142.5,290,b,14,GRAY,'normal','middle')
rect(d,285,335,830,74,'#FFFDF5','#AEB4B8',3,18); text(d,700,365,'SHARED RUNTIME STATE / RETENTION BUDGET',25,'#111111','bold','middle'); text(d,700,393,'traces  |  KV state  |  environment snapshots  |  execution context',17,GRAY,'normal','middle')
text(d,240,374,'retain',18,BLUE,'bold','end'); line(d,250,368,283,368,BLUE,3,True); text(d,1160,374,'discard / reclaim',18,ORANGE,'bold'); line(d,1117,368,1148,368,ORANGE,3,True)
rect(d,55,430,1290,70,ORANGE_L,ORANGE,3,22); text(d,80,462,'INFRASTRUCTURE LAYER',25,ORANGE,'bold'); text(d,1320,462,'serve within memory / latency / power budgets',18,ORANGE,'bold','end')
for x,a,b in [(600,'Memory','evict / prefetch'),(790,'Scheduling','place / prioritize'),(980,'Cache lifecycle','reuse / TTL'),(1175,'Power','resource states')]: text(d,x,480,a,18,NAVY,'bold','middle'); text(d,x,496,b,13,GRAY,'normal','middle')
save(d,name)

name='fig2_diagnostics_taxonomy'; W,H=1400,620; d=dwg_new(name,W,H); text(d,700,48,'MULTI-AGENT DIAGNOSTICS: TAXONOMY',32,NAVY,'bold','middle')
cols=[(60,RED,RED_L,'Failure localization',[('Statistical','FAMAS ★'),('LLM-guided','TrajAudit ★'),('RL-trained','AgenTracer ★')]),(400,TEAL,TEAL_L,'Observability',[('Provenance','Agent Traces ★'),('Standards','OpenTelemetry'),('Tooling','LangSmith / AgentTrace')]),(740,PURPLE,PURPLE_L,'Safety',[('Topology-based','G-Safeguard ★'),('Policy verification','ShieldAgent ★'),('ML-layered','LlamaFirewall')]),(1080,BLUE,BLUE_L,'Benchmarks',[('Trace fidelity','TraceElephant ★'),('Software engineering','RootSE ★'),('General MAS','Who&When')])]
for x,c,cl,title,rows in cols:
    rect(d,x,80,280,470,cl,c,3,20); multiline(d,x+140,122,title.split(' '),24,c,'bold','middle',1.05); y=185
    for a,b in rows:
        rect(d,x+20,y,240,86,WHITE,c,1.5,12); text(d,x+140,y+34,a,20,NAVY,'bold','middle'); text(d,x+140,y+62,b,15,GRAY,'normal','middle'); y+=105
text(d,700,590,'★ full-text verified in the review evidence coding; unstarred entries are abstract-verified or contextual.',15,GRAY,'normal','middle'); save(d,name)

name='fig3_diagnostic_pipeline'; W,H=1400,590; d=dwg_new(name,W,H); text(d,700,48,'END-TO-END DIAGNOSTIC PIPELINE',32,NAVY,'bold','middle')
stages=[(60,BLUE,BLUE_L,'1  AGENT EXECUTION',[('A1  A2  A3  A4',18),('multi-agent trajectory',14),('task • tools • messages',14)]),(385,TEAL,TEAL_L,'2  TRACE CAPTURE',[('agent / step / tool',17),('observation + action',17),('causal / timing context',17)]),(710,PURPLE,PURPLE_L,'3  FAILURE LOCALIZATION',[('Statistical',17),('LLM-guided',17),('RL-trained',17)]),(1035,RED,RED_L,'4  ROOT-CAUSE OUTPUT',[('faulty agent',17),('faulty step / action',17),('supporting evidence',17)])]
for x,c,cl,title,rows in stages:
    rect(d,x,90,285,285,cl,c,3,20); text(d,x+142.5,130,title,20,c,'bold','middle'); y=175
    for val,sz in rows: rect(d,x+25,y,235,48,WHITE,c,1.3,9); text(d,x+142.5,y+31,val,sz,NAVY,'bold' if y==175 else 'normal','middle'); y+=66
for x in [345,670,995]: line(d,x,235,x+30,235,GRAY,3,True)
rect(d,60,420,1260,125,GREEN_L,GREEN,3,20); text(d,85,455,'SAFETY & RUNTIME GUARDRAILS',23,GREEN,'bold'); text(d,1295,455,'operate alongside the execution path',16,GREEN,'bold','end')
for x,a,b in [(110,'Topology-based','graph anomalies / propagation'),(515,'Policy verification','rules before action'),(920,'ML-layered','classifiers / alignment')]: rect(d,x,475,320,50,WHITE,'#A9D0B9',1.5,10); text(d,x+160,497,a,17,NAVY,'bold','middle'); text(d,x+160,518,b,13,GRAY,'normal','middle')
save(d,name)

name='fig4_infrastructure'; W,H=1400,650; d=dwg_new(name,W,H); text(d,700,48,'MULTI-AGENT SERVING: WORKLOADS → OPTIMIZATION FAMILIES',30,NAVY,'bold','middle'); text(d,175,120,'Workload characteristic',20,GRAY,'bold','middle')
headers=[(430,BLUE,BLUE_L,'Memory','optimization'),(670,GREEN,GREEN_L,'Prefix-aware','scheduling'),(910,ORANGE,ORANGE_L,'Cache','lifecycle'),(1150,PURPLE,PURPLE_L,'Power','management')]
for x,c,cl,a,b in headers: rect(d,x-105,88,210,70,cl,c,2,12); text(d,x,116,a,18,c,'bold','middle'); text(d,x,141,b,16,c,'bold','middle')
rows=[('Sparse activation','few agents generate at once',[('ScaleSim','prefetch / eviction',BLUE,BLUE_L),('Activity-aware','placement',None,None),('Idle KV','reclamation',None,None),('KAIROS','phase-aware power',PURPLE,PURPLE_L)]),('Invocation distance','predictable next-use gap',[('ScaleSim','distance-aware eviction',BLUE,BLUE_L),('TOPAS / TokenCake','future-aware placement',GREEN,GREEN_L),('Continuum','TTL / resume policy',ORANGE,ORANGE_L),('Idle phases','expose slack',None,None)]),('Inter-agent sharing','shared prompts / KV prefixes',[('Shared-state','memory pressure',None,None),('TokenCake / KVFlow','prefix-aware routing',GREEN,GREEN_L),('ForkKV / KVCOMM','reuse / copy-on-write',ORANGE,ORANGE_L),('Indirect','efficiency effect',None,None)])]
y=190
for title,sub,cells in rows:
    rect(d,45,y,260,110,WHITE,LINE,2,14); text(d,175,y+42,title,18,NAVY,'bold','middle'); text(d,175,y+72,sub,13,GRAY,'normal','middle')
    for j,(a,b,c,cl) in enumerate(cells):
        x=325+j*240; rect(d,x,y,210,110,cl or WHITE,c or LINE,2 if c else 1.5,14); text(d,x+105,y+42,a,17,NAVY,'bold' if c else 'normal','middle'); text(d,x+105,y+72,b,13,GRAY,'normal','middle')
    y+=130
rect(d,45,590,1270,42,PALE,LINE,1.5,10); text(d,680,617,'Current gap: surveyed systems optimize subsets of the stack; diagnostic signals are not a first-class serving input.',15,NAVY,'bold','middle'); save(d,name)

name='fig5_tension'; W,H=1400,720; d=dwg_new(name,W,H); text(d,700,48,'THE DIAGNOSTICS–INFRASTRUCTURE RETENTION TENSION',30,NAVY,'bold','middle')
rect(d,55,100,270,500,BLUE_L,BLUE,3,20); rect(d,1075,100,270,500,ORANGE_L,ORANGE,3,20); text(d,190,140,'DIAGNOSTICS',24,BLUE,'bold','middle'); text(d,190,168,'RETAIN',17,BLUE,'bold','middle'); text(d,1210,140,'INFRASTRUCTURE',24,ORANGE,'bold','middle'); text(d,1210,168,'DISCARD / RECLAIM',17,ORANGE,'bold','middle')
for y,a,b in [(220,'Failure localization','full traces / history'),(330,'Observability','rich execution context'),(440,'Replay / repair','restorable state')]: rect(d,82,y,216,82,WHITE,'#9FC0DA',1.5,10); text(d,190,y+33,a,17,NAVY,'bold','middle'); text(d,190,y+59,b,13,GRAY,'normal','middle')
for y,a,b in [(220,'Memory management','evict low-reuse state'),(330,'Scheduling','bound latency / overhead'),(440,'Cache lifecycle','expire / recompute')]: rect(d,1102,y,216,82,WHITE,'#E1B27A',1.5,10); text(d,1210,y+33,a,17,NAVY,'bold','middle'); text(d,1210,y+59,b,13,GRAY,'normal','middle')
rect(d,390,100,620,86,'#FFFDF5','#AEB4B8',2.5,14); text(d,700,134,'SHARED RUNTIME STATE',23,'#111111','bold','middle'); text(d,700,164,'retention budget: memory | trace fidelity | replayability',15,GRAY,'normal','middle'); line(d,325,143,388,143,BLUE,3,True); line(d,1074,143,1012,143,ORANGE,3,True)
cards=[(210,RED,RED_L,'Cross-layer conflict 1: eviction','Serving evicts inactive state; post-hoc diagnosis values that history.'),(305,RED,RED_L,'Cross-layer conflict 2: snapshots','Replay methods need restorable environment state not retained by default.'),(400,PURPLE,PURPLE_L,'Intra-layer analogue: compression','TrajAudit trades retained context for lower diagnostic cost.'),(495,'#7B8790','#F3F5F6','Boundary condition: replay cost','Replay becomes a serving conflict when diagnosis moves online.')]
for y,c,cl,a,b in cards: rect(d,390,y,620,76,cl,c,1.8,10); text(d,420,y+30,a,16,c,'bold'); text(d,420,y+55,b,13,GRAY)
rect(d,120,630,1160,50,GREEN_L,GREEN,2,12); text(d,700,661,'Empirical anchor (TraceElephant): full traces raise step-level attribution from 16% to 28.1% (+76% relative).',15,GREEN,'bold','middle'); save(d,name)

name='fig6_codesign_agenda'; W,H=1400,640; d=dwg_new(name,W,H); text(d,700,48,'CO-DESIGN RESEARCH AGENDA',32,NAVY,'bold','middle'); text(d,700,78,'Four ways to make the retention budget an explicit cross-layer resource',17,GRAY,'normal','middle')
qs=[(55,110,RED,RED_L,'1. Retention-aware eviction',['suspect state','pin / protect','preserve evidence'],'Trade bounded memory for replayable diagnostic evidence.'),(715,110,BLUE,BLUE_L,'2. Failure-aware scheduling',['attribution signal','scheduler','deprioritize risk'],'Feed reliability evidence back into placement and execution policy.'),(55,350,GREEN,GREEN_L,'3. Budgeted observability',['SLO / budget','trace fidelity','dynamic capture'],'Negotiate diagnostic fidelity against serving cost at runtime.'),(715,350,PURPLE,PURPLE_L,'4. Infrastructure-triggered diagnostics',['latency / memory','early warning','start diagnosis'],'Use serving anomalies as triggers before task-level failure surfaces.')]
for x,y,c,cl,title,steps,desc in qs:
    rect(d,x,y,630,200,cl,c,3,18); text(d,x+24,y+38,title,21,c,'bold'); sx=x+28
    for i,step in enumerate(steps):
        rect(d,sx+i*190,y+75,160,52,WHITE,'#D4DADF',1.5,9); text(d,sx+i*190+80,y+107,step,14,NAVY,'bold','middle')
        if i<2: line(d,sx+i*190+160,y+101,sx+i*190+185,y+101,c,2.5,True)
    text(d,x+315,y+165,desc,13,GRAY,'normal','middle')
rect(d,180,585,1040,38,PALE,LINE,1.5,9); text(d,700,610,'All four are research proposals grounded in surveyed components; none is claimed as an implemented system.',14,GRAY,'normal','middle'); save(d,name)

print('generated', sorted(p.name for p in ROOT.glob('fig*.pdf')))
