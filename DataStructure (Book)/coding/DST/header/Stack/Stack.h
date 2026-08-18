#ifndef DST_STACK_H
#define DST_STACK_H

#include "..\Vector\Vector.h"

namespace DST {
	template <typename T>
	class Stack : public Vector<T> {
	public:
		void push(T const& e) {
			insert(size(), e);
		}

		T pop() {
			return remove(size() - 1);
		}

		T& top() {
			return (*this)[size() - 1];
		}
	};
}

#endif //~DST_STACK