project('cyipopt', 'cython')
ipopt = dependency('ipopt')
numpy = dependency('numpy')
py = import('python').find_installation()
py.extension_module(
  'ipopt_wrapper',
  'src/cyipopt/cython/ipopt_wrapper.pyx',
  dependencies: [ipopt, numpy],
  install: true,
  subdir: 'cyipopt',
  )
py.install_sources([
  'src/cyipopt/exceptions.py',
  'src/cyipopt/__init__.py',
  'src/cyipopt/ipopt_wrapper.py',
  'src/cyipopt/scipy_interface.py',
  'src/cyipopt/utils.py',
  'src/cyipopt/version.py',
  ],
  subdir: 'cyipopt',
  pure: false,
  )
py.install_sources([
  'src/ipopt/__init__.py',
  ],
  subdir: 'ipopt',
  pure: false,
  )
