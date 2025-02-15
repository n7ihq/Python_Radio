set comport=%1
ampy -p %comport% put webrepl_cfg.py
ampy -p %comport% put boot.py
ampy -p %comport% put the_code.py
ampy -p %comport% put morse.py
ampy -p %comport% put main.py
