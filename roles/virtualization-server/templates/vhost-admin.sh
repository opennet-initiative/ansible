#!/bin/sh
#
# {{ ansible_managed }}
#

set -eu

LVM_GROUP="{{ virtualization_lvm_group }}"
RAW_IMAGE_PATH="{{ virtualization_storage_path }}"
VIRT_BASE_CONFIG=/etc/libvirt/qemu/_template.xml
USE_LVM='{% if virtualization_storage == "lvm" %}true{% else %}false{% endif %}'
MOUNTPOINT=$(mktemp -d)
SUB_MOUNTS="dev proc sys"
DISTRIBUTION=${DISTRIBUTION:-stretch}
APT_URL="http://ftp.de.debian.org/debian"
DEBOOTSTRAP_BIN=${DEBOOTSTRAP_BIN:-debootstrap}
# Zu installierende oder wegzulassende Pakete (komma-separiert)
# python-apt: fuer ansible
# olsrd: Mesh-Routing
# acpi-support-base: sanfte Abschaltung via "virsh shutdown"
# irqbalance: unnoetig fuer einzel-CPU-Systeme
PACKAGES_INCLUDE="openssh-server,python-apt,olsrd,acpi-support-base,linux-image-amd64,grub-pc"
PACKAGES_EXCLUDE="irqbalance"
AP_FIRMWARE_MAP="\
	0.4.1	http://downloads.opennet-initiative.de/openwrt/stable/0.4.1/x86/openwrt-x86-generic-combined-squashfs.img
	0.4.4	http://downloads.opennet-initiative.de/openwrt/stable/0.4.4/x86/openwrt-x86-generic-combined-squashfs.img
	0.4.5	http://downloads.opennet-initiative.de/openwrt/stable/0.4.5/x86/openwrt-x86-generic-combined-squashfs.img
	0.5.0	http://downloads.opennet-initiative.de/openwrt/stable/0.5.0/x86/openwrt-x86-generic-combined-squashfs.img.gz
	0.5.1	http://downloads.opennet-initiative.de/openwrt/stable/0.5.1/x86/openwrt-x86-generic-combined-squashfs.img.gz
	0.5.2	http://downloads.opennet-initiative.de/openwrt/stable/0.5.2/x86/openwrt-0.5.2-1697-x86-generic-combined-squashfs.img.gz
	0.5.3	http://downloads.opennet-initiative.de/openwrt/stable/0.5.3/x86/openwrt-0.5.3-1992-x86-generic-combined-squashfs.img.gz
	latest	http://downloads.opennet-initiative.de/openwrt/stable/0.5.3/x86/openwrt-0.5.3-1992-x86-generic-combined-squashfs.img.gz
"


die() {
	echo "$2" >&2
	return "$1"
}


create_volume() {
	local host="$1"
	local vol_type="$2"
	local size="$3"
	if "$USE_LVM"; then
		local vol_name="${host}-${vol_type}"
		lvs | grep -q "^ *$vol_name " && die 3 "Volume '$vol_name' exists already - aborting ..."
		lvcreate --yes -n "$vol_name" -L "$size" "$LVM_GROUP"
	else
		local image
		image=$(get_volume_path "$host" "$vol_type")
		mkdir -p "$(dirname "$image")"
		[ -e "$image" ] && die 3 "Volume image ($image) exists already - aborting ..."
		dd if=/dev/zero of="$image" bs="$size" seek=1 count=0 status=none
	fi
}


remove_volume() {
	local host="$1"
	local vol_type="$2"
	local path
	# eventuell haengt das Device von einem frueheren Lauf noch an einem anderen Mountpoint
	path=$(get_volume_path "$host" "$vol_type")
	umount "$path" 2>/dev/null || true
	if "$USE_LVM"; then
		lvremove -f "$LVM_GROUP/${host}-${vol_type}"
	else
		rm -f "$(get_volume_path "$host" "$vol_type")"
		rmdir --ignore-fail-on-non-empty "$RAW_IMAGE_PATH/$host"
	fi
}


get_volume_path() {
	local host="$1"
	local vol_type="$2"
	if "$USE_LVM"; then
		echo "/dev/$LVM_GROUP/${host}-${vol_type}"
	else
		echo "$RAW_IMAGE_PATH/$host/${vol_type}.img"
	fi
}


create_host_volumes() {
	local host="$1"
	local maker
	local size
	local path
	echo "	mkfs.ext4	root	3G
		mkswap		swap	512M" \
	 | while read -r maker vol_type size; do
		create_volume "$host" "$vol_type" "$size"
		path=$(get_volume_path "$host" "$vol_type")
		wipefs -a "$path"
		"$maker" "$path"
	 done
}


create_access_point_volume() {
	local host="$1"
	create_volume "$host" "root" "64M" >/dev/null
}


mount_system() {
	local host="$1"
	local dev
	local path
	dev=$(get_volume_path "$host" "root")
	mkdir -p "$MOUNTPOINT"
	mountpoint -q "$MOUNTPOINT" && die 7 "The mountpoint '$MOUNTPOINT' is already in use - aborting ..."
	mount "$dev" "$MOUNTPOINT" || die 9 "Failed to mount base filesystem '$dev' - aborting ..."
	for path in $SUB_MOUNTS; do
		[ -d "$MOUNTPOINT/$path" ] || continue
		mount --bind "/$path" "$MOUNTPOINT/$path"
	done
}


umount_system() {
	local path
	for path in $SUB_MOUNTS; do
		mountpoint -q "$MOUNTPOINT/$path" || continue
		umount "$MOUNTPOINT/$path"
	done
	mountpoint -q "$MOUNTPOINT" && umount "$MOUNTPOINT"
	rmdir "$MOUNTPOINT" 2>/dev/null || true
	return 0
}


create_debian_system() {
	local host="$1"
	local ip="$2"
	mount_system "$host"
	which "$DEBOOTSTRAP_BIN" >/dev/null || die 11 "Missing requirement: $DEBOOTSTRAP_BIN"
	echo "$DISTRIBUTION" "$MOUNTPOINT" "$APT_URL"
	"$DEBOOTSTRAP_BIN" --include "$PACKAGES_INCLUDE" --exclude "$PACKAGES_EXCLUDE" "$DISTRIBUTION" "$MOUNTPOINT" "$APT_URL" || {
		umount_system
		die 8 "Debootstrap failed - aborting ..."
	}
	# starting with "stretch" the new kernel-based naming scheme is required
	# We override the default names with predictable ethX names.
	mkdir -p "$MOUNTPOINT/etc/udev/rules.d"
	virsh dumpxml "$host" \
			| grep -w "mac address" \
			| cut -f 2 -d "'" \
			| nl --starting-line-number=0 \
			| while read -r id mac; do
		printf 'SUBSYSTEM=="net", ACTION=="add", DRIVERS=="?*", ATTR{address}=="%s", NAME="eth%d"\n' "$mac" "$id"
	done >"$MOUNTPOINT/etc/udev/rules.d/70-persistent-net.rules"
	cat - >"$MOUNTPOINT/etc/network/interfaces" <<-EOF
		auto lo
		iface lo inet loopback

		# mesh interface
		allow-hotplug eth0
		iface eth0 inet static
			address $ip
			netmask 255.255.0.0

		# internet uplink
		allow-hotplug eth1
		iface eth1 inet dhcp
EOF
	cat - >"$MOUNTPOINT/etc/fstab" <<-EOF
		/dev/sda	/	auto	noatime	0	1
		/dev/sdb	none	swap	sw	0	0
EOF
	# debootstrap erzeugt keine security-Eintraege
	grep -q security "$MOUNTPOINT/etc/apt/sources.list" \
		|| echo "deb http://security.debian.org/ $DISTRIBUTION/updates main" >>"$MOUNTPOINT/etc/apt/sources.list"
	umount_system
}


create_access_point_image() {
	local host="$1"
	local image_url="$2"
	local blockdev
	local tmpfile
	local exitcode
	blockdev=$(get_volume_path "$host" "root")
	tmpfile=$(mktemp)
	# Abbruch, falls curl fehlschlaegt
	if ! curl --silent --show-error --fail --out "$tmpfile" "$image_url"; then
		echo >&2 "Failed to download '$image_url'"
		exitcode=1
	elif ! gunzip --stdout --force <"$tmpfile" | dd "of=$blockdev" status=none conv=notrunc; then
		echo >&2 "Failed to write decompressed image to '$blockdev'"
		exitcode=1
	else
		exitcode=0
	fi
	rm -f "$tmpfile"
	return "$exitcode"
}


wait_for_ap() {
	local ttydev
	ttydev=$(virsh --quiet ttyconsole "$host")
	while ! timeout 1 cat "$ttydev" | grep -q "^/"; do
		sleep 1
		echo "pwd" >"$ttydev"
	done
}


is_ap_running() {
	local host="$1"
	local status
	status=$(virsh list | awk '{ if ($1 == "'"$host"'") print $2; }')
	[ "$status" = "running" ] && return 0
	return 1
}


configure_access_point_networking() {
	local host="$1"
	local ip="$2"
	virsh start "$host"
	# das Booten auf ryoko dauert ca. 12 Sekunden, bei aqua dauert es noch laenger
	echo "Warte auf Booten des Access-Points ..."
	sleep 10
	local ttydev
	ttydev=$(virsh --quiet ttyconsole "$host")
	# sende Eingaben an die Konsole - sie werden erst durch "virsh console" wirksam
	# zuerst eine Leerzeile (bzw. "true") um die Konsole zu oeffnen
	wait_for_ap
	echo "Bootvorgang abgeschlossen"
	sed 's/^[[:space:]]*//' >"$ttydev" <<EOF1
		cat >"/etc/uci-defaults/99-virt-init" <<EOF2
			#!/bin/sh
			true
			# eth0 aus dem LAN-Netzwerk entfernen
			uci set network.lan.ifname=none
			# fruezeitig Erstinitialisierungen triggern
			uci commit
			/etc/init.d/network restart
			sleep 3
			uci set network.lan.ifname=none
			# eth0 mit der selbstgewaehlten mesh-IP konfigurieren
			uci set network.on_eth_0.ifname=eth0
			uci set network.on_eth_0.proto=static
			uci set network.on_eth_0.ipaddr="$ip"
			uci commit
			reload_config
			on-function set_opennet_id "${ip#192.168.}"
			reload_config
		EOF2
		chmod +x "/etc/uci-defaults/99-virt-init"
		/etc/uci-defaults/99-virt-init && rm /etc/uci-defaults/99-virt-init
EOF1
	# nur bei existierendem Rueckgabekanal werden die obigen Eingaben verarbeitet
	timeout 10 cat "$ttydev" >/dev/null 2>&1 || true
	echo "AP-Konfiguration abgeschlossen"
}


configure_access_point_host_definition() {
	local host="$1"
	local libvirt_file="/etc/libvirt/qemu/${host}.xml"
	local key
	# externen Boot-Kernel aus der Konfiguration entfernen
	for key in initrd kernel cmdline; do
		sed -i "/<$key>.*<\/$key>$/d" "$libvirt_file"
	done
	# zweites Blockdevice entferne
	sed -i -n '0,/<\/disk>/p; /<controller/,$p' "$libvirt_file"
	virsh --quiet define "$libvirt_file" >/dev/null
}


get_network_mac() {
	# beware: some prefixes are multicast ones - thus we just pick a good one hard-coded
	# return a number of random hexadecimal characters
	shuf -i 0-255 -n 3 | xargs printf "00:16:3e:%02x:%02x:%02x"
}


create_virt_config() {
	local host="$1"
	local memory="$2"
	local target_file="/etc/libvirt/qemu/${host}.xml"
	local item
	which "uuidgen" >/dev/null || die 5 "Missing requirement: uuidgen"
	[ -e "$target_file" ] && die 4 "Host config file '$target_file' exists already - aborting ..."
	cp "$VIRT_BASE_CONFIG" "$target_file"
	sed -i "s/__NAME__/$host/g" "$target_file"
	sed -i "s/__MEMORY__/$memory/g" "$target_file"
	item=$(uuidgen)
	sed -i "s/__UUID__/$item/g" "$target_file"
	item=$(get_network_mac)
	sed -i "s/__MAC1__/$item/g" "$target_file"
	item=$(get_network_mac)
	sed -i "s/__MAC2__/$item/g" "$target_file"
	item=$(get_network_mac)
	sed -i "s/__MAC3__/$item/g" "$target_file"
	virsh --quiet define "$target_file" >/dev/null
}


run_in_chroot() {
	chroot "$MOUNTPOINT" "$@" || {
		umount_system
		die 12 "Failed to run command in chroot: $*"
	}
	return 0
}


prepare_system() {
	local host="$1"
	local root_path
	root_path=$(get_volume_path "$host" "root")
	mount_system "$host"
	echo "$host" >"$MOUNTPOINT/etc/hostname"
	echo "127.0.0.1 $host" >> "$MOUNTPOINT/etc/hosts"
	cat - >"$MOUNTPOINT/etc/resolv.conf" <<-EOF
		search on
		nameserver 192.168.0.246
		nameserver 192.168.0.247
		nameserver 192.168.0.248
	EOF
	# import the server ssh key
	run_in_chroot mkdir -p /root/.ssh
	{
		# der root-Nutzer des Virtualisierungsservers hat ohnehin die volle Kontrolle
		# Wir kopieren also den Schluessel fuer vereinfachte Problembehebung.
		cat /root/.ssh/id_rsa.pub
		# Zusaetzlich kopieren wir den ssh-Schluessel des aktuell angemeldeten Nutzers
		# (sofern er sich spontan ermitteln laesst).
		if [ -n "${SSH_USER:-}" ]; then
			grep -wF "environment=\"SSH_USER=$SSH_USER\"" .ssh/authorized_keys
		fi
	} >"$MOUNTPOINT/root/.ssh/authorized_keys"
	# olsrd-Interface konfigurieren und Daemon aktivieren
	sed -i 's/^Interface.*$/Interface "eth0"/' "$MOUNTPOINT/etc/olsrd/olsrd.conf"
	sed -i 's/^#START_OLSRD=.*$/START_OLSRD="YES"/' "$MOUNTPOINT/etc/default/olsrd"
	# grub installieren (wirft mit jessie eine Fehlermeldung)
	if [ "$DISTRIBUTION" != "jessie" ]; then
		# vermeide diskfilter-Fehlermeldung wegen LVM (bezueglich des root-Device des Wirts)
		echo "(hd0) $root_path" >"$MOUNTPOINT/boot/grub/device.map"
		run_in_chroot update-grub
		run_in_chroot grub-install --force "$root_path"
	fi
	umount_system
}


get_firmware_versions() {
	echo "$AP_FIRMWARE_MAP" | awk '{print $1}' | grep -v "^$"
}


get_url_of_firmware_version() {
	local version="$1"
	echo "$AP_FIRMWARE_MAP" | awk '{ if ($1 == "'"$version"'") print $2 }'
}


ACTION=help
[ $# -gt 0 ] && ACTION="$1" && shift

case "$ACTION" in
	create-debian)
		[ "$#" -eq 2 ] || die 3 "Not enough arguments: HOSTNAME IP"
		host="$1"
		ip="$2"
		echo "$host" | grep -q "^[a-z][a-z0-9_-]*$" || die 1 "Hostname contains invalid characters: $host"
		echo "$ip" | grep -q "^\([0-9]\{1,3\}\.\)\{3\}[0-9]\{1,3\}$" || die 2 "invalid IP given: $ip"
		create_host_volumes "$host"
		create_virt_config "$host" "$((512*1024))"
		create_debian_system "$host" "$ip"
		prepare_system "$host"
		;;
	create-ap)
		[ "$#" -eq 3 ] || die 3 "Not enough arguments: HOSTNAME IP [IMAGE_URL]"
		host="$1"
		ip="$2"
		image_url=$(get_url_of_firmware_version "${3:-latest}")
		[ -z "$image_url" ] && image_url="$3"
		echo "$host" | grep -q "^[a-z][a-z0-9_-]*$" || die 1 "Hostname contains invalid characters: $host"
		echo "$ip" | grep -q "^\([0-9]\{1,3\}\.\)\{3\}[0-9]\{1,3\}$" || die 2 "invalid IP given: $ip"
		create_access_point_volume "$host"
		create_virt_config "$host" "$((128*1024))"
		create_access_point_image "$host" "$image_url"
		configure_access_point_host_definition "$host"
		configure_access_point_networking "$host" "$ip"
		;;
	remove)
		host="$1"
		echo "$host" | grep -q "^[a-z][a-z0-9_-]*$" || die 1 "Hostname contains invalid characters: $host"
		(
			set +e
			virsh --quiet destroy "$host" 2>/dev/null
			umount_system
			remove_volume "$host" "root"
			remove_volume "$host" "swap" 2>/dev/null
			virsh undefine "$host"
			rm -f "/etc/libvirt/qemu/auto/${host}.xml"
			rm -f "/etc/libvirt/qemu/${host}.xml"
			set -e
			true
		);# 2>/dev/null
		;;
	list)
		virsh --quiet list --all | awk '{print $2}' | sort -n
		;;
	list-ap-firmware-versions)
		get_firmware_versions
		;;
	help|--help )
		echo "Usage:"
		echo "	create-debian HOSTNAME IP"
		echo "	create-ap HOSTNAME IP IMAGE_URL_OR_TEMPLATE"
		echo "	remove HOSTNAME"
		echo "	list"
		echo "	list-ap-firmware-versions"
		echo
		;;
	*)
		"$0" help >&2
		exit 1
		;;
esac

# entferne das temp-Verzeichnis
umount_system
exit 0
