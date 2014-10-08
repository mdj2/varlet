#!/usr/bin/env python
from mock import Mock, patch
import unittest
import os
import __builtin__
import readline
import yaml
import varlet
from varlet import variable, get_preceeding_comments

class TestCase(unittest.TestCase):
    def setUp(self):
        self.tearDown()

    def tearDown(self):
        try:
            os.remove("variables.yaml")
        except OSError as e:
            pass

        varlet.variables = {}

    @patch('__builtin__.print')
    def test_non_yaml_value(self, print_mock):
        def func(_, return_values=["object()", "'foo'"]):
            return return_values.pop(0)

        # the first time raw_input return object() which is not YAML
        # serializable, and the second time it returns 'foo', which is fine
        with patch('__builtin__.raw_input', func):
            foo = variable("LAME")
            self.assertTrue("The value must be YAML serializable" in "".join(map(repr, print_mock.call_args_list)))
            self.assertEqual(foo, "foo")

    @patch('__builtin__.print')
    def test_non_valid_python_value(self, print_mock):
        def func(_, return_values=["asdf", "'foo'"]):
            return return_values.pop(0)

        # the first time raw_input return asdf  which is not Python
        # and the second time it returns 'foo'
        with patch('__builtin__.raw_input', func):
            foo = variable("LAME")
            self.assertTrue("name 'asdf' is not defined" in "".join(map(repr, print_mock.call_args_list)))
            self.assertEqual(foo, "foo")

    def test_get_variable_that_is_not_in_yaml_file(self):
        with patch('__builtin__.raw_input', lambda _: "'hello world'"):
            foo = variable("FOO")
            # we patched raw_input to return hello world, so that is what we should
            # get back
            self.assertEqual(foo, "hello world")
            # it should be written to the YAML file
            self.assertEqual(open("variables.yaml").read(), "FOO: hello world\n")

        # a second call should get the value right back without prompting for raw_input
        with patch('__builtin__.raw_input') as m:
            foo = variable("FOO")
            self.assertFalse(m.called)
            self.assertEqual(foo, "hello world")

    @patch('readline.set_startup_hook')
    @patch('readline.insert_text', lambda x: x)
    @patch('__builtin__.raw_input', lambda _: "'foo'")
    def test_get_variable_that_is_not_in_yaml_file_with_default(self, set_startup_hook):
        default = {"a": 123, (1,2): [1, "b"]}
        foo = variable("FOO", default=default)
        # set_startup_hook should be called so the prompt has an initial value
        self.assertTrue(set_startup_hook.called)
        # make sure the callback function returns the repr of the default value
        args, kwargs = set_startup_hook.call_args_list[0]
        self.assertEqual(args[0](), repr(default))
        # it should be called with 0 args to reset the prompt
        self.assertEqual(set_startup_hook.call_args_list[1], ())

    def test_get_preceeding_comments(self):
        # the comments below are significant so don't change them!

        # foo
        # bar
# fog
        comment = (lambda: get_preceeding_comments())()

        self.assertEqual(comment, "# foo\n# bar\n# fog")

        comment = (lambda: get_preceeding_comments())()
        self.assertEqual(comment, "")


if __name__ == '__main__':
    unittest.main()

