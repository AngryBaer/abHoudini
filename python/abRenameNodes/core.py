"""
    Houdini renaming utils.
"""
import hou


def get_selected():
    """ Return selected Houdini nodes. """
    return hou.selectedNodes()


def rename_selection(name: str, prefix: str = '', suffix: str = '', start: int = 1):
    """ Rename the selected nodes using the given pattern. """
    for node in get_selected():
        node.setName(prefix + name + f"_{start:0>3}" + suffix)
        start += 1


def prefix_selection(prefix: str):
    """ Prefix the selected nodes using the given pattern. """
    for node in get_selected():
        node.setName(prefix + node.name())


def suffix_selection(suffix: str):
    """ Suffix the selected nodes using the given pattern. """
    for node in get_selected():
        node.setName(node.name() + suffix)
