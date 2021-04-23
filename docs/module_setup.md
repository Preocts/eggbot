# Module Setup

***WIP***

## Requirements

1. Import EventType model
1. Global `str` constant named `AUTO_LOAD` assigned the name of the class to load
1. Name of module file with no file extension in `.configs/eggbotcore.json` under the `load_modules` key.
1. Ensure class has methods for the desired hooks
   - MESSAGE: `onmessage`

---

`sample_module.py`
```python
""" Some good docstrings here """
import foobar
from typing import List

from eggbot.models.eventtype import EventType

...

AUTO_LOAD: str = "SampleModule"

class SampleModule:
    """ My sample class that does things with messages """

    def __init__(self) -> None:
        """ Some code here """

    def onmessage(self, message) -> None:
        """ On message hook """
        ...

```
