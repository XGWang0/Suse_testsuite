#!/bin/bash

wait_for_resource ()
{
  while !crm_resource --locate --resource $1 2>&1 | grep - q 'running on';  do
    $BE_QUIET || echo -n '.' sleep 1
  done
}

while getopts :a:b:u: arg; do
	case $arg in
	a)	sitea="$OPTARG";;
	b)	siteb="$OPTARG";;
	u)	usage=$OPTARG;;
	:)
		echo "$0:Option $OPTARG requires variable".
	exit 1
	;;
	\?)
		echo "Wrong option $OPTARG was ignored".
	;;
	esac
done

sntp -P no -r ntp.suse.cz

if [[ $sitea && $siteb && $usage ]]; then
  zypper se -t pattern | grep ha_geo | grep "i |" 2>&1 > /dev/null
  ha_geo=$?
  if [ "$ha_geo" != "0" ]; then
    zypper ar -f http://fallback.suse.cz/install/SLP/SLE-11-SP2-HA-GEO-GM/unknown/CD1/ ha_geo
    zypper in -l -y -t product sle-haegeo
    zypper in -y -t pattern ha_geo
  fi

cat<<EOF > /etc/booth/booth.conf
transport="UDP"
port="6666"
arbitrator="$ROLE_0_IP"
site="$sitea"
site="$siteb"
ticket="ticketA;1000"
ticket="ticketB;1000"
EOF

  if [ "$usage" = "arb" ] ; then
    rcbooth-arbitrator start
    sleep 60
    booth client grant -t ticketA -s $sitea
    booth client grant -t ticketB -s $siteb
  fi

  if [ "$usage" = "ocfs2" ] ; then
  crm_resource --locate --resource g-booth
  booth=$?
    if [[ "$booth" != "0" ]]; then
crm configure << EOF
primitive booth ocf:pacemaker:booth-site \
        meta resource-stickiness="INFINITY" \
        op monitor interval="10s" timeout="40s"
primitive booth-ip ocf:heartbeat:IPaddr2 \
        params ip="$sitea" cidr_netmask="21"
group g-booth booth-ip booth \
        meta target-role="Started"
rsc_ticket base-clone-req-ticketA ticketA: base-clone loss-policy=stop
EOF
    fi
  fi

  if [ "$usage" = "mysql" ] ; then
  crm_resource --locate --resource g-booth
  booth=$?
    if [[ "$booth" != "0" ]]; then
crm configure << EOF
primitive booth ocf:pacemaker:booth-site \
        meta resource-stickiness="INFINITY" \
        op monitor interval="10s" timeout="40s"
primitive booth-ip ocf:heartbeat:IPaddr2 \
        params ip="$siteb" cidr_netmask="21"
group g-booth booth-ip booth \
        meta target-role="Started"
EOF
crm configure << EOF
rsc_ticket iscsi_ext3-req-ticketB ticketB: iscsi_ext3 loss-policy=stop
EOF
    fi
  fi

else
  echo -a $sitea -b $siteb -u $usage
  echo "Wrong or missing arguments"
  echo "Usage: geo_setup.sh -a arbitrator -b sitea -c sitea -u usage"
  echo "       arbitrator - IP ddress of arbitrator"
  echo "       sitea - IP address of booth-ip resource in ocfs2 cluster [10.100.101.37]"
  echo "       siteb - IP address of booth-ip resource in mysql cluster [10.100.101.43]"
  echo "       usage - specifies whether machine is arbitrator or node of ocfs2 or mysql cluster [arb|ocfs2|mysql]"
fi
