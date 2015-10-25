from distutils.core import setup

setup(name='Jason',
      version='0.2',
      description='Thin Django-like object mapper for REST services',
      author='Paris Kasidiaris',
      author_email='pariskasidiaris@gmail.com',
      packages=['jason'],
      package_dir={
        'jason': 'jason'
      })
