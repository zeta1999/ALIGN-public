# Simple tutorial on packaging python using setuptools.

To run the test in a container:
````bash
tar cvf - . | docker run -i --rm --mount source=funniestVol,target=/vol ubuntu bash -c "cd /vol; tar xvf -"
docker run --rm --mount source=funniestVol,target=/vol -it with_python_protobuf bash -c "source /sympy/bin/activate; cd /vol; python setup.py develop; python setup.py test"
````
