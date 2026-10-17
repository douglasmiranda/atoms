# Incus VM helper scripts

Small guest-side scripts for Debian/Ubuntu Incus VMs. Copy them into the VM and install them under `/usr/local/sbin`. Most commands take `[on|off|toggle|status]` and default to `toggle`. Run them as root (`sudo`).

*Not all scripts are "Incus exclusive".

## Install

Copy the scripts into the VM (`scp`, a shared folder, etc.), then:

```bash
sudo install -m 755 vm-* /usr/local/sbin/
```

## Scripts

### `vm-autologin`

Passwordless login on the VGA console (`tty1`) and the serial console (`ttyS0`, used by `incus console`).

```bash
sudo vm-autologin on          # first normal user (UID 1000), or root if there isn't one
sudo vm-autologin on doug     # a specific user
sudo vm-autologin off
sudo vm-autologin status
```

Takes effect at the next login prompt, not immediately — applying it right away would kill the current console session.

On an encrypted VM the LUKS passphrase still guards boot. Once unlocked, anyone who can run `incus console` on the host gets a shell without a password.

### `vm-share`

Mount the Incus virtiofs share at boot.

Attach it on the host first:

```bash
incus config device add <vm> share disk source=/path/to/share path=/mnt/share
```

Then inside the VM:

```bash
sudo vm-share on
```

It assumes the host-side device is named `share`, which gives the tag `incus_share`. For another name:

```bash
SHARE_TAG=incus_<name> vm-share on
```

The mount path defaults to `/mnt/share` (`SHARE_PATH` to change it). If the share isn't attached, the VM still boots and the script tells you the mount failed.

It warns if the Incus agent is running, since the agent already mounts shares and the two can conflict.

### `vm-ssh`

OpenSSH server, now and at boot. Installs `openssh-server` the first time you turn it on.

```bash
sudo vm-ssh on
sudo vm-ssh off
```

Turning it off stops new connections but leaves open SSH sessions running.

### `vm-reset-identity`

Give a cloned VM its own identity so clones don't share a hostname, machine ID, SSH host keys, or the same DHCP IP.

```bash
sudo vm-reset-identity <new-hostname>
```

Run it once in each clone, then reboot.

On encrypted VMs it reminds you the LUKS key is still shared with the original. It doesn't re-encrypt automatically, because that rewrites the whole disk.

### `vm-net`

Take all network cards down or up. Not persistent: every boot starts online.

```bash
sudo vm-net off
sudo vm-net on
sudo vm-net status
```

Root inside the VM can undo this. For real isolation, detach the NIC on the host:

```bash
incus config device add <vm> eth0 none
# undo:
incus config device remove <vm> eth0
```



### `vm-shrink`

Free space inside the VM and hand it back to the host, so the sparse disk file and exports stay small. Run before `incus export` or `incus copy`.

```bash
sudo vm-shrink
```

Cleans apt caches, old packages, journal logs and temp files, then runs `fstrim`.

If the encrypted disk isn't passing discards through, it warns you and tells you what to add to `/etc/crypttab`.

### `vm-agent`

Incus guest agent: lets the host run `incus exec` / `incus file` without a password, and auto-mounts shares. The first `on` installs it from the Incus config drive.

```bash
sudo vm-agent on
sudo vm-agent off
```

`off` masks the agent completely, rather than just disabling it, because udev would otherwise start it again at every boot.

Turning it off ends any shell you opened with `incus exec`, so run it from the console or SSH.
