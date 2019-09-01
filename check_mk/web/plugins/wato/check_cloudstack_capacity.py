#!/usr/bin/python

group = "cloudstack"
subgroup_applications = _("Cloud Platforms")

register_check_parameters(
    subgroup_applications,
    "check_cloudstack_capacity",
    _("Cloudstack Overall Resources"),
    Dictionary(
        elements=[
            ("global",
                 Dictionary(
                     elements=[
                         ("CAPACITY_TYPE_CPU",
                          Tuple(
                              title=_("CPU Resource Usage"),
                              help=_("Add the warn and critical thresholds for cpu resources of a cloudstack"),
                              elements=[
                                  Integer(title=_("warn"), help=_("WARN threshold of CPU Metric"), unit=_("%"),default_value=80, ),
                                  Integer(title=_("critical"), help=_("CRITICAL threshold of CPU Metric"), unit=_("%"),default_value=90, ),
                              ],
                          ),
                          ),
                         ("CAPACITY_TYPE_MEMORY",
                          Tuple(
                              title=_("Memory Resource Usage"),
                              help=_("Add the warn and critical thresholds for Memory resources of a cloudstack"),
                              elements=[
                                  Integer(title=_("warn"), help=_("WARN threshold of Memory Metric"), unit=_("%"),default_value=80, ),
                                  Integer(title=_("critical"), help=_("CRITICAL threshold of Memory Metric"),unit=_("%"), default_value=90, ),
                              ],
                          ),
                          ),
                         ("CAPACITY_TYPE_STORAGE",
                          Tuple(
                              title=_("Storage Resource Usage"),
                              help=_("Add the warn and critical thresholds for Storage resources of a cloudstack"),
                              elements=[
                                  Integer(title=_("warn"), help=_("WARN threshold of storage Metric"),unit=_("%"), default_value=80, ),
                                  Integer(title=_("critical"), help=_("CRITICAL threshold of storage Metric"),unit=_("%"), default_value=90, ),
                              ],
                          ),
                          ),
                         ("CAPACITY_TYPE_STORAGE_ALLOCATED",
                          Tuple(
                              title=_("Storage allocated Resource Usage"),
                              help=_("Add the warn and critical thresholds for storage allocated resources of a cloudstack"),
                              elements=[
                                  Integer(title=_("warn"), help=_("WARN threshold of storage allocated Metric"),unit=_("%"), default_value=80, ),
                                  Integer(title=_("critical"), help=_("CRITICAL threshold of storage allocated Metric"),unit=_("%"), default_value=90, ),
                              ],
                          ),
                          ),
                         ("CAPACITY_TYPE_SECONDARY_STORAGE",
                          Tuple(
                              title=_("Secondary Storage Resource Usage"),
                              help=_("Add the warn and critical thresholds for secondary storage resources of a cloudstack"),
                              elements=[
                                  Integer(title=_("warn"), help=_("WARN threshold of secondary storage Metric"), unit=_("%"),default_value=80, ),
                                  Integer(title=_("critical"), help=_("CRITICAL threshold of secondary storage Metric"),unit=_("%"), default_value=90, ),
                              ],
                          ),
                          ),
                         ("CAPACITY_TYPE_LOCAL_STORAGE",
                          Tuple(
                              title=_("Local storage Resource Usage"),
                              help=_(
                                  "Add the warn and critical thresholds for local storage resources of a cloudstack"),
                              elements=[
                                  Integer(title=_("warn"), help=_("WARN threshold of local storage Metric"),unit=_("%"), default_value=80, ),
                                  Integer(title=_("critical"), help=_("CRITICAL threshold of local storage Metric"),unit=_("%"), default_value=90, ),
                              ],
                          ),
                          ),
                         ("CAPACITY_TYPE_VLAN",
                          Tuple(
                              title=_("VLAN Resource Usage"),
                              help=_("Add the warn and critical thresholds for VLAN resources of a cloudstack"),
                              elements=[
                                  Integer(title=_("warn"), help=_("WARN threshold of VLAN Metric"), unit=_("%"),default_value=80, ),
                                  Integer(title=_("critical"), help=_("CRITICAL threshold of VLAN Metric"), unit=_("%"),default_value=90, ),
                              ],
                          ),
                          ),
                         ("CAPACITY_TYPE_PRIVATE_IP",
                          Tuple(
                              title=_("Private IP Resource Usage"),
                              help=_("Add the warn and critical thresholds for private IP resources of a cloudstack"),
                              elements=[
                                  Integer(title=_("warn"), help=_("WARN threshold of private IP Metric"), unit=_("%"),default_value=80, ),
                                  Integer(title=_("critical"), help=_("CRITICAL threshold of private IP Metric"), unit=_("%"), default_value=90, ),
                              ],
                          ),
                          ),
                         ("CAPACITY_TYPE_DIRECT_ATTACHED_PUBLIC_IP",
                          Tuple(
                              title=_("Direct Public IP Resource Usage"),
                              help=_(
                                  "Add the warn and critical thresholds for Direct public IP resources of a cloudstack"),
                              elements=[
                                  Integer(title=_("warn"), help=_("WARN threshold of direct public IP Metric"),unit=_("%"), default_value=80, ),
                                  Integer(title=_("critical"), help=_("CRITICAL threshold of direct public IP Metric"),unit=_("%"), default_value=90, ),
                              ],
                          ),
                          ),
                         ("CAPACITY_TYPE_VIRTUAL_NETWORK_PUBLIC_IP",
                          Tuple(
                              title=_("Public IP Resource Usage"),
                              help=_("Add the warn and critical thresholds for public IP resources of a cloudstack"),
                              elements=[
                                  Integer(title=_("warn"), help=_("WARN threshold of public IP Metric"), unit=_("%"),default_value=80, ),
                                  Integer(title=_("critical"), help=_("CRITICAL threshold of public IP Metric"),unit=_("%"), default_value=90, ),
                              ],
                          ),
                          ),
                     ],
                title = _("Cloudstack overall resources"),
                help = _("Cloudstack overall resources"),
                ),
            ),
            ],
            optional_keys = False,
        ),
    TextAscii( title = _("Status Description"), allow_empty = True),
    "dict",
)