
import re


def clean_extracted_text(text: str) -> str:
    """Normalize whitespace and repair known PDF extraction artifacts."""

    text = text.replace("\u00a0", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Repair verified merged phrases from the Amanara PDF.
    replacements = [
        (r"TheElectricityAct,2003", "The Electricity Act, 2003"),
        (r"2003allows", "2003 allows"),
        (r"availnondiscriminatory", "avail nondiscriminatory"),
        (r"allows\s*powerConsumers", "allows power Consumers"),
        (r"Consumerstoavail", "Consumers to avail"),
        (r"nondiscriminatoryOpenAccess", "nondiscriminatory Open Access"),
        (r"OpenAccess", "Open Access"),
        (r"InlinewiththisRegulatorsallow", "In line with this, regulators allow"),
        (r"MERCalsointroducedGreenOpenAccess", "MERC also introduced Green Open Access"),
        (r"MERCalsointroducedGreenOpenAccessdated10thNov","MERC also introduced Green Open Access dated 10th Nov"),
        (r"GreenOpenAccess", "Green Open Access"),
        (r"MERCalsointroduced", "MERC also introduced"),
        (r"introducedGreenOpen", "introduced Green Open"),
        (r"Open Accessdated", "Open Access dated"),
        (r"dated10thNov", "dated 10th Nov"),
        (r"below1MW", "below 1 MW"),
        (r"contracteddemand", "contracted demand"),
        (r"theGenerator", "the Generator"),
        (r"ofsolar", "of solar"),
        (r"intothegrid", "into the grid"),
        (
            r"dated10thNov[’']?23",
            "dated 10th Nov '23",
        ),
        (
            r"below1MW",
            "below 1 MW",
        ),
        (
            r"upto100KW",
            "up to 100 kW",
        ),
        (
            r"contracteddemand",
            "contracted demand",
        ),
        (
            r"demandorsanctioned",
            "demand or sanctioned",
        ),
        (
            r"sanctionedload",
            "sanctioned load",
        ),
        (
            r"Howan Open access policy works",
            "How an Open Access policy works",
        ),
        (r"(?<=[a-z])\.(?=[A-Z])", ". "),
    ]

    for pattern, replacement in replacements:
        text = re.sub(pattern, replacement, text)

    return text.strip()
