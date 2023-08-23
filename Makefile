PREFIX := $(if $(PREFIX),$(PREFIX),"/usr/local")

install:
	mkdir -p /usr/local/lib/systemd/system
	install -m 644 systemd/tailscale-node-online@.target ${PREFIX}/lib/systemd/system/tailscale-node-online@.target
	install -m 644 systemd/tailscale-watcher.timer ${PREFIX}/lib/systemd/system/tailscale-watcher.timer
	install -m 644 systemd/tailscale-watcher.service ${PREFIX}/lib/systemd/system/tailscale-watcher.service
	install -m 755 tailscale-watcher.py ${PREFIX}/bin/tailscale-watcher

uninstall:
	rm -f ${PREFIX}/lib/systemd/system/tailscale-node-online@.target
	rm -f ${PREFIX}/lib/systemd/system/tailscale-watcher.timer
	rm -f ${PREFIX}/lib/systemd/system/tailscale-watcher.service
	rm -f ${PREFIX}/bin/tailscale-watcher
