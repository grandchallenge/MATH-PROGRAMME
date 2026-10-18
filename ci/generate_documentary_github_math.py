#!/usr/bin/env python3
"""Create source-traceable GitHub equation readers from raw-HTML documentaries."""
import argparse, hashlib, posixpath, re
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString, Tag

ROOT=Path(__file__).resolve().parents[1]
DOCS=ROOT/"docs/documentaries"
NAMES=("bsd","riemann","hodge","navier_stokes","poincare","p_vs_np","yang_mills")
DEST=DOCS/"github_math"

def relink(url):
    # Original URLs are relative to the public /documentaries/<name>/ HTML
    # pages. The generated Markdown file lives at /documentaries/github_math/
    # and its rendered URL has the same nesting depth as the originals.
    return url

def render(n,inline=False):
    if isinstance(n,NavigableString):
        s=str(n)
        return s if inline else ("\n\n"+s.strip()+"\n\n" if s.strip() else "")
    if not isinstance(n,Tag):return ""
    tag=n.name
    if tag in ("script","style","noscript"):return ""
    if tag=="br":return "\n"
    if tag=="img":return ""
    if tag=="a":
        body="".join(render(c,True) for c in n.children)
        url=relink(n.get("href",""))
        return "["+body+"]("+url+")" if url else body
    if tag in ("strong","b","em","i"):
        mark="**" if tag in ("strong","b") else "*"
        return mark+"".join(render(c,True) for c in n.children).strip()+mark
    if tag=="code":return chr(96)+n.get_text().strip()+chr(96)
    if tag in ("h1","h2","h3","h4"):
        return "\n\n"+("#" * int(tag[1]))+" "+n.get_text(" ",strip=True)+"\n\n"
    if tag=="p":return "\n\n"+"".join(render(c,True) for c in n.children).strip()+"\n\n"
    if tag=="figure":
        label=n.select_one(".plate-label")
        caption=n.select_one("figcaption")
        img=n.select_one("img")
        title=label.get_text(" ",strip=True) if label else "Figure"
        desc=caption.get_text(" ",strip=True) if caption else ""
        alt=img.get("alt","") if img else ""
        href=relink(img.get("src","")) if img else ""
        return "\n\n> **"+title+".** "+desc+(" [Illustration]("+href+")." if href else "")+(" *Alt text:* "+alt if alt else "")+"\n\n"
    if tag=="table":
        rows=[]
        for tr in n.select("tr"):
            cells=[]
            for cell in tr.find_all(("td","th"),recursive=False):
                s="".join(render(c,True) for c in cell.children).strip()
                cells.append(" ".join(s.splitlines()).replace("|",r"\|"))
            if cells:rows.append(cells)
        if not rows:return ""
        width=max(map(len,rows))
        rows=[r+[""]*(width-len(r)) for r in rows]
        row=lambda r:"| "+" | ".join(r)+" |"
        return "\n\n"+"\n".join([row(rows[0]),row(["---"]*width)]+[row(r) for r in rows[1:]])+"\n\n"
    if tag in ("ul","ol"):
        chunks=[]
        for i,li in enumerate(n.find_all("li",recursive=False),1):
            marker=f"{i}." if tag=="ol" else "-"
            chunks.append(marker+" "+"".join(render(c,True) for c in li.children).strip())
        return "\n\n"+"\n".join(chunks)+"\n\n"
    if tag in ("span","sup","sub","small","label","output","li"):
        return "".join(render(c,True) for c in n.children)
    return "".join(render(c,inline) for c in n.children)

def norm_math(t):
    t=re.sub(r"\\\[(.*?)\\\]",lambda m:"\n\n$$\n"+m.group(1).strip()+"\n$$\n\n",t,flags=re.S)
    t=re.sub(r"\\\((.*?)\\\)",lambda m:"$"+m.group(1).strip()+"$",t,flags=re.S)
    t=re.sub(r"(?<!\$)\$\$(?!\$)\s*(.*?)\s*(?<!\$)\$\$(?!\$)",lambda m:"\n\n$$\n"+m.group(1).strip()+"\n$$\n\n",t,flags=re.S)
    # GitHub-compatible equivalent for named math operators. Source TeX is
    # preserved in the canonical HTML; the generated reader uses an explicit
    # math-op with roman lettering, and the inverse transform is parity-tested.
    t=re.sub(r"\\operatorname\{([^{}]+)\}",
             lambda m:r"\mathop{\mathrm{"+m.group(1)+"}}",t)
    # Invisible word boundaries retain established mathematical compounds
    # (L-function, p-adic, codimension-p) while separating dollar delimiters
    # from adjacent letters/hyphens for GitHub and source preflight.
    single=re.compile(r"(?<!\$)\$([^$\n]+)\$(?!\$)")
    old=t
    def boundary(m):
        left=old[m.start()-1] if m.start() else ""
        right=old[m.end()] if m.end()<len(old) else ""
        return ("\u200b" if re.match(r"[\w-]",left) else "")+m.group(0)+( "\u200b" if re.match(r"[\w-]",right) else "")
    t=single.sub(boundary,old)
    # Indentation belongs to the source HTML template, not the article. In
    # Markdown, four accidental template spaces create code fences and suppress
    # mathematical typesetting. Do not retain that presentation whitespace.
    t="\n".join(line.strip() for line in t.splitlines())
    t=re.sub(r"\n{3,}","\n\n",t)
    return t.strip()+"\n"

def formula_bodies(t):
    regex=r"(?<!\$)\$\$(?!\$)(.*?)(?<!\$)\$\$(?!\$)|(?<!\\)\$(?!\$)(.*?)(?<!\\)\$(?!\$)|\\\((.*?)\\\)|\\\[(.*?)\\\]"
    return ["".join(x for x in m.groups() if x is not None).strip() for m in re.finditer(regex,t,flags=re.S)]

def generate(n):
    src=DOCS/(n+".md")
    s=src.read_text(encoding="utf-8")
    dom=BeautifulSoup(s,"html.parser")
    art=dom.select_one("article.monograph-body")
    title=dom.select_one(".monograph-hero h1")
    status=dom.select_one(".monograph-status")
    assert art and title and status,n
    header="# "+title.get_text(" ",strip=True)+"\n\n**Source status:** "+status.get_text(" · ",strip=True)+".\n\n"
    header+="> **GitHub equation reader; automatically generated from the original manuscript.**\n"
    header+="> The [illustrated documentary](../"+n+".md) has the canonical layout, figures and reader controls.\n"
    header+="> This is not independent mathematical or publication certification.\n\n"
    txt=norm_math(header+render(art))
    expected=formula_bodies(art.get_text(" ",strip=False))
    actual=formula_bodies(txt)
    def compact(x):
        x=x.replace("\u200b","")
        x=re.sub(r"\\mathop\{\\mathrm\{([^{}]+)\}\}",
                 lambda m:r"\operatorname{"+m.group(1)+"}",x)
        return re.sub(r"\s+","",x)
    a=list(map(compact,expected));b=list(map(compact,actual))
    if a!=b:
        mismatch=next(((i,x,y) for i,(x,y) in enumerate(zip(a,b)) if x!=y),None)
        raise ValueError(f"{n} source formula mismatch expected={len(a)} generated={len(b)} example={mismatch}")
    assert len(a)>5,(n,len(a))
    assert not re.search(r"\\\(|\\\[",txt)
    note="\n**GitHub equation reader:** [Read the mathematical text with typeset equations](github_math/"+n+".md). The illustrated manuscript below remains canonical.\n\n"
    if note not in s:
        s=note+s
    return src,s,DEST/(n+".md"),txt,len(a)

def main():
    p=argparse.ArgumentParser();p.add_argument("--check",action="store_true");args=p.parse_args()
    stale=[]
    for n in NAMES:
        src,s,out,txt,count=generate(n)
        for path,want in ((src,s),(out,txt)):
            have=path.read_text(encoding="utf-8") if path.exists() else None
            if have!=want:
                if args.check:stale.append(str(path.relative_to(ROOT)))
                else:
                    path.parent.mkdir(parents=True,exist_ok=True)
                    path.write_text(want,encoding="utf-8")
        print(n,count,len(txt),hashlib.sha256(txt.encode()).hexdigest())
    if stale:raise SystemExit("OUTDATED: "+", ".join(stale))
if __name__=="__main__":main()
