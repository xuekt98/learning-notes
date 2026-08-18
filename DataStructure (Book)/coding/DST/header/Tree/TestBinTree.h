#ifndef TEST_BINTREE_H
#define TEST_BINTREE_H

#include "BinNode.h"
#include "BinTree.h"
#include <iostream>

void testBinTree() {
	using DST::BinNode;
	using DST::BinTree;
	using std::cin;
	using std::cout;
	using std::endl;

	BinTree<int> *tr0 = new BinTree<int>, *tr1 = new BinTree<int>;
	tr0->insertAsRoot(0);
	tr1->insertAsRoot(1);

	tr0->attachAsLC(tr0->root(), tr1);
}

#endif //~TEST_BINTREE_H