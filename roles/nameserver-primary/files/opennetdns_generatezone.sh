#!/bin/sh

set -eu

API_URL="https://api.opennet-initiative.de/api/v1"
FORWARD_ZONE_SUFFIX="aps"
REVERSE_ZONE_SUFFIX="aps.on."


# each line of output contains an IPv4 address and its corresponding IPv6 address
get_ipv4_ipv6_mapping() {
    curl -s "${API_URL%/}/accesspoint/" \
            | jq -r '.[] | [.main_ip, .main_ipv6] | @sh' \
            | grep -v null$ \
            | tr -d "'" \
            | sort -V
}


convert_to_forward_zone() {
    while read -r ipv4 ipv6; do
        printf '%-10s  IN  AAAA  %s\n' "$(echo "$ipv4" | cut -f 3,4 -d .).$FORWARD_ZONE_SUFFIX" "$ipv6"
    done
}


convert_ipv6_addresses_to_reverse_pointers() {
    python3 -c "import ipaddress, os, sys; print(os.linesep.join(ipaddress.IPv6Address(line.strip()).reverse_pointer for line in sys.stdin))"
}


convert_to_reverse_zone() {
    while read -r ipv4 ipv6; do
        printf '%s  IN  PTR  %s\n' "$(echo "$ipv6" | convert_ipv6_addresses_to_reverse_pointers)" "$(echo "$ipv4" | cut -f 3,4 -d .).$REVERSE_ZONE_SUFFIX"
    done
}


# exitcode 0: file has changed and was updated
# exitcode 1: no update required
update_zone_file_if_changed() {
    local zone_filename="$1"
    local new_zone_content="$2"
    if echo "$new_zone_content" | cmp -s "$zone_filename" -; then
        return 1
    else
        echo "$new_zone_content" | sponge "$zone_filename"
        return 0
    fi
}


update_zone_file_serial_timestamp() {
    local filename="$1"
    sed -i "s|[0-9]\+\(\s*; serial\)$|$(date +%Y%m%d)00\1|" "$filename"
}


ACTION=${1:-help}

case "$ACTION" in
    forward)
        get_ipv4_ipv6_mapping | convert_to_forward_zone
        ;;
    reverse)
        get_ipv4_ipv6_mapping | convert_to_reverse_zone
        ;;
    auto)
        forward=$("$0" forward)
        reverse=$("$0" reverse)
        [ -z "$forward" ] && echo >&2 "Invalid/empty forward zone content" && exit 1
        [ -z "$reverse" ] && echo >&2 "Invalid/empty reverse zone content" && exit 1
        update_zone_file_if_changed "/etc/bind/zones/on.zone.ipv6-by-api" "$forward" \
            && update_zone_file_serial_timestamp "/etc/bind/zones/on.zone"
        update_zone_file_if_changed "/etc/bind/zones/fd32_d8d3_87da.zone.by-api" "$reverse" \
            && update_zone_file_serial_timestamp "/etc/bind/zones/fd32_d8d3_87da.zone"
        /usr/sbin/rndc reload
        ;;
    help|--help)
        echo "Syntax:  $(basename "$0")  { forward | reverse | help }"
        echo
        ;;
    *)
        "$0" help >&2
        exit 1
        ;;
esac
