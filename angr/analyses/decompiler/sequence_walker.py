# pylint:disable=unused-argument,useless-return

from ...errors import UnsupportedNodeTypeError
from .structurer import CodeNode, SequenceNode, SwitchCaseNode, MultiNode


class SequenceWalker:
    """
    Walks a SequenceNode and all its nodes, recursively.
    """
    def __init__(self, handlers=None, exception_on_unsupported=False):
        self._exception_on_unsupported = exception_on_unsupported

        default_handlers = {
            # Structurer nodes
            CodeNode: self._handle_Code,
            SequenceNode: self._handle_Sequence,
            SwitchCaseNode: self._handle_SwitchCase,
            MultiNode: self._handle_MultiNode,
        }

        self._handlers = default_handlers
        if handlers:
            self._handlers.update(handlers)

    def walk(self, sequence):
        return self._handle(sequence)

    #
    # Handlers
    #

    def _handle(self, node, **kwargs):
        handler = self._handlers.get(node.__class__, None)
        if handler is not None:
            return handler(node, **kwargs)
        if self._exception_on_unsupported:
            raise UnsupportedNodeTypeError("Node type %s is not supported yet." % type(node))
        return None

    def _handle_Code(self, node, parent=None, index=0):
        return self._handle(node.node, parent=node, index=0)

    def _handle_Sequence(self, node, parent=None, index=0):
        i = 0
        while i < len(node.nodes):
            node_ = node.nodes[i]
            self._handle(node_, parent=node, index=i)
            i += 1
        return None

    def _handle_MultiNode(self, node, parent=None, index=0):
        i = 0
        while i < len(node.nodes):
            node_ = node.nodes[i]
            self._handle(node_, parent=node, index=i)
            i += 1
        return None

    def _handle_SwitchCase(self, node):
        self._handle(node.switch_expr, parent=node, label='switch_expr')
        for idx, case in node.cases.items():
            self._handle(case, parent=node, index=idx, label='case')
        if node.default_node is not None:
            self._handle(node.default_node, parent=node, label='default')
        return None
