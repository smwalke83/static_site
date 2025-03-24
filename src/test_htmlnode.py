import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType
from splitnodes import *
from texttohtml import *

children1 = [1, 2, 3, 4, 5]
children2 = [6, 7, 8, 9, 10]

props1 = {"href": "www.www.www", "target": "your mom"}
props2 = {"href": "www.www.org", "target": "your dad"}

class TestHTMLNode(unittest.TestCase):
    def test_tag_eq(self):
        node = HTMLNode("tag", "value")
        node2 = HTMLNode("tag", "value")
        node3 = HTMLNode("other tag", "value")
        self.assertEqual(node, node2)
        self.assertNotEqual(node, node3)
    def test_value_eq(self):
        node = HTMLNode("tag", "value", children1, props1)
        node2 = HTMLNode("tag", "value", children1, props1)
        node3 = HTMLNode("tag", "other value", children1, props1)
        self.assertEqual(node, node2)
        self.assertNotEqual(node, node3)
    def test_children_eq(self):
        node = HTMLNode("tag", "value", children1, props1)
        node2 = HTMLNode("tag", "value", children1, props1)
        node3 = HTMLNode("tag", "value", children2, props1)
        self.assertEqual(node, node2)
        self.assertNotEqual(node, node3)
    def test_props_eq(self):
        node = HTMLNode("tag", "value", children1, props1)
        node2 = HTMLNode("tag", "value", children1, props1)
        node3 = HTMLNode("tag", "value", children1, props2)
        self.assertEqual(node, node2)
        self.assertNotEqual(node, node3)
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Text")
        self.assertEqual(node.to_html(), "<a>Text</a>")
    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Words")
        self.assertEqual(node.to_html(), "Words")
    def test_to_html_one_child(self):
        child_node = LeafNode("a", "Child")
        parent_node = ParentNode("b", [child_node])
        self.assertEqual(parent_node.to_html(), "<b><a>Child</a></b>")
    def test_to_html_grandchild(self):
        grandchild_node = LeafNode("a", "Grandchild")
        child_node = ParentNode("b", [grandchild_node])
        parent_node = ParentNode("c", [child_node])
        self.assertEqual(parent_node.to_html(), "<c><b><a>Grandchild</a></b></c>")
    def test_nested_to_html(self):
        ggc1 = LeafNode("a", "No")
        ggc2 = LeafNode("b", "Lie")
        gc1 = LeafNode("c", "Text")
        gc2 = ParentNode("d", [ggc1, ggc2])
        gc3 = LeafNode("e", "Words")
        gc4 = LeafNode("f", "Are")
        gc5 = LeafNode("g", "Fun")
        child1 = ParentNode("h", [gc1, gc2])
        child2 = LeafNode(None, "Hello")
        child3 = ParentNode("i", [gc3, gc4, gc5])
        parent = ParentNode("j", [child1, child2, child3])
        self.assertEqual(gc2.to_html(), "<d><a>No</a><b>Lie</b></d>")
        self.assertEqual(
            parent.to_html(),
            "<j><h><c>Text</c><d><a>No</a><b>Lie</b></d></h>Hello<i><e>Words</e><f>Are</f><g>Fun</g></i></j>"
        )
    def test_empty_children_list(self):
        children = []
        parent = ParentNode("a", children)
        self.assertEqual(parent.to_html(), "<a></a>")
    
    def test_text_to_html_text(self):
        node = TextNode("Text", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "Text")
    def test_text_to_html_ital(self):
        node = TextNode("Text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Text")
    def test_text_to_html_bold(self):
        node = TextNode("Text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Text")
    def test_text_to_html_code(self):
        node = TextNode("Text", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "Text")
    def test_text_to_html_link(self):
        URL = "www.www.www"
        props = {
            "href" : URL
        }
        node = TextNode("Text", TextType.LINK, URL)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Text")
        self.assertEqual(html_node.props, props)
    def test_text_to_html_image(self):
        URL = "www.www.www"
        props = {
            "src" : URL,
            "alt" : "Text"
        }
        node = TextNode("Text", TextType.IMAGE, URL)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, props)
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>"
        )
    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>",
        )
    def test_ordered_list_block(self):
        md = """
1. Item one
2. The second item
3. Item 3
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>Item one</li><li>The second item</li><li>Item 3</li></ol></div>"
        )
    def test_unordered_list_block(self):
        md = """
- Item one
- The second item
- Item 3
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item one</li><li>The second item</li><li>Item 3</li></ul></div>"
        )
    def test_blockquote(self):
        md = """
>This is a quote.
>This is the second line of the quote.
>Quote line 3.
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote. This is the second line of the quote. Quote line 3.</blockquote></div>"
        )
    def test_header_block(self):
        md = """
# This is a header 1

## This is a header 2

Paragraph text

### This is a header 3
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is a header 1</h1><h2>This is a header 2</h2><p>Paragraph text</p><h3>This is a header 3</h3></div>"
        )
    def test_multiple_blocks(self):
        md = """
# Header

Paragraph

- Unordered list 1
- ul 2
- ul 3

Paragraph

```Short **code** block```

1. Ordered list 1
2. ol 2
3. ol 3

>Quotes
>and more quotes
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Header</h1><p>Paragraph</p><ul><li>Unordered list 1</li><li>ul 2</li><li>ul 3</li></ul><p>Paragraph</p><pre><code>Short **code** block</code></pre><ol><li>Ordered list 1</li><li>ol 2</li><li>ol 3</li></ol><blockquote>Quotes and more quotes</blockquote></div>"
        )
#if __name__ == "__main__":
#    unittest.main()            These two lines are only necessary when you want to run just this specific file, not when using ./test.sh