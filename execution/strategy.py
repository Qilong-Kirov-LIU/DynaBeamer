from . import load
from . import framemaker


def basic_strategy(node, tex, if_sub_sec, if_two_columns):
    """the standard strategy for latex-beamer formated filling.
    Noted that the function outputs the information from a nodes' tree. Therefore, this function is called traversally.
    
    Args:
        tex: The list of strings that stores the contents of the generated .tex file.
        node: The OutlineNode object that this slide contains.
        if_sub_sec: A boolean indicates if we use two level section, i.e. subsection, or not.
        if_two_columns: A boolean indicates if we use two columns or not.
    """

    # if the node's layer is 0, add standard preamble
    if node.layer == 0:
        framemaker.PreambleMaker(node, tex)
        
    # if the node's layer is 1, add first level section title
    # and if the node's note is not empty, makes a normal frame
        
    elif node.layer == 1:
        framemaker.SectionMaker(node, tex)
        
        if node.note != '':
            if if_two_columns:
                framemaker.TwoColumnFrameMaker(node, tex)
            else:
                framemaker.OneColumnFrameMaker(node, tex)
    
    # if the node's layer is 2 and the if_sub_sec is true, add second level section title
    # at the same time, if the node's note is not empty,makes a frame
    # otherwise, if the if_sub_sec is false, treat it like a normal frame
    elif node.layer == 2:
        if if_sub_sec:
            framemaker.SubsectionMaker(node, tex)
            if node.note != '':
                if if_two_columns:
                    framemaker.TwoColumnFrameMaker(node, tex)
                else:
                    framemaker.OneColumnFrameMaker(node, tex)
        else:
            if node.note != '':
                if if_two_columns:
                    framemaker.TwoColumnFrameMaker(node, tex)
                else:
                    framemaker.OneColumnFrameMaker(node, tex)
            
    # otherwise, makes a normal frame
    else:
        if node.note != '':
            if if_two_columns:
                framemaker.TwoColumnFrameMaker(node, tex)
            else:
                framemaker.OneColumnFrameMaker(node, tex)

    # traversal call this function for all the children of the node
    for child in node.child:
        basic_strategy(child, tex, if_sub_sec, if_two_columns)


def guide_through(loc_in, loc_out):
    """This function provides an interactive way for the user to use AutoPre.
    
    And it now serves as the default way of exploiting the capacity of AutoPre.
    
    Args:
        loc_in: A string that indicates folder that contains the content files (.opml or .docx).
        loc_out: A string that indicates folder that contains the output files (.pptx).
    """
    # files loading
    root_node_list, filename_list = load.load_files(loc_in)
    print("\n  {} files has been loaded.".format(len(filename_list)))

    # setting and outputting
    for n in range(len(root_node_list)):
        print("generating latex-beamer presentation file from: {}".format(filename_list[n]))
        title = input("output filename: ")
        subsec_mode = input("use two level section [y/n]: \n")
        subsec_dict = {"y": True, "n": False}
        column_mode = input("one column or two column [1/2]: \n")
        column_dict = {"2": True, "1": False}

        # outputs the presentation file.
        tex = []
        basic_strategy(root_node_list[n], tex, subsec_dict[subsec_mode], column_dict[column_mode])
        framemaker.BackMaker(root_node_list[n], tex)

        with open(loc_out + title + '.tex', 'w') as output:
            output.writelines(tex)
        print("beamer file is outputted to " + loc_out + title + '.tex')
    

if __name__ == '__main__':
    
    guide_through("../documents/", "../outputs/")
