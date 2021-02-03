#! /usr/bin/env python3

import random, os

def loadBibles(folder):
	data = [set() for _ in range(43906)]
	for filename in os.listdir(folder):
		f = open(folder + "/" + filename, 'r', encoding='utf-8')
		for i, line in enumerate(f):
			if line.strip() != "":
				data[i].add(line.strip())
		f.close()
	nonempty = len([x for x in data if x != set()])
	all = sum([len(x) for x in data])
	ndocs = len(os.listdir(folder))
	print("{}: {} documents, {} verses, {} translations".format(folder, ndocs, nonempty, all))
	return data


def sample(data1, data2, outfilename, maxpairs=2, seed=7):
	f = open(outfilename, "w", encoding="utf-8")
	count = 0
	random.seed(seed)
	for set1, set2 in zip(data1, data2):
		if len(set1) == 0 or len(set2) == 0:
			continue
		used1, used2 = set(), set()
		while len(set1-used1) > 0 and len(set2-used2) > 0 and max(len(used1), len(used2)) < maxpairs:
			cand1 = random.choice(list(set1-used1))
			cand2 = random.choice(list(set2-used2))
			used1.add(cand1)
			used2.add(cand2)
			f.write("{}\t{}\n".format(cand1, cand2))
			count += 1
	f.close()
	print("{} verse pairs written to {}".format(count, outfilename))
	print()


if __name__ == "__main__":
	l1 = loadBibles("spanish")
	for lg in ("ashaninka", "aymara", "bribri", "guarani", "hñähñu", "nahuatl", "quechua", "raramuri", "shipibo", "wixarika"):
		l2 = loadBibles(lg)
		sample(l1, l2, "sampled/spanish_{}.txt".format(lg))
	