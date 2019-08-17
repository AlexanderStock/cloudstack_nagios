#!/usr/bin/python

group = "cloudstack"
subgroup_applications = _("Cloud Platforms")

register_check_parameters(
    subgroup_applications,
    "check_cloudstack_offerings",
    _("Cloudstack offering Resources"),
     ListOf(
        Dictionary(
            elements = [
                ("name",
                 TextAscii(
                     title=_("Name of offering"),
                     help=_("Add the name of the offering"),
                 ),
                 ),
                 ("count",
                  Tuple(
                      title=_("Offeringcount usage"),
                      help=_("Add the warn and critical thresholds for offeringcount of a cloudstack domain"),
                      elements=[
                          Integer(title=_("warn"), help=_("WARN threshold of offeringcount Metric"),default_value=5, ),
                          Integer(title=_("critical"), help=_("CRITICAL threshold of offeringcount Metric"),default_value=1, ),
                      ],
                  ),
                  ),
            ],
            optional_keys = False,
         ),
        title=_("Offering settings"),
        add_label=_("Add offering"),
    ),
    None,
    "dict",
)