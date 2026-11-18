// Independent exact enumeration and Ramsey tester for Q (11 edges).
// Standard C++17, no graph packages or external files required.
#include <bits/stdc++.h>
using namespace std;
using Edge=pair<int,int>;
vector<Edge> H={{0,1},{0,2},{0,3},{0,4},{5,6},{5,7},{5,8},{9,10}};

bool has_H(const vector<Edge>& edges, unsigned int redmask) {
  vector<unsigned> adj(14,0);
  int blue=0;
  for(int i=0;i<11;i++) if(!(redmask&(1u<<i))){
    auto [a,b]=edges[i];adj[a]|=1u<<b;adj[b]|=1u<<a;blue++;
  }
  if(blue<8)return false;
  for(int c0=0;c0<14;c0++) if(__builtin_popcount(adj[c0])>=4){
    unsigned p=adj[c0];
    for(unsigned l4=p;l4;l4=(l4-1)&p) if(__builtin_popcount(l4)==4){
      unsigned used=l4|(1u<<c0);
      for(int c1=0;c1<14;c1++) if(!(used>>c1&1)){
        unsigned p2=adj[c1]&~used;
        if(__builtin_popcount(p2)<3)continue;
        for(unsigned l3=p2;l3;l3=(l3-1)&p2) if(__builtin_popcount(l3)==3){
          unsigned used2=used|l3|(1u<<c1);
          for(int i=0;i<11;i++) if(!(redmask>>i&1)){
            auto [u,v]=edges[i];
            if(!(used2>>u&1)&&!(used2>>v&1))return true;
          }
        }
      }
    }
  }
  return false;
}

bool arrows(const vector<Edge>& E){
  for(unsigned r=0;r<(1u<<11);r++){
    unsigned used=0;
    bool matching=true;
    for(int i=0;i<11;i++) if(r>>i&1){
      auto [a,b]=E[i]; unsigned ab=(1u<<a)|(1u<<b);
      if(used&ab){matching=false;break;}
      used|=ab;
    }
    if(matching && !has_H(E,r))return false;
  }
  return true;
}
int main(){
  bool inH[14][14]{};
  for(auto [u,v]:H)inH[u][v]=inH[v][u]=true;
  vector<Edge> can;
  for(int u=0;u<14;u++)for(int v=u+1;v<14;v++){
    if(u>=11)continue; // no new-new edge
    if(inH[u][v])continue;
    can.push_back({u,v});
  }
  unsigned long long tested=0,positive=0;
  for(int i=0;i<(int)can.size();i++)
  for(int j=i+1;j<(int)can.size();j++)
  for(int k=j+1;k<(int)can.size();k++){
    Edge A=can[i],B=can[j],C=can[k];
    unsigned ends=0;bool valid=true;
    for(auto [u,v]:{A,B,C}){
      unsigned b=(1u<<u)|(1u<<v);
      if(ends&b){valid=false;break;}ends|=b;
    }
    if(!valid)continue;
    // Fresh vertex labels must be 11,12,.. in order, and their
    // respective old endpoint indices are increasing (remove fresh symmetry).
    vector<int> front;
    for(auto [u,v]:{A,B,C})if(v>=11)front.emplace_back(u);
    int n=front.size();
    unsigned bits=(ends>>11)&7u;
    if(bits!=((1u<<n)-1))continue;
    // from ordered candidate edge triples, mapping old endpoints to fresh
    // can be in any order: check actual fresh endpoint order.
    vector<int> dest(n,-1);
    for(auto [u,v]:{A,B,C})if(v>=11)dest[v-11]=u;
    for(int a=1;a<n;a++)if(dest[a]<dest[a-1])valid=false;
    if(!valid)continue;
    vector<Edge> E=H;E.insert(E.end(),{A,B,C});tested++;
    if(arrows(E)){
      positive++;
      cout << "PASS extra edges";
      for(auto [u,v]:{A,B,C})cout << " (" << u << "," << v << ")";
      cout << "\n";
    }
  }
  cout << "TOTAL tested=" << tested << " arrows=" << positive << "\n";
  if(tested!=11197 || positive!=2) return 1;
}
