import re,time,tempfile,subprocess,urllib.request
from config import *
CACHE={}
def fetch(url):
 h=CACHE.get(url)
 if h and time.time()-h[0]<TTL:return h[1]
 q=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/pdf"})
 with urllib.request.urlopen(q,timeout=40) as r:d=r.read(18000000)
 CACHE[url]=(time.time(),d);return d
def pdftext(url):
 d=fetch(url)
 with tempfile.NamedTemporaryFile(suffix=".pdf") as f:
  f.write(d);f.flush()
  return subprocess.check_output(["pdftotext","-layout",f.name,"-"],timeout=60).decode("utf-8","replace")
def cancelled():
 return {int(x) for x in re.findall(r"(?i)S[ÚU]MULA\s+(?:TJ\s*)?(?:N[º°.]?\s*)?(\d{1,4})",pdftext(CANCELADAS))}
STOP={"de","da","do","das","dos","e","a","o","em","para","por","com","um","uma","no","na","nos","nas","lei","art"}
def toks(q):return [x for x in re.findall(r"[a-z0-9áéíóúâêôãõç]+",q.lower()) if len(x)>2 and x not in STOP]
HEAD=re.compile(r"(?im)^\s*N[º°.]?\s*(\d{1,4})\s*:\s*")
def search(q,limit):
 t=pdftext(SUMULAS);c=cancelled();m=list(HEAD.finditer(t));rows=[];qt=toks(q);excluded=0
 for i,x in enumerate(m):
  n=int(x.group(1));end=m[i+1].start() if i+1<len(m) else len(t)
  body=re.sub(r"\s+"," ",t[x.end():end]).strip()
  if n in c:excluded+=1;continue
  if len(body)<20:continue
  score=sum(k in body.lower() for k in qt)
  if score and (len(qt)<=1 or score>=min(2,len(qt))):
   rows.append((score,{"id":f"tjrj-sumula:{n}","title":f"TJRJ — Súmula {n}","summary":body[:1700],"type":"sumula_tjrj","date":"","organization":"Tribunal de Justiça do Estado do Rio de Janeiro","source":"tjrj_sumulas","source_label":"TJRJ — Súmulas","source_url":SUMULAS,"official_url":SUMULAS,"is_official":True,"is_synthetic":False,"retrieved_at":time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime()),"match_score":score}))
 rows.sort(key=lambda z:(-z[0],-int(z[1]["id"].split(":")[1])))
 return [r for _,r in rows[:limit]],{"source":"tjrj_sumulas","status":"ok","count":min(len(rows),limit),"cancelled_excluded":excluded,"request_url":SUMULAS,"cancelled_registry_url":CANCELADAS,"cache_ttl_seconds":TTL}
