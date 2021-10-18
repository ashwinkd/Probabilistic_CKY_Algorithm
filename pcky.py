from matplotlib import pyplot as plt


def get_grammar_rules(grammar_text=None):
    """

    :param grammar_text: a default grammar given in assignment 5 is copied here.
    If you want to try a new grammar, make sure there are no leading spaces.
    Every line has to be in this format:
    A,B C,prob
    :return:
    """
    if grammar_text is None:
        grammar_text = """S,NP VP,60
            S,N VP,20
            S,NP V,20
            VP,VP P,5
            VP,VP PP,30
            VP,VP NP,20
            VP,VP N,10
            VP,V P,5
            VP,V N,10
            VP,V PP,10
            VP,V NP,10
            NP,DT NP,20
            NP,DT N,15
            NP,NP N,5
            NP,NP NP,10
            NP,NP PP,20
            NP,N N,5
            NP,N NP,5
            NP,N PP,20
            PP,P N,40
            PP,P NP,60
            DT,the,100
            P,with,100
            V,mixed,75
            V,candy,25
            N,Dracula,25
            N,Halloween,25
            N,candy,25
            N,chopsticks,25"""
    # clean up leading and trailing spaces on each line
    grammar = [grammar_rule.strip() for grammar_rule in grammar_text.split('\n')]
    # split line to a A BC and prob
    grammar = [grammar_rule.split(',') for grammar_rule in grammar]
    grammar = [rule for rule in grammar if len(rule) == 3]
    for i, rule in enumerate(grammar):
        left, right, prob = rule
        # B C is converted to [B, C] or 'dracula' if terminal
        right = right.split()
        if len(right) == 1:
            right = right[0].lower()
        # prob is assumed to be in percentage, change /100 if not
        prob = int(prob) / 100
        # save in grammar
        grammar[i] = (left, right, prob)

    return grammar


def pcky(words, grammar):
    """
                               0         1       2         3         4        5         6
    :param words: example ['dracula', 'mixed', 'the', 'halloween', 'candy', 'with', 'chopsticks']
          0    -- j -->       6
      0  [k][ ][ ][ ][ ][ * ][ ]
      ^  [-][ ][ ][ ][ ][k+1][ ]
      |  [-][-][ ][ ][ ][   ][ ]
      i  [-][-][-][ ][ ][   ][ ]
      |  [-][-][-][-][ ][   ][ ]
      j  [-][-][-][-][-][5,5][ ]
      6  [-][-][-][-][-][ - ][ ]
    say j=5, i will travel from j-1=4 up the column till 0
    each cell [i,j] has a dict with all unique A in a grammar A --> B C
    for each grammar A in cell [i,j] say cell [0,5] marked * in above diagram
    k will run from i = 0 to j = 4, each column in row i = 0
    each word at k is paired with k+1
    :param grammar: check get_grammar_rules() for more
    :return: table for example sentence it will be nxnxV --> 7x7x8
    """
    # for example grammar {'NP', 'DT', 'N', 'S', 'P', 'VP', 'PP', 'V'}
    vocab = set([rule[0] for rule in grammar])
    # each cell will contain a vocab_dict with initialized 0 probability for each A in vocab
    # for example grammar {'NP': 0, 'DT': 0, 'N': 0, 'S': 0, 'P': 0, 'VP': 0, 'PP': 0, 'V': 0}
    vocab_dict = {v: 0.0 for v in vocab}
    n = len(words)
    # create nxnxV table
    table = [[vocab_dict.copy() for i in range(n)] for j in range(n)]
    # create nxnxV back
    back = [[vocab_dict.copy() for i in range(n)] for j in range(n)]
    for j in range(n):
        # loop through each word j
        for rule in grammar:
            # add pos tag in [j,j] position
            A, right, prob = rule
            if right == words[j]:
                table[j][j][A] = prob
        for i in range(j - 1, -1, -1):
            # run up the column j till 0
            for k in range(i, j):
                # k,k+1 word pair from k = i until word j
                for rule in grammar:
                    # each rule in each cell
                    A, right, prob = rule
                    if len(right) != 2:
                        # non-terminal rules only
                        continue
                    B, C = right
                    if table[i][k][B] <= 0 or table[k + 1][j][C] <= 0:
                        continue
                    if table[i][j][A] < prob * table[i][k][B] * table[k + 1][j][C]:
                        # if grammar A has higher probability, switch it
                        table[i][j][A] = prob * table[i][k][B] * table[k + 1][j][C]
                        back[i][j][A] = (k, B, C)
    print("Sentence Probability: {}".format(table[0][n - 1]['S']))
    print("Backtrace: {}".format(back[0][n - 1]['S']))
    return table, back


def plot_cky(table, back, words):
    n = len(table)

    fig, axs = plt.subplots(n, n)
    fig.set_figheight(10)
    fig.set_figwidth(15)
    for i in range(n):
        for j in range(n):
            if i == 0:
                axs[i, j].set_title(str(j) + "-" + words[j])
            if j == 0:
                axs[i, j].set_ylabel(str(i) + "-" + words[i])
            cell = table[i][j]
            c_back = back[i][j]
            label = ""
            for key, value in cell.items():
                if value <= 0:
                    continue
                label += str(key) + " : {:.2e}".format(value) + '\n'
            if not label:
                label = '-'
            axs[i, j].set_yticklabels([])
            axs[i, j].set_xticklabels([])
            axs[i, j].text(0.5, 0.5, label, verticalalignment='center', horizontalalignment='center')
    plt.show()


def main():
    sentence = "dracula mixed the halloween candy with chopsticks"
    words = sentence.split()
    grammar = get_grammar_rules()
    table, back = pcky(words, grammar)
    plot_cky(table, back, words)


if __name__ == '__main__':
    main()
