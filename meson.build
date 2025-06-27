project('cyipopt', 'cython')
ipopt = dependency('ipopt')
numpy = dependency('numpy')
py = import('python').find_installation()
py.extension_module(
  'ipopt_wrapper',
  'cyipopt/cython/ipopt_wrapper.pyx',
  dependencies: [ipopt, numpy],
  install: true
)
