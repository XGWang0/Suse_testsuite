### User settings

ROOT_NAME="root"
ROOT_REAL_NAME="koren"
ROOT_GROUP_NAME="root"
ROOT_GID="0"
ROOT_UID="0"
ROOT_HOME="/root"

# NOTE: here are single quotes important!
# usual root password
ROOT_PASSWORD='$2a$05$jLj7kQsx3ENZp7/MxN7YuOQ.D0/GWbamixsghVQ5qMTvINK0qzI2S'

USER_NAME="kkt"
USER_REAL_NAME="k*k*t"
USER_GROUP_NAME="users"
USER_GID="100"
USER_UID="1000"
USER_HOME="/home/$USER_NAME"

# NOTE: here are single quotes important!
# password is 'kkt'
USER_PASSWORD='$2a$05$P0jCmpsz6AbckFlOwn2Zo.dLv83YyrPlK92trZDs/OpQeBoq/ST9m'

create_this_image() {

	# I'll get image name as parameter - if it is not used, you can just ignore it
	# in template_image.sh it is used to differ minimal, graphical (and desktop)
	THIS_IMAGE="$1"

	IMAGE_VERSION="`ls -l $SLEPOS_TEMPLATE_PATH | grep "^l.*$THIS_IMAGE" | sed "s@.*-> $THIS_IMAGE-\([0-9.]*\)@\1@"`"

	if [ "$pos_version" = 9 ]; then
		info "Image definition $THIS_IMAGE is for SLEPOS 10/11 - skipping..."
		return $SKIPPED_CODE
	fi

	if [ "$pos_version" = 11 -a "$THIS_IMAGE" = desktop ]; then
		info "SLEPOS11 doesn't contain desktop image - skipping..."
		return $SKIPPED_CODE
	fi

	if [ -d "$IMAGE_PATH/$THIS_IMAGE" ]; then
		rm -rf "$IMAGE_PATH/$THIS_IMAGE"/* &> /dev/null
	else
		mkdir "$IMAGE_PATH/$THIS_IMAGE"
	fi

	cp -R "$SLEPOS_TEMPLATE_PATH/$THIS_IMAGE-$IMAGE_VERSION"/* "$IMAGE_PATH/$THIS_IMAGE" || return $ERROR_CODE

	# add users to template
	# find good place (after </preferences>)

	case "$pos_version" in
		10) sed -i "/<\/preferences>/s@\$@\n        <users group=\"$USER_GROUP_NAME\">\n                <user home=\"$USER_HOME\" name=\"$USER_NAME\" pwd=\"$USER_PASSWORD\"/>\n        </users>@" "$IMAGE_PATH/$THIS_IMAGE/config.xml" ;;
		11) sed -i "/<\/preferences>/s@\$@\n  <users group=\"$USER_GROUP_NAME\" id=\"$USER_GID\"\>\n    <user home=\"$USER_HOME\" id=\"$USER_UID\" name=\"$USER_NAME\" pwd=\"$USER_PASSWORD\" realname=\"$USER_REAL_NAME\"/>\n  </users>\n  <users group=\"$ROOT_GROUP_NAME\" id=\"$ROOT_GID\">\n    <user home=\"$ROOT_HOME\" id=\"$ROOT_UID\" name=\"$ROOT_NAME\" pwd=\"$ROOT_PASSWORD\" realname=\"$ROOT_REAL_NAME\"/>\n  </users>@" "$IMAGE_PATH/$THIS_IMAGE/config.xml" ;;
	esac

	# first remove mess from previous runs
	info "Removing old mess"

	# unmount these dirs from previous interrupted kiwi build
	umount /var/cache/zypp /var/cache/kiwi &> /dev/null
	rm -rf "$IMAGE_PATH/chroot/$THIS_IMAGE/" &> /dev/null

	[ -d "$IMAGE_PATH/chroot" ] || mkdir -p "$IMAGE_PATH/chroot"
	[ -d "$IMAGE_PATH/images/$THIS_IMAGE" ] || mkdir -p "$IMAGE_PATH/images/$THIS_IMAGE"

	# add script for checking dependencies
	mkdir -p "$IMAGE_PATH/$THIS_IMAGE/root/bin" && cp "$CONF_PATH/check_deps.sh" "$IMAGE_PATH/$THIS_IMAGE/root/bin" && info "Dependency checker added to image"

	# allow 32bit image on x86_64
	if [ "$(uname -i)" = "x86_64" ]; then
		LINUX32="linux32 "
	else
		LINUX32=""
	fi

	info "Step one - prepare image"
	${LINUX32}/usr/sbin/kiwi --nocolor --root "$IMAGE_PATH/chroot/$THIS_IMAGE" --prepare "$IMAGE_PATH/$THIS_IMAGE" --logfile "/var/log/image_prepare-$THIS_IMAGE" || \
		{ die "Step one failed - see log /var/log/image_prepare-$THIS_IMAGE" ; return $ERROR_CODE; }
	info "Step two - create image"
	${LINUX32}/usr/sbin/kiwi --nocolor --create "$IMAGE_PATH/chroot/$THIS_IMAGE" --destdir "$IMAGE_PATH/images/$THIS_IMAGE" --logfile "/var/log/image_create-$THIS_IMAGE" || \
		{ die "Step two failed - see log /var/log/image_prepare-$THIS_IMAGE" ; return $ERROR_CODE; }
	info "create_image $THIS_IMAGE succeeded"

}
