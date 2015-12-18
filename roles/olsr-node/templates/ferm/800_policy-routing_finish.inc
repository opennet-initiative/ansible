table mangle chain "new_non_olsr_connections" {
	# alle neuen Pakete, die nicht vorher aussortiert wurden, werden symmetrisch geroutet
	CONNMARK set-mark {{ non_olsr_policy_routing_mark }}/{{ non_olsr_policy_routing_mark }};
}
