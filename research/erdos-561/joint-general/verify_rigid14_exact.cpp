#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <unordered_set>
#include <vector>
using namespace std;
struct Edge{int a,b;};
using M=uint32_t;
struct Graph{vector<Edge> e;array<vector<int>,20> inc;int N=0;};
static M vm(int v){return M(1)<<v;}
static int pc(M x){return __builtin_popcount(x);}
static Graph graph(int A,int B,int shared){
 Graph G;G.e={{0,1},{0,2},{0,3},{4,5},{4,6},{7,8}};
 for(int j=0;j<9;j++){if(A>>j&1)G.e.push_back({9,j});if(B>>j&1)G.e.push_back({10,j});}
 int next=11;
 for(int j=0;j<shared;j++){G.e.push_back({9,next});G.e.push_back({10,next});next++;}
 for(int j=0;j<4-pc(A)-shared;j++)G.e.push_back({9,next++});
 for(int j=0;j<4-pc(B)-shared;j++)G.e.push_back({10,next++});
 if(G.e.size()!=14)abort();
 for(int j=0;j<14;j++){auto [u,v]=G.e[j];G.inc[u].push_back(j);G.inc[v].push_back(j);G.N=max(G.N,max(u,v)+1);}
 return G;
}
static vector<pair<M,uint16_t>> stars(const Graph&G,int d){
 vector<pair<M,uint16_t>> out;
 for(int v=0;v<G.N;v++){
  int N=G.inc[v].size();if(N<d)continue;
  for(int bm=0;bm<(1<<N);bm++)if(__builtin_popcount((unsigned)bm)==d){
   M vertices=vm(v);uint16_t mask=0;
   for(int i=0;i<N;i++)if(bm>>i&1){int k=G.inc[v][i];auto e=G.e[k];vertices|=vm(e.a==v?e.b:e.a);mask|=1<<k;}
   out.push_back({vertices,mask});
  }
 }
 return out;
}
static vector<pair<M,uint16_t>> forest(const Graph&G,vector<int> target){
 vector<vector<pair<M,uint16_t>>> ps;
 for(int d:target)ps.push_back(stars(G,d));
 vector<pair<M,uint16_t>> result;
 auto dfs=[&](auto&&self,int step,M vertices,uint16_t mask)->void{
  if(step==(int)ps.size()){result.push_back({vertices,mask});return;}
  for(auto [v,e]:ps[step])if(!(vertices&v))self(self,step+1,vertices|v,mask|e);
 };
 dfs(dfs,0,0,0);
 sort(result.begin(),result.end());result.erase(unique(result.begin(),result.end()),result.end());
 return result;
}
static bool two_vertex_deletion_necessary(const Graph&G){
 auto patterns=forest(G,{3,2,1});if(patterns.empty())return false;
 for(int u=0;u<G.N;u++){
  M common=0xffffffffu;bool exists=false;
  for(auto [verts,mask]:patterns)if(!(verts&vm(u))){exists=true;common &= verts;}
  if(!exists||common)return false;
 }
 return true;
}
static bool A_fails_single_red_star(const Graph&G){
 auto b=forest(G,{4,1,1,1});if(b.empty())return true;
 M common=0xffffffffu;
 for(auto [v,mask]:b)common &= v;
 return common!=0;
}
static bool A_arrows(const Graph&G){
 auto r=forest(G,{2,1});auto b=forest(G,{4,1,1,1});
 if(b.empty())return false;
 const int size=1<<14;const int all=size-1;
 vector<uint8_t> R(size),B(size);
 for(auto [v,mask]:r)R[mask]=1;
 for(auto [v,mask]:b)B[mask]=1;
 for(int k=0;k<14;k++)for(int mask=0;mask<size;mask++)if(mask&(1<<k)){
  R[mask]|=R[mask^(1<<k)];B[mask]|=B[mask^(1<<k)];
 }
 for(int mask=0;mask<size;mask++)if(!R[mask]&&!B[all^mask])return false;
 return true;
}
static bool B_arrows(const Graph&G){
 auto r=forest(G,{3,2,1});auto b=forest(G,{1,1,1});
 if(r.empty()||b.empty())return false;
 const int size=1<<14;const int all=size-1;
 vector<uint8_t> R(size),B(size);
 for(auto [v,mask]:r)R[mask]=1;
 for(auto [v,mask]:b)B[mask]=1;
 for(int k=0;k<14;k++)for(int mask=0;mask<size;mask++)if(mask&(1<<k)){
  R[mask]|=R[mask^(1<<k)];B[mask]|=B[mask^(1<<k)];
 }
 for(int mask=0;mask<size;mask++)if(!R[mask]&&!B[all^mask])return false;
 return true;
}
int main(int argc,char**argv){int start=argc>1?atoi(argv[1]):0;int stop=argc>2?atoi(argv[2]):256;
 vector<int> subsets;for(int q=0;q<=4;q++)for(int x=0;x<512;x++)if(pc(x)==q)subsets.push_back(x);
 if(stop>256)stop=256;
 uint64_t generated=0,failBnecessary=0,passBnecessary=0,passA=0,passB=0,starred=0;
 for(int ai=start;ai<stop;ai++){
  int A=subsets[ai];
  for(int B:subsets){if((A&B)&1)continue;
   int leftover=min(4-pc(A),4-pc(B));
   for(int h=0;h<=leftover;h++){
    generated++;auto G=graph(A,B,h);
    if(!two_vertex_deletion_necessary(G)){failBnecessary++;continue;}
    passBnecessary++;
    if(A_fails_single_red_star(G)){starred++;continue;}
    if(!A_arrows(G))continue;
    passA++;
    if(!B_arrows(G))continue;
    passB++;
    cout<<"COUNTEREXAMPLE A="<<A<<" B="<<B<<" h="<<h<<" edges=";
    for(auto e:G.e)cout<<"("<<e.a<<","<<e.b<<")";
    cout<<"\n";return 2;
   }
  }
 }
 if(start==0 && stop==256){
  if(generated!=74553 || failBnecessary!=72512 || passBnecessary!=2041 || starred!=1914 || passA!=0 || passB!=0){
    cerr<<"CLASSIFICATION_COUNTS_MISMATCH\n";return 3;
  }
  cout<<"RIGID14_COMPLETE_CPP_EXHAUSTION_PASS\n";
 }
 cout<<"EXACT_PARTITION start="<<start<<" stop="<<stop<<" generated="<<generated<<" failBnecessary="<<failBnecessary<<" passBnecessary="<<passBnecessary<<" single_red_star_avoids_A="<<starred<<" passA="<<passA<<" passB="<<passB<<"\n";
}
