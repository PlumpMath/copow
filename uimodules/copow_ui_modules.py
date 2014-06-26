#
# copow ui modules.
#
# see: http://tornado.readthedocs.org/en/latest/overview.html#ui-modules
#
# remark: wheneer I say "nice" in this module it's purely subjective to me ;)
#
import tornado.web

class FormSelect(tornado.web.UIModule):
    """
        Renders a nice html selection list from
        given model entries

        Shows the specified model.attribute as selector.
        Default is _id (Which is probably something you want to change ;)
    """

    def render(self, model=None, attribute="_id"):
        return self.render_string(
            "uimodules/form_select.html", model=model, attribute=attribute, value="")


class FormTextInput(tornado.web.UIModule):
    """
        Renders a nice html textfield

        Shows the specified model.attribute as selector.
        Default is _id (Which is probably something you want to change ;)
    """

    def render(self, model=None, attribute="_id"):
        return self.render_string(
            "uimodules/form_textinput.html", model=model, attribute=attribute, value="")


class FormTextArea(tornado.web.UIModule):
    """
        Renders a nice html text area

        Shows the specified model.attribute as selector.
        Default is _id (Which is probably something you want to change ;)
    """

    def render(self, model=None, attribute="_id"):
        return self.render_string(
            "uimodules/form_textarea.html", model=model, attribute=attribute, value="")

class FormFileSelect(tornado.web.UIModule):
    """
        Renders a nice html Files selector

        Shows the specified model.attribute as selector.
        Default is _id (Which is probably something you want to change ;)
    """

    def render(self, model=None, attribute="_id"):
        return self.render_string(
            "uimodules/form_fileselect.html", model=model, attribute=attribute, value="")

class FormDatePicker(tornado.web.UIModule):
    """
        Renders a nice html Date picker

        Shows the specified model.attribute as selector.
        Default is powlib.gettime(_id) (Which is probably something you want to change ;)
    """

    def render(self, model=None, attribute="_id"):
        return self.render_string(
            "uimodules/form_datepicker.html", model=model, attribute=attribute, value="")

class FormCheckBox(tornado.web.UIModule):
    """
        Renders a nice html checkbox

        Shows the specified model.attribute as selector.
        Default is powlib.gettime(_id) (Which is probably something you want to change ;)
    """

    def render(self, model=None, attribute="_id"):
        return self.render_string(
            "uimodules/form_checkbox.html", model=model, attribute=attribute, value="")