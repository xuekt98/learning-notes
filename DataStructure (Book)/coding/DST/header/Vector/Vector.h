#ifndef DST_VECTOR_H
#define DST_VECTOR_H

#include "..\DST.h"

namespace DST {
	template <typename T>
	class Vector {
	protected:
		Rank _size;		//规模
		int _capacity;	//容量
		T* _elem;		//数据区

		void copyFrom(T const* A, Rank lo, Rank hi);	//复制数据区间A[lo, hi)
		void expand();	//空间不足时扩容
		void shrink();	//装填因子过小时压缩
		
		bool bubble(Rank lo, Rank hi);		//扫描交换
		void bubbleSort(Rank lo, Rank hi);	//起泡排序

		//Rank max(Rank lo, Rank hi);				//选取最大元素
		//void selectionSort(Rank lo, Rank hi);	//选择排序算法

		void merge(Rank lo, Rank mi, Rank hi);	//归并算法
		void mergeSort(Rank lo, Rank hi);		//归并排序算法

		//Rank partition(Rank lo, Rank hi);		//轴点构造算法
		//void quickSort(Rank lo, Rank hi);		//快速排序算法
		
		//void heapSort(Rank lo, Rank hi);		//堆排序

	public:
	//构造函数
		Vector(int c = DEFAULT_CAPACITY, int s = 0, T v = 0) {		//容量c，规模s，所有元素初始为v
			_elem = new T[_capacity = c];
			for(_size = 0; _size < s; _elem[_size++] = v); 
		}

		Vector(T const* A, Rank n) {				//数组整体复制
			copyFrom(A, 0, n);
		}

		Vector(T const* A, Rank lo, Rank hi) {		//区间复制
			copyFrom(A, lo, hi);
		}

		Vector(Vector<T> const& V) {				//拷贝构造函数
			copyFrom(V._elem, 0, V._size());
		}

		Vector(Vector<T> const& V, Rank lo, Rank hi) {	//区间拷贝
			copyFrom(V._elem, lo, hi);
		}

	//析构函数
		~Vector() { delete[] _elem; }	//析构函数

	//只读访问接口
		Rank size() const { return _size; }		//规模
		bool empty() const { return !_size; }	//判空
		int disordered() const;					//判断是否已排序

		Rank find(T const& e) const { return find(e, 0, _size); }	//无序向量整体查找
		Rank find(T const& e, Rank lo, Rank hi) const;				//无序向量区间查找

		Rank search(T const& e) const {								//有序向量整体查找
			return (0 >= _size) ? -1 : search(e, 0, _size);
		}
		Rank search(T const& e, Rank lo, Rank hi) const;					//有序向量区间查找

	//可写访问接口
		T& operator[] (Rank r) const;					//重载下标操作符
		Vector<T> & operator= (Vector<T> const&);		//重载赋值操作符

		T remove(Rank r);								//删除秩为r的元素
		int remove(Rank lo, Rank hi);					//区间删除

		Rank insert(T const& e) {						//默认作为末元素插入
			return insert(_size, e);
		}
		Rank insert(Rank r, T const& e);				//插入元素

		void sort(Rank lo, Rank hi);					//对[lo, hi)排序
		void sort() { sort(0, _size); }					//整体排序

		void unsort(Rank lo, Rank hi);					//对[lo, hi)置乱
		void unsort() { unsort(0, _size); }				//整体置乱

		int deduplicate();								//无序向量去重
		int uniquify();									//有序向量去重
	
	//遍历
		void tranverse(void(*) (T&));					//遍历（使用函数指针，只读或局部性修改）
		template <typename VST> void tranverse(VST&);	//遍历（使用函数对象，全局性修改）
	};

	/******保护接口******/
	template <typename T>
	void Vector<T>::copyFrom(T const* A, Rank lo, Rank hi) {	//区间复制
		_elem = new T[_capacity = 2 * (hi - lo)];
		_size = 0;
		while(lo < hi) {
			_elem[_size++] = A[lo++];
		}
	}

	template <typename T>
	void Vector<T>::expand() {									//向量空间不足时扩容
		if(_size < _capacity) return;
		if(_capacity < DEFAULT_CAPACITY) _capacity = DEFAULT_CAPACITY;
		T* oldElem = _elem;
		_elem = new T[_capacity <<= 1];
		for(int i = 0; i < _size; ++ i) {
			_elem[i] = oldElem[i];
		}
		delete[] oldElem;
	}

	template <typename T>
	void Vector<T>::shrink() {									//装填因子过小时压缩容量
		if(_capacity < DEFAULT_CAPACITY << 1) return;			//不致收缩到DEFAULT_CAPACITY以下
		if(_size << 2 > _capacity) return;						//装填因子至少25%
		T* oldELem = _elem;
		_elem = new T[_capacity >>= 1];
		for(int i = 0; i < _size; ++ i) {
			_elem[i] = oldElem[i];
		}
		delete oldElem;
	}

	template <typename T>
	bool Vector<T>::bubble(Rank lo, Rank hi) {					//一次冒泡的过程
		bool sorted = true;
		while(++lo < hi) {
			if(_elem[lo - 1] > _elem[lo]) {
				sorted = false;
				swap(_elem[lo - 1], _elem[lo]);
			}
		}
		return sorted;
	}

	template <typename T>
	void Vector<T>::bubbleSort(Rank lo, Rank hi) {				//冒泡排序
		while(!bubble(lo, hi--));
	}

	template <typename T>
	void Vector<T>::merge(Rank lo, Rank hi, Rank mi) {			//归并
		T* A = _elem + lo;
		int lb = mi - lo;
		T* B = new T[lb];
		for(Rank i = 0; i < lb; B[i] = A[i++]);
		int lc = hi - mi;
		T* C = _elem + mi;
		for(Rank i = 0, j = 0, k = 0; (j < lb) || (k < lc);) {
			if((j < lb) && (!(k < lc) || (B[j] <= C[k]))) A[i++] = B[j++];
			if((k < lc) && (!(j < lb) || (C[k] < B[j]))) A[i++] = C[k++];
		}
	}

	template <typename T>
	void Vector<T>::mergeSort(Rank lo, Rank hi) {			//归并排序
		if(hi - lo < 2) return;
		int mi = (lo + hi) / 2;
		mergeSort(lo, mi);
		mergeSort(mi, hi);
		merge(lo, mi, hi);
	}

	/******只读访问接口******/
	//无序向量顺序查找,返回最后一个元素e的位置,失败则返回lo - 1
	template <typename T>
	Rank Vector<T>::find(T const& e, Rank lo, Rank hi) const {
		while((lo < hi--) && (e != _elem[hi]));
		return hi;
	}

	//判定乱序,返回相邻逆序对的总数
	template <typename T>
	int Vector<T>::disordered() const {
		int n = 0;
		for(int i = 1; i < _size; ++ i) {
			if(_elem[i - 1] > _elem[i]) {
				++n;
			}
		}
		return n;
	}

	//在有序向量的区间[lo, hi)内,确定不大于e的最后一个节点的秩
	template <typename T>
	Rank Vector<T>::search(T const& e, Rank lo, Rank hi) const {
		return binSearch(_elem, e, lo, hi);
		//return fibSearch(_elem, e, lo, hi);
	}

	/******可写访问接口******/
	template <typename T>
	Vector<T>& Vector<T>::operator= (Vector<T> const& V) {		//重载赋值操作符
		if(_elem) delete[] _elem;
		copyFrom(V._elem, 0, V.size());
		return *this;
	}

	template <typename T>
	T& Vector<T>::operator[] (Rank r) const {					//循秩访问
		return _elem[r];
	}

	template <typename T>
	int Vector<T>::remove(Rank lo, Rank hi) {					//区间删除[lo, hi)
		if(lo == hi) return 0;
		while(hi < _size) {
			_elem[lo++] = _elem[hi++];
		}
		_size = lo;
		shrink();
		return hi - lo;
	}

	template <typename T>
	T Vector<T>::remove(Rank r) {								//单个元素删除
		T e = _elem[r];
		remove(r, r + 1);
		return e;
	}

	template <typename T>
	Rank Vector<T>::insert(Rank r, T const& e) {							//插入元素
		expand();	//如果当前的规模已经和容量相等,则需要先扩容
		for(int i = _size; i > r; --i) {
			_elem[i] = _elem[i - 1];
		}
		return r;
	}

	template <typename T>
	void Vector<T>::unsort(Rank lo, Rank hi) {					//等概率随机置乱区间
		T* V = _elem + lo;
		for(Rank i = hi - lo; i > 0; -- i) {
			swap(V[i - 1], V[rand() % i]);
		}
	}

	template <typename T>
	int Vector<T>::deduplicate() {								//无序向量去重
		int oldSize = _size;
		Rank i = 1;
		while(i < _size) {
			(find(_elem, 0, i) < 0) ? i++ : remove(i);
		}
		return oldSize - _size;
	}

	template <typename T>
	int Vector<T>::uniquify() {									//有序向量去重
		Rank i = 0, j = 0;
		while(++j < _size) {
			if(_elem[i] != _elem[j]) {
				_elem[++i] = _elem[j];
			}
		}
		_size = ++i;
		shrink();
		return j - i;
	}

	template <typename T>
	void Vector<T>::sort(Rank lo, Rank hi) {
		bubbleSort(lo, hi);
	}

	/******遍历******/
	template <typename T>
	void Vector<T>::tranverse(void(*visit)(T&)) {				//使用函数指针
		for(int i = 0; i < _size; ++i) {
			visit(_elem[i]);
		}
	}

	template <typename T>
	template <typename VST>
	void Vector<T>::tranverse(VST& visit) {						//使用函数对象
		for(int i = 0; i < _size; ++i) {
			visit(_elem[i]);
		}
	}
}

#endif //~DST_VECTOR_H