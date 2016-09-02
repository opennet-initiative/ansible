#/bin/sh

set -eu

LVM_GROUP="lvm-$(hostname)"
VIRT_BASE_CONFIG=/etc/libvirt/qemu/_template.xml
MOUNTPOINT=/mnt/temp
DISTRIBUTION=${DISTRIBUTION:-jessie}
APT_URL="http://httpredir.debian.org/debian"
DOMAIN=on
# Zu installierende oder wegzulassende Pakete (komma-separiert)
# python-apt: fuer ansible
# olsrd: Mesh-Routing
# acpi-support-base: sanfte Abschaltung via "virsh shutdown"
# irqbalance: unnoetig fuer einzel-CPU-Systeme
PACKAGES_INCLUDE="openssh-server,python-apt,olsrd,acpi-support-base,linux-image-amd64,grub-pc"
PACKAGES_EXCLUDE="irqbalance"
AP_FIRMWARE_MAP="\
	0.4.1	http://downloads.on-i.de/openwrt/stable/0.4.1/x86/openwrt-x86-generic-combined-squashfs.img
	0.4.4	http://downloads.on-i.de/openwrt/stable/0.4.4/x86/openwrt-x86-generic-combined-squashfs.img
	0.4.5	http://downloads.on-i.de/openwrt/stable/0.4.5/x86/openwrt-x86-generic-combined-squashfs.img
	0.5.0	http://downloads.on-i.de/openwrt/stable/0.5.0/x86/openwrt-x86-generic-combined-squashfs.img.gz
	0.5.1	http://downloads.on-i.de/openwrt/stable/0.5.1/x86/openwrt-x86-generic-combined-squashfs.img.gz
	0.5.2	http://downloads.on-i.de/openwrt/stable/0.5.2/x86/openwrt-0.5.2-1697-x86-generic-combined-squashfs.img.gz
	latest	http://downloads.on-i.de/openwrt/stable/0.5.2/x86/openwrt-0.5.2-1697-x86-generic-combined-squashfs.img.gz
"


die()
{
        echo "$2" >&2
        exit $1
}


create_host_volumes() {
	local host="$1"
	local vol
	local maker
	local suffix
	local size
	echo "	mkfs.ext4	root	3G
		mkswap		swap	512M" \
	 | while read maker suffix size; do
		vol="${host}-$suffix"
		lvs | grep -q "^ *$vol " && die 3 "Volume '$vol' exists already - aborting ..."
		lvcreate -n "$vol" -L "$size" "$LVM_GROUP"
		"$maker" "/dev/$LVM_GROUP/$vol"
	 done
}


create_access_point_volume() {
	local host="$1"
	local vol="${host}-root"
	lvs | grep -q "^ *$vol " && die 3 "Volume '$vol' exists already - aborting ..."
	lvcreate -n "$vol" -L 64M "$LVM_GROUP"
}


mount_system() {
	local host="$1"
	local dev="/dev/$LVM_GROUP/${host}-root"
	[ -d "$MOUNTPOINT" ] || die 6 "The mountpoint '$MOUNTPOINT' does not exist - aborting ..."
	mountpoint -q "$MOUNTPOINT" && die 7 "The mountpoint '$MOUNTPOINT' is already in use - aborting ..."
	mount "$dev" "$MOUNTPOINT" || die 9 "Failed to mount base filesystem '$dev' - aborting ..."
}


umount_system() {
	mountpoint -q "$MOUNTPOINT" && umount "$MOUNTPOINT"
	return 0
}


create_debian_system() {
	local host="$1"
	local ip="$2"
	mount_system "$host"
	which debootstrap >/dev/null || die 11 "Missing requirement: debootstrap"
	echo "$DISTRIBUTION" "$MOUNTPOINT" "$APT_URL" 
	local DEBOOTSTRAP_OPTS="--include $PACKAGES_INCLUDE --exclude $PACKAGES_EXCLUDE"
	debootstrap $DEBOOTSTRAP_OPTS "$DISTRIBUTION" "$MOUNTPOINT" "$APT_URL" || { umount_system; die 8 "Debootstrap failed - aborting ..."; }
	cat - >"$MOUNTPOINT/etc/network/interfaces" <<-EOF
		auto lo
		iface lo inet loopback

		# mesh interface
		auto eth0
		iface eth0 inet static
			address $ip
			netmask 255.255.0.0

		# internet uplink
		auto eth1
		iface eth1 inet dhcp
EOF
	cat - >"$MOUNTPOINT/etc/fstab" <<-EOF
		/dev/sda	/	auto	noatime,nodiratime	0	1
		/dev/sdb	none	swap	sw			0	0
EOF
	# debootstrap erzeugt keine security-Eintraege
	grep -q security "$MOUNTPOINT/etc/apt/sources.list" || echo "deb http://security.debian.org/ $DISTRIBUTION/updates main" >>"$MOUNTPOINT/etc/apt/sources.list"
	umount_system
}


create_access_point_image() {
	local host="$1"
	local image_url="$2"
	local blockdev="/dev/$LVM_GROUP/${host}-root"
	# Abbruch, falls curl fehlschlaegt
	set -o pipefail
	{ curl --silent "$image_url" || { echo >&2 "Failed to download '$image_url'" && return 1; }; } \
		| gunzip --stdout --force | dd "of=$blockdev" status=none
	set +o pipefail
}


wait_for_ap() {
	local ttydev=$(virsh --quiet ttyconsole "$host")
	while ! timeout 1 cat "$ttydev" | grep -q "^/"; do
		sleep 1
		echo "pwd" >"$ttydev"
	done
}


configure_access_point_networking() {
	local host="$1"
	local ip="$2"
	virsh start "$host"
	# das Booten auf ryoko dauert ca. 12 Sekunden
	echo "Warte auf Booten des Access-Points ..."
	local ttydev=$(virsh --quiet ttyconsole "$host")
	# sende Eingaben an die Konsole - sie werden erst durch "virsh console" wirksam
	# zuerst eine Leerzeile (bzw. "true") um die Konsole zu oeffnen
	wait_for_ap
	echo "Bootvorgang abgeschlossen"
	cat >"$ttydev" <<-EOF
		true
		# eth0 aus dem LAN-Netzwerk entfernen
		uci set network.lan.ifname=none
		# fruezeitig Erinitialisierungen triggern
		uci commit
		/etc/init.d/network restart
		sleep 3
		uci set network.lan.ifname=none
		# eth0 mit der selbstgewaehlten mesh-IP konfigurieren
		uci set network.on_eth_0.ifname=eth0
		uci set network.on_eth_0.proto=static
		uci set network.on_eth_0.ipaddr="$ip"
		uci commit
		sync
		/etc/init.d/network restart
		# warte auf den Abschluss des Schreibvorgangs
		sleep 3
		poweroff
EOF
	# nur bei existierendem Rueckgabekanal werden die obigen Eingaben verarbeitet
	timeout 10 cat "$ttydev" >/dev/null 2>&1 || true
	sleep 4
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
	virsh --quiet define "$libvirt_file"
}


get_random() {
	# return a number of random hexadecimal characters
	uuidgen | sed 's/-//g' | cut -c "1-$1"
}


get_network_mac() {
	which "uuidgen" >/dev/null || die 5 "Missing requirement: uuidgen"
	# beware: some prefixes are multicast ones - thus we just pick a good one hard-coded
	local mac="00:16:3e"
        for i in 1 2 3; do mac="${mac}:$(get_random 2)"; done
	echo "$mac"
}


create_virt_config() {
	local host="$1"
	local memory="$2"
	local target_file="/etc/libvirt/qemu/${host}.xml"
	[ -e "$target_file" ] && die 4 "Host config file '$target_file' exists already - aborting ..."
	local mac1=$(get_network_mac)
	local mac2=$(get_network_mac)
	cp "$VIRT_BASE_CONFIG" "$target_file"
	sed -i "s/__NAME__/$host/g" "$target_file"
	sed -i "s/__MEMORY__/$memory/g" "$target_file"
	sed -i "s/__UUID__/$(uuidgen)/g" "$target_file"
	sed -i "s/__MAC1__/$mac1/g" "$target_file"
	sed -i "s/__MAC2__/$mac2/g" "$target_file"
	virsh --quiet define "$target_file"
}


run_in_chroot() {
	chroot "$MOUNTPOINT" "$@" || { umount_system; die 12 "Failed to run command in chroot: $@"; }
	return 0
}


prepare_system() {
	local host="$1"
	mount_system "$host"
	echo "$host" >"$MOUNTPOINT/etc/hostname"
	# import the server ssh key
	run_in_chroot mkdir -p /root/.ssh
	# der root-Nutzer des Virtualisierungsservers hat ohnehin die volle Kontrolle
	# Wir kopieren also den Schluessel fuer vereinfachte Problembehebung.
	cp /root/.ssh/id_rsa.pub "$MOUNTPOINT/root/.ssh/authorized_keys"
	# olsrd-Interface konfigurieren und Daemon aktivieren
	sed -i 's/^Interface.*$/Interface "eth0"/' "$MOUNTPOINT/etc/olsrd/olsrd.conf"
	sed -i 's/^#START_OLSRD=.*$/START_OLSRD="YES"/' "$MOUNTPOINT/etc/default/olsrd"
	umount_system
}


get_firmware_versions() {
	echo "$AP_FIRMWARE_MAP" | awk '{print $1}' | grep -v "^$"
}


get_url_of_firmware_version() {
	local version="$1"
	echo "$AP_FIRMWARE_MAP" | awk '{ if ($1 == "'$version'") print $2 }'
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
		create_virt_config "$host" "$((128*1024))"
		create_debian_system "$host" "$ip"
		prepare_system "$host"
		;;
	create-ap)
		[ "$#" -eq 3 ] || die 3 "Not enough arguments: HOSTNAME IP IMAGE_URL"
		host="$1"
		ip="$2"
		image_url=$(get_url_of_firmware_version "$3")
		[ -z "$image_url" ] && image_url="$3"
		echo "$host" | grep -q "^[a-z][a-z0-9_-]*$" || die 1 "Hostname contains invalid characters: $host"
		echo "$ip" | grep -q "^\([0-9]\{1,3\}\.\)\{3\}[0-9]\{1,3\}$" || die 2 "invalid IP given: $ip"
		create_access_point_volume "$host"
		create_virt_config "$host" "$((64*1024))"
		create_access_point_image "$host" "$image_url"
		configure_access_point_host_definition "$host"
		configure_access_point_networking "$host" "$ip"
		virsh start "$host"
		;;
	remove)
		host="$1"
		echo "$host" | grep -q "^[a-z][a-z0-9_-]*$" || die 1 "Hostname contains invalid characters: $host"
		(
			set +e
			virsh --quiet destroy "$host" 2>/dev/null
			umount_system
			for suffix in root swap; do
				lvremove -f "$LVM_GROUP/${host}-$suffix" 2>/dev/null
			 done
			virsh list | grep -q " $host  *running$" && virsh destroy "$host"
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

exit 0
