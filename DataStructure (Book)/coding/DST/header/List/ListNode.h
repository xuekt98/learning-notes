#ifndef DST_LISTNODE_H
#define DST_LISTNODE_H

#define ListNodePosi(T) ListNode<T>*

namespace DST {
	template <typename T>
	class ListNode {
	public:
	//成员
		T data;
		ListNodePosi(T) pred;
		ListNodePosi(T) succ;
	//构造函数
		ListNode() {}
		ListNode(T e, ListNodePosi(T) p = NULL, ListNodePosi(T) s = NULL) : data(e), pred(p), succ(s) {}
	//操作接口
		ListNodePosi(T) insertAsPred(T const& e);
		ListNodePosi(T) insertAsSucc(T const& e);
	};

	template <typename T>
	ListNodePosi(T) ListNode<T>::insertAsPred(T const& e) {
		ListNodePosi(T) x = new ListNode(e, pred, this);
		pred->succ = x;
		pred = x;
		return x;
	}

	template <typename T>
	ListNodePosi(T) ListNode<T>::insertAsSucc(T const& e) {
		ListNodePosi(T) x = new ListNode(e, this, succ);
		succ->pred = x;
		succ = x;
		return x;
	}
}

#endif //~DST_LISTNODE_H