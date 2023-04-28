"""
The module implements a function that generates
permutations of child nouns with each other.
"""
import re
from itertools import permutations, product
from typing import List, Tuple, Optional, Union

from nltk.tree import Tree


def _output_only_type_tree(tree: Union[str, Tree]) -> Tree:
    """
    Returns only object Tree or raises exceptions.
    """
    if isinstance(tree, Tree):
        return tree
    elif isinstance(tree, str):
        # TODO validation str as bracketed tree
        return Tree.fromstring(tree)
    else:
        raise TypeError("Input argument should be a str or Tree, "
                        "not a %s" % type(tree).__name__)


def separate_by_comma_or_conjunctive(func):
    """
    This function is decorator to _find_noun_phrases().
    Separates noun trees that contain a comma, or a conjunction, or both.
    """
    def wrapper(*args) -> List[Tree]:
        new_list_tree: List[Tree] = []
        for tree in func(*args):
            if not any((child.label() not in ('NP', 'CC', ',')) for child in tree):
                new_list_tree.append(tree)
        return new_list_tree
    return wrapper


def separate_only_noun_phrases(func):
    """
    This function is decorator to _find_noun_phrases().
    Separates and groups trees of nouns that are subject to substitution.
    """
    def wrapper(*args) -> List[List[Tree]]:
        list_of_lists_noun_tree: List[List[Tree]] = []
        for list_noun_tree in func(*args):
            group_noun_tree: List[Tree] = []
            for tree in list_noun_tree:
                if tree.label() == 'NP':
                    group_noun_tree.append(tree)
            list_of_lists_noun_tree.append(group_noun_tree)
        return list_of_lists_noun_tree
    return wrapper


@separate_only_noun_phrases
@separate_by_comma_or_conjunctive
def _find_noun_phrases(tree: Union[str, Tree]) -> List[Tree]:
    """
    Search for noun phrases consisting of several NPs.
    Returns a list of found noun phrase trees.
    """
    tree: Tree = _output_only_type_tree(tree)

    noun_phrase_subtrees: List[Tree] = []
    for subtree in tree.subtrees():

        if subtree.label() == 'NP' and len(subtree) >= 2:
            noun_phrase_subtrees.append(subtree)
    return noun_phrase_subtrees


def _generate_list_of_substitutions(lst_trees: List[List[Tree]]) -> List[List[Tree]]:
    """
    Returns successive permutations of noun phrases in the list.
    """
    lst_sub: List[List[List[Tree]]] = [list(map(list, permutations(tree))) for tree in lst_trees]
    lst_sub_united: List[List[Tree]] = [sum(list(item), []) for item in product(*lst_sub)]
    return lst_sub_united


def _find_subtree_index(tree: Tree, search_element: Tree) -> Tuple[Optional[Tree], Optional[int]]:
    """
    Recursively searches for the <tree.Tree> element in the main object <tree.Tree>.
    Returns the parent subtree and its index.
    """
    if tree == search_element:
        return None, 0
    else:
        index_sum = 0
        for i, subtree in enumerate(tree):
            if type(subtree) is Tree:
                parent_subtree, index = _find_subtree_index(subtree, search_element)
                if parent_subtree is not None:
                    return parent_subtree, index
                elif index is not None:
                    return tree, index_sum + i + index
            else:
                index_sum += 1
        return None, None


def tree_to_str(func):
    """
    This function is decorator to generator_noun_paraphrases().
    Сonverts tree.Tree objects to type str.
    """
    def wrapper(*args, **kwargs) -> List[str]:
        return list(map(lambda x: re.sub('\s+', ' ', str(x).replace('\n', '')), func(*args, **kwargs)))
    return wrapper


@tree_to_str
def generator_noun_paraphrases(tree: Union[str, Tree], *, limit: int = 20) -> List[Tree]:
    """
    The function generates permutations of these child noun phrases with each other.
    Returns a list of paraphrases in tree.Tree objects.
    """
    tree: Tree = _output_only_type_tree(tree)
    noun_phrases: List[List[Tree]] = _find_noun_phrases(tree)
    lst_substitution: List[List[Tree]] = _generate_list_of_substitutions(noun_phrases)
    # the original version is always first in the list
    sequence_noun_tree_original: list = lst_substitution.pop(0)

    # find the index of the phrase in the original version and keep its sequence
    sequence_index_phrase: List[tuple[int, Tree]] = []
    for noun_tree in sequence_noun_tree_original:
        _, index_phrase = _find_subtree_index(tree, noun_tree)
        sequence_index_phrase.append((index_phrase, noun_tree))

    lst_index_substitution = [list(zip(sequence_index_phrase, i)) for i in lst_substitution]

    paraphrases: List[Tree] = []
    for sequence in lst_index_substitution:
        new_tree: Tree = tree.copy(deep=Tree)
        for item in sequence:
            search_phrase = item[0][1]
            insert_phrase = item[1]
            if search_phrase == insert_phrase:
                continue
            index = item[0][0]
            parent_subtree, _ = _find_subtree_index(new_tree, search_phrase)
            parent_subtree[index] = insert_phrase
        paraphrases.append(new_tree)

        if len(paraphrases) >= limit:
            break

    return paraphrases
