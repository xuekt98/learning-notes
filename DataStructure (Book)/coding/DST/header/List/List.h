#ifndef DST_LIST_H
#define DST_LIST_H

#include "ListNode.h"
#include "..\DST.h"

namespace DST {
	template <typename T>
	class List {
	private:
		int _size;					//规模
		ListNodePosi(T) header;		//头哨兵
		ListNodePosi(T) trailer;	//尾哨兵

	protected:
	//保护接口
		void init();	//列表创建时的初始化
		int clear();	//清除所有节点
		void copyNodes(ListNodePosi(T), int);	//复制列表自位置p起的n项

		void merge(ListNodePosi(T)&, int, List<T>&, ListNodePosi(T), int);	//归并
		void mergeSort(ListNodePosi(T)&, int);								//归并排序

		void selectionSort(ListNodePosi(T), int);	//选择排序
		void insertionSort(ListNodePosi(T), int);	//插入排序

	public:
	//构造函数
		List() { init(); }							//默认构造函数
		List(List<T> const& L);						//整体复制列表L
		List(List<T> const& L, Rank r, int n);		//复制列表L中从r项开始的n项
		List(ListNodePosi(T) p, int n);				//复制列表从位置p起的n项

	//析构函数
		~List();

	//只读访问接口
		Rank size() const { return _size; }			//规模
		Rank empty() const { return _size <= 0; }	//判空
		T& operator[] (Rank r) const;				//重载[],循秩访问
		ListNodePosi(T) first() const { return header->succ; }		//首节点位置
		ListNodePosi(T) last() const { return trailer->pred; }		//末节点位置

		bool valid(ListNodePosi(T) p) {				//判断位置p是否对外合法
			return p && (trailer != p) && (header != p);
		}
		int disordered() const;						//判断是否已排序

		ListNodePosi(T) find(T const& e, int n, ListNodePosi(T) p) const;	//无序区间查找
		ListNodePosi(T) find(T const& e) const {							//无序列表查找
			return find(e, _size, trailer);
		}

		ListNodePosi(T) search(T const& e, int n, ListNodePosi(T) p) const;	//有序区间查找
		ListNodePosi(T) search(T const& e) const {							//有序列表查找
			return search(e, _size, trailer);
		}

		ListNodePosi(T) selectMax(ListNodePosi(T) p, int n);				//p及其n-1后继中选出最大者
		ListNodePosi(T) selectMax() {										//整体最大者
			return selectMax(header->succ, _size);
		}
	
	//可写访问接口
		ListNodePosi(T) insertAsFirst(T const& e);					//将e作为首节点插入
		ListNodePosi(T) insertAsLast(T const& e);					//将e作为末节点插入
		ListNodePosi(T) insertA(ListNodePosi(T) p, T const& e);		//将e当作p的后继插入
		ListNodePosi(T) insertB(ListNodePosi(T) p, T const& e);		//将e当作p的前驱插入
		
		T remove(ListNodePosi(T) p);			//删除合法位置p处的节点,返回被删除的节点
		void merge(List<T>& L) {				//全列表归并
			merge(first(), size, L, L.first(), L._size);
		}
		
		void sort(ListNodePosi(T) p, int n);	//列表区间排序
		void sort() {							//列表整体排序
			sort(first(), _size);
		}
		
		int deduplicate();		//无序列表去重
		int uniquify();			//有序列表去重
		void reverse();			//前后倒置

	//遍历
		void tranverse(void(*)(T&));	//遍历(函数指针)
		template <typename VST>
		void tranverse(VST&);			//遍历(函数对象)
	};

	/******构造函数******/
	template <typename T>
	List<T>::List(ListNodePosi(T) p, int n) {	//复制列表中自位置p起的n项
		copyNodes(p, n);
	}

	template <typename T>
	List<T>::List(List<T> const& L) {			//整体复制列表L
		copyNodes(L.first(), L._size);
	}

	template <typename T>
	List<T>::List(List<T> const& L, int r, int n) {		//复制L中自第r项起的n项
		copyNodes(L[r], n);
	}

	/******析构函数******/
	template <typename T>
	List<T>::~List() {
		clear();
		delete header;
		delete trailer;
	}

	/******保护接口******/
	template <typename T>
	void List<T>::init() {				//列表初始化,在创建列表时统一调用
		header = new ListNode<T>;
		trailer = new ListNode<T>;
		header->succ = trailer;
		header->pred = NULL;
		trailer->succ = header;
		trailer->pred = NULL;
		_size = 0;
	}

	template <typename T>
	void List<T>::copyNodes(ListNodePosi(T) p, int n) {		//列表内部方法,复制列表中自位置p起的n项
		init();
		while(n--) {
			insertAsLast(p->data);
			p = p->succ;
		}
	}
	
	template <typename T>
	int List<T>::clear() {			//清空列表
		int oldSize = _size;
		while(0 < _size) {
			remove(header->succ);
		}
		return oldSize;
	}

	template <typename T>
	void List<T>::insertionSort(ListNodePosi(T) p, int n) {		//插入排序:对起始于p的n个元素排序
		for(int r = 0; r < n; ++r) {
			insertA(search(p->data, r, p), p->data);
			p = p->succ;
			return (p->pred);
		}
	}

	template <typename T>
	void List<T>::selectionSort(ListNodePosi(T) p, int n) {		//选择排序
		ListNodePosi(T) head = p->pred;
		ListNodePosi(T) tail = p;
		for(int i = 0; i < n; ++i) {
			tail = tail->succ;
		}
		while(1 < n) {
			ListNodePosi(T) max = selectMax(head->succ, n);
			insertB(tail, remove(max));
			tail = tail->pred;
			n--;
		}
	}

	template <typename T>
	void List<T>::mergeSort(ListNodePosi(T)& p, int n) {
		if(n < 2) return;
		int m = n >> 1;
		ListNodePosi(T) q = p;
		for(int i = 0; i < m; i++) q = q->succ;
		mergeSort(p, m);
		mergeSort(q, n - m);
		merge(p, m, *this, q, n - m);
	}

	template <typename T>
	void List<T>::merge(ListNodePosi(T)& p, int n, List<T>& L, ListNodePosi(T) q, int m) {
		ListNodePosi(T) pp = p->pred;
		while(0 < m) {
			if((0 < n) && (p->data <= q->data)) {
				if(q == (p = p->succ)) break;
				n--;
			}
			else {
				insertB(p, L.remove((q = q->succ)->pred));
				m--;
			}
		}
		p = pp->succ;
	}

	/******只读访问接口******/
	template <typename T>
	T& List<T>::operator[] (Rank r) const {		//循秩访问
		ListNodePosi(T) p = first();
		while(0 < r--) p = p->succ;
		return p->data;
	}

	//在无序列表内节点p(可能是trailer)的n个(真)前驱中,找到等于e的最后者
	template <typename T>
	ListNodePosi(T) List<T>::find(T const& e, int n, ListNodePosi(T) p) const {
		while(0 < n--) {
			if(e == (p = p->pred)->data) return p;
		}
		return NULL;
	}

	//在有序列表内节点p(可能是trailer)的n个(真)前驱中,找到不大于e的最后者
	template <typename T>
	ListNodePosi(T) List<T>::search(T const& e, int n, ListNodePosi(T) p) const {
		while(0 <= n--) {
			if(((p = p->pred)->data) <= e) break;
		}
		return p;
	}

	template <typename T>
	ListNodePosi(T) List<T>::selectMax(ListNodePosi(T) p, int n) {		//从起始于p的n个元素中找出最大者
		ListNodePosi(T) max = p;
		for(ListNodePosi(T) cur = p; 1 < n; n--) {
			if(!lt((cur = cur->succ)->data, max->data)) 
				max = cur;
		}
		return max;
	}

	/******可写访问接口******/
	template <typename T>
	ListNodePosi(T) List<T>::insertAsFirst(T const& e) {		//当作首节点插入
		++_size;
		return header->insertAsSuccc(e);
	}

	template <typename T>
	ListNodePosi(T) List<T>::insertAsLast(T const& e) {			//当作末节点插入
		++_size;
		return trailer->insertAsPred(e);
	}

	template <typename T>
	ListNodePosi(T) List<T>::insertA(ListNodePosi(T) p, T const& e) {	//e当作p的后继插入
		++_size;
		return p->insertAsSucc(e);
	}

	template <typename T>
	ListNodePosi(T) List<T>::insertB(ListNodePosi(T) p, T const& e) {	//e当作p的前驱插入
		++_size;
		return p->insertAsPred(e);
	}

	template <typename T>
	T List<T>::remove(ListNodePosi(T) p) {		//删除合法节点p,返回其数值
		T e = p->data;
		p->pred->succ = p->succ;
		p->succ->pred = p->pred;
		delete p;
		--_size;
		return e;
	}

	template <typename T>
	void List<T>::sort(ListNodePosi(T) p, int n) {		//列表区间排序
		
	}

	template <typename T>
	int List<T>::deduplicate() {		//无序列表去重
		if(_size < 2) return 0;
		int oldSize = _size;
		ListNodePosi(T) p = header;
		Rank r = 0;
		while(trailer != (p = p->succ)) {	//p从首节点开始
			ListNodePosi(T) p = find(p->data, r, p);
			q ? remove(q) : r++;
		}
		return oldSize - _size;
	}

	template <typename T>
	int List<T>::uniquify() {			//有序列表去重
		if(_size < 2) return 0;
		int oldSize = _size;
		ListNodePosi(T) p = first();
		ListNodePosi(T) q;
		while(trailer != (q = p->succ)) { //如果雷同,删除后者
			if(p->data != q->data) p = q;
			else remove(q);
		}
		return oldSize - _size;
	}

	/******遍历******/
	template <typename T>
	void List<T>::tranverse(void (*visit) (T&)) {
		for(ListNodePosi(T) p = header->succ; p != trailer; p = p->succ) {
			visit(p->data);
		}
	}

	template <typename T>
	template <typename VST>
	void List<T>::tranverse(VST& visit) {
		for(ListNodePosi(T) p = header->succ; p != trailer; p = p->succ) {
			visit(p->data);
		}
	}
}

#endif //~DST_LIST_H