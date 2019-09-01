#!/usr/bin/python

group = "cloudstack"
subgroup_applications = _("Cloud Platforms")

register_check_parameters(
    subgroup_applications,
    "check_cloudstack_projects",
    _("Cloudstack Project Resources"),
    Dictionary(
        elements=[
            ("global",
                 Dictionary(
                     elements=[
                         ("cpu",
                          Tuple(
                              title=_("CPU Resource Usage"),
                              help=_("Add the warn and critical thresholds for cpu resources of a cloudstack domain"),
                              elements=[
                                  Integer(title=_("warn"), help=_("WARN threshold of CPU Metric"), unit=_("%"),default_value=80, ),
                                  Integer(title=_("critical"), help=_("CRITICAL threshold of CPU Metric"), unit=_("%"),default_value=90, ),
                              ],
                          ),
                          ),
                         ("ip",
                          Tuple(
                              title=_("IP Resource Usage"),
                              help=_("Add the warn and critical thresholds for IP resources of a cloudstack domain"),
                              elements=[
                                  Integer(title=_("warn"), help=_("WARN threshold of IP Metric"), unit=_("%"),default_value=80, ),
                                  Integer(title=_("critical"), help=_("CRITICAL threshold of IP Metric"), unit=_("%"),default_value=90, ),
                              ],
                          ),
                          ),
                         ("memory",
                          Tuple(
                              title=_("Memory Resource Usage"),
                              help=_("Add the warn and critical thresholds for MEMORY resources of a cloudstack domain"),
                              elements=[
                                  Integer(title=_("warn"), help=_("WARN threshold of MEMORY Metric"), unit=_("%"),default_value=80, ),
                                  Integer(title=_("critical"), help=_("CRITICAL threshold of MEMORY Metric"),unit=_("%"), default_value=90, ),
                              ],
                          ),
                          ),
                         ("network",
                          Tuple(
                              title=_("Network Resource Usage"),
                              help=_("Add the warn and critical thresholds for NETWORK resources of a cloudstack domain"),
                              elements=[
                                  Integer(title=_("warn"), help=_("WARN threshold of NETWORK Metric"), unit=_("%"),default_value=80, ),
                                  Integer(title=_("critical"), help=_("CRITICAL threshold of NETWORK Metric"),unit=_("%"), default_value=90, ),
                              ],
                          ),
                          ),
                         ("primarystorage",
                          Tuple(
                              title=_("Primarystorage Resource Usage"),
                              help=_("Add the warn and critical thresholds for Primary Storage resources of a cloudstack domain"),
                              elements=[
                                  Integer(title=_("warn"), help=_("WARN threshold of Primary Storage Metric"),unit=_("%"), default_value=80, ),
                                  Integer(title=_("critical"), help=_("CRITICAL threshold of Primary Storage Metric"),unit=_("%"), default_value=90, ),
                              ],
                          ),
                          ),
                         ("secondarystorage",
                          Tuple(
                              title=_("Secondarystorage Resource Usage"),
                              help=_("Add the warn and critical thresholds for Secondary Storage resources of a cloudstack domain"),
                              elements=[
                                  Integer(title=_("warn"), help=_("WARN threshold of Secondary Storage Metric"),unit=_("%"), default_value=80, ),
                                  Integer(title=_("critical"), help=_("CRITICAL threshold of Secondary Storage Metric"),unit=_("%"), default_value=90, ),
                              ],
                          ),
                          ),
                         ("snapshot",
                          Tuple(
                              title=_("Snapshot Resource Usage"),
                              help=_("Add the warn and critical thresholds for SNAPSHOT resources of a cloudstack domain"),
                              elements=[
                                  Integer(title=_("warn"), help=_("WARN threshold of SNAPSHOT Metric"), unit=_("%"),default_value=80, ),
                                  Integer(title=_("critical"), help=_("CRITICAL threshold of SNAPSHOT Metric"),unit=_("%"), default_value=90, ),
                              ],
                          ),
                          ),
                         ("template",
                          Tuple(
                              title=_("Template Resource Usage"),
                              help=_("Add the warn and critical thresholds for TEMPLATE resources of a cloudstack domain"),
                              elements=[
                                  Integer(title=_("warn"), help=_("WARN threshold of TEMPLATE Metric"), unit=_("%"),default_value=80, ),
                                  Integer(title=_("critical"), help=_("CRITICAL threshold of TEMPLATE Metric"),unit=_("%"), default_value=90, ),
                              ],
                          ),
                          ),
                         ("vm",
                          Tuple(
                              title=_("Virtualmachine Resource Usage"),
                              help=_("Add the warn and critical thresholds for VM resources of a cloudstack domain"),
                              elements=[
                                  Integer(title=_("warn"), help=_("WARN threshold of VM Metric"), unit=_("%"),default_value=80, ),
                                  Integer(title=_("critical"), help=_("CRITICAL threshold of VM Metric"), unit=_("%"),default_value=90, ),
                              ],
                          ),
                          ),
                         ("volume",
                          Tuple(
                              title=_("Volume Resource Usage"),
                              help=_("Add the warn and critical thresholds for VOLUME resources of a cloudstack domain"),
                              elements=[
                                  Integer(title=_("warn"), help=_("WARN threshold of VOLUME Metric"), unit=_("%"),default_value=80, ),
                                  Integer(title=_("critical"), help=_("CRITICAL threshold of VOLUME Metric"),unit=_("%"), default_value=90, ),
                              ],
                          ),
                          ),
                         ("vpc",
                          Tuple(
                              title=_("VPC Resource Usage"),
                              help=_("Add the warn and critical thresholds for VPC resources of a cloudstack domain"),
                              elements=[
                                  Integer(title=_("warn"), help=_("WARN threshold of VPC Metric"), unit=_("%"),default_value=80, ),
                                  Integer(title=_("critical"), help=_("CRITICAL threshold of vpc Metric"), unit=_("%"),default_value=90, ),
                              ],
                          ),
                          ),
                     ],
                title = _("Global Settings"),
                help = _("Global parameters for cloudstack projects"),
                ),
            ),
            ("custom",
             ListOf(
                Dictionary(
                    elements = [
                        ("name",
                         TextAscii(
                             title=_("Name of project"),
                             help=_("Add the name of the project"),
                         ),
                         ),
                         ("cpu",
                          Tuple(
                              title=_("CPU Resource Usage"),
                              help=_("Add the warn and critical thresholds for cpu resources of a cloudstack domain"),
                              elements=[
                                  Integer(title=_("warn"), help=_("WARN threshold of CPU Metric"), unit=_("%"),default_value=80, ),
                                  Integer(title=_("critical"), help=_("CRITICAL threshold of CPU Metric"), unit=_("%"),default_value=90, ),
                              ],
                          ),
                          ),
                         ("ip",
                          Tuple(
                              title=_("IP Resource Usage"),
                              help=_("Add the warn and critical thresholds for IP resources of a cloudstack domain"),
                              elements=[
                                  Integer(title=_("warn"), help=_("WARN threshold of IP Metric"), unit=_("%"),default_value=80, ),
                                  Integer(title=_("critical"), help=_("CRITICAL threshold of IP Metric"), unit=_("%"),default_value=90, ),
                              ],
                          ),
                          ),
                         ("memory",
                          Tuple(
                              title=_("Memory Resource Usage"),
                              help=_("Add the warn and critical thresholds for MEMORY resources of a cloudstack domain"),
                              elements=[
                                  Integer(title=_("warn"), help=_("WARN threshold of MEMORY Metric"), unit=_("%"),default_value=80, ),
                                  Integer(title=_("critical"), help=_("CRITICAL threshold of MEMORY Metric"),unit=_("%"), default_value=90, ),
                              ],
                          ),
                          ),
                         ("network",
                          Tuple(
                              title=_("Network Resource Usage"),
                              help=_("Add the warn and critical thresholds for NETWORK resources of a cloudstack domain"),
                              elements=[
                                  Integer(title=_("warn"), help=_("WARN threshold of NETWORK Metric"), unit=_("%"),default_value=80, ),
                                  Integer(title=_("critical"), help=_("CRITICAL threshold of NETWORK Metric"),unit=_("%"), default_value=90, ),
                              ],
                          ),
                          ),
                         ("primarystorage",
                          Tuple(
                              title=_("Primarystorage Resource Usage"),
                              help=_("Add the warn and critical thresholds for Primary Storage resources of a cloudstack domain"),
                              elements=[
                                  Integer(title=_("warn"), help=_("WARN threshold of Primary Storage Metric"),unit=_("%"), default_value=80, ),
                                  Integer(title=_("critical"), help=_("CRITICAL threshold of Primary Storage Metric"),unit=_("%"), default_value=90, ),
                              ],
                          ),
                          ),
                         ("secondarystorage",
                          Tuple(
                              title=_("Secondarystorage Resource Usage"),
                              help=_("Add the warn and critical thresholds for Secondary Storage resources of a cloudstack domain"),
                              elements=[
                                  Integer(title=_("warn"), help=_("WARN threshold of Secondary Storage Metric"),unit=_("%"), default_value=80, ),
                                  Integer(title=_("critical"), help=_("CRITICAL threshold of Secondary Storage Metric"),unit=_("%"), default_value=90, ),
                              ],
                          ),
                          ),
                         ("snapshot",
                          Tuple(
                              title=_("Snapshot Resource Usage"),
                              help=_("Add the warn and critical thresholds for SNAPSHOT resources of a cloudstack domain"),
                              elements=[
                                  Integer(title=_("warn"), help=_("WARN threshold of SNAPSHOT Metric"), unit=_("%"),default_value=80, ),
                                  Integer(title=_("critical"), help=_("CRITICAL threshold of SNAPSHOT Metric"),unit=_("%"), default_value=90, ),
                              ],
                          ),
                          ),
                         ("template",
                          Tuple(
                              title=_("Template Resource Usage"),
                              help=_("Add the warn and critical thresholds for TEMPLATE resources of a cloudstack domain"),
                              elements=[
                                  Integer(title=_("warn"), help=_("WARN threshold of TEMPLATE Metric"), unit=_("%"),default_value=80, ),
                                  Integer(title=_("critical"), help=_("CRITICAL threshold of TEMPLATE Metric"),unit=_("%"), default_value=90, ),
                              ],
                          ),
                          ),
                         ("vm",
                          Tuple(
                              title=_("Virtualmachine Resource Usage"),
                              help=_("Add the warn and critical thresholds for VM resources of a cloudstack domain"),
                              elements=[
                                  Integer(title=_("warn"), help=_("WARN threshold of VM Metric"), unit=_("%"),default_value=80, ),
                                  Integer(title=_("critical"), help=_("CRITICAL threshold of VM Metric"), unit=_("%"),default_value=90, ),
                              ],
                          ),
                          ),
                         ("volume",
                          Tuple(
                              title=_("Volume Resource Usage"),
                              help=_("Add the warn and critical thresholds for VOLUME resources of a cloudstack domain"),
                              elements=[
                                  Integer(title=_("warn"), help=_("WARN threshold of VOLUME Metric"), unit=_("%"),default_value=80, ),
                                  Integer(title=_("critical"), help=_("CRITICAL threshold of VOLUME Metric"),unit=_("%"), default_value=90, ),
                              ],
                          ),
                          ),
                         ("vpc",
                          Tuple(
                              title=_("VPC Resource Usage"),
                              help=_("Add the warn and critical thresholds for VPC resources of a cloudstack domain"),
                              elements=[
                                  Integer(title=_("warn"), help=_("WARN threshold of VPC Metric"), unit=_("%"),default_value=80, ),
                                  Integer(title=_("critical"), help=_("CRITICAL threshold of vpc Metric"), unit=_("%"),default_value=90, ),
                              ],
                          ),
                          ),
                    ],
                    optional_keys = [ "cpu","ip","memory","network","primarystorage","secondarystorage","snapshot","template","vm","volume","vpc" ],
                 ),
                 title=_("Custome settings"),
                 add_label=_("Add project"),
             ),
             ),
            ],
            optional_keys = False,
        ),
    TextAscii( title = _("Status Description"), allow_empty = True),
    "dict",
)