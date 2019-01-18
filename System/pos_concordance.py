from concordance import Concordance
import re
import os
from build_feature_table import build_feature_table


# Pattern of the lines from the POS file we are interested in.
reg_pos_line = re.compile(r'(\d+)\s+(\d+)\s+(\S+)[\s<>]+(\d+)\s+(.+)')


class PoS_Concordance(Concordance):
    def __init__(self, texts):
        Concordance.__init__(self, texts)

    def make_concordance(self, pos_reg):
        for article in self.texts.get_articles():
            fname = os.path.join(article.folder, "{}.txt.pos".format(article.index))
            with open(fname) as pos_file:
                text = pos_file.readlines()
                text = [line.strip() for line in text]

            words = []
            pos = []
            for line in text:
                line = line.strip()
                # match the pattern of the lines we are interesting and define groups within.
                m = reg_pos_line.match(line)
                if m:
                    curr_word = m.group(3)  # Get the group we're interested in (possible tags)
                    words.append(curr_word)

                    curr_pos = m.group(5).split(']')[0].split('/')[0]
                    pos.append(curr_pos)

            for i, (curr_word, curr_pos) in enumerate(zip(words, pos)):
                # print(curr_pos)
                m = re.fullmatch(pos_reg, curr_pos)
                if m:
                    if i < 5:
                        before_index = 0
                    else:
                        before_index = i - 5

                    if i > len(words) - 5:
                        after_index = len(words)
                    else:
                        after_index = i + 5

                    print(" ".join(words[before_index:after_index]))


if __name__ == "__main__":
    corp = build_feature_table("bow", kind='bow')
    conc = PoS_Concordance(corp)
    conc.make_concordance(r'T[1-4][\.\d\+-]*')
