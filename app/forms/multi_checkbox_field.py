from wtforms import SelectMultipleField
from wtforms.widgets import CheckboxInput, ListWidget

class Multi_Checkbox_Field(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    open_widget = CheckboxInput()