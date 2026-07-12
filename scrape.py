import re,time,tempfile,subprocess,urllib.request
from html.parser import HTMLParser
from config import *
CACHE={}
class P(HTMLParser):
 def __init__(s):super().__init__();s.b=[];s.skip=0
 def handle_starttag(s,t,a):
  if t in {"script","style","nav","header","footer"}:s.skip+=1
  elif t in {"p","li","div","h1","h2","h3","h4","br","td"} and not s.skip:s.b.append("\n")
 def handle_endtag(s,t):
  if t in {"script","style","nav","header","footer"} and s.skip:s.skip-=1
  elif t in {"p","li","div","h1","h2","h3","h4","td"} and not s.skip:s.b.append("\n")
 def handle_data(s,d):
  if not s.skip:s.b.append(d)
def fetch(url,accept):
 h=CACHE.get(url)
 if h and time.time()-h[0]<TTL:return h[1]
 q=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":accept})
 with urllib.request.urlopen(q,timeout=35) as r:d=r.read(15000000)
 CACHE[url]=(time.time(),d);return d
def htmltext():
 p=P();p.feed(fetch(SUMULAS,"text/html").decode("utf-8","replace"))
 return re.sub(r"\n{2,}","\n",re.sub(r"[ \t]+"," ","".join(p.b)))
def cancelled():
 data=fetch(CANCELADAS,"application/pdf")
 with tempfile.NamedTemporaryFile(suffix=".pdf") as f:
  f.write(data);f.flush()
  t=subprocess.check_output(["pdftotext","-layout",f.name,"-"],timeout=50).decode("utf-8","replace")
 return {int(x) for x in re.findall(r"(?i)S[ÚU]MULA\s+(?:TJ\s*)?(?:N[º°.]?\s*)?(\d{1,4})",t)}
STOP={"de","da","do","das","dos","e","a","o","em","para","por","com","um","uma","no","na","nos","nas","lei","art"}
def toks(q):return [x for x in re.findall(r"[a-z0-9áéíóúâêôãõç]+",q.lower()) if len(x)>2 and x not in STOP]
HEAD=re.compile(r"(?i)(?:S[ÚU]MULA\s+(?:TJ\s*)?(?:N[º°.]?\s*)?|N[º°.]?\s*)(\d{1,4})\s*[-–—:]?\s*")
def search(q,limit):
 t=htmltext();c=cancelled();m=list(HEAD.finditer(t));rows=[];qt=toks(q);excluded=0
 for i,x in enumerate(m):
  n=int(x.group(1));end=m[i+1].start() if i+1<len(m) else min(len(t),x.end()+2500)
  body=re.sub(r"\s+"," ",t[x.end():end]).strip()
  if n in c:excluded+=1;continue
  if len(body)<20:continue
  score=sum(k in body.lower() for k in qt)
  if score and (len(qt)<=1 or score>=min(2,len(qt))):
   rows.append((score,{"id":f"tjrj-sumula:{n}","title":f"TJRJ — Súmula {n}","summary":body[:1700],"type":"sumula_tjrj","date":"","organization":"Tribunal de Justiça do Estado do Rio de Janeiro","source":"tjrj_sumulas","source_label":"TJRJ — Súmulas","source_url":SUMULAS,"official_url":SUMULAS,"is_official":True,"is_synthetic":False,"retrieved_at":time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime()),"match_score":score}))
 rows.sort(key=lambda z:(-z[0],z[1]["title"]))
 return [r for _,r in rows[:limit]],{"source":"tjrj_sumulas","status":"ok","count":min(len(rows),limit),"cancelled_excluded":excluded,"request_url":SUMULAS,"cancelled_registry_url":CANCELADAS,"cache_ttl_seconds":TTL}
