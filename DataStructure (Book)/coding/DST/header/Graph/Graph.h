#ifndef DST_GRAPH_H
#define DST_GRAPH_H

#include "..\Stack\Stack.h"
#include "..\Queue\Queue.h"
#include <climits>

typedef enum { UNDISCOVERED, DISCOVERED, VISITED } VStatus;	//顶点状态
typedef enum { UNDETERMINED, TREE, CROSS, FORWARD, BACKWARD } EType;	//边在遍历树中所属的类型

namespace DST {
	template <typename Tv, typename Te>		//顶点类型,边类型
	class Graph {
	private:
		void reset() {	//所有顶点,边的辅助信息复位
			for(int i = 0; i < n; ++i) {
				status(i) = UNDISCOVERED;
				dTime(i) = fTime(i) = -1;
				parent(i) = -1;
				priority(i) = INT_MAX;
				for(int j = 0; j < n; ++j) {
					if(exists(i, j)) type(i, j) = UNDETERMINED;
				}
			}
		}

		void BFS(int, int&);	//广度优先搜索算法
		void DFS(int, int&);	//深度优先搜索算法
		void BCC(int, int&, Stack<int>&);	//基于DFS的双连通分量分解算法
		bool TSort(int, int&, Stack<Tv>*);	//基于DFS的拓扑排序算法
		template <typename PU> void PFS(int, PU);	//优先级搜索框架

	public:
		int n;	//顶点总数
		virtual int insert(Tv const&) = 0;		//插入顶点,返回编号
		virtual Tv remove(int) = 0;				//删除顶点及其关联边,返回该顶点信息
		virtual Tv& vertex(int) = 0;			//顶点v的数据
		virtual int inDegree(int) = 0;			//顶点入度
		virtual int outDegree(int) = 0;			//顶点出度
		virtual int firstNbr(int, int) = 0;		//首个邻接顶点
		virtual int nextNbr(int, int) = 0;		//下一个邻接顶点
		virtual VStatus& status(int) = 0;		//顶点状态
		virtual int& dTime(int) = 0;			//dTime
		virtual int& fTime(int) = 0;			//fTime
		virtual int& parent(int) = 0;			//遍历树中的父亲
		virtual int& priority(int) = 0;			//遍历树中的优先级

		int e;	//边总数
		virtual bool exists(int, int) = 0;		//边(u, v)是否存在
		virtual void insert(Te const&, int, int, int) = 0;	//插入(u, v)权重w的边
		virtual Te remove(int, int) = 0;		//删除u和v之间的边e,返回边的信息
		virtual EType& type(int, int) = 0;		//边(u, v)的类型
		virtual Te& edge(int, int) = 0;			//边(u, v)的数据
		virtual int& weight(int, int) = 0;		//边(u, v)的权重

		void bfs(int);			//广度优先搜索
		void dfs(int);			//深度优先搜索
		void bcc(int);			//基于DFS的双连通分量分解算法
		Stack<Tv>* tSort(int);	//基于DFS的拓扑排序算法
		void prim(int);			//最小支撑树算法
		void dijkstra(int);		//最短路径算法
		template <typename PU> void pfs(int, PU);	//优先级搜索框架
	};

	//广度优先搜索
	template <typename Tv, typename Te>
	void Graph<Tv, Te>::bfs(int s) {
		reset();
		int clock = 0;
		int v = s;
		do {
			if(status(v) == UNDISCOVERED) BFS(v, clock);
		} while(s != (v = (++v % n)));
	}

	template <typename Tv, typename Te>
	void Graph<Tv, Te>::BFS(int v, int& clock) {
		Queue<int> Q;
		status(v) = DISCOVERED;
		Q.enqueue(v);
		while(!Q.empty()) {
			int v = Q.dequeue();
			dTime(v) = ++clock;
			for(int u = firstNbr(v); -1 < u; u = nextNbr(v, u)) {
				if(UNDISCOVERED == status(u)) {
					status(u) = DISCOVERED;
					Q.enqueue(u);
					type(v, u) = TREE;
					parent(u) = v;
				}
				else {
					type(v, u) = CROSS;
				}
			}
			status(v) = VISITED;
		}
	}

	//深度优先搜索
	template <typename Tv, typename Te>
	void Graph<Tv, Te>::dfs(int s) {
		reset();
		int clock = 0;
		int v = s;
		do {
			if(status(v) == UNDISCOVERED) DFS(v, clock);
		} while(s != (v = (++v % n)));
	}

	template <typename Tv, typename Te>
	void Graph<Tv, Te>::DFS(int v, int& clock) {
		dTime(v) = ++clock;
		status(v) = DISCOVERED;
		for(int u = firstNbr(v); -1 < u; u = nextNbr(v, u)) {
			switch(status(u)) {
			case UNDISCOVERED:
				type(v, u) = TREE;
				parent(u) = v;
				DFS(u, clock);
				break;
			case DISCOVERED:
				type(v, u) = BACKWARD;
				break;
			default:
				type(v, u) = (dTime(v) < dTime(u)) ? FORWARD : CROSS;
				break;
			}
		}
		status(v) = VISITED;
		fTime(v) = ++clock;
	}

	//拓扑排序
	template <typename Tv, typename Te>
	Stack<Tv>* Graph<Tv, Te>::tSort(int s) {
		reset();
		int clock = 0;
		int v = s;
		Stack<Tv>* S = new Stack<Tv>;
		do {
			if(UNDISCOVERED == status(v)) {
				if(!TSort(v, clock, S)) {
					while(!S->empty())
						S->pop();
					break;
				}
			}
		} while(s != (v = (++v % n)));
		return S;
	}

	template <typename Tv, typename Te>
	bool Graph<Tv, Te>::TSort(int v, int& clock, Stack<Tv>* S) {
		dTime(v) = ++clock;
		status(v) = DISCOVERED;
		for(int u = firstNbr(v); -1 < u; u = nextNbr(v, u)) {
			switch(status(u)) {
			case UNDISCOVERED:
				parent(u) = v;
				type(v, u) = TREE;
				if(!TSort(u, clock, S)) return false;
				break;
			case DISCOVERED:
				type(v, u) = BACKWARD;
				return false;
			default:
				type(v, u) = (dTime(v) < dTime(u)) ? FORWARD : CROSS;
				break;
			}
		}
		status(v) = VISITED;
		S->push(vertex(v));
		return true;
	}

	//双连通域分解
	template <typename Tv, typename Te>
	void Graph<Tv, Te>::bcc(int s) {
		reset();
		int clock = 0, v = s;
		Stack<int> S;
		do {
			if(UNDISCOVERED == status(v)) {
				BCC(v, clock, S);
				S.pop();
			}
		} while(s != (v = (++v % n)));
	}

	#define hac(x) (fTime(x))

	template <typename Tv, typename Te>
	void Graph<Tv, Te>::BCC(int v, int& clock, Stack<int>& S) {
		hca(v) = dTime(v) = ++clock;
		status(v) = DISCOVERED;
		S.push(x);
		for(int u = firstNbr(v); -1 < u; u = nextNbr(v, u)) {
			switch(status(u)) {
			case UNDISCOVERED:
				parent(u) = v;
				type(v, u) = TREE;
				BCC(u, clock, S);
				if(hca(u) < dTime(v))
					hac(v) = min(hca(v), hca(u));
				else {
					while(v != S.pop());
					S.push(v);
				}
				break;
			case DISCOVERED:
				type(v, u) = BACKWARD;
				if(u != parent(v))
					hca(v) = min(hca(v), dTime(v));
				break;
			default:
				type(v, u) = (dTime(v) < dTime(u)) ? FORWARD : CROSS;
				break;
			}
		}
		status(v) = VISITED;
	}

	//优先级搜索
	template<typename Tv, typename Te>
	template<typename PU>
	void Graph<Tv, Te>::pfs(int s, PU prioUpdater) {
		reset();
		int v = s;
		do {
			if(UNDISCOVERED == status(v))
				PFS(v, prioUpdater);
		} while(s != (v = (++v % n)));
	}

	template <typename Tv, typename Te>
	template <typename PU>
	void Graph<Tv, Te>::PFS(int s, PU prioUpdater) {
		priority(s) = 0;
		status(s) = VISITED;
		parent(s) = -1;
		while(1) {
			for(int w = firstNbr(s); -1 < w; w = nextNbr(s, w)) {
				prioUpdater(this, s, w);
			}
			for(int shortest = INT_MAX, w = 0; w < n; ++w) {
				if(UNDISCOVERED == status(v)) {
					if(shortest > priority(w)) {
						shortest = priority(w);
						s = w;
					}
				}
			}
			if(VISITED == status(s)) break;
			status(s) = VISITED;
			type(parent(s), s) = TREE;
		}
	}

	//针对prim算法的顶点优先级更新器
	template <typename Tv, typename Te>
	struct PrimPU {
		virtual void operator() (Graph<Tv, Te>* g, int uk, int v) {
			if(UNDISCOVERED == g->status(v))
				if(g->priority(v) > g->weight(uk, v)) {
					g->priority(v) = g->weight(uk, v);
					g->parent(v) = uk;
				}
		}
	};

	//针对Dijkstra算法的顶点优先级更新器
	template <typename Tv, typename Te>
	struct  DijkstraPU {
		virtual void operator() (Graph<Tv, Te>* g, int uk, int v) {
			if(UNDISCOVERED == g->status(v))
				if(g->priority(v) > g->priority(uk) + g->weight(uk, v)) {
					g->priority(v) = g->priority(uk) + g->weight(uk, v);
					g->parent(v) = uk;
				}
		}
	};
}

#endif //~DST_GRAPH_H