#ifndef DST_BINTREE_H
#define DST_BINTREE_H

#include "BinNode.h"
#include <memory>

namespace DST {
	template <typename T>
	class BinTree {
	protected:
		int _size;
		BinNodePosi(T) _root;
		virtual int updateHeight(BinNodePosi(T) x);
		void updateHeightAbove(BinNodePosi(T) x);

	public:
		BinTree() : _size(0), _root(nullptr) {}		//构造函数
		~BinTree() {								//析构函数
			if(_size > 0) remove(_root);
		}
		int size() const { return _size; }				//规模
		bool empty() const { return !_root; }			//判空
		BinNodePosi(T) root() const { return _root; }	//树根

		BinNodePosi(T) insertAsRoot(T const& e);		//插入根节点
		BinNodePosi(T) insertAsLC(BinNodePosi(T) x, T const& e);		//e作为x的左孩子插入
		BinNodePosi(T) insertAsRC(BinNodePosi(T) x, T const& e);		//e作为x的右孩子插入
		BinNodePosi(T) attachAsLC(BinNodePosi(T) x, BinTree<T>* &T);	//T作为x的左子树插入
		BinNodePosi(T) attachAsRC(BinNodePosi(T) x, BinTree<T>* &T);	//T作为x的右子树插入
		int remove(BinNodePosi(T) x);			//删除以位置x处节点为根的子树,返回该子树原先的规模
		BinTree<T>* secede(BinNodePosi(T) x);	//将子树x从当前树种摘除,并转换成一棵独立子树

		template <typename VST>
		void travLevel(VST& visit) {			//层次遍历
			if(_root) _root->travLevel(visit);
		}

		template <typename VST>
		void travPre(VST& visit) {				//先序遍历
			if(_root) _root->travPre(visit);
		}

		template <typename VST>
		void travIn(VST& visit) {				//中序遍历
			if(_root) _root->travIn(visit);
		}

		template <typename VST>
		void travPost(VST& visit) {				//后序遍历
			if(_root) _root->travPost(visit);
		}

		bool operator< (BinTree<T> const& t) {				//小于
			return _root && t._root && lt(_root, t._root);
		}

		bool operator== (BinTree<T> const& t) {				//等于
			return _root && t._root && (_root == t._root);
		}
	};

	template <typename T>
	int BinTree<T>::updateHeight(BinNodePosi(T) x) {	//更新节点x的高度
		return x->height = 1 + max(stature(x->lc), stature(x->rc));
	}

	template <typename T>
	void BinTree<T>::updateHeightAbove(BinNodePosi(T) x) {	//更新高度
		while(x) {
			updateHeight(x);
			x = x->parent;
		}
	}

	template <typename T>
	BinNodePosi(T) BinTree<T>::insertAsRoot(T const& e) {	//将e当作根节点插入空的二叉树
		_size = 1;
		return _root = new BinNode<T>(e);
	}

	template <typename T>
	BinNodePosi(T) BinTree<T>::insertAsLC(BinNodePosi(T) x, T const& e) {	//e插入为x的左孩子
		_size++;
		x->insertAsLC(e);
		updateHeightAbove(x);
		return x->lc;
	}

	template <typename T>
	BinNodePosi(T) BinTree<T>::insertAsRC(BinNodePosi(T) x, T const& e) {	//e插入为x的左孩子
		_size++;
		x->insertAsRC(e);
		updateHeightAbove(x);
		return x->rc;
	}

	template <typename T>	//二叉树接入算法:将S作为节点x的左子树接入,S本身置空
	BinNodePosi(T) BinTree<T>::attachAsLC(BinNodePosi(T) x, BinTree<T>* &S) {
		if(x->lc = S->_root) x->lc->parent = x;
		_size += S->_size;
		updateHeightAbove(x);
		S->_root = NULL;
		S->_size = 0;
		//release(S);
		S = NULL;
		return x;
	}

	template <typename T>	//二叉树接入算法:将S作为节点x的右子树接入,S本身置空
	BinNodePosi(T) BinTree<T>::attachAsRC(BinNodePosi(T) x, BinTree<T>* &S) {
		if(x->rc = S->_root) x->rc->parent = x;
		_size += S->_size;
		updateHeightAbove(x);
		S->_root = nullptr;
		S->_size = 0;
		//release(S);
		S = nullptr;
		return x;
	}

	template <typename T>	//删除二叉树中位置x处的节点及其后代,返回被删除节点的数值
	int BinTree<T>::remove(BinNodePosi(T) x) {
		FromParentTo(*x) = NULL;
		updateHeightAbove(x->parent);
		int n = removeAt(x);
		_size = n;
		return n;
	}

	template <typename T>	//二叉树子树分离算法:将子树x从当前树种摘除,将其封装城一棵独立的子树返回
	BinTree<T>* BinTree<T>::secede(BinNodePosi(T) x) {
		FromParentTo(*x) = NULL;
		updateHeightAbove(x->parent);
		BinTree<T>* S = new BinTree<T>;
		S->_root = x;
		x->parent = nullptr;
		S->_size = x->size();
		_size -= S->_size;
		return S;
	}


	/******其他非类内部接口******/
	template <typename T>	//删除二叉树中位置x处的节点及其后代,返回被删除节点的数值
	static int removeAt(BinNodePosi(T) x) {
		if(!x) return 0;
		int n = 1 + removeAt(x->lc) + removeAt(x->rc);
		release(x->data);
		release(x);
		return n;
	}
}

#endif //~DST_BINTREE_H