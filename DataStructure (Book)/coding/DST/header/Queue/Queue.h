#ifndef DST_QUEUE_H
#define DST_QUEUE_H

#include "..\List\List.h"

namespace DST {
	template <typename T>
	class Queue : public List<T> {
	public:
		void enqueue(T const& e) {
			insertAsLast(e);
		}

		T dequeue() {
			return remove(first());
		}

		T& front() {
			return first()->data;
		}
	};
}

#endif //~DST_QUEUE_H