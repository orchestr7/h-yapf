# -*- coding: utf-8 -*-

try:
    with open('/some/file') as f:
        pass
except RuntimeError:
    pass
except:
    pass
