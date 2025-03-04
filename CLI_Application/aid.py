#!/usr/bin/python3


__doc__ = \
    """
CLI Audio Recorder in Python
Usage: 
    aid <Option> <Module>
    aid -c | --crawler
    aid -d | --downloader
    aid -v | --verifier
    aid -p | --packager
    aid -u | --unpackager
    aid -m | --modules    
    aid -h | --help
    aid -l | --list

Options:
    -h --help                   Show this screen
    -c --crawler                Run the Crawler component.
    -d --downloader             Run the Downloader component.
    -v --verifier               Run the Verifier component.
    -p --packager               Run the Packaging components (Pre- and Packaging).
    -u --unpackager             Run the Unpackaging component.
    -m --modules                List of modules to run [default: all]
    -l --list                   List all available modules
"""


# Default values
OPTION=""
MODULE=""

# Function to display usage
usage() {
    echo "AID - Automated Internet Downloader"
    echo "Usage: aid [OPTIONS] [MODULES]"
    echo "Example: aid -c,      Runs the crawler for all modules"
    echo "Example: aid -c 7zip, Runs the crawler for 7zip module"
    echo "Options:"
    echo "  -c, --crawler       Run the Crawler component."
    echo "  -d, --downloader    Run the Downloader component."
    echo "  -v, --verifier      Run the Verifier component."
    echo "  -p, --packager      Run the Packaging components (Pre- and Packaging)"
    echo "  -u, --unpackager    Run the Unpackaging component."
    echo "  -m, --modules       List of modules to run"
    echo "  -h, --help          Show this help message."
    exit 1
}

# Parse command-line options
while getopts "c:d:v:p:u:m:h" opt; do
    case ${opt} in
        c) OPTION=${OPTARG} ;;
        a) ARGS=${OPTARG} ;;
        h) usage ;;
        *) usage ;;
    esac
done

# Check if the script argument is provided
if [[ -z "$SCRIPT" ]]; then
    echo "Error: no Option given."
    usage
fi

# Check if the script file exists
if [[ ! -f "$SCRIPT" ]]; then
    echo "Error: Script '$SCRIPT' not found."
    exit 1
fi

# Run the Python script with arguments
python3 "$SCRIPT" $ARGS
