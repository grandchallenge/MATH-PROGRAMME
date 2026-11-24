(* GCL / RH-A26. Reproducible public figures. Evaluate in Wolfram Language.
   Output: five SVG strings, marked FIGURE:<basename>:<svg...>.
   No theorem certification; all diagrams are bounded illustrations. *)
ClearAll[num, el, tx, ln, box, dot, path, arr, plate, figs, x, y, p, q];
num[v_] := ToString[Round[v], InputForm];
ink = "#20262b"; muted = "#56616a"; blue = "#35647a"; light = "#eaf1f3"; pale = "#f5f6f7"; red = "#9b5140"; white = "#ffffff"; grid = "#d8dde0";
el[tag_, attrs_, body_:""] := "<"<>tag<>" "<>StringRiffle[(#[[1]]<>"='"<>ToString[#[[2]]]<>"'")& /@ attrs," "]<>If[body==="","/>",">"<>body<>"</"<>tag<>">"];
tx[x_,y_,s_,size_:18,col_:ink,anchor_:"start",weight_:"400"] := el["text",{{"x",num[x]},{"y",num[y]},{"font-size",size},{"fill",col},{"text-anchor",anchor},{"font-weight",weight}},s];
ln[x_,y_,u_,v_,c_:grid,w_:1,d_:""] := el["line",Join[{{"x1",num[x]},{"y1",num[y]},{"x2",num[u]},{"y2",num[v]},{"stroke",c},{"stroke-width",w}},If[d==="",{},{{"stroke-dasharray",d}}]]];
box[x_,y_,w_,h_,fill_:white,stroke_:grid,r_:0] := el["rect",{{"x",num[x]},{"y",num[y]},{"width",num[w]},{"height",num[h]},{"fill",fill},{"stroke",stroke},{"rx",r}}];
dot[x_,y_,r_:5,c_:blue] := el["circle",{{"cx",num[x]},{"cy",num[y]},{"r",r},{"fill",c}}];
path[pts_,c_:ink,w_:2,d_:""] := el["polyline",Join[{{"points",StringRiffle[(num[#[[1]]]<>","<>num[#[[2]]])& /@ pts," "]},{"fill","none"},{"stroke",c},{"stroke-width",w},{"stroke-linejoin","round"},{"stroke-linecap","round"}},If[d==="",{},{{"stroke-dasharray",d}}]]];
arr[x_,y_,u_,v_,c_:muted] := Module[{d={u-x,v-y},t,b},t=Normalize[d];b={-t[[2]],t[[1]]};ln[x,y,u,v,c,2]<>path[{{u,v}-9t+5b,{u,v},{u,v}-9t-5b},c,2]];
plate[id_,title_,desc_,h_,body_,kind_] := "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 760 "<>num[h]<>"' role='img' aria-labelledby='"<>id<>"-t "<>id<>"-d'><title id='"<>id<>"-t'>"<>title<>"</title><desc id='"<>id<>"-d'>"<>desc<>"</desc><g font-family='Arial, Helvetica, sans-serif'>"<>box[0,0,760,h,white,white]<>tx[28,34,title,23,ink,"start","700"]<>tx[732,58,kind,12,muted,"end","600"]<>ln[28,70,732,70,grid]<>body<>"</g></svg>";
(* A: sampled zero heights; axes are linear, not an exhaustive zero search. *)
heights=N[Table[Im[ZetaZero[k]],{k,1,5}],14];
figA=Module[{xx,yy,b},xx[t_]:=120+440t;yy[t_]:=346-7t;
 b=box[xx[0],yy[36],440,252,light,light]<>ln[xx[0],yy[36],xx[0],yy[0],muted,1]<>ln[xx[1],yy[36],xx[1],yy[0],muted,1]<>ln[xx[1/2],yy[36],xx[1/2],yy[0],blue,2,"6 5"]<>ln[xx[0],yy[0],xx[1],yy[0],ink,1];
 b=b<>StringJoin[Table[ln[xx[0],yy[t],xx[1],yy[t],grid]<>tx[108,yy[t]+5,ToString[t],13,muted,"end"],{t,{0,10,20,30}}]];
 b=b<>StringJoin[MapIndexed[dot[xx[1/2],yy[#1],6,blue]<>tx[xx[1/2]+14,yy[#1]+4,"zero "<>ToString[First[#2]],12,ink]&,heights]];
 b=b<>tx[xx[0],368,"0",14,ink,"middle"]<>tx[xx[1/2],368,"1/2",14,ink,"middle","700"]<>tx[xx[1],368,"1",14,ink,"middle"]<>tx[340,395,"real part",15,muted,"middle"]<>tx[28,89,"imaginary",13,muted]<>tx[28,104,"height",13,muted]<>tx[578,124,"Critical line",16,blue,"start","700"]<>tx[578,147,"RH concerns every",14,ink]<>tx[578,167,"nontrivial zero,",14,ink]<>tx[578,187,"not just these five.",14,ink];
 plate["rhstrip","A. What RH says","Five known upper-half-plane zeta zeros, at heights 14.13 through 32.94, plotted on the line real part one-half. No claim of exhaustive search.",420,b,"NUMERICAL SAMPLE"]];
(* B: right-continuous prime-count staircase. Sample RiemannR every integer. *)
figB=Module[{xx,yy,b,pr,stairs,smooth},xx[t_]:=86+6.12(t-2);yy[t_]:=350-9.8t;
 pr=Prime[Range[PrimePi[100]]];stairs=Join[{{2,0}},Flatten[Table[{{pr[[j]],j-1},{pr[[j]],j}},{j,Length[pr]}],1],{{100,Length[pr]}}];
 smooth=Table[{n,N[RiemannR[n],12]},{n,2,100}];
 b=StringJoin[Table[ln[xx[2],yy[t],xx[100],yy[t],grid]<>tx[76,yy[t]+4,ToString[t],13,muted,"end"],{t,0,25,5}]];
 b=b<>ln[xx[2],yy[0],xx[100],yy[0],ink]<>ln[xx[2],yy[0],xx[2],yy[27],ink]<>path[({xx[#[[1]]],yy[#[[2]]]}& /@ smooth),blue,3]<>path[({xx[#[[1]]],yy[#[[2]]]}& /@ stairs),ink,2];
 b=b<>StringJoin[Table[tx[xx[t],371,ToString[t],13,muted,"middle"],{t,{2,20,40,60,80,100}}]]<>tx[380,397,"Numbers up to x",15,muted,"middle"]<>ln[98,91,133,91,ink,2]<>tx[143,96,"Actual prime count",15,ink]<>ln[382,91,417,91,blue,3]<>tx[427,96,"Smooth Riemann R(x)",15,blue]<>tx[86,121,"Number of primes",13,muted];
 plate["rhprimes","B. A staircase and its smooth approximation","Exact prime counting staircase from 2 to 100, alongside Riemann R sampled at integer arguments and joined by segments. Both axes linear; rounded screen coordinates.",420,b,"DATA-DERIVED"]];
(* C: exact homomorphism classes for trivial action. *)
classes=Select[Range[0,2],Mod[3 #,3]==0&]; targets=Select[Range[0,2],Mod[# ,3]==0&];
If[classes!={0,1,2}||targets!={0},Abort[]];
figC=Module[{b,ys={130,200,270}},b=tx[175,100,"Three distinct classes",17,ink,"middle","700"]<>tx[590,100,"One class after restriction",17,ink,"middle","700"];
 b=b<>StringJoin[MapThread[(arr[220,#2,536,200,If[#1==0,muted,red]]<>box[125,#2-23,95,46,If[#1==0,pale,light],grid,6]<>tx[172,#2+6,ToString[#1],23,ink,"middle","700"])&,{classes,ys}]]<>box[536,177,104,46,pale,grid,6]<>tx[588,206,"0",23,ink,"middle","700"]<>tx[380,322,"The two nonzero classes become zero.",18,red,"middle","700"]<>tx[380,349,"Index = 3; division by 3 is impossible modulo 3.",16,muted,"middle"];
 plate["rhcollapse","C. A transformation can erase information","Exact finite counterexample: first cohomology of C3 with trivial F3 coefficients has three classes 0, 1, 2. Restriction to the trivial subgroup sends all three to zero.",380,b,"EXACT FINITE MODEL"]];
(* D: exact finite parity quotient, not a literal image of a Galois group. *)
perms=Permutations[Range[3]];fibers=GatherBy[SortBy[perms,-Signature[#]&],Signature];
If[Length[fibers]!=2||Length/@fibers!={3,3},Abort[]];
nameMap=<|"123"->"identity","231"->"(123)","312"->"(132)","213"->"(12)","321"->"(13)","132"->"(23)"|>;
figD=Module[{b,ys={157,272},cols={blue,muted},labels,yy},b=tx[180,101,"Six symmetries in S3",17,ink,"middle","700"]<>tx[590,101,"Two quotient classes",17,ink,"middle","700"];
 Do[yy=ys[[j]];labels=(nameMap[StringJoin[ToString /@ #]]& /@ fibers[[j]]);
 b=b<>box[35,yy-36,319,75,If[j==1,light,pale],grid,6]<>tx[48,yy-15,If[j==1,"Even permutations","Odd permutations"],13,cols[[j]],"start","700"]<>StringJoin[MapIndexed[tx[58+100(First[#2]-1),yy+19,#1,16,ink]&,labels]]<>arr[354,yy,525,yy,cols[[j]]]<>box[525,yy-27,198,54,white,cols[[j]],6]<>tx[624,yy+6,If[j==1,"Even coset","Odd coset"],18,cols[[j]],"middle","700"],{j,2}];
 b=b<>tx[380,345,"A function that is constant within each group descends to the quotient.",15,ink,"middle"]<>tx[380,370,"For the arithmetic argument, vanishing on inertia supplies this condition.",14,muted,"middle"];
 plate["rhquotient","D. When can we safely forget symmetries?","Exact S3 parity fibers, schematic placement. The map to the quotient C2 groups all three even permutations and all three odd permutations. The actual Galois group is not pictured.",400,b,"EXACT FINITE MODEL"]];
(* E: a status map, not the full dependency graph or completion percentage. *)
figE=Module[{b},b=box[36,92,688,70,light,grid,6]<>tx[52,117,"Reconstructed mathematics",18,blue,"start","700"]<>tx[52,143,"Local restriction and quotient inflation, under their hypotheses.",15,ink]<>arr[380,162,380,188]<>box[36,188,688,70,pale,grid,6]<>tx[52,213,"Source bridges still to verify",18,ink,"start","700"]<>tx[52,239,"Do the actual arithmetic modules and eigenspaces match?",15,ink]<>arr[380,258,380,284]<>box[36,284,688,84,"#fbf2ef",red,6]<>tx[52,309,"Open arithmetic estimate",18,red,"start","700"]<>tx[52,333,"ML.vChar: bound the size of arithmetic structures by divisibility.",15,ink]<>tx[52,354,"The reciprocity hypothesis Rec and the precise inequality need scrutiny.",14,muted]<>tx[380,403,"Original Lean replay and final RH/GRH claim: not independently certified.",15,ink,"middle","700"];
 plate["rhstatus","E. What the audit has and has not established","Schematic audit reading order: reconstructed conditional transfer; source bridges requiring verification; unresolved Bernoulli-to-cohomology valuation bound. This is not a complete dependency graph.",430,b,"SCHEMATIC STATUS MAP"]];
figs=<|"rh-a26-critical-line"->figA,"rh-a26-prime-count"->figB,"rh-a26-restriction"->figC,"rh-a26-quotient"->figD,"rh-a26-frontier"->figE|>;
KeyValueMap[(Print["FIGURE:"<>#1<>":"<>#2])&,figs];
(* To export locally: KeyValueMap[(Export[#1<>".svg",#2,"Text"])&,figs]; *)
