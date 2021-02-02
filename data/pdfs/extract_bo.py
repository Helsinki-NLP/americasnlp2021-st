#! /usr/bin/env python3

import fitz, re, itertools


def checkLongWords(s, pageno):
	lw = [x for x in re.split(r'\s', s) if len(x) > 20]
	if len(lw) > 0:
		print("- Long words on page {}: {}".format(pageno, ", ".join(lw)))


def block2lines(b):
	s = re.sub(r' +\n', r'\n', b)
	t = re.sub(r'(\w)-\n(\w)', r'\1\2', s)
	u = re.sub(r'([^:.])\n', r'\1 ', t)
	v = re.split(r'\n', u)
	return [x.strip() for x in v if x.strip() != ""]


def fixBlocks(b):
	toremove = []
	for i in range(len(b)-1):
		if re.match(r'^[0-9IVX]+\.?$', b[i]):
			toremove.append(i)
			b[i+1] = b[i] + " " + b[i+1]
	if toremove != []:
		toremove.reverse()
		for i in toremove:
			del b[i]


def extract(filename, frompage, topage, colsep, outfilename):
	doc = fitz.open(filename)
	print("Pages:", doc.pageCount)
	outfile = open(outfilename, 'w', encoding='utf-8')

	for pageno in range(frompage, topage):
		page = doc.loadPage(pageno)
		outfile.write("** Page {} **\n".format(pageno))
		blocks = page.getText("blocks")
		left_blocks, right_blocks, common_blocks = [], [], []
		for b in blocks:
			if b[4].strip() == "":
				continue
			elif b[4] == "ConstituCión PolítiCa del estado\nMaChaqa tayka kaMaChi\n":
				continue
			elif "Ministerio de Culturas y Turismo - Viceministerio de Descolonización\nFundación Konrad Adenauer (KAS)" in b[4]:
				continue
			elif "Ministerio de Culturas y turismo - Viceministerio de descolonización\nFundación konrad adenauer (kas)" in b[4]:
				continue
			elif b[4] == "ESTADOQ KURAQ KAMACHIYNIN\nCONSTITUCIÓN POLÍTICA DEL ESTADO\n":
				continue
			elif b[4] == "Ministerio de la Presidencia - V.C.G.G\nFundación Konrad Adenauer (KAS)\n":
				continue
			elif b[4].strip().isnumeric():
				continue
			elif b[0] < colsep and b[2] < colsep:
				checkLongWords(b[4], pageno)
				text = block2lines(b[4])
				left_blocks.extend(text)			
			elif b[0] > colsep and b[2] > colsep:
				checkLongWords(b[4], pageno)
				text = block2lines(b[4])
				right_blocks.extend(text)
			else:
				checkLongWords(b[4], pageno)
				text = block2lines(b[4])
				common_blocks.extend(text)
		print("Page {}, left {}, right {}, other {}".format(pageno, len(left_blocks), len(right_blocks), len(common_blocks)))
		
		fixBlocks(left_blocks)
		fixBlocks(right_blocks)
		fixBlocks(common_blocks)
		
		for left, right in itertools.zip_longest(left_blocks, right_blocks):
			if left is None:
				outfile.write("\t{}\t\n".format(right))
			elif right is None:
				outfile.write("{}\t\t\n".format(left))
			else:
				outfile.write("{}\t{}\t\n".format(left, right))
		
		for common in common_blocks:
			outfile.write("\t\t{}\n".format(common))


if __name__ == "__main__":
	extract("bo_aymara_spanish.pdf", 7, 138, 290, "aymara.txt")
	extract("bo_quechua_spanish.pdf", 8, 121, 310, "quechua.txt")