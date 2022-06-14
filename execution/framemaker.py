TAB = " "*4


class BasicFrameMaker(object):
    """The basic frame maker class. All other frame makers are inherited from this class.
    
    Attributes:
        node: The OutlinNode object that this slide contains.
        tex: The tex file object it creates and works on.
    """
    
    def __init__(self, node, tex):
        
        self.node = node
        self.tex = tex


class PreambleMaker(BasicFrameMaker):
    """Make the preamble of the .tex file"""

    def __init__(self, node, tex):
        BasicFrameMaker.__init__(self, node, tex)
        self.write_preamble()

    def write_preamble(self):
        with open('templates/front.tex', 'r') as front:
            lines = front.readlines()

        for line in lines:
            self.tex.append(line)


class SectionMaker(BasicFrameMaker):
    """Make the section command of the .tex file"""

    def __init__(self, node, tex):
        BasicFrameMaker.__init__(self, node, tex)
        self.write_section()

    def write_section(self):
        self.tex.append("\section{" + self.node.title + "}\n\n")


class SubsectionMaker(BasicFrameMaker):
    """Make the subsection command of the .tex file"""

    def __init__(self, node, tex):
        BasicFrameMaker.__init__(self, node, tex)
        self.write_subsection()

    def write_subsection(self):
        self.tex.append("\subsection{" + self.node.title + "}\n\n")


class OneColumnFrameMaker(BasicFrameMaker):
    """Make the one column frame in the .tex file"""

    def __init__(self, node, tex):
        BasicFrameMaker.__init__(self, node, tex)
        self.begin_frame()
        self.add_content()
        self.end_frame()

    def begin_frame(self):
        self.tex.append("\\begin{frame}{" + self.node.title + "}\n")

    def add_content(self):
        self.tex.append(TAB + "\\begin{itemize}\n")
        for line in self.node.note.split("\n")[:-1]:
            self.tex.append(TAB*2 + "\item " + line + "\n")
        self.tex.append(TAB + "\end{itemize}\n")

    def end_frame(self):
        self.tex.append("\end{frame}\n\n")


class TwoColumnFrameMaker(OneColumnFrameMaker):
    """Make the two column frame in the .tex file"""

    def add_content(self):
        self.tex.append(TAB + "\\begin{columns}\n")

        self.tex.append(TAB*2 + "\\begin{column}{0.6\\textwidth}\n")
        self.tex.append(TAB*3 + "\\begin{itemize}\n")
        for line in self.node.note.split("\n")[:-1]:
            self.tex.append(TAB*4 + "\item " + line + "\n")
        self.tex.append(TAB*3 + "\end{itemize}\n")
        self.tex.append(TAB*2 + "\end{column}\n")

        self.tex.append(TAB * 2 + "\\begin{column}{0.3\\textwidth}\n")
        self.tex.append(TAB * 3 + "\n")
        self.tex.append(TAB * 2 + "\end{column}\n")

        self.tex.append(TAB + "\end{columns}\n")


class BackMaker(BasicFrameMaker):
    """Make the preamble of the .tex file"""

    def __init__(self, node, tex):
        BasicFrameMaker.__init__(self, node, tex)
        self.write_back()

    def write_back(self):
        with open('templates/back.tex', 'r') as back:
            lines = back.readlines()

        for line in lines:
            self.tex.append(line)


if __name__ == '__main__':
    tex = []

    node = PreambleMaker([], [])
    node.title = "test"
    node.note = "test\ntest\ntest"

    PreambleMaker(node, tex)
    SectionMaker(node, tex)
    SubsectionMaker(node, tex)
    OneColumnFrameMaker(node, tex)
    TwoColumnFrameMaker(node, tex)
    BackMaker(node, tex)

    with open('../outputs/example.tex', 'w') as output:
        output.writelines(tex)
