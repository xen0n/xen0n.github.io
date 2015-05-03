# xen0n blog

Nothing to see here for now; I'll update when I have time.


## License

* Blog content: cc-by-nc-sa 4.0
* Static site/template generator: 3-clause BSD license


## Build

```sh
# you need bower and gulp to generate the static templates
cd _src
npm install --dev
bower install

# prepare the generator
# create the virtualenv with a Python 3.4+ (only tested on that version)
cd ../_generator
pyvenv-3.4 venv
./venv/bin/pip install -r requirements.txt

# generate the site
cd ..
make templates && make
```


<!-- vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8: -->
