import importlib

try:
    module = importlib.import_module('Controller.1')
    module.main('xxxx')
    print('ok')
except Exception as e:
    print(e)

# import importlib.util
#
# module_spec = importlib.util.find_spec('Controller.1')
# if module_spec:
#     print('found')
#     module = importlib.util.module_from_spec(module_spec)
#     module_spec.loader.exec_module(module)
# else:
#     print('not found.')
