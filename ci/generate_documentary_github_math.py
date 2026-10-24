#!/usr/bin/env python3
"""Create source-traceable GitHub equation readers from raw-HTML documentaries."""
import argparse, hashlib, posixpath, re
from pathlib import Path
from html.parser import HTMLParser

class NavigableString(str):
    """Minimal immutable HTML text node."""

class Tag:
    def __init__(self,name,attrs=None):
        self.name=name
        self.attrs=dict(attrs or [])
        if "class" in self.attrs and self.attrs["class"] is not None:
            self.attrs["class"]=self.attrs["class"].split()
        self.children=[]

    def get(self,name,default=None):
        return self.attrs.get(name,default)

    def _descendants(self):
        for item in self.children:
            if isinstance(item,Tag):
                yield item
                yield from item._descendants()

    def find_all(self,names,recursive=True):
        if isinstance(names,str):names=(names,)
        candidates=self._descendants() if recursive else (x for x in self.children if isinstance(x,Tag))
        return [node for node in candidates if node.name in names]

    def select(self,selector):
        tokens=selector.split()
        def match(node,tok):
            if tok.startswith("."):return tok[1:] in node.get("class",[])
            if "." in tok:
                name,cls=tok.split(".",1)
                return node.name==name and cls in node.get("class",[])
            return node.name==tok
        current=[self]
        for tok in tokens:
            current=[node for item in current for node in item._descendants() if match(node,tok)]
        return current

    def select_one(self,selector):
        matches=self.select(selector)
        return matches[0] if matches else None

    def _strings(self):
        for item in self.children:
            if isinstance(item,NavigableString):yield str(item)
            elif isinstance(item,Tag):yield from item._strings()

    def get_text(self,separator="",strip=False):
        pieces=self._strings()
        if strip:
            pieces=(x.strip() for x in pieces)
            pieces=(x for x in pieces if x)
        return separator.join(pieces)

class HTMLFragmentParser(HTMLParser):
    VOID={"area","base","br","col","embed","hr","img","input","link",
          "meta","param","source","track","wbr"}
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root=Tag("document")
        self.stack=[self.root]
    def handle_starttag(self,name,attrs):
        node=Tag(name,attrs)
        self.stack[-1].children.append(node)
        if name not in self.VOID:self.stack.append(node)
    def handle_startendtag(self,name,attrs):
        self.stack[-1].children.append(Tag(name,attrs))
    def handle_endtag(self,name):
        for index in range(len(self.stack)-1,0,-1):
            if self.stack[index].name==name:
                del self.stack[index:]
                return
    def handle_data(self,data):
        if not data:return
        children=self.stack[-1].children
        # HTMLParser may split text around a literal less-than sign. Preserve
        # contiguous TeX such as 0<Re(s)<1 as ONE math-bearing text span.
        if children and isinstance(children[-1],NavigableString):
            children[-1]=NavigableString(str(children[-1])+data)
        else:children.append(NavigableString(data))

def BeautifulSoup(source,_parser):
    parser=HTMLFragmentParser()
    parser.feed(source)
    parser.close()
    return parser.root


ROOT=Path(__file__).resolve().parents[1]
DOCS=ROOT/"docs/documentaries"
NAMES=("bsd","riemann","hodge","navier_stokes","poincare","p_vs_np","yang_mills","union_closed")
DEST=DOCS/"github_math"

def relink(url):
    # Keep existing manuscript URLs by default. A retained status notice uses
    # a Markdown file target so both GitHub and MkDocs resolve the same page.
    if url == "../MILLENNIUM_PRIZE_STATUS/":
        # Preserve the source notice's status-comparison destination from the
        # reader's deeper source directory; MkDocs rewrites this Markdown link.
        return "../../MILLENNIUM_PRIZE_STATUS.md"
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
        # GitHub does not typeset math inside Markdown link labels. Keep the
        # exact source label as prose and attach the citation as a source link.
        if url and ("$" in body or r"\(" in body or r"\[" in body):
            return body+" ([source]("+url+"))"
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
    # GitHub's GFM Markdown layer consumes TeX escapes for '#' and '|'.
    # Protect literal cardinality marks and replace norm bars by an equivalent
    # operator before markdown parsing, without changing the canonical source.
    t=t.replace(r"\#",r"\\#").replace(r"\|",r"\Vert{}")
    # Visible spaces (not zero-width separators) make GFM recognize inline
    # TeX at compound boundaries such as codimension-$p$ and $L$-function.
    # Invisible word boundaries retain established mathematical compounds
    # (L-function, p-adic, codimension-p) while separating dollar delimiters
    # from adjacent letters/hyphens for GitHub and source preflight.
    single=re.compile(r"(?<!\$)\$([^$\n]+)\$(?!\$)")
    old=t
    def boundary(m):
        left=old[m.start()-1] if m.start() else ""
        right=old[m.end()] if m.end()<len(old) else ""
        return (" " if re.match(r"[\w-]",left) else "")+m.group(0)+( " " if re.match(r"[\w-]",right) else "")
    t=single.sub(boundary,old)
    # GitHub's inline GFM parser treats paired underscores in the mixed-norm
    # scaling identity as Markdown emphasis *before* its math renderer runs.
    # Render that same TeX body as display math, retaining exact source parity.
    t=re.sub(r"(For mixed norms,) \$([^$\n]+)\$\. Thus ",
             lambda m:m.group(1)+"\n\n$$\n"+m.group(2)+"\n$$\n\nThus ",t)
    # Indentation belongs to the source HTML template, not the article. In
    # Markdown, four accidental template spaces create code fences and suppress
    # mathematical typesetting. Do not retain that presentation whitespace.
    t="\n".join(line.strip() for line in t.splitlines())
    t=re.sub(r"\n{3,}","\n\n",t)
    return t.strip()+"\n"

def formula_bodies(t):
    regex=r"(?<!\$)\$\$(?!\$)(.*?)(?<!\$)\$\$(?!\$)|(?<!\\)\$(?!\$)(.*?)(?<!\\)\$(?!\$)|\\\((.*?)\\\)|\\\[(.*?)\\\]"
    return ["".join(x for x in m.groups() if x is not None).strip() for m in re.finditer(regex,t,flags=re.S)]

def pre_article_notices(dom,article):
    """Retain source status notes that precede the canonical article."""
    notices=[]
    for node in dom._descendants():
        if node is article:break
        if node.get("role")=="note":notices.append(node)
    return notices

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
    notices=pre_article_notices(dom,art)
    txt=norm_math(header+"".join(render(note) for note in notices)+render(art))
    expected=formula_bodies(" ".join(node.get_text(" ",strip=False)
                                     for node in [*notices,art]))
    actual=formula_bodies(txt)
    def compact(x):
        x=x.replace("\u200b","").replace(r"\\#",r"\#").replace(r"\Vert{}",r"\|")
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
