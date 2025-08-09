# """Ensure the Sphinx template bridge is installed and works."""
#
# from unittest.mock import Mock
#
# from themester.sphinx.template_bridge import ThemesterBridge, View
#
#
# def test_render():
#     """Test that render gets a View from the container."""
#     container = Mock()
#     context = {"context_container": container}
#     tb = ThemesterBridge()
#     tb.render("some_template", context)
#     container.get.assert_called_once_with(View)
