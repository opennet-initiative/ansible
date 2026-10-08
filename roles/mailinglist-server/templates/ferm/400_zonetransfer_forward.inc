
###############################################################################
# {{ ansible_managed }}
# Lokale Anpassungen koennen unter /etc/ferm/ferm.d/ abgelegt werden.
###############################################################################

@def $PUBLIC_IF = eth1;
@def $MESH_IF = eth0;
@def $IP_INTERNAL_IZUMI = 192.168.10.7;

# List InternetX IP ranges here to block the rest of the internet
@def $InternetX_IPS = ( 62.116.132.5 62.116.131.31 217.160.113.32 83.169.55.5 195.34.161.195 74.208.164.110 ); 

domain ip {
    table filter {
        chain FORWARD {
            # Connection tracking: allow returning traffic from the mesh to the internet
            interface $MESH_IF outerface $PUBLIC_IF mod state state (RELATED ESTABLISHED) ACCEPT;

            # Forward traffic from public interface to the hidden primary inside the mesh
            interface $PUBLIC_IF outerface $MESH_IF proto (tcp udp) dport 53 daddr $IP_INTERNAL_IZUMI {
                # strictly restrict to InternetX IPs
                saddr $InternetX_IPS 
                ACCEPT;
            }
        }
    }

    table nat {
        chain PREROUTING {
            # DNAT: Redirect incoming public Port 53 traffic to the hidden primary's MESH IP
            interface $PUBLIC_IF proto (tcp udp) dport 53 DNAT to "$IP_INTERNAL_IZUMI:53";
        }

        chain POSTROUTING {
            # MASQUERADE: Rewrite the source IP to IP_INTERNAL_IZUMI as traffic enters the mesh
            outerface $MESH_IF proto (tcp udp) daddr $IP_INTERNAL_IZUMI dport 53 MASQUERADE;
        }
    }
}
