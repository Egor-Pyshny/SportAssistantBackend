from enum import Enum


class Prefixes(Enum):

    api_prefix = "/api/v1.0"

    auth = f"{api_prefix}/auth"
    user = f"{api_prefix}/user"
    coach = f"{api_prefix}/coaches"
    competition = f"{api_prefix}/competition"
    camps = f"{api_prefix}/camps"
    ofp_results = f"{api_prefix}/ofp"
    sfp_results = f"{api_prefix}/sfp"
    ant_params = f"{api_prefix}/anthropometric_params"
    notes = f"{api_prefix}/notes"
    med_examination = f"{api_prefix}/med_examination"
    comprehensive_examination = f"{api_prefix}/comprehensive_examination"

    redis_session_prefix = "sessions"
    redis_email_code_prefix = "email_verification"
    redis_reset_password_code_prefix = "reset_password"
