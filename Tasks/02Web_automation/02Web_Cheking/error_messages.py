# Lots of signatures here: https://github.com/projectdiscovery/nuclei-templates/tree/main/http/takeovers
# Also here: https://github.com/EdOverflow/can-i-take-over-xyz/blob/master/fingerprints.json

ERROR_MESSAGES = {
    "aws":  [
        "<Code>NoSuchBucket</Code>",
        "The specified bucket does not exist"
    ],
    "github":  [
        "There isn't a GitHub Pages site here."
    ]
}
