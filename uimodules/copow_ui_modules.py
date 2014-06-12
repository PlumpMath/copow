#
# copow ui modules.
#
# see: http://tornado.readthedocs.org/en/latest/overview.html#ui-modules
import tornado.web

class FormSelect(tornado.web.UIModule):
    """
        Renders a nice html selection list from
        given model entries

        Shows the specified model.model_attribute as selector.
        Default is _id (Which is probably something you want to change ;)
    """

    def render(self, models=None, model_attribute="_id"):
        return self.render_string(
            "uimodules/form_select.html", models=models, model_attribute=model_attribute)