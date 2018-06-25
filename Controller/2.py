import importlib
import importlib.util
import importlib.machinery


# try:
#     module = importlib.import_module('Controller.1')
#     module.main('xxxx')
#     print('ok')
# except Exception as e:
#     print(e)

# import importlib.util
#
# module_spec = importlib.util.find_spec('Controller.1')
# if module_spec:
#     print('found')
#     module = importlib.util.module_from_spec(module_spec)
#     module_spec.loader.exec_module(module)
# else:
#     print('not found.')

# def test():
#     import sys
#
#     # For illustrative purposes.
#     # import tokenize
#     # file_path = tokenize.__file__
#     # module_name = tokenize.__name__
#     file_path = ''
#     module_name = ''
#
#     spec = importlib.util.spec_from_file_location(module_name, file_path)
#     module = importlib.util.module_from_spec(spec)
#     spec.loader.exec_module(module)

# try:
#     module_name = 'Controller.script_toutiao_NoxCon'
#     # self._log('<<info>> run_script reload:', module_name)
#     # import importlib.util
#     #
#     module = importlib.import_module(module_name)
#     # module = importlib.reload(module_name)
#     module.main('nox-1')
#     # module_name = ''
#     # file_path = ''
#     # importlib.util.spec_from_file_location(module_name, file_path)
# except Exception as e:
#     print(e)


