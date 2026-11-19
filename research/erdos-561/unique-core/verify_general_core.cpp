// GCL Erdős #561. Independent C++17 finite test of the ordinary Lovasz
// (g,f)-factor cut criterion, and the maximum-degree core theorem.
// This is an exhaustive BOUNDED sanity check, not a general proof.
#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <vector>
using namespace std;
struct E {int u,v;};
static uint64_t graph_total=0, cap_total=0, fail_total=0, factor_checks=0, general_cases=0, general_obstructions=0;
static int dc(const vector<E>& edges, vector<int>& deg) {
  fill(deg.begin(),deg.end(),0);
  for(auto e:edges) {deg[e.u]++;deg[e.v]++;}
  return *max_element(deg.begin(),deg.end());
}
static bool splitDFS(const vector<E>& edges,int i,int a,int b,vector<int>& red,vector<int>& blue) {
  if(i==(int)edges.size())return true;
  auto e=edges[i];
  if(red[e.u]<a && red[e.v]<a) {++red[e.u];++red[e.v];if(splitDFS(edges,i+1,a,b,red,blue))return true;--red[e.u];--red[e.v];}
  if(blue[e.u]<b && blue[e.v]<b) {++blue[e.u];++blue[e.v];if(splitDFS(edges,i+1,a,b,red,blue))return true;--blue[e.u];--blue[e.v];}
  return false;
}
static bool capSplit(const vector<E>& edges,int n,int a,int b) {
  vector<int> red(n),blue(n); return splitDFS(edges,0,a,b,red,blue);
}
static int maxCoreComponent(const vector<E>& edges,const vector<int>&deg,int D) {
  int n=deg.size(),done=0,big=0;
  for(int v=0;v<n;++v)if(deg[v]==D && !(done&(1<<v))) {
    int reach=1<<v,prev=0;
    while(reach!=prev) {prev=reach;for(auto e:edges)if(deg[e.u]==D&&deg[e.v]==D) {
      if(reach&(1<<e.u))reach|=1<<e.v;
      if(reach&(1<<e.v))reach|=1<<e.u;
    }}
    done|=reach;big=max(big,__builtin_popcount((unsigned)reach));
  }
  return big;
}
// Componentwise exact classification for k <= 2D+1.
static bool oddIsolatedRegular(const vector<E>& edges,const vector<int>& deg,int D) {
  const int n=deg.size();int visited=0;
  for(int v=0;v<n;++v)if(!(visited&(1<<v))) {
    int C=1<<v,old=0;
    while(C!=old) {old=C;for(auto e:edges) {
      if(C&(1<<e.u))C|=1<<e.v;
      if(C&(1<<e.v))C|=1<<e.u;
    }}
    visited|=C;
    if((__builtin_popcount((unsigned)C)&1)==0)continue;
    bool regular=true;
    for(int w=0;w<n;++w)if(C&(1<<w))if(deg[w]!=D)regular=false;
    if(regular)return true;
  }
  return false;
}
static bool factorCriterion(const vector<E>& edges,const vector<int>&deg,int a,int b) {
  int n=deg.size(),cases=1;for(int i=0;i<n;++i)cases*=3;
  for(int code=0;code<cases;++code) {
    int x=code,S=0,T=0;
    for(int v=0;v<n;++v){int z=x%3;x/=3;if(z==1)S|=1<<v;else if(z==2)T|=1<<v;}
    int U=((1<<n)-1)&~(S|T),fS=0,gT=0,degT=0,eST=0,q=0;
    for(int v=0;v<n;++v){if(S&(1<<v))fS+=min(a,deg[v]);if(T&(1<<v)){gT+=max(0,deg[v]-b);degT+=deg[v];}}
    for(auto e:edges)if(((((S>>e.u)&1)!=0)&&(((T>>e.v)&1)!=0))||((((T>>e.u)&1)!=0)&&(((S>>e.v)&1)!=0)))++eST;
    int seen=0;
    for(int v=0;v<n;++v)if((U&(1<<v))&&!(seen&(1<<v))) {
      int C=1<<v,prior=0;
      while(C!=prior){prior=C;for(auto e:edges)if((U&(1<<e.u))&&(U&(1<<e.v))) {
        if(C&(1<<e.u))C|=1<<e.v;
        if(C&(1<<e.v))C|=1<<e.u;
      }}
      seen|=C;bool tight=true;int fC=0,eCT=0;
      for(int w=0;w<n;++w)if(C&(1<<w)){
        int f=min(a,deg[w]),g=max(0,deg[w]-b);
        if(f!=g)tight=false;
        fC+=f;
      }
      for(auto e:edges)if(((((C>>e.u)&1)!=0)&&(((T>>e.v)&1)!=0))||((((T>>e.u)&1)!=0)&&(((C>>e.v)&1)!=0)))++eCT;
      if(tight && ((fC+eCT)&1))++q;
    }
    if(fS+degT-gT-eST-q<0)return false;
  }
  return true;
}
int main(){
  for(int n=2;n<=6;++n){
    vector<E> complete;for(int u=0;u<n;++u)for(int v=u+1;v<n;++v)complete.push_back({u,v});
    int total=1<<complete.size();
    for(int mask=0;mask<total;++mask){
      ++graph_total;vector<E> ed;vector<int> deg(n);
      for(int i=0;i<(int)complete.size();++i)if(mask&(1<<i))ed.push_back(complete[i]);
      int D=dc(ed,deg);
      for(int a=1;a<D;++a){
        int b=D-a;++cap_total;
        bool split=capSplit(ed,n,a,b);
        int core=maxCoreComponent(ed,deg,D);
        int saturated=0;for(int z:deg)if(z==D)++saturated;
        if(saturated <= 2*D+1) {
          ++general_cases;
          bool predictsFailure=(D%2==0 && a%2==1 && oddIsolatedRegular(ed,deg,D));
          if(predictsFailure != !split) {
            cerr<<"GENERAL_CLASSIFIER_MISMATCH n="<<n<<" mask="<<mask<<" a="<<a<<" D="<<D<<" k="<<saturated<<"\n";
            return 9;
          }
          if(!split)++general_obstructions;
        }
        if(!split){++fail_total;if(core<D+1){cerr<<"CORE_COUNTEREXAMPLE n="<<n<<" mask="<<mask<<" a="<<a<<" D="<<D<<" core="<<core<<"\n";return 7;}}
        // Exact Lovasz parity criterion independent of red-edge DFS.
        if(n<=5 || (n==6 && ((mask*1103515245u+12345u)%127u)==0)){
          ++factor_checks;
          bool criterion=factorCriterion(ed,deg,a,b);
          if(criterion!=split){cerr<<"FACTOR_CRITERION_MISMATCH n="<<n<<" mask="<<mask<<" a="<<a<<"\n";return 8;}
        }
      }
    }
  }
  // New odd-order D-regular connected obstructions beyond the clique.
  // K_{D+3} minus a Hamilton cycle is D-regular with odd order.
  for(int D : {2,4,6}) {
    int n=D+3;
    vector<E> ed;vector<int> deg(n);
    for(int a=0;a<n;++a)for(int b=a+1;b<n;++b) {
      if(b==(a+1)%n || a==(b+1)%n)continue;
      ed.push_back({a,b});
    }
    assert(dc(ed,deg)==D);
    for(int a=1;a<D;++a) {
      const bool predicts=(a%2==1);
      const bool split=capSplit(ed,n,a,D-a);
      if(split==predicts){
        cerr<<"DPLUS3_ODD_CORE_CLASSIFICATION_MISMATCH D="<<D<<" alpha="<<a<<"\n";
        return 13;
      }
    }
  }
  cout<<"PASS {graphs:"<<graph_total<<",cap_instances:"<<cap_total
      <<",obstructions:"<<fail_total<<",exact_lovasz_comparisons:"<<factor_checks<<",general_cases:"<<general_cases<<",general_obstructions:"<<general_obstructions<<"}\n";
}
