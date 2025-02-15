from enum import Enum


class Urls(Enum):

    # lead
    lead_list = "/"
    lead_detail = "/{lead_id}"
    lead_create = "/create"
    lead_update = "/update/{lead_id}"
    lead_patch = "/{lead_id}"
    lead_count_by_status = "/statuses"
    lead_import = "/import"
    delete = "/delete/{lead_id}"
    generate_template = "/generate_message/{lead_id}"

    # auth
    login = "/login"
    logout = "/logout"
    registration = "/registration"
    verify_email = "/verify_email"
    resend_verification_code = "/resend_verification_code"
    forgot_password = "/forgot_password"
    reset_password = "/reset_password"

    # user
    get_me = "/get_me"
    check_email = "/check_email"
