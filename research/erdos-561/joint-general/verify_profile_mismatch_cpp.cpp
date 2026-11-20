// Independent complete C++ finite corroboration for arbitrary host
// equality case (red 3,1,1), (blue 5,2,2,1), edge count 15.
// For each allowed attachment description, explicit avoiding colouring:
// red all edges at hub8; blue all edges elsewhere.
#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <vector>
using namespace std;
struct E{int u,v;};
static int pc(int x){return __builtin_popcount((unsigned)x);}
static bool is_target_blue(const vector<E>& edges,bool &is_all_stars){
 array<vector<int>,20> adj;
 for(auto e:edges){adj[e.u].push_back(e.v);adj[e.v].push_back(e.u);}
 array<bool,20> seen{};
 vector<int> sizes;
 is_all_stars=true;
 for(int i=0;i<20;i++){
  if(adj[i].empty()||seen[i])continue;
  vector<int> vertices{i};seen[i]=true;
  for(size_t j=0;j<vertices.size();j++)for(int v:adj[vertices[j]]){
   if(!seen[v]){seen[v]=true;vertices.push_back(v);}
  }
  int degrees=0,highest=0;
  for(int v:vertices){degrees+=(int)adj[v].size();highest=max(highest,(int)adj[v].size());}
  int Ecount=degrees/2;
  if(Ecount!=(int)vertices.size()-1 || highest!=Ecount){is_all_stars=false;return false;}
  sizes.push_back(Ecount);
 }
 sort(sizes.begin(),sizes.end(),greater<int>());
 return sizes==vector<int>({5,2,2,1});
}
int main(){
 vector<int> subsets;
 for(int k=0;k<=5;k++)for(int mask=0;mask<(1<<8);mask++)if(pc(mask)==k)subsets.push_back(mask);
 uint64_t generated=0,nonstars=0,wrong_profile=0;
 for(int B:subsets)for(int A:subsets){
  for(int h=0;h<=min(5-pc(A),5-pc(B));h++){
   generated++;
   vector<E> red,blue{{0,1},{0,2},{0,3},{4,5},{6,7}};
   int f=10;
   for(int k=0;k<8;k++){
    if(A>>k&1)red.push_back({8,k});
    if(B>>k&1)blue.push_back({9,k});
   }
   for(int j=0;j<h;j++){red.push_back({8,f});blue.push_back({9,f});f++;}
   for(int j=0;j<5-pc(A)-h;j++)red.push_back({8,f++});
   for(int j=0;j<5-pc(B)-h;j++)blue.push_back({9,f++});
   assert(red.size()==5&&blue.size()==10&&f<=20);
   bool all_stars=false;
   if(is_target_blue(blue,all_stars)){
    cerr<<"FOUND_UNEXPECTED_BLUE_F5221 A="<<A<<" B="<<B<<" shared="<<h<<"\n";
    return 2;
   }
   if(all_stars)wrong_profile++;else nonstars++;
  }
 }
 if(generated!=84630 || nonstars!=84108 || wrong_profile!=522){
  cerr<<"CLASSIFICATION_DISAGREEMENT "<<generated<<" "<<nonstars<<" "<<wrong_profile<<"\n";
  return 3;
 }
 cout<<"RIGID15_PROFILE_MISMATCH_CPP_COMPLETE_PASS generated="<<generated
     <<" blue_not_star_forest="<<nonstars
     <<" blue_wrong_star_partition="<<wrong_profile
     <<" both_residuals_15edge_hosts=0\n";
}
