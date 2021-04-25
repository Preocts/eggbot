# Module Setup

Outline for a basic module boiler-plate.  Anything following this pattern that is placed in the `./modules` directory will be auto-loaded.

## Requirements

1. `.py` file placed in the `./modules` directory
1. Prefix the module filename with `module_`
1. Global `str` constant named `AUTO_LOAD` assigned the name of the class to load
1. Ensure class has methods for the desired hooks
   - on_ready()
   - on_disconnect()
   - on_member_join(member: Discord.Member)
   - on_message(message: Discord.Message)

---

`module_sample.py`
```python
""" Some good docstrings here """
from discord import Member
from discord import Message
...

AUTO_LOAD: str = "SampleModule"

class SampleModule:
    """ My sample class that does things with messages """

    def __init__(self) -> None:
        """ Some code here """

    def on_message(self, message: Message) -> None:
        """ On message hook """
        ...

    def on_member_join(self, member: Member) -> None:
        """ On member hook """
        ...

    def on_ready(self) -> None:
        """ On Ready hook """
        ...

    def on_disconnect(self) -> None:
        """ On Disconnect hook """
        ...
```
