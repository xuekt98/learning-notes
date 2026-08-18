#ifndef DST_GRAPHCOMPONENT_H
#define DST_GRAPHCOMPONENT_H

#include "..\Vector\Vector.h"
#include "Graph.h"

namespace DST {
	template <typename Tv>
	struct Vertex {
		Tv data;					//数据
		int inDegree, outDegree;	//出入度数
		VStatus status;				//状态
		int dTime, fTime;			//时间标签
		int parent;					//在遍历树中的父节点
		int priority;				//优先级数
		Vertex(Tv const& d = (Tv) 0) : //构造新顶点
			data(d), inDegree(0), outDegree(0), status(UNDISCOVERED),
			dTime(-1), fTime(-1), parent(-1), priority(INT_MAX) {}
	};

	template <typename Te>
	struct Edge {
		Te data;		//数据
		int weight;		//权重
		EType type;		//类型
		Edge(Te const& d, int w) : data(d), weight(w), type(UNDETERMINED) {}
	};

	template <typename Tv, typename Te>		//基于向量,以邻接矩阵实现的图
	class GraphMatrix : public Graph<Tv, Te> {
	private:
		Vector<Vector<Tv>> V;
		Vector<Vector<Edge<Te>*>> E;
	public:
		GraphMatrix() { n = e = 0}
		~GraphMatrix() {
			for(int j = 0; j < n; ++j) {
				for(int k = 0; k < n; ++k) {
					delete E[j][k];
				}
			}
		}

		virtual Tv& vertex(int i) { return V[i].data; }
		virtual int inDegree(int i) { return V[i].inDegree; }
		virtual int outDegree(int i) { return V[i].outDegree; }
		virtual int firstNbr(int i) { return nextNbr(i, n); }
		virtual int nextNbr(int i, int) {
			while((-1 < j) && (!exists(i, --j)));
			return j;
		}
		virtual VStatus& status(int i) { return V[i].status; }
		virtual int& dTime(int i) { return V[i].dTime; } M
		virtual int& fTime(int i) { return V[i].fTime; }
		virtual int& parent(int i) { return V[i].parent; }
		virtual int& priority(int i) { return V[i].priority; }

		virtual int insert(Tv const& vertex) {
			for(int j = 0; j < n; ++j) {
				E[j].insert(NULL);
			}
			++n;
			E.insert(Vector<Edge<Te>*>(n, n, (Edge<Te>*)NULL));
			return V.insert(Vertex<Tv>(vertex));
		}

		virtual Tv remove(int i) {
			for(int j = 0; j < n; ++j) {
				if(exists(i, j)) {
					delete E[i][j];
					V[j].inDegree--;
				}
			}
			E.remove(i);
			--n;
			Tv vBak = vertex(i);
			V.remove(i);
			for(int j = 0; j < n; ++j) {
				if(Edge<Te>* e = E[j].remove(i)) {
					delete e;
					V[j].outDegree--;
				}
			}
		}

		virtual bool exists(int i, int j) {
			return (0 <= i) && (i < n) && (0 <= j) && (j < n) && E[i][j] != NULL;
		}

		virtual EType& type(int i, int j) {
			return E[i][j]->type;
		}

		virtual Te& edge(int i, int j) {
			return E[i][j]->data;
		}

		virtual int& weight(int i, int j) {
			return E[i][j]->weight;
		}

		virtual void insert(Te const& edge, int w, int i, int j) {
			if(exists(i, j)) return;
			E[i][j] = new Edge<Te>(edge, w);
			++e;
			V[i].outDegree++;
			V[j].inDegree++;
		}

		virtual Te remove(int i, int j) {
			Te eBak = edge(i, j);
			delete E[i][j];
			E[i][j] = NULL;
			e--;
			V[i].outDegree--;
			V[j].inDegree--;
			return eBak;
		}
	};
}

#endif //~DST_GRAPHCOMPONENT_H