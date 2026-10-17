Use `incus copy`. It makes a full independent copy under the new name and gives it a new MAC address and new Incus-side IDs:

```bash
incus stop secure-debian
incus copy secure-debian secure-debian-2
incus start secure-debian-2 --console
```

To rename a VM in place instead, use `incus rename secure-debian new-name` while it's stopped.

You can also copy from a snapshot, which doesn't require stopping the original:

```bash
incus snapshot create test-debian base
incus copy test-debian/base test-debian-2
```

## Inside the clone: give it its own identity

Incus only changes the host-side identity. The guest's disk is byte-for-byte the same, so run this once in the new VM:

```bash
hostnamectl set-hostname secure-debian-2
rm -f /etc/machine-id /var/lib/dbus/machine-id
systemd-machine-id-setup
rm -f /etc/ssh/ssh_host_*
dpkg-reconfigure openssh-server
reboot
```

The machine ID matters most. Debian's network setup derives its DHCP client ID from it, so two VMs with the same machine ID can end up being given the **same IPv4 address** even with different MACs. The SSH host keys matter if you SSH into both VMs, since your SSH client would see them as the same machine.

## For the encrypted VMs: the copy shares the disk key

A clone of a LUKS VM uses the same passphrase and the same underlying encryption key as the original. Changing the passphrase with `cryptsetup luksChangeKey` only changes the passphrase; the key protecting the data stays the same. That's usually fine for your own copies.

If you want the clone fully independent, for example because you'll hand it to someone or keep the two at different trust levels, re-encrypt it with a new key from inside the running clone. Find the partition with `lsblk -f` (look for `crypto_LUKS`; it's usually `/dev/sda3`), then:

```bash
cryptsetup reencrypt /dev/sda3
```

This works while the system is running, but it rewrites the whole encrypted partition. That takes a while, and on your sparse disk it will grow the file to the partition's full size.
