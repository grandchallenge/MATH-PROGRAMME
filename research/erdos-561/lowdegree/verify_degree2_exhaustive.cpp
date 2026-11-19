// All non-isolated finite simple graphs of maximum degree <= 2 with E edges
// are unions of edge-paths and cycles. This exhausts EVERY such isomorphism
// class for E = 8, 10, 11, 12, 13, 14, then finds a red/blue avoidance
// coloring for the exact 3-star target pairs with leading star size 2.
// No external solver; deterministic full-search and exact integer masks.
#include <algorithm>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <map>
#include <set>
#include <string>
#include <vector>
using namespace std;
struct Edge{int a,b;};
struct Component{int edges;bool cycle;};
struct Target{int x,y,z;};
struct Pair{Target red,blue;int E;};
using u64=uint64_t;
static string targetName(Target t){return to_string(t.x)+to_string(t.y)+to_string(t.z);}
static bool equalTarget(vector<int> counts,Target t){
  if(counts.size()!=3)return false;
  sort(counts.begin(),counts.end(),greater<int>());
  return counts[0]==t.x&&counts[1]==t.y&&counts[2]==t.z;
}
// For a mask on E edges, test exact disjoint union of three given stars.
// Because every target component uses <=2 edges, any monochromatic copy
// with exactly target-edge-count edges MUST have exactly this component profile.
static bool exactStarForest(int bits,const vector<Edge>&es,int n,Target t){
  if(__builtin_popcount((unsigned)bits)!=t.x+t.y+t.z)return false;
  vector<int> parent(n);for(int v=0;v<n;++v)parent[v]=v;
  auto root=[&](int v){while(parent[v]!=v)v=parent[v];return v;};
  for(int i=0;i<(int)es.size();++i)if(bits&(1<<i)){
    int a=root(es[i].a),b=root(es[i].b);
    if(a!=b)parent[b]=a;
  }
  vector<int> sizes(n);
  for(int i=0;i<(int)es.size();++i)if(bits&(1<<i)){
    ++sizes[root(es[i].a)];
  }
  vector<int>counts;
  for(int z:sizes)if(z)counts.push_back(z);
  return equalTarget(counts,t);
}
static bool avoidanceExists(const vector<Edge>&es,int n,Target red,Target blue){
  const int E=es.size(),size=1<<E,all=size-1;
  vector<uint8_t>red_contains(size),blue_contains(size);
  const int red_total=red.x+red.y+red.z;
  const int blue_total=blue.x+blue.y+blue.z;
  for(int m=1;m<size;++m){
    int cnt=__builtin_popcount((unsigned)m);
    if(cnt==red_total&&exactStarForest(m,es,n,red))red_contains[m]=1;
    if(cnt==blue_total&&exactStarForest(m,es,n,blue))blue_contains[m]=1;
  }
  // Upward closure: a color mask contains F iff one of its subsets does.
  for(int i=0;i<E;++i)for(int m=0;m<size;++m)if(m&(1<<i)){
    red_contains[m] |=red_contains[m^(1<<i)];
    blue_contains[m]|=blue_contains[m^(1<<i)];
  }
  for(int m=0;m<size;++m)if(!red_contains[m]&&!blue_contains[all^m])return true;
  return false;
}
static void addComponent(vector<Edge>&es,int&n,Component c){
  int base=n;
  if(c.cycle){
    assert(c.edges>=3);
    for(int i=0;i<c.edges;++i)es.push_back({base+i,base+(i+1)%c.edges});
    n+=c.edges;
  }else{
    for(int i=0;i<c.edges;++i)es.push_back({base+i,base+i+1});
    n+=c.edges+1;
  }
}
static vector<Component> species(int E){
  vector<Component>s;
  for(int j=1;j<=E;++j){s.push_back({j,false});if(j>=3)s.push_back({j,true});}
  return s;
}
static bool runGraph(const vector<Component>&components,int E,Target red,Target blue){
  vector<Edge>es;int n=0;
  for(auto c:components)addComponent(es,n,c);
  assert((int)es.size()==E);
  return avoidanceExists(es,n,red,blue);
}
static u64 test_types=0,failed=0;
static void enumerate(const vector<Component>&species,int next,int budget,
                      vector<Component>&components,int E,Target red,Target blue){
  if(budget==0){
    ++test_types;
    if(!runGraph(components,E,red,blue)){
      ++failed;
      cerr<<"ARROWING_COUNTEREXAMPLE E="<<E<<" red="<<targetName(red)
          <<" blue="<<targetName(blue)<<" components:";
      for(auto c:components)cerr<<" "<<(c.cycle?"C":"P")<<c.edges;
      cerr<<"\n";
    }
    return;
  }
  for(int i=next;i<(int)species.size();++i){
    auto c=species[i];if(c.edges>budget)break;
    components.push_back(c);
    enumerate(species,i,budget-c.edges,components,E,red,blue);
    components.pop_back();
  }
}
int main(){
  vector<Pair>cases={
    {{2,1,1},{2,1,1},8},{{2,1,1},{2,2,1},10},
    {{2,1,1},{2,2,2},12},{{2,2,1},{2,2,1},11},
    {{2,2,1},{2,2,2},13},{{2,2,2},{2,2,2},14}};
  // Graph reversal symmetry handles the three other ordered cases.
  for(auto t:cases){
    test_types=failed=0;
    auto s=species(t.E);
    vector<Component>cs;
    enumerate(s,0,t.E,cs,t.E,t.red,t.blue);
    cout<<"CASE "<<targetName(t.red)<<"_"<<targetName(t.blue)
        <<" E="<<t.E<<" graph_types="<<test_types
        <<" arrowing_counterexamples="<<failed<<"\n";
    if(failed)return 11;
  }
  cout<<"DEGREE2_FULL_EXHAUSTIVE_PASS\n";
}
