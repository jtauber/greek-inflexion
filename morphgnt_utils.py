# @@@ move this to greek-utils


def bcv_tuple(bcv):
    """
    converts a BBCCVV string into a tuple of book, chapter, verse number.

    e.g. "012801" returns (1, 28, 1)
    """
    return (int(i) for i in [bcv[0:2], bcv[2:4], bcv[4:6]])


def convert_parse(ccat_parse):
    if ccat_parse[3] in "DISO":
        result = ccat_parse[1:4] + "." + ccat_parse[0] + ccat_parse[5]
    elif ccat_parse[3] == "P":
        result = ccat_parse[1:4] + "." + ccat_parse[4:7]
    elif ccat_parse[3] == "N":
        result = ccat_parse[1:4]
    if result[1] == "P" and result[0] not in "AF":
        result = result[0] + "M" + result[2:]
    return result


PARTS = {
    "1-": [
        "PAI", "PAD", "PAN", "PAP", "PAS", "PAO",
        "PMI", "PMD", "PMN", "PMP", "PMS", "PMO",
    ],
    "1+": [
        "IAI",
        "IMI",
    ],
    "2-": [
        "FAI", "FAN", "FAP", "FAO",
        "FMI", "FMN", "FMP", "FMO",
    ],
    "3-": [
        "AAD", "AAN", "AAP", "AAS", "AAO",
        "AMD", "AMN", "AMP", "AMS", "AMO",
    ],
    "3+": [
        "AAI",
        "AMI",
    ],
    "4-": [
        "XAI", "XAD", "XAN", "XAP", "XAS", "XAO",
    ],
    "4+": [
        "YAI",
    ],
    "5-": [
        "XMI", "XMD", "XMN", "XMP",
    ],
    "5+": [
        "YMI", "YMP",
    ],
    "6-": [
        "APD", "APN", "APP", "APS", "APO",
    ],
    "6+": [
        "API",
    ],
    "7-": [
        "FPI", "FPP", "FPO",
    ],
    "8-": [
        "ZMI",
    ],
}

REVERSE_PARTS = {}

for part, tvm_list in PARTS.items():
    for tvm in tvm_list:
        REVERSE_PARTS[tvm] = part


def key_to_part(key):
    return REVERSE_PARTS[key[0:3]]
