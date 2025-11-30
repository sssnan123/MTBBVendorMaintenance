from . import ShortDescGenerator
from . import DateTimeGenerator
from . import CISGenerator
from . import ImpleGenerator

# 获取Service-Now的Payloads信息
def getPayloads(startTime, endTime, isWinter, assignee, BCNotes, validCircuitsList):

    # 获取Change开始及结束时间
    plannedStartTime, plannedEndTime = DateTimeGenerator.getPlannedTime(startTime, endTime, isWinter)

    # 获取Payload中的UTC时间
    startDate = DateTimeGenerator.getStartTimeInPayloads(startTime)

    # 获取整个change的持续时间
    changeDuration = DateTimeGenerator.getChangeDuration(plannedStartTime, plannedEndTime)

    # 获取Short Description
    shortDescription = ShortDescGenerator.getShortDescription(plannedStartTime, plannedEndTime, validCircuitsList)

    # 获取所有链路信息
    cis = CISGenerator.getCIS(validCircuitsList)

    # 获取Implementation Plan中的链路信息
    cisInImplementation = CISGenerator.getCISInImplementation(cis)

    # 获取Implementation Plan中Vendor的时间
    vendorTimeInImplementation = DateTimeGenerator.getVendorTimeInImplementation(startTime, endTime, isWinter)

    # 获取Implementation Plan
    implementation = ImpleGenerator.getImplementation(plannedStartTime, vendorTimeInImplementation, cisInImplementation)

    # 生成Payloads
    payloads = {
        'source': 'Neteng',
        'table': 'x_ebay_change_mgmt_import_change_api_data',
        'payload': {
            'short_description': shortDescription,
            'category': 'network_eng_mtbb',
            'change_duration': changeDuration,
            'type': 'Core Interface',
            'type_of_change': 'normal',
            'subtype': 'maintenance',
            'start_date': startDate,
            'assigned_to': assignee,
            'requested_by' : assignee,
            'cis': cis,
            'comments' : BCNotes,
            'x_ebay_change_mgmt_not_able_to_find_ci': 'true',
            'implementation_plan': implementation,
            'verification_plan': (
                                    'a. Verification of circuits is automatically ran utilizing the view_circuit_output.py script as part of the maint_vendors.py script. The view_circuit_output.py script is called directly after tunnel re-optimization has occurred during cost out and directly after the configurations have been pushed during post-maintenance.\n'
                                    '  i.  The output may take some time as the script will go to each device to gather the output. Some responses may take longer then others. For example, if the circuit is down, then ping may take additional time to complete.\n'
                                    '  ii. Copy all of the verification output into the associated tickets.'
            ),
            'rollback_plan': (
                                'Cost-in procedure:\n'
                                '\n'
                                '  a. Login to preferred MTBB automation server\n'
                                '\n'
                                '  b. Verify circuit before putting back in service\n'
                                '    i.   IS-IS neighbor Up\n'
                                '    ii.  Ping with max mtu (IPv4 = 8972, IPv6 = 8952) successfully\n'
                                '    iii. Check interfaces for errors.  Clear before testing if errors accumulated during the maintenance.\n'
                                '\n'
                                '  c. For WAN/DDS/Transit/Private/LOCAL: Run the following command:\n'
                                '    i. WAN & DDS POST-maintenance\n'
                                '      1. maint_vendors.py -post -cid <cid>\n'
                                '    ii. Transit & Private POST-maintenance\n'
                                '      1. maint_vendors.py -post -tp <cid>\n'
                                '    iii. LOCAL & WAN & DDS POST-maintenance\n'
                                '      1. maint_vendors.py -post -dev <router> -int <interface>\n'
                                '\n'
                                '  d. For Public Peering: Run the following command:\n'
                                '    i. This will gather all peers on the router with that ASN and generates the POST-maintenance configs to apply the route filters\n'
                                '      1. maint_vendors.py -post -pp -dev <router> -as <asn>\n'
                                '    ii. This will cost in ALL peering sessions on that router through that interface by APPLYING  route filters to every neighbor\n'
                                '      1. maint_vendors.py -post -pp -dev <router_name> -int <interface> -all\n'
                                '    iii. This will gather all neighbors belonging to ASN on BOTH edge routers at the location (ber1 & ber2) and generate POST-maintenance configs to APPLY route filters\n'
                                '      1. maint_vendors.py -post -pp -dev <router> -as <asn>\n'
                                '\n'
                                '  e. Enter your TACACS+ password when prompted and enter\n'
                                '\n'
                                '  f. Monitor the output to verify configuration push\n'
                                '\n'
                                '  g. Perform final verification\n'
                                '    i.   MAINT removed from description\n'
                                '    ii.  The admin-group maintenance should no longer be applied under protocols mpls\n'
                                '      1. NOTE: if the admin-group maintenance is not in the output, that is exactly what is expected.\n'
                                '    iii. The metric should be set back to the original value (matching the metric in the description)\n'
                                '  h. Document final verification in a Message Update (or equivalent in SNOW)\n'
                                '\n'
                                '  i. Complete the change request and follow current Think Twice/SEC procedures to announce complete.\n'
                                '    i. Generally should be announcing in Slack channel that CHNGE is complete unless there is an issue.'
            ),
            'business_justification': (
                                'Vendor Maintenance - Vendor is performing maintenance on a core circuit.\n'
                                '\n'
                                'Core circuits provide connectivity between data centers on the backbone.\n'
                                '\n'
                                'While there are protections in place to minimize the impact of a circuit going down, there could be packet loss or multiple outages during the maintenance window.\n'
                                '\n'
                                'Moving traffic away from the circuit manually before the vendor maintenance begins allows us to remove traffic from the link with no impact, and to return traffic to the link after the maintenance is complete and verified to have been completed successfully.\n'
                                '\n'
                                'Available network capacity has been verified for the core circuits that will be unavailable during the maintenance window.'
            ),
            'environment': 'Production',
            'assigned_group': 'IRT',
            'human_trigger': 'True',
            'status': 'New',
            'risk' : 'Low'
        }
    }

    return payloads
