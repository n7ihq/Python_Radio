set comport=%1
esptool --port %comport% erase_flash
esptool.exe --port %comport% write_flash -fm dio -fs 16MB 0 firmware.bin
send_files %comport%
putty -load %comport%
