Bunshin
=======

Documentation
-------------
Please see our ATC'17 [paper](https://sslab.gtisc.gatech.edu/assets/papers/2017/xu:bunshin.pdf)

Pop-up Vagrant
--------------
```
cd bunshin
vagrant up && vagrant ssh
cd /vagrant
```

Build Bunshin
-------------
```
cd template && ./gen.py
./mvee build
```

Install Bunshin kernel module
-----------------------------
```
./mvee launch
```

Try out Bunshin (2 variant)
---------------------------
```
./mvee buddy ls
```

A more generic way to run
-------------------------
```
./mvee run <number of variants> <path-to-v1> ... <path-to-vN> <args>
```

Remove Bunshin kernel module
----------------------------
```
./mvee finish
```
