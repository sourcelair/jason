from distutils.core import setup

setup(name='Jason',
      version='0.1',
      description='Thin ORM-like layer for REST services',
      author='Paris Kasidiaris',
      author_email='pariskasidiaris@gmail.com',
      packages=['jason'],
      package_dir={
        'jason': 'jason'
      })
