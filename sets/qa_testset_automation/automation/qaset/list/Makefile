
default_list_sle11 += acceptance-SLE11SP3.list acceptance-SLE11SP4.list
default_list_sle11 += kernel-SLE11SP3.list kernel-SLE11SP4.list
default_list_sle11 += performance-SLE11SP3.list performance-SLE11SP4.list
default_list_sle11 += regression-SLE11SP3.list regression-SLE11SP4.list
default_list_sle11 += kernel-all-default.list kernel-all-SLE11SP3.list kernel-all-SLE11SP4.list

default_list_sle12 += acceptance-SLE12.list kernel-SLE12.list regression-SLE12.list performance-SLE12.list
default_list_sle12 += kernel-all-default-SLE12.list kernel-all-SLE12SP1.list

kgraft_list += kgraft-kernel-SLE12.list kgraft-performance-SLE12.list

dynamic_list += performance-IO.sh performance-SYS.sh

all_list := $(default_list_sle11) $(default_list_sle12) $(kgraft_list) $(dynamic_list)

LIST_DEST := $(dest)/list

install:
	install -d $(LIST_DEST)
	install -m 644 $(all_list) $(LIST_DEST)

.PHONY: install
