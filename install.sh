ARCHIVE_URL = ""

main "$@"

main() {
    check_if_script_is_run_under_root
    check_arguments_count

    local email="$1"
    local password="$2"
    local bind_address="0.0.0.0"
    local bind_port=40400
    if [ "$#" -eq 5 ]; then
        bind_address="$3"
        bind_port="$4"
    fi

    install_mutablesecurity
    download_repository
    install_service

}

check_if_script_is_run_under_root() {
    if [ "$(whoami)" != root ]; then
        log_error "The required permissions are not offered. Please run the script\
 as root.\n"

        exit
    fi
}

check_arguments_count() {
    if [ "$#" -ne 3 ] || [ "$#" -ne 5 ]; then
        log_error "The number of arguments is invalid.\n"

        exit
    fi
}

install_mutablesecurity() {
    pip install mutablesecurity
}

download_repository() {
    wget $ARCHIVE_URL --output /tmp/orchestration-agent.zip
    unzip /tmp/orchestration-agent.zip -d /root/orchestration-agent
}

create_configuration_file() {
    echo "bind_address: $0\n" >> /root/orchestration-agent/.mutablesecurity
    echo "bind_port: $1\n" >> /root/orchestration-agent/.mutablesecurity
    echo "email: $2\n" >> /root/orchestration-agent/.mutablesecurity
    echo "password: $3\n" >> /root/orchestration-agent/.mutablesecurity
}

install_service()  {
    cp /root/orchestration-agent/service/orchestration-agent.service /etc/systemd/system/orchestration-agent.service
    systemctl start orchestration-agent
    systemctl enable orchestration-agent
}

log_info() {
    local message="$1"

    echo -ne "${FONT_COLOR_BLUE}[i]${FONT_RESET} $message"
}

log_success() {
    local message="$1"

    echo -ne "${FONT_COLOR_GREEN}[+]${FONT_RESET} $message"
}

log_error() {
    local message="$1"

    echo -ne "${FONT_COLOR_RED}[!]${FONT_RESET} $message"
}
