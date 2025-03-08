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

    # competition
    competition_list = "/"
    competition_detail = "/{competition_id}"
    competition_days = "/{competition_id}/days"
    competition_create = "/create"
    competition_update = "/update/{competition_id}"
    competition_patch = "/{competition_id}"
    competition_delete = "/delete/{competition_id}"
    competition_day = "/{competition_id}/days/{day}"
    competition_update_day = "/update_day/{competition_id}"

    # coach
    coach_list = "/"
    coach_detail = "/{coach_id}"
    coach_create = "/create"
