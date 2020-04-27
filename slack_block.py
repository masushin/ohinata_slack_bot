import json
import slack


"""
Payload
"""



"""
View
"""


"""
Composition Object
"""


class Object:
    def __init__(self):
        pass

    def getPayload(self):
        return {}


class ObjectText(Object):
    def __init__(self, type: str, text: str, emoji: bool = True,
                 verbatim: bool = False):
        if type == "plain_text" or type == "mrkdwn":
            self.type = type
        else:
            return None
        self.text = text
        self.emoji = emoji
        self.verbatim = verbatim

    def getPayload(self):
        payload = super().getPayload()
        payload['type'] = self.type
        payload['text'] = self.text
        #payload['emoji'] = self.emoji
        # payload['verbatim'] = self.verbatim
        return payload


class ObjectPlainText(ObjectText):
    def __init__(self, text: str, emoji: bool = True):
        super().__init__("plain_text", text, emoji, False)


class ObjectMrkdwnText(ObjectText):
    def __init__(self, text: str, verbatim: bool = False):
        super().__init__("mrkdwn", text, True, verbatim)


class ObjectConfirmationDialog(Object):
    def __init__(self, title: ObjectPlainText, text: ObjectPlainText,
                 confirm: ObjectPlainText, deny: ObjectPlainText):
        super().__init__()
        self.type = "_object_confirmation_dialog"
        self.title = title
        self.text = text
        self.confirm = confirm
        self.deny = deny

    def getPayload(self):
        payload = super().getPayload()
        payload['title'] = self.title.getPayload()
        payload['text'] = self.text.getPayload()
        payload['confirm'] = self.confirm.getPayload()
        payload['deny'] = self.deny.getPayload()
        return payload


class ObjectOption(Object):
    def __init__(self, text: ObjectPlainText, value: str,
                 description: ObjectPlainText = None, url: str = None):
        super().__init__()
        self.type = "_object_option"
        self.text = text
        self.value = value
        self.description = description
        self.url = url

    def getPayload(self):
        payload = super().getPayload()
        payload['text'] = self.text.getPayload()
        payload['value'] = self.value
        if self.description is not None:
            payload['description'] = self.description.getPayload()
        if self.url is not None:
            payload['url'] = self.url
        return payload


class ObjectOptionGroup(Object):
    def __init__(self, label: ObjectPlainText, options: [ObjectOption]):
        super().__init__()
        self.type = "_object_option_group"
        self.label = label
        self.options = options

    def getPayload(self):
        payload = super().getPayload()
        payload['label'] = self.label.getPayload()
        payload['options'] = []
        for option in self.options:
            payload['option'].append(option.getPayload())
        return payload


"""
Block Elements
"""


class Element:
    def __init__(self, type: str):
        self.type = type

    def getPayload(self):
        payload = {}
        payload['type'] = self.type
        return payload


class ElementButton(Element):
    def __init__(self, text: ObjectText, action_id: str, url: str = None,
                 value: str = None, style: str = None,
                 confirm: ObjectConfirmationDialog = None):
        super().__init__("button")
        self.text = text
        self.action_id = action_id
        self.url = url
        self.value = value
        self.style = style
        self.confirm = confirm

    def getPayload(self):
        payload = super().getPayload()
        payload['text'] = self.text.getPayload()
        payload['action_id'] = self.action_id
        if self.url is not None:
            payload['url'] = self.url
        if self.value is not None:
            payload['value'] = self.value
        if self.style is not None:
            payload['style'] = self.style
        if self.confirm is not None:
            payload['confirm'] = self.confirm.getPayload()
        return payload


class ElementCheckbox(Element):
    def __init__(self, action_id: str, options: [ObjectOption],
                 initial_options: [ObjectOption] = None,
                 confirm: ObjectConfirmationDialog = None):
        super().__init__("checkboxes")
        self.action_id = action_id
        self.options = options
        self.initial_options = initial_options
        self.confirm = confirm

    def getPayload(self):
        payload = super().getPayload()
        payload['action_id'] = self.action_id
        if self.options is not None:
            payload['options'] = []
            for option in self.options:
                payload['options'].append(option.getPayload())
        if self.initial_options is not None:
            payload['initial_options'] = []
            for initial_option in self.initial_options:
                payload['initial_options'].append(initial_option.getPayload())
        if self.confirm is not None:
            payload['confirm'] = self.confirm.getPayload()
        return payload


class ElementDatepicker(Element):
    def __init__(self, action_id: str, placeholder: ObjectText = None,
                 initial_date: str = None,
                 confirm: ObjectConfirmationDialog = None):
        super().__init__("datepicker")
        self.action_id = action_id
        self.placeholder = placeholder
        self.initial_date = initial_date
        self.confirm = confirm

    def getPayload(self):
        payload = super().getPayload()
        payload['action_id'] = self.action_id
        if self.placeholder is not None:
            payload['placeholder'] = self.placeholder.getPayload()
        if self.initial_date is not None:
            payload['initial_date'] = self.initial_date
        if self.confirm is not None:
            payload['confirm'] = self.confirm.getPayload()
        return payload


class ElementImage(Element):
    def __init__(self, image_url: str, alt_text: str):
        super().__init__("image")
        self.image_url = image_url
        self.alt_text = alt_text

    def getPayload(self):
        payload = super().getPayload()
        payload['image_url'] = self.image_url
        payload['alt_text'] = self.alt_text
        return payload


class ElementMultiselectWithStatic(Element):
    """
    not implemented
    """

    def __init__(self):
        super().__init__()
        pass


class ElementMultiselectWithExternalData(Element):
    """
    not implemented
    """

    def __init__(self):
        super().__init__()
        pass


class ElementMultiselectWithUserList(Element):
    """
    not implemented
    """

    def __init__(self):
        super().__init__()
        pass


class ElementMultiselectWithConversationsList(Element):
    """
    not implemented
    """

    def __init__(self):
        super().__init__()
        pass


class ElementMultiselectWithChannelsList(Element):
    """
    not implemented
    """

    def __init__(self):
        super().__init__()
        pass


class ElementOverflow(Element):
    """
    not implemented
    """

    def __init__(self):
        super().__init__()
        pass


class ElementPlainTextInput(Element):
    def __init__(self, action_id: str, placeholder: ObjectText = None,
                 initial_value: str = None, multiline: bool = False,
                 min_length: int = None, max_length: int = None):
        super().__init__("plain_text_input")
        self.action_id = action_id
        self.placeholder = placeholder
        self.initial_value = initial_value
        self.multiline = multiline
        self.min_length = min_length
        self.max_length = max_length

    def getPayload(self):
        payload = super().getPayload()
        payload['action_id'] = self.action_id
        if self.placeholder is not None:
            payload['placeholder'] = self.placeholder.getPayload()
        if self.initial_value is not None:
            payload['initial_value'] = self.initial_value
        payload['multiline'] = self.multiline
        if self.min_length is not None:
            payload['min_length'] = self.min_length
        if self.max_length is not None:
            payload['max_length'] = self.max_length
        return payload


class ElementRadioButton(Element):
    """
    not implemented
    """

    def __init__(self):
        super().__init__()
        pass


class ElementSelectWithStatic(Element):
    def __init__(self, placeholder: ObjectText, action_id: str,
                 options: [ObjectOption],
                 option_groups: [ObjectOptionGroup] = None,
                 initial_option: ObjectOption = None,
                 confirm: ObjectConfirmationDialog = None):
        super().__init__("static_select")
        self.placeholder = placeholder
        self.action_id = action_id
        self.options = options
        self.option_groups = option_groups
        self.initial_option = initial_option
        self.confirm = confirm

    def getPayload(self):
        payload = super().getPayload()
        payload['action_id'] = self.action_id
        payload['options'] = []
        for option in self.options:
            payload['options'].append(option.getPayload())
        if self.option_groups is not None:
            payload['option_groups'] = []
            for option_group in self.option_groups:
                payload['option_groups'].append(option_group.getPayload())
        if self.initial_option is not None:
            payload['initial_option'] = self.initial_option.getPayload()
        if self.confirm is not None:
            payload['confirm'] = self.confirm.getPayload()
        return payload


class ElementSelectWithExternalData(Element):
    """
    not implemented
    """

    def __init__(self):
        super().__init__()
        pass


class ElementSelectWithUserList(Element):
    """
    not implemented
    """

    def __init__(self):
        super().__init__()
        pass


class ElementSelectWithConversationsList(Element):
    """
    not implemented
    """

    def __init__(self):
        super().__init__()
        pass


class ElementSelectWithChannelsList(Element):
    """
    not implemented
    """

    def __init__(self):
        super().__init__()
        pass


"""
Blocks
"""


class Block:
    def __init__(self, type: str, block_id: str):
        self.type = type
        self.block_id = None

    def getPayload(self):
        payload = {}
        payload['type'] = self.type
        if self.block_id is not None:
            payload['block_id'] = self.block_id
        return payload


class BlockSection(Block):
    def __init__(self, text: ObjectText, block_id: str = None,
                 fields: [ObjectText] = None, accessory: Element = None):
        super().__init__("section", block_id)
        self.text = text
        self.fields = fields
        self.accessory = accessory

    def getPayload(self):
        payload = super().getPayload()
        payload['text'] = self.text.getPayload()
        if self.fields is not None:
            payload['fields'] = []
            for field in self.fields:
                payload['fields'].append(field.getPayload())
        if self.accessory is not None:
            payload['accessory'] = self.accessory.getPayload()
        return payload


class BlockDivider(Block):
    def __init__(self, block_id: str = None):
        super().__init__("divider", block_id)

    def getPayload(self):
        payload = super().getPayload()
        return payload


class BlockImage(Block):
    def __init__(self, image_url: str, alt_text: str,
                 title: ObjectText = None, block_id: str = None):
        super().__init__("image", block_id)
        self.image_url = image_url
        self.alt_text = alt_text
        self.title = title

    def getPayload(self):
        payload = super().getPayload()
        payload['image_url'] = self.image_url
        payload['alt_text'] = self.alt_text
        payload['title'] = self.text.getPayload()
        return payload


class BlockAction(Block):
    def __init__(self, elements: [Element], block_id: str = None):
        super().__init__("actions", block_id)
        self.elements = elements

    def getPayload(self):
        payload = super().getPayload()
        if self.elements is not None:
            payload['elements'] = []
            for element in self.elements:
                payload['elements'].append(element.getPayload())
        return payload


class BlockContext(Block):
    def __init__(self, elements: [Element], block_id: str = None):
        super().__init__("context", block_id)
        self.elements = elements

    def getPayload(self):
        payload = super().getPayload()
        if self.elements is not None:
            payload['elements'] = []
            for element in self.elements:
                payload['elements'].append(element.getPayload())
        return payload


class BlockInput(Block):
    def __init__(self, label: ObjectText, element: Element,
                 block_id: str = None, hint: ObjectText = None,
                 optional: bool = False):
        super().__init__("input", block_id)
        self.label = label
        self.element = element
        self.hint = hint
        self.optional = optional

    def getPayload(self):
        payload = super().getPayload()
        payload['label'] = self.label.getPayload()
        payload['element'] = self.element.getPayload()
        if self.hint is not None:
            payload['hint'] = self.hint.getPayload()
        payload['optional'] = self.optional
        return payload


class BlockFile(Block):
    def __init__(self, external_id: str, source: str, block_id: str = None):
        super().__init__("file", block_id)
        self.external_id = external_id
        self.source = source


"""
Block types
"""


class Surface:
    def __init__(self, type=None):
        self.type = type
        self.blocks = []
        self.payload = {}

    def addBlocks(self, blocks: [Block]):
        for block in blocks:
            self.blocks.append(block)

    def getPayload(self):
        if self.type is not None:
            self.payload['type'] = self.type
        self.payload['blocks'] = []
        for block in self.blocks:
            self.payload['blocks'].append(block.getPayload())
        return self.payload


class Message(Surface):
    def __init__(self):
        super().__init__()

    def getPayload(self):
        return super().getPayload()

class Home(Surface):
    def __init__(self):
        super().__init__("home")

    def getPayload(self):
        return super().getPayload()


class Modal(Surface):
    def __init__(self, title: ObjectText, callback_id: str = None,
                 submit: ObjectText = None, close: ObjectText = None,
                 private_metadata: dict = {}, clear_on_close: bool = False,
                 notify_on_close: bool = False, external_id: str = None):
        super().__init__("modal")
        self.title = title
        self.callback_id = callback_id
        self.submit = submit
        self.close = close
        self.private_metadata = private_metadata
        self.clear_on_close = clear_on_close
        self.notify_on_close = notify_on_close
        self.external_id = external_id

    def getPayload(self):
        payload = super().getPayload()
        payload['title'] = self.title.getPayload()
        if self.callback_id is not None:
            payload['callback_id'] = self.callback_id
        if self.submit is not None:
            payload['submit'] = self.submit.getPayload()
        if self.close is not None:
            payload['close'] = self.close.getPayload()
        if self.private_metadata is not None:
            payload['private_metadata'] = str(json.dumps(self.private_metadata))
        payload['clear_on_close'] = self.clear_on_close
        payload['notify_on_close'] = self.notify_on_close
        if self.external_id is not None:
            payload['external_id'] = self.external_id
        return payload
