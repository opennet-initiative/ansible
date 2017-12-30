# History-Eintraege mit Zeitstempel versehen
export HISTTIMEFORMAT='%F %T '

# separate History-Datei pro Nutzer
if [ -n "$SSH_USER" ]; then
	logger -ip auth.notice -t sshd "Accepted publickey for $SSH_USER"
	export HISTFILE="$HOME/.history_$SSH_USER"
fi

# doppelte Eintraege ignorieren
export HISTIGNORE=\&

# laengere History
export HISTSIZE=10000
