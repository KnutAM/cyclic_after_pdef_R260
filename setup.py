from distutils.core import setup
import pathlib as pl

this_dir = pl.Path(__file__).parent
data_path = this_dir / 'data'
data_path_file = this_dir / 'cyclic_data' / 'data_path.py'
with open(data_path_file, 'w') as fid:
    fid.write('data_path = "{:s}"\n'.format(str(data_path.absolute())))

setup(name='cyclic_data',
      version='1.0',
      description='Analysis and plotting of cyclic data',
      author='Knut Andreas Meyer',
      author_email='knutam@gmail.com',
      url='https://cyclic-after-pdef-r260.readthedocs.io/en/latest/',
      packages=['cyclic_data', 
                'cyclic_data.hdf5_data',
                'cyclic_data.filter',
                'cyclic_data.plot',
                'cyclic_data.yield'],
     )
