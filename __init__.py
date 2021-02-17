#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals, print_function
from html.parser import HTMLParser

__all__ = ['slate_parser_loads', 'slate_parser_load']


class MyHTMLParser(HTMLParser, object):
    def __init__(self):
        self._parent = ''
        self.is_new_parent = False
        self.stack_tags = []
        self.stack_attrs = []
        self.stack_childs = []
        self.nodes = []
        self.slate_obj = {
            "object": "value",
            "document": {
                "nodes": [],
                "object": "document",
                "data": {}
            }
        }
        super(MyHTMLParser, self).__init__()

    def handle_starttag(self, tag, attrs):
        self.stack_tags.append(tag)
        self.stack_attrs.append(attrs)
        self.update_parent_tag(tag)

    def handle_endtag(self, tag):
        self.is_new_parent = False
        if tag in ['div', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            self._parent = ''

    def handle_data(self, data):
        if data == '\n'.encode('utf-8') or data.isspace():
            return

        if self.stack_tags:
            tag = self.stack_tags.pop()
        else:
            if self.is_new_parent:
                self.is_new_parent = False
                self.slate_obj['document']['nodes'].append({
                    "object": "block",
                    "type": "paragraph",
                    "data": {},
                    "nodes": [{
                        "text": data,
                        "object": "text",
                        "marks": []}],
                })
            else:
                self.attach_inline_element({
                    "text": data,
                    "object": "text",
                    "marks": []
                })
            return

        if self.stack_attrs:
            attrs = self.stack_attrs.pop()

        if tag == 'p':
            if self.is_new_parent:
                self.is_new_parent = False
                self.slate_obj['document']['nodes'].append({
                    "object": "block",
                    "type": "paragraph",
                    "data": {},
                    "nodes": [{
                        "text": data,
                        "object": "text",
                        "marks": []}],
                })
            else:
                self.attach_inline_element({
                    "text": data,
                    "object": "text",
                    "marks": []
                })
        elif tag == 'blockquote':
            self.slate_obj['document']['nodes'].append({
                "data": {},
                "nodes": [
                    {
                        "text": data,
                        "object": "text",
                        "marks": []
                    }
                ],
                "object": "block",
                "type": "blockquote"
            })
        elif tag == 'h1':
            self.is_new_parent = False
            self.slate_obj['document']['nodes'].append({
                "nodes": [
                    {
                        "text": data,
                        "object": "text",
                        "marks": []
                    }
                ],
                "object": "block",
                "type": "h1",
                "data": {}
            }),
        elif tag == 'h2':
            self.is_new_parent = False
            self.slate_obj['document']['nodes'].append({
                "nodes": [
                    {
                        "text": data,
                        "object": "text",
                        "marks": []
                    }
                ],
                "object": "block",
                "type": "h2",
                "data": {}
            }),
        elif tag == 'h3':
            self.is_new_parent = False
            self.slate_obj['document']['nodes'].append({
                "nodes": [
                    {
                        "text": data,
                        "object": "text",
                        "marks": []
                    }
                ],
                "object": "block",
                "type": "h3",
                "data": {}
            }),
        elif tag == 'h4':
            self.is_new_parent = False
            self.slate_obj['document']['nodes'].append({
                "nodes": [
                    {
                        "text": data,
                        "object": "text",
                        "marks": []
                    }
                ],
                "object": "block",
                "type": "h4",
                "data": {}
            }),
        elif tag == 'h5':
            self.is_new_parent = False
            self.slate_obj['document']['nodes'].append({
                "nodes": [
                    {
                        "text": data,
                        "object": "text",
                        "marks": []
                    }
                ],
                "object": "block",
                "type": "h5",
                "data": {}
            }),
        elif tag == 'h6':
            self.is_new_parent = False
            self.slate_obj['document']['nodes'].append({
                "nodes": [
                    {
                        "text": data,
                        "object": "text",
                        "marks": []
                    }
                ],
                "object": "block",
                "type": "h6",
                "data": {}
            }),
        elif tag == 'div':
            self.is_new_parent = False
            if data != '\n'.encode('utf-8'):
                self.slate_obj['document']['nodes'].append({
                    "object": "block",
                    "type": "paragraph",
                    "data": {},
                    "nodes": [{
                        "text": data,
                        "object": "text",
                        "marks": []}],
                })
        elif tag == 'br':
            if data == '\n'.encode('utf-8') or data.isspace():
                self.slate_obj['document']['nodes'].append({
                    "data": {},
                    "nodes": [
                        {
                            "text": "",
                            "object": "text",
                            "marks": []
                        },
                    ],
                    "object": "block",
                    "type": "paragraph"
                })
            else:
                self.slate_obj['document']['nodes'].append({
                    "data": {},
                    "nodes": [
                        {
                            "text": "",
                            "object": "text",
                            "marks": []
                        },
                        {
                            "text": data,
                            "object": "text",
                            "marks": []
                        },
                    ],
                    "object": "block",
                    "type": "paragraph"
                })
        elif tag == 'a':
            for attr in attrs:
                if attr[0] == 'href':
                    url = attr[1]

            self.attach_inline_element({
                "data": {
                    "url": url if url else ''
                },
                "nodes": [
                    {
                        "text": data,
                        "object": "text",
                        "marks": []
                    }
                ],
                "object": "inline",
                "type": "link"
            })
        elif tag == 'strong':
            self.attach_inline_element({
                "text": data,
                "object": "text",
                "marks": [
                    {
                        "data": {},
                        "object": "mark",
                        "type": "bold"
                    }
                ]})
        elif tag == 'em' or tag == 'i':
            self.attach_inline_element({
                "text": data,
                "object": "text",
                "marks": [
                    {
                        "data": {},
                        "object": "mark",
                        "type": "italic"
                    }
                ]})
        elif tag == 'code':
            self.attach_inline_element({
                "text": data,
                "object": "text",
                "marks": [
                    {
                        "data": {},
                        "object": "mark",
                        "type": "code"
                    }
                ]})
        elif tag == 'u':
            self.attach_inline_element({
                "text": data,
                "object": "text",
                "marks": [
                    {
                        "data": {},
                        "object": "mark",
                        "type": "underline"
                    }
                ]})
        elif tag == 's':
            self.attach_inline_element({
                "text": data,
                "object": "text",
                "marks": [
                    {
                        "data": {},
                        "object": "mark",
                        "type": "strikethrough"
                    }
                ]})
        elif tag == 'img':
            for attr in attrs:
                if attr[0] == 'height':
                    height = attr[1]
                elif attr[0] == 'width':
                    width = attr[1]
                elif attr[0] == 'src':
                    src = attr[1]
                elif attr[0] == 'alt':
                    alt = attr[1]

            self.slate_obj['document']['nodes'].append({
                "data": {
                    "height": height,
                    "url": src,
                    "width": width
                },
                "nodes": [
                    {
                        "marks": [],
                        "object": "text",
                        "text": alt
                    }
                ],
                "object": "block",
                "type": "image"
            })
        else:
            if self.is_new_parent:
                self.is_new_parent = False
                self.slate_obj['document']['nodes'].append({
                    "object": "block",
                    "type": "paragraph",
                    "data": {},
                    "nodes": [{
                        "text": data,
                        "object": "text",
                        "marks": []}],
                })
            else:
                self.attach_inline_element({
                    "text": data,
                    "object": "text",
                    "marks": []
                })

    def attach_inline_element(self, elem):
        if not self.is_new_parent:
            if len(self.slate_obj['document']['nodes']):
                last_node = self.slate_obj['document']['nodes'].pop()
                if last_node['type'] in ['paragraph', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                    last_node['nodes'].append(elem)
                    self.slate_obj['document']['nodes'].append(last_node)
                    return

        if self._parent in ['div', 'p']:
            parent_type = 'paragraph'
        elif self._parent == 'h1':
            parent_type = 'h1'
        elif self._parent == 'h2':
            parent_type = 'h2'
        elif self._parent == 'h3':
            parent_type = 'h3'
        else:
            parent_type = 'paragraph'

        self.slate_obj['document']['nodes'].append({
            "object": "block",
            "type": parent_type,
            "data": {},
            "nodes": [elem],
        })

    def update_parent_tag(self, tag):
        if tag in ['div', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            self._parent = tag
            self.is_new_parent = True


def _slate_parser(data):
    parser = MyHTMLParser()
    parser.feed(data)
    return parser.slate_obj


def slate_parser_loads(s):
    return _slate_parser(s)


def slate_parser_load(s):
    with open(s) as fp:
        data = fp.read()
    return _slate_parser(data)