# apt_mirror-list
apt mirror list auto update by github actions
## debain
mirror list and mirror info update every day
### usage
replace
`http://deb.debian.org/debian`
to
`mirror+https://raw.githubusercontent.com/BikerDuality/apt_mirror-list/main/debain/mirrors.txt`
at /apt/etc/sources.list
## ubuntu
mirror list update every day,mirror info update every month
### usage
replace
`http://archive.ubuntu.com/ubuntu/`
to
`mirror+https://raw.githubusercontent.com/BikerDuality/apt_mirror-list/main/ubuntu/mirrors.txt`
at /apt/etc/sources.list